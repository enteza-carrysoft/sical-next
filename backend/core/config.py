# backend/core/config.py
import os
from typing import Optional


def get_cfg(key: str, default: str = "") -> str:
    """Obtiene valor de variable de entorno con fallback."""
    return os.getenv(key, default)


def get_oracle_config() -> dict:
    """
    Devuelve configuración de Oracle desde variables de entorno.

    Estructura esperada:
    - ORACLE_HOST: Host del servidor Oracle
    - ORACLE_PORT: Puerto (default: 1521)
    - ORACLE_USER: Usuario de conexión
    - ORACLE_PASSWORD: Contraseña
    - ORACLE_SERVICE: Service name (alternativa a SID)
    - ORACLE_SID: SID (alternativa a SERVICE)
    - ORACLE_CLIENT_DIR: Directorio Oracle Instant Client
    """
    return {
        "host": get_cfg("ORACLE_HOST", "localhost"),
        "port": int(get_cfg("ORACLE_PORT", "1521")),
        "user": get_cfg("ORACLE_USER", ""),
        "password": get_cfg("ORACLE_PASSWORD", ""),
        "service": get_cfg("ORACLE_SERVICE", ""),
        "sid": get_cfg("ORACLE_SID", ""),
        "client_dir": get_cfg("ORACLE_CLIENT_DIR", r"C:\oracle\instantclient_19_23"),
    }
