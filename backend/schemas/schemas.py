from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── Auth ──────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    rol: str
    nombre: str


# ── Usuarios ──────────────────────────────────────────
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "cajero"

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool
    creado_en: datetime
    class Config:
        from_attributes = True


# ── Categorías ────────────────────────────────────────
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    class Config:
        from_attributes = True


# ── Productos ─────────────────────────────────────────
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    precio_costo: float = 0
    stock: int = 0
    stock_minimo: int = 5
    categoria_id: Optional[int] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    precio_costo: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio_venta: float
    precio_costo: float
    stock: int
    stock_minimo: int
    activo: bool
    categoria: Optional[CategoriaOut]
    class Config:
        from_attributes = True


# ── Ventas ────────────────────────────────────────────
class ItemVentaCreate(BaseModel):
    producto_id: int
    cantidad: int

class ItemVentaOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto: Optional[ProductoOut]
    class Config:
        from_attributes = True

class VentaCreate(BaseModel):
    items: List[ItemVentaCreate]
    metodo_pago: str = "efectivo"

class VentaOut(BaseModel):
    id: int
    cajero_id: int
    total: float
    metodo_pago: str
    fecha: datetime
    items: List[ItemVentaOut]
    cajero: Optional[UsuarioOut]
    class Config:
        from_attributes = True


# ── Dashboard ─────────────────────────────────────────
class ProductoTop(BaseModel):
    producto_id: int
    nombre: str
    total_vendido: int

class DashboardOut(BaseModel):
    ventas_hoy: float
    transacciones_hoy: int
    productos_stock_bajo: int
    top_productos: List[ProductoTop]
