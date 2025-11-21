# backend/domain/models/factura.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class Proveedor(BaseModel):
    """Modelo de proveedor."""
    id: str
    nif: str
    nombre: str


class AplicacionPresupuestaria(BaseModel):
    """Aplicación presupuestaria."""
    ejercicio: str
    organica: str
    funcional: str
    economica: str
    importe: float = 0.0


class TramiteFactura(BaseModel):
    """Trámite de una factura."""
    id: str
    facturaId: str
    tipo: str
    fecha: str  # ISO format
    usuario: str
    observaciones: Optional[str] = None


class Factura(BaseModel):
    """Modelo completo de factura."""
    id: str
    numeroFactura: str
    fechaFactura: str
    fechaRegistro: str
    canal: str  # "MANUAL" | "FACE" | "OTRO"
    proveedor: Proveedor
    baseImponible: float
    iva: float
    total: float

    # Info 413 / morosidad / PMP
    afecta413: bool = False
    fechaInicioPMP: Optional[str] = None

    estadoTramitacion: str
    estadoContable: str

    aplicaciones: List[AplicacionPresupuestaria] = []
    tramites: List[TramiteFactura] = []

    # Campos mínimos para obligación
    numeroObligacion: Optional[str] = None
    ejercicioObligacion: Optional[str] = None

    # Abonos
    esAbono: bool = False
    facturaAbonadaId: Optional[str] = None


class FacturaListItem(BaseModel):
    """Modelo simplificado para listado de facturas."""
    id: str
    numeroFactura: str
    fechaFactura: str
    fechaRegistro: str
    canal: str
    proveedor: Proveedor
    total: float
    estadoTramitacion: str
    estadoContable: str
