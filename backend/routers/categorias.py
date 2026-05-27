from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.deps import get_current_user, require_admin
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate, CategoriaOut
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CategoriaOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Categoria).all()

@router.post("/", response_model=CategoriaOut)
def crear(data: CategoriaCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Categoria).filter(Categoria.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    cat = Categoria(nombre=data.nombre)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}")
def eliminar(cat_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(cat)
    db.commit()
    return {"mensaje": "Categoría eliminada"}
