from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routers import auth, productos, ventas, categorias, reportes, usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POS Licorería - API",
    description="Sistema POS para gestión de inventarios y ventas en microempresas del sector licorero de Fusagasugá",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://pos-licoreria-frontend.onrender.com"
],
allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,       prefix="/auth",       tags=["Autenticación"])
app.include_router(productos.router,  prefix="/productos",  tags=["Productos"])
app.include_router(ventas.router,     prefix="/ventas",     tags=["Ventas"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])
app.include_router(reportes.router,   prefix="/reportes",   tags=["Reportes"])
app.include_router(usuarios.router,   prefix="/usuarios",   tags=["Usuarios"])

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "mensaje": "POS Licorería API funcionando"}
