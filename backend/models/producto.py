from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "productos"
    id           = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String, nullable=False, index=True)
    descripcion  = Column(String, default="")
    precio_venta = Column(Float, nullable=False)
    precio_costo = Column(Float, default=0.0)
    stock        = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    categoria    = relationship("Categoria", back_populates="productos")
    detalles     = relationship("DetalleVenta", back_populates="producto")
