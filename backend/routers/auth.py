from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verify_password, create_access_token, get_password_hash
from core.deps import get_current_user
from models.usuario import Usuario
from schemas.usuario import TokenOut, UsuarioOut, LoginRequest, UsuarioCreate

router = APIRouter()

@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not user.activo:
        raise HTTPException(status_code=403, detail="Usuario desactivado")
    token = create_access_token({"sub": str(user.id), "rol": user.rol})
    return {"access_token": token, "token_type": "bearer", "usuario": user}

@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.post("/setup-admin", response_model=UsuarioOut)
def setup_admin(data: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe al menos un usuario en el sistema")
    user = Usuario(
        nombre=data.nombre,
        email=data.email,
        password=get_password_hash(data.password),
        rol="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
