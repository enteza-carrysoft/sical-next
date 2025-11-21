# core/db.py
import datetime as _dt
from typing import Optional, Dict, Any, List, Tuple

try:
    import oracledb as cx_Oracle  # oracledb moderno (modo thick)
except Exception:
    cx_Oracle = None

from core.config import get_cfg

# =========================
#   Inicialización cliente
# =========================
_cx_init = False
def init_oracle_client_once():
    """Inicializa el cliente Oracle (modo THICK)."""
    global _cx_init
    if _cx_init:
        return
    if cx_Oracle is None:
        raise RuntimeError("No se pudo importar 'oracledb'. Instala con: pip install oracledb")

    client_dir = get_cfg("ORACLE_CLIENT_DIR", r"C:\oracle\instantclient_19_23")
    try:
        cx_Oracle.init_oracle_client(lib_dir=client_dir)
    except Exception as e:
        # Si ya estaba inicializado, Oracle puede lanzar un benigno "already initialized".
        if "already initialized" not in str(e).lower():
            raise
    _cx_init = True


def _build_dsn(host: str, port: int, service: Optional[str], sid: Optional[str]):
    """Construye el DSN a partir de service_name o SID."""
    if service:
        return cx_Oracle.makedsn(host, port, service_name=service)
    return cx_Oracle.makedsn(host, port, sid=sid)


def get_connection_for_sid(*, sid: Optional[str] = None, service: Optional[str] = None):
    """
    Abre una conexión a Oracle usando SIEMPRE las credenciales del .env:
      ORACLE_USER / ORACLE_PASSWORD / ORACLE_HOST / ORACLE_PORT
    y permitiendo cambiar SOLAMENTE el destino (service_name o sid) según empresa.
    """
    init_oracle_client_once()

    host = get_cfg("ORACLE_HOST", "localhost").strip()
    port = int(get_cfg("ORACLE_PORT", "1521").strip() or "1521")
    user = get_cfg("ORACLE_USER", "").strip()
    password = get_cfg("ORACLE_PASSWORD", "").strip()

    # Por defecto (si no se pasa nada) usa los valores del .env
    env_service = get_cfg("ORACLE_SERVICE", "").strip()
    env_sid = get_cfg("ORACLE_SID", "").strip()
    target_service = (service or env_service or "") or None
    target_sid = (sid or env_sid or "") or None

    if not (target_service or target_sid):
        raise ValueError("Debes tener ORACLE_SERVICE u ORACLE_SID en .env, o pasar 'sid'/'service' a esta función.")

    dsn = _build_dsn(host, port, target_service, target_sid)
    try:
        return cx_Oracle.connect(user=user, password=password, dsn=dsn)
    except cx_Oracle.DatabaseError as e:
        raise ConnectionError(f"No se pudo conectar a Oracle (SID/Service destino). Detalle: {e}") from e


# =========================
#   Validación de usuario
# =========================
import re
_SAFE_IDENT = re.compile(r"^[A-Z0-9_]+$", re.IGNORECASE)

def validar_usuario(
    conn,
    usuario: str,
    password: str,
    *,
    tabla: Optional[str] = None,
    col_user: Optional[str] = None,
    col_pass: Optional[str] = None,
    condicion_activo: Optional[str] = None,
) -> bool:
    """
    Valida usuario/contraseña de la APLICACIÓN contra una tabla configurable.
    Por defecto: USUARIO(USUARIO, PASSWORD). Opcionalmente, condición de activo.
    Variables .env (opcionales):
      AUTH_TABLE, AUTH_USER_COL, AUTH_PASS_COL, AUTH_ACTIVE_COND (p.ej. "ACTIVO='S'")
    """
    tabla = (tabla or get_cfg("AUTH_TABLE", "USUARIO")).strip()
    col_user = (col_user or get_cfg("AUTH_USER_COL", "USUARIO")).strip()
    col_pass = (col_pass or get_cfg("AUTH_PASS_COL", "PASSWORD")).strip()
    condicion_activo = (condicion_activo or get_cfg("AUTH_ACTIVE_COND", "")).strip()

    # Evitar inyección en identificadores
    for ident in (tabla, col_user, col_pass):
        if not _SAFE_IDENT.match(ident):
            raise ValueError("Identificadores no válidos en configuración de autenticación")

    where_conds = [f"UPPER({col_user}) = UPPER(:u)", f"{col_pass} = :p"]
#    if condicion_activo:
#        where_conds.append(f"({condicion_activo})")

    # Versión compatible con 11g/12c/19c (EXISTS + DUAL). Devuelve 1/0 siempre.
    sql = (
        "SELECT CASE WHEN EXISTS ("
        f"  SELECT 1 FROM {tabla} WHERE " + " AND ".join(where_conds) +
        ") THEN 1 ELSE 0 END AS ok FROM dual"
    )
    cur = conn.cursor()
    cur.execute(sql, u=(usuario or "").strip(), p=(password or ""))
    row = cur.fetchone()
    return bool(row and row[0] == 1)


