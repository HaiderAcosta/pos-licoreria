from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""
    precio_venta: float
    precio_costo: Optional[float] = 0.0
    stock: Optional[int] = 0
    stock_minimo: Optional[int] = 5
    categoria_id: Optional[int] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    precio_costo: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio_venta: float
    precio_costo: float
    stock: int
    stock_minimo: int
    categoria_id: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True
