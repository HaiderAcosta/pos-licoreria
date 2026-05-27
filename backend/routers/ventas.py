from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from core.database import get_db
from core.deps import get_current_user, require_admin
from models.venta import Venta, DetalleVenta
from models.producto import Producto
from models.usuario import Usuario
from schemas.venta import VentaCreate, VentaOut

router = APIRouter()

@router.post("/", response_model=VentaOut)
def registrar_venta(data: VentaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    total = 0.0
    detalles_data = []
    for item in data.detalles:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
        if producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
        subtotal = producto.precio_venta * item.cantidad
        total += subtotal
        detalles_data.append((producto, item.cantidad, producto.precio_venta, subtotal))

    venta = Venta(cajero_id=current_user.id, total=round(total, 2), metodo_pago=data.metodo_pago)
    db.add(venta)
    db.flush()

    for producto, cantidad, precio_unit, subtotal in detalles_data:
        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=producto.id,
            cantidad=cantidad,
            precio_unit=precio_unit,
            subtotal=subtotal
        )
        db.add(detalle)
        producto.stock -= cantidad

    db.commit()
    db.refresh(venta)
    return venta

@router.get("/", response_model=List[VentaOut])
def listar_ventas(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    cajero_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    from datetime import datetime
    q = db.query(Venta)
    if fecha_inicio:
        q = q.filter(Venta.created_at >= datetime.combine(fecha_inicio, datetime.min.time()))
    if fecha_fin:
        q = q.filter(Venta.created_at <= datetime.combine(fecha_fin, datetime.max.time()))
    if cajero_id:
        q = q.filter(Venta.cajero_id == cajero_id)
    return q.order_by(Venta.created_at.desc()).all()

@router.get("/mis-ventas", response_model=List[VentaOut])
def mis_ventas(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    from datetime import datetime, date
    hoy = date.today()
    return db.query(Venta).filter(
        Venta.cajero_id == current_user.id,
        Venta.created_at >= datetime.combine(hoy, datetime.min.time())
    ).order_by(Venta.created_at.desc()).all()

@router.get("/{venta_id}", response_model=VentaOut)
def obtener_venta(venta_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    v = db.query(Venta).filter(Venta.id == venta_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return v
