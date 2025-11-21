# backend/application/services/factura_service.py
from typing import List, Optional
from backend.core.db import get_connection_for_sid, obtener_datos_factura
from backend.domain.models.factura import Factura, FacturaListItem, Proveedor, AplicacionPresupuestaria, TramiteFactura


class FacturaService:
    """Servicio de aplicación para gestión de facturas."""

    def __init__(self):
        self.conn = None

    def _get_connection(self):
        """Obtiene conexión a Oracle SICAL."""
        if self.conn is None:
            self.conn = get_connection_for_sid()
        return self.conn

    def listar_facturas(self, limit: int = 100, offset: int = 0) -> List[FacturaListItem]:
        """
        Lista facturas desde la base de datos SICAL.

        Args:
            limit: Número máximo de resultados
            offset: Offset para paginación

        Returns:
            Lista de FacturaListItem
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT
                F.NFACREG,
                F.NFACREG AS NUM_FACTURA,
                F.FECHAREGISTROFACE,
                F.FREGGEN,
                F.VTERCOD,
                COALESCE(T.RAZON_REDU, T.RAZON1) AS PROVEEDOR,
                F.NFACIMP,
                'EN_SERVICIO' AS ESTADO_TRAMITACION,
                'NO_OBLIGADA' AS ESTADO_CONTABLE
            FROM INGRES.FACTURAS F
            LEFT JOIN INGRES.TER_GENERAL T ON T.COD_TERCE = F.VTERCOD
            WHERE ROWNUM <= :limit
            ORDER BY F.NFACREG DESC
        """

        cursor.execute(sql, limit=limit + offset)

        facturas = []
        for row in cursor.fetchall():
            (nfacreg, num_factura, fecha_face, freggen,
             nif, proveedor, importe, estado_tram, estado_cont) = row

            # Determinar canal
            canal = "FACE" if fecha_face else "MANUAL"

            # Fecha de registro
            fecha_reg = fecha_face or freggen
            fecha_registro = fecha_reg.isoformat() if fecha_reg else ""

            factura = FacturaListItem(
                id=str(nfacreg),
                numeroFactura=f"F{nfacreg}",
                fechaFactura=fecha_registro,
                fechaRegistro=fecha_registro,
                canal=canal,
                proveedor=Proveedor(
                    id=str(nif or ""),
                    nif=str(nif or ""),
                    nombre=str(proveedor or "Sin nombre")
                ),
                total=float(importe or 0.0),
                estadoTramitacion=estado_tram,
                estadoContable=estado_cont
            )
            facturas.append(factura)

        return facturas[offset:]

    def obtener_factura(self, factura_id: str) -> Optional[Factura]:
        """
        Obtiene detalle completo de una factura.

        Args:
            factura_id: ID de la factura (NFACREG)

        Returns:
            Factura completa o None si no existe
        """
        try:
            conn = self._get_connection()
            datos = obtener_datos_factura(factura_id, areas_dict=None, conn=conn)

            if not datos:
                return None

            # Mapear datos del diccionario a modelo Pydantic
            aplicaciones = []
            for org, fun, eco in datos.get("aplicaciones", []):
                aplicaciones.append(AplicacionPresupuestaria(
                    ejercicio="2024",  # TODO: Obtener del ejercicio real
                    organica=org,
                    funcional=fun,
                    economica=eco,
                    importe=0.0  # TODO: Obtener importe real
                ))

            # TODO: Obtener trámites reales de la BD
            tramites = []

            # Parsear importe (eliminar formato español)
            importe_str = datos.get("importe_total", "0,00 €")
            total = float(importe_str.replace(".", "").replace(",", ".").replace("€", "").strip())

            # Calcular base e IVA (asumiendo IVA 21%)
            base = total / 1.21
            iva = total - base

            factura = Factura(
                id=str(datos.get("num_rcf", "")),
                numeroFactura=datos.get("vfacnum", f"F{factura_id}"),
                fechaFactura=datos.get("fecha_expedicion", ""),
                fechaRegistro=datos.get("fecha_hora_entrada", ""),
                canal=datos.get("punto_entrada", "MANUAL"),
                proveedor=Proveedor(
                    id=str(datos.get("nif_proveedor", "")),
                    nif=str(datos.get("nif_proveedor", "")),
                    nombre=datos.get("proveedor", "Sin nombre")
                ),
                baseImponible=round(base, 2),
                iva=round(iva, 2),
                total=round(total, 2),
                afecta413=False,  # TODO: Determinar desde BD
                estadoTramitacion="EN_SERVICIO",  # TODO: Obtener real
                estadoContable="NO_OBLIGADA",  # TODO: Obtener real
                aplicaciones=aplicaciones,
                tramites=tramites,
                esAbono=False
            )

            return factura

        except Exception as e:
            print(f"Error obteniendo factura {factura_id}: {e}")
            return None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
