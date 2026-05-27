from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DetalleVentaIn(BaseModel):
    producto_id: int
    cantidad: int

class VentaCreate(BaseModel):
    detalles: List[DetalleVentaIn]
    metodo_pago: Optional[str] = "efectivo"

class DetalleVentaOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unit: float
    subtotal: float
    class Config:
        from_attributes = True

class VentaOut(BaseModel):
    id: int
    cajero_id: int
    total: float
    metodo_pago: str
    created_at: datetime
    detalles: List[DetalleVentaOut]
    class Config:
        from_attributes = True

class CierreVentaOut(BaseModel):
    total_ventas: float
    num_transacciones: int
    fecha: str
