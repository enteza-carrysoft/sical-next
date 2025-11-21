# backend/main_simple.py
"""
Versión simplificada del backend para pruebas SIN Oracle.
Usa mock data para verificar que FastAPI funciona correctamente.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

# Crear aplicación FastAPI
app = FastAPI(
    title="SICAL Next API - Modo Prueba",
    description="API de prueba sin conexión a Oracle (usa mock data)",
    version="0.1.0-mock",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuración CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class Proveedor(BaseModel):
    id: str
    nif: str
    nombre: str

class FacturaListItem(BaseModel):
    id: str
    numeroFactura: str
    fechaFactura: str
    fechaRegistro: str
    canal: str
    proveedor: Proveedor
    total: float
    estadoTramitacion: str
    estadoContable: str

class AplicacionPresupuestaria(BaseModel):
    ejercicio: str
    organica: str
    funcional: str
    economica: str
    importe: float = 0.0

class TramiteFactura(BaseModel):
    id: str
    facturaId: str
    tipo: str
    fecha: str
    usuario: str
    observaciones: str = None

class Factura(BaseModel):
    id: str
    numeroFactura: str
    fechaFactura: str
    fechaRegistro: str
    canal: str
    proveedor: Proveedor
    baseImponible: float
    iva: float
    total: float
    afecta413: bool = False
    fechaInicioPMP: str = None
    estadoTramitacion: str
    estadoContable: str
    aplicaciones: List[AplicacionPresupuestaria] = []
    tramites: List[TramiteFactura] = []
    numeroObligacion: str = None
    ejercicioObligacion: str = None
    esAbono: bool = False
    facturaAbonadaId: str = None

# Mock Data
MOCK_FACTURAS = [
    FacturaListItem(
        id="1001",
        numeroFactura="F2024/1001",
        fechaFactura="2024-01-15",
        fechaRegistro="2024-01-16T10:30:00",
        canal="FACE",
        proveedor=Proveedor(id="p1", nif="B12345678", nombre="Construcciones García SL"),
        total=5420.50,
        estadoTramitacion="EN_SERVICIO",
        estadoContable="NO_OBLIGADA"
    ),
    FacturaListItem(
        id="1002",
        numeroFactura="F2024/1002",
        fechaFactura="2024-01-20",
        fechaRegistro="2024-01-21T09:15:00",
        canal="MANUAL",
        proveedor=Proveedor(id="p2", nif="B87654321", nombre="Suministros López SA"),
        total=2150.00,
        estadoTramitacion="EN_INTERVENCION",
        estadoContable="NO_OBLIGADA"
    ),
    FacturaListItem(
        id="1003",
        numeroFactura="F2024/1003",
        fechaFactura="2024-02-05",
        fechaRegistro="2024-02-06T11:45:00",
        canal="FACE",
        proveedor=Proveedor(id="p3", nif="A11111111", nombre="Tecnología Avanzada Corp"),
        total=12750.00,
        estadoTramitacion="OBLIGADA",
        estadoContable="OBLIGADA"
    ),
    FacturaListItem(
        id="1004",
        numeroFactura="F2024/1004",
        fechaFactura="2024-02-10",
        fechaRegistro="2024-02-11T14:20:00",
        canal="MANUAL",
        proveedor=Proveedor(id="p4", nif="B99999999", nombre="Servicios Integrales Martínez"),
        total=890.50,
        estadoTramitacion="PAGADA",
        estadoContable="PAGADA"
    ),
]

# Endpoints
@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "SICAL Next API - Modo Prueba (Mock Data)",
        "version": "0.1.0-mock",
        "docs": "/api/docs",
        "note": "Usando datos de prueba. Configure Oracle para datos reales."
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "sical-next-api",
        "mode": "mock",
        "oracle_connected": False
    }

@app.get("/api/facturas", response_model=List[FacturaListItem])
async def listar_facturas(limit: int = 100, offset: int = 0):
    """Lista facturas (mock data)."""
    print(f"GET /api/facturas - Retornando {len(MOCK_FACTURAS)} facturas de prueba")
    return MOCK_FACTURAS[offset:offset+limit]

@app.get("/api/facturas/{factura_id}", response_model=Factura)
async def obtener_factura(factura_id: str):
    """Obtiene detalle de una factura (mock data)."""
    print(f"GET /api/facturas/{factura_id} - Retornando factura de prueba")

    # Buscar en mock data
    factura_list = next((f for f in MOCK_FACTURAS if f.id == factura_id), None)

    if not factura_list:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")

    # Crear factura completa con trámites
    return Factura(
        id=factura_list.id,
        numeroFactura=factura_list.numeroFactura,
        fechaFactura=factura_list.fechaFactura,
        fechaRegistro=factura_list.fechaRegistro,
        canal=factura_list.canal,
        proveedor=factura_list.proveedor,
        baseImponible=round(factura_list.total / 1.21, 2),
        iva=round(factura_list.total - (factura_list.total / 1.21), 2),
        total=factura_list.total,
        afecta413=True,
        fechaInicioPMP=factura_list.fechaRegistro,
        estadoTramitacion=factura_list.estadoTramitacion,
        estadoContable=factura_list.estadoContable,
        aplicaciones=[
            AplicacionPresupuestaria(
                ejercicio="2024",
                organica="100",
                funcional="920",
                economica="22699",
                importe=factura_list.total
            )
        ],
        tramites=[
            TramiteFactura(
                id="t1",
                facturaId=factura_list.id,
                tipo="REGISTRADA",
                fecha=factura_list.fechaRegistro,
                usuario="Registro General",
                observaciones="Factura registrada (MOCK DATA)"
            ),
            TramiteFactura(
                id="t2",
                facturaId=factura_list.id,
                tipo=factura_list.estadoTramitacion,
                fecha=factura_list.fechaRegistro,
                usuario="Sistema",
                observaciones="Estado actual (MOCK DATA)"
            ),
        ],
        esAbono=False
    )


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("SICAL Next API - Modo Prueba (Mock Data)")
    print("="*60)
    print("Servidor iniciando en http://localhost:8000")
    print("Documentacion: http://localhost:8000/api/docs")
    print("Usando datos de prueba (sin conexion a Oracle)")
    print("="*60 + "\n")

    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
