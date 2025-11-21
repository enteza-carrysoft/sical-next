#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba de conexión a Oracle SICAL.
Ejecuta varias pruebas para verificar la configuración.
"""

import os
import sys
from pathlib import Path

# Configurar salida para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Añadir el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent))

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    print(f"[*] Cargando configuracion desde: {env_path}")
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
    print("[OK] Variables de entorno cargadas\n")
else:
    print(f"[!] No se encontro archivo .env en: {env_path}\n")

from core.db import (
    init_oracle_client_once,
    get_connection_for_sid,
    validar_usuario,
    obtener_datos_factura
)
from core.config import get_oracle_config


def test_config():
    """Prueba 1: Verificar configuración"""
    print("=" * 60)
    print("[TEST 1] Verificar configuracion desde .env")
    print("=" * 60)

    config = get_oracle_config()
    print(f"Host: {config['host']}")
    print(f"Puerto: {config['port']}")
    print(f"Usuario: {config['user']}")
    print(f"Password: {'*' * len(config['password']) if config['password'] else '(vacio)'}")
    print(f"SID: {config['sid']}")
    print(f"Service: {config['service']}")
    print(f"Cliente Oracle: {config['client_dir']}")
    print()


def test_client_init():
    """Prueba 2: Inicializar cliente Oracle"""
    print("=" * 60)
    print("[TEST 2] Inicializar cliente Oracle (modo thick)")
    print("=" * 60)

    try:
        init_oracle_client_once()
        print("[OK] Cliente Oracle inicializado correctamente")
        print()
        return True
    except Exception as e:
        print(f"[ERROR] Error al inicializar cliente Oracle: {e}")
        print()
        return False


def test_connection():
    """Prueba 3: Conectar a la base de datos"""
    print("=" * 60)
    print("[TEST 3] Conectar a Oracle")
    print("=" * 60)

    try:
        conn = get_connection_for_sid()
        print("[OK] Conexion establecida correctamente")

        # Probar una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT 'Hola desde Oracle!' FROM dual")
        result = cursor.fetchone()
        print(f"[*] Query de prueba: {result[0]}")

        # Verificar versión de Oracle
        cursor.execute("SELECT * FROM v$version WHERE banner LIKE 'Oracle%'")
        version = cursor.fetchone()
        if version:
            print(f"[*] Version Oracle: {version[0]}")

        conn.close()
        print()
        return True
    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        print()
        return False


def test_auth():
    """Prueba 4: Validar usuario de aplicación"""
    print("=" * 60)
    print("[TEST 4] Validacion de usuario (tabla tb_depart)")
    print("=" * 60)

    try:
        conn = get_connection_for_sid()

        # Prueba con usuario inválido (debería fallar)
        test_user = "usuario_prueba_invalido"
        test_pass = "password_invalido"

        resultado = validar_usuario(conn, test_user, test_pass)

        if resultado:
            print(f"[!] Usuario '{test_user}' validado (inesperado)")
        else:
            print(f"[OK] Usuario '{test_user}' rechazado correctamente (esperado)")

        conn.close()
        print()
        return True
    except Exception as e:
        print(f"[ERROR] Error en validacion: {e}")
        print()
        return False


def test_factura_query():
    """Prueba 5: Consultar datos de factura"""
    print("=" * 60)
    print("[TEST 5] Consultar datos de factura")
    print("=" * 60)

    try:
        conn = get_connection_for_sid()

        # Primero intentar obtener el número de alguna factura existente
        cursor = conn.cursor()
        cursor.execute("""
            SELECT NFACREG
            FROM INGRES.FACTURAS
            WHERE ROWNUM = 1
            ORDER BY NFACREG DESC
        """)

        row = cursor.fetchone()
        if not row:
            print("[!] No se encontraron facturas en la base de datos")
            conn.close()
            return True

        num_factura = row[0]
        print(f"[*] Consultando factura: {num_factura}")

        datos = obtener_datos_factura(str(num_factura), conn=conn)

        if datos:
            print("\n[OK] Datos obtenidos:")
            print(f"   - Punto entrada: {datos.get('punto_entrada')}")
            print(f"   - ID punto entrada: {datos.get('id_punto_entrada')}")
            print(f"   - Proveedor: {datos.get('proveedor')}")
            print(f"   - NIF: {datos.get('nif_proveedor')}")
            print(f"   - Importe: {datos.get('importe_total')}")
            print(f"   - Concepto: {datos.get('concepto', '')[:50]}...")
            print(f"   - Aplicaciones: {len(datos.get('aplicaciones', []))} encontradas")
        else:
            print(f"[!] No se encontraron datos para factura {num_factura}")

        conn.close()
        print()
        return True
    except Exception as e:
        print(f"[ERROR] Error consultando factura: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 60)
    print("TEST DE CONEXION ORACLE SICAL")
    print("=" * 60 + "\n")

    tests = [
        ("Configuracion", test_config),
        ("Cliente Oracle", test_client_init),
        ("Conexion", test_connection),
        ("Autenticacion", test_auth),
        ("Consulta Factura", test_factura_query),
    ]

    resultados = []

    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"[ERROR] Error critico en {nombre}: {e}")
            resultados.append((nombre, False))

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    for nombre, resultado in resultados:
        estado = "[OK] PASS" if resultado else "[FAIL]   "
        print(f"{estado} - {nombre}")

    total = len(resultados)
    exitosas = sum(1 for _, r in resultados if r)

    print(f"\n[*] Total: {exitosas}/{total} pruebas exitosas")

    if exitosas == total:
        print("\n[SUCCESS] Todas las pruebas pasaron correctamente!")
        return 0
    else:
        print(f"\n[WARNING] {total - exitosas} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
