# backend/api/facturas_router.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from backend.domain.models.factura import Factura, FacturaListItem
from backend.application.services.factura_service import FacturaService

router = APIRouter(prefix="/api/facturas", tags=["facturas"])


@router.get("", response_model=List[FacturaListItem])
async def listar_facturas(
    limit: int = Query(default=100, le=1000, description="Máximo de resultados"),
    offset: int = Query(default=0, ge=0, description="Offset para paginación")
):
    """
    Lista facturas desde la base de datos SICAL.

    - **limit**: Número máximo de resultados (máx 1000)
    - **offset**: Desplazamiento para paginación
    """
    try:
        service = FacturaService()
        facturas = service.listar_facturas(limit=limit, offset=offset)
        service.close()
        return facturas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo facturas: {str(e)}")


@router.get("/{factura_id}", response_model=Factura)
async def obtener_factura(factura_id: str):
    """
    Obtiene detalle completo de una factura por su ID (NFACREG).

    - **factura_id**: ID de la factura en SICAL
    """
    try:
        service = FacturaService()
        factura = service.obtener_factura(factura_id)
        service.close()

        if not factura:
            raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")

        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo factura: {str(e)}")


@router.get("/health", tags=["health"])
async def health_check():
    """Endpoint de health check."""
    return {"status": "ok", "service": "facturas"}