# =========================
#   Datos de factura + apps
# =========================
def _obtener_aplicaciones_por_factura(cur, nfacreg) -> List[Tuple[str, str, str]]:
    """
    Devuelve una lista de tuplas (org, fun, eco) desde INGRES.FACTGAST para NFACREG.
    IMPORTANTE: el campo correcto es VAPLECO (corrección aplicada).
    """
    sql_apps = """
        SELECT DISTINCT
            TRIM(FG.VAPLORG) AS ORG,
            TRIM(FG.VAPLFUN) AS FUN,
            TRIM(FG.VAPLECO) AS ECO
        FROM INGRES.FACTGAST FG
        WHERE FG.NFACREG = :n
        ORDER BY ORG, FUN, ECO
    """
    cur.execute(sql_apps, n=nfacreg)
    apps: List[Tuple[str, str, str]] = []
    for org, fun, eco in cur.fetchall() or []:
        apps.append((org or "", fun or "", eco or ""))
    return apps


def obtener_datos_factura(num_factura: str, areas_dict: dict | None = None, *, conn=None) -> Optional[Dict[str, Any]]:
    """
    Lee FACTURAS + TER_GENERAL, compone bloque 'Registro de entrada' (FACe vs Registro Sideral),
    añade nº factura proveedor (VFACNUM), expediente (EXPNORMA), código de área (AREA_SICAL/AREA)
    y APLICACIONES presupuestarias (VAPLORG/VAPLFUN/VAPLECO).
    Si no se pasa 'conn', abre/cierra usando .env y el SID/service definidos en .env.
    """
    must_close = False
    if conn is None:
        conn = get_connection_for_sid()
        must_close = True

    sql = """
        SELECT
            F.NFACREG,
            F.NUMREGISTROFACE,
            F.FECHAREGISTROFACE,
            F.NREGNUM,
            F.FREGGEN,
            F.VTERCOD,
            COALESCE(T.RAZON_REDU, T.RAZON1) AS PROVEEDOR,
            F.VTEXTO1,
            F.NFACIMP,
            F.VFACNUM,                               -- nº factura proveedor
            F.EXPNORMA,                              -- expediente del contrato
            COALESCE(F.AREA_SICAL, F.AREA) AS AREA_CODE
        FROM INGRES.FACTURAS F
        LEFT JOIN INGRES.TER_GENERAL T ON T.COD_TERCE = F.VTERCOD
        WHERE F.NFACREG = :num_factura
    """

    try:
        cur = conn.cursor()
        bind_val = int(num_factura) if str(num_factura).isdigit() else num_factura
        cur.execute(sql, num_factura=bind_val)
        row = cur.fetchone()
        if not row:
            return None

        (
            nfacreg,
            numregistroface,
            fechareg_face,
            nregnum,
            freggen,
            nif,
            proveedor,
            concepto,
            imp,
            vfacnum,
            expnorma,
            area_code,
        ) = row

        # Aplicaciones presupuestarias
        aplicaciones = _obtener_aplicaciones_por_factura(cur, nfacreg)

        # --- helpers ---
        def fmt_dt(dt, with_time=True):
            if isinstance(dt, _dt.datetime):
                return dt.strftime("%d/%m/%Y %H:%M") if with_time else dt.strftime("%d/%m/%Y")
            return str(dt) if dt is not None else ""

        def fmt_year(dt):
            if isinstance(dt, _dt.datetime):
                return dt.strftime("%Y")
            return ""

        importe_texto = f"{float(imp or 0.0):,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

        # FACe vs Registro Sideral
        if str(numregistroface or "").strip():
            punto_entrada = "FACe"
            id_punto = str(numregistroface).strip()
            fecha_hora_entrada = fmt_dt(fechareg_face, with_time=True)
        else:
            punto_entrada = "Registro Sideral"
            anyo = fmt_year(freggen)
            nregnum_s = str(nregnum or "").strip()
            id_punto = f"{nregnum_s}/{anyo}" if nregnum_s or anyo else nregnum_s or ""
            fecha_hora_entrada = fmt_dt(freggen, with_time=True)

        area_code_s = (str(area_code or "").strip())
        area_name = areas_dict.get(area_code_s) if areas_dict else None

        # Si tu “fecha de expedición” real es otra, cámbiala aquí:
        fecha_expedicion = fmt_dt(fechareg_face, with_time=False)

        return {
            # Registro de entrada
            "punto_entrada": punto_entrada,
            "id_punto_entrada": id_punto,
            "fecha_hora_entrada": fecha_hora_entrada,
            "num_rcf": nfacreg,

            # Datos factura
            "proveedor": proveedor or "",
            "nif_proveedor": nif,
            "concepto": (concepto or ""),
            "importe_total": importe_texto,
            "fecha_expedicion": fecha_expedicion,
            "vfacnum": vfacnum or "",

            # Expediente contrato
            "expediente_contrato": expnorma or "",

            # Área
            "area_code": area_code_s,
            "area_name": area_name,
            "area": area_name or "",
            "unidad": "Unidad de Gestión",

            # Aplicaciones
            "aplicaciones": aplicaciones,
        }
    finally:
        if must_close:
            try:
                conn.close()
            except Exception:
                pass
