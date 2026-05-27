from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from core.security import get_current_user, require_admin, hash_password
from models.categoria import Categoria
from models.usuario import Usuario
from schemas.schemas import CategoriaCreate, CategoriaOut, UsuarioCreate, UsuarioOut

# ── Categorías ────────────────────────────────────────
cat_router = APIRouter(prefix="/categorias", tags=["Categorías"])

@cat_router.get("/", response_model=List[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Categoria).order_by(Categoria.nombre).all()

@cat_router.post("/", response_model=CategoriaOut, status_code=201)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Categoria).filter(Categoria.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    c = Categoria(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@cat_router.delete("/{cat_id}", status_code=204)
def eliminar_categoria(cat_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(c)
    db.commit()


# ── Usuarios ──────────────────────────────────────────
usr_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@usr_router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(Usuario).all()

@usr_router.post("/", response_model=UsuarioOut, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    u = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
        rol=data.rol
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@usr_router.put("/{user_id}/desactivar", response_model=UsuarioOut)
def desactivar_usuario(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    u.activo = False
    db.commit()
    db.refresh(u)
    return u
