# Backend SICAL Next

API Backend para el tramitador de facturas SICAL - Diputación de Sevilla.

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- Oracle Instant Client 19c o superior
- Acceso a base de datos Oracle SICAL

### Instalación de Oracle Instant Client

**Windows:**
1. Descargar desde [Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/downloads.html)
2. Extraer en `C:\oracle\instantclient_19_23\`
3. Añadir al PATH del sistema (opcional)

**Linux:**
```bash
# Descargar e instalar
wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linux.x64-19.23.0.0.0dbru.zip
unzip instantclient-basic-linux.x64-19.23.0.0.0dbru.zip -d /opt/oracle
export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_23:$LD_LIBRARY_PATH
```

### Configuración del Entorno

1. **Copiar archivo de configuración:**
```bash
cp ../.env.example ../.env
```

2. **Editar `.env` con tus credenciales:**
```bash
ORACLE_HOST=tu_servidor_oracle
ORACLE_PORT=1521
ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_password
ORACLE_SERVICE=ORCL
ORACLE_CLIENT_DIR=C:\oracle\instantclient_19_23
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🏃 Ejecución

### Modo Desarrollo
```bash
# Desde la raíz del proyecto
python backend/main.py

# O usando uvicorn directamente
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/api/docs
- Documentación alternativa (ReDoc): http://localhost:8000/api/redoc

### Modo Producción
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Endpoints Disponibles

### Facturas

**Listar facturas**
```
GET /api/facturas
Query params:
  - limit: int (default: 100, max: 1000)
  - offset: int (default: 0)
```

**Obtener detalle de factura**
```
GET /api/facturas/{factura_id}
Path params:
  - factura_id: ID de la factura (NFACREG)
```

### Health Check
```
GET /health
GET /api/facturas/health
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=backend --cov-report=html

# Ver reporte
open htmlcov/index.html
```

## 📁 Estructura

```
backend/
├── main.py                          # Punto de entrada FastAPI
├── requirements.txt                 # Dependencias Python
├── README.md                        # Esta documentación
│
├── api/                             # 🌐 Capa de presentación
│   └── facturas_router.py          # Endpoints de facturas
│
├── application/                     # 🎯 Casos de uso
│   └── services/
│       └── factura_service.py      # Lógica de negocio facturas
│
├── domain/                          # 💎 Modelos de dominio
│   └── models/
│       └── factura.py              # Modelos Pydantic
│
└── core/                            # 🔧 Utilidades core
    ├── config.py                   # Configuración
    └── db.py                       # Conexión Oracle
```

## 🔒 Seguridad

- **NO** commitear el archivo `.env` al repositorio
- Las credenciales de Oracle deben mantenerse seguras
- Usar variables de entorno en producción
- Implementar autenticación JWT (pendiente)

## 🐛 Troubleshooting

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"
- Verificar que Oracle Instant Client está instalado
- Verificar que `ORACLE_CLIENT_DIR` apunta al directorio correcto
- En Windows, verificar que es la versión 64-bit

### Error: "ORA-12154: TNS:could not resolve the connect identifier"
- Verificar `ORACLE_SERVICE` o `ORACLE_SID` en `.env`
- Verificar conectividad con el servidor Oracle
- Verificar `ORACLE_HOST` y `ORACLE_PORT`

### Error de conexión a base de datos
```bash
# Testear conexión manualmente
python -c "from backend.core.db import get_connection_for_sid; conn = get_connection_for_sid(); print('✓ Conexión exitosa')"
```

## 📝 TODOs

- [ ] Implementar autenticación JWT
- [ ] Añadir tests unitarios y de integración
- [ ] Implementar caché con Redis
- [ ] Añadir logging estructurado
- [ ] Implementar rate limiting
- [ ] Añadir validación de permisos por área/unidad
- [ ] Obtener trámites reales desde BD
- [ ] Calcular estados reales de tramitación y contables
