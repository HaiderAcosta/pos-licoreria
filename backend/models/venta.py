from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Venta(Base):
    __tablename__ = "ventas"
    id          = Column(Integer, primary_key=True, index=True)
    cajero_id   = Column(Integer, ForeignKey("usuarios.id"))
    total       = Column(Float, nullable=False)
    metodo_pago = Column(String, default="efectivo")
    created_at  = Column(DateTime, default=datetime.utcnow)
    cajero      = relationship("Usuario", back_populates="ventas")
    detalles    = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"
    id          = Column(Integer, primary_key=True, index=True)
    venta_id    = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad    = Column(Integer, nullable=False)
    precio_unit = Column(Float, nullable=False)
    subtotal    = Column(Float, nullable=False)
    venta       = relationship("Venta", back_populates="detalles")
    producto    = relationship("Producto", back_populates="detalles")
