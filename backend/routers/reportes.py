from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from core.database import get_db
from core.deps import require_admin
from models.venta import Venta, DetalleVenta
from models.producto import Producto

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(require_admin)):
    hoy = date.today()
    inicio_hoy = datetime.combine(hoy, datetime.min.time())
    fin_hoy = datetime.combine(hoy, datetime.max.time())

    ventas_hoy = db.query(Venta).filter(Venta.created_at.between(inicio_hoy, fin_hoy)).all()
    total_hoy = sum(v.total for v in ventas_hoy)
    num_transacciones = len(ventas_hoy)

    productos_bajo_stock = db.query(Producto).filter(Producto.stock <= Producto.stock_minimo).count()
    total_productos = db.query(Producto).count()

    top_productos = db.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label("total_vendido"),
        func.sum(DetalleVenta.subtotal).label("total_ingresos")
    ).join(DetalleVenta).join(Venta).filter(
        Venta.created_at.between(inicio_hoy, fin_hoy)
    ).group_by(Producto.id).order_by(func.sum(DetalleVenta.cantidad).desc()).limit(5).all()

    return {
        "fecha": hoy.isoformat(),
        "total_ventas_hoy": round(total_hoy, 2),
        "num_transacciones": num_transacciones,
        "productos_bajo_stock": productos_bajo_stock,
        "total_productos": total_productos,
        "top_productos": [
            {"nombre": p.nombre, "total_vendido": p.total_vendido, "total_ingresos": round(p.total_ingresos, 2)}
            for p in top_productos
        ]
    }

@router.get("/cierre-caja")
def cierre_caja(cajero_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    hoy = date.today()
    inicio = datetime.combine(hoy, datetime.min.time())
    fin = datetime.combine(hoy, datetime.max.time())
    ventas = db.query(Venta).filter(
        Venta.cajero_id == cajero_id,
        Venta.created_at.between(inicio, fin)
    ).all()
    total = sum(v.total for v in ventas)
    return {
        "cajero_id": cajero_id,
        "fecha": hoy.isoformat(),
        "total_ventas": round(total, 2),
        "num_transacciones": len(ventas)
    }

@router.get("/inventario")
def reporte_inventario(db: Session = Depends(get_db), _=Depends(require_admin)):
    productos = db.query(Producto).order_by(Producto.nombre).all()
    return {
        "total_productos": len(productos),
        "valor_costo_total": round(sum(p.precio_costo * p.stock for p in productos), 2),
        "valor_venta_total": round(sum(p.precio_venta * p.stock for p in productos), 2),
        "productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "stock": p.stock,
                "stock_minimo": p.stock_minimo,
                "precio_venta": p.precio_venta,
                "precio_costo": p.precio_costo,
                "valor_venta": round(p.precio_venta * p.stock, 2),
                "alerta_stock": p.stock <= p.stock_minimo
            }
            for p in productos
        ]
    }
