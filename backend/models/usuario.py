from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id         = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    rol        = Column(String, default="cajero")  # admin | cajero
    activo     = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    ventas     = relationship("Venta", back_populates="cajero")
