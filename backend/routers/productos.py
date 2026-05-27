from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.deps import get_current_user, require_admin
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut

router = APIRouter()

@router.get("/", response_model=List[ProductoOut])
def listar(categoria_id: Optional[int] = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(Producto)
    if categoria_id:
        q = q.filter(Producto.categoria_id == categoria_id)
    return q.order_by(Producto.nombre).all()

@router.get("/stock-bajo", response_model=List[ProductoOut])
def stock_bajo(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Producto).filter(Producto.stock <= Producto.stock_minimo).all()

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener(producto_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

@router.post("/", response_model=ProductoOut)
def crear(data: ProductoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = Producto(**data.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{producto_id}")
def eliminar(producto_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()
    return {"mensaje": "Producto eliminado"}
