# 🍾 POS Licorería Fusagasugá

Sistema POS para gestión de inventarios y ventas en microempresas del sector licorero de Fusagasugá. Desarrollado con metodología RAD.

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML5 + CSS3 + JavaScript vanilla |
| Backend | Python 3.11 + FastAPI |
| Base de datos | SQLite (local) / PostgreSQL (producción) |
| ORM | SQLAlchemy |
| Autenticación | JWT (python-jose + bcrypt) |
| Deploy Frontend | Vercel / Netlify |
| Deploy Backend | Render.com |

## Instalación local

### Backend

```bash
cd backend
pip install -r requirements.txt
python seed.py          # Carga datos de prueba
uvicorn main:app --reload --port 8000
```

API disponible en: http://localhost:8000  
Documentación Swagger: http://localhost:8000/docs

### Frontend

```bash
# Opción 1: servidor simple
cd frontend
python3 -m http.server 3000

# Opción 2: Live Server de VS Code
# Abrir frontend/index.html con Live Server
```

Frontend en: http://localhost:3000

## Credenciales de prueba

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Administrador | admin@licoreria.com | admin123 |
| Cajero | cajero@licoreria.com | cajero123 |

## Módulos del sistema

- **Punto de venta (POS)**: carrito, búsqueda, cobro, métodos de pago
- **Inventario**: CRUD productos, alertas de stock bajo, categorías
- **Dashboard**: métricas del día, top productos, indicadores
- **Historial de ventas**: por fecha, cajero, con detalles
- **Usuarios**: gestión de roles (admin/cajero), activar/desactivar

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /auth/login | Iniciar sesión |
| GET | /productos/ | Listar productos |
| POST | /productos/ | Crear producto (admin) |
| POST | /ventas/ | Registrar venta |
| GET | /reportes/dashboard | Métricas del día |
| GET | /ventas/ | Historial (admin) |
| GET | /productos/stock-bajo | Alertas inventario |

## Despliegue en Render (backend)

1. Crear cuenta en render.com
2. New > Web Service > conectar repositorio GitHub
3. Variables de entorno:
   - `DATABASE_URL`: URL de PostgreSQL (Render ofrece DB gratuita)
   - `SECRET_KEY`: clave secreta larga y aleatoria
4. Build Command: `pip install -r requirements.txt && python seed.py`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Despliegue en Vercel (frontend)

1. En `frontend/index.html` cambiar la constante `API` por la URL de Render
2. Crear cuenta en vercel.com
3. Import > carpeta `frontend/`
4. Deploy (sin configuración adicional)

## Estructura del repositorio

```
pos-licoreria/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── seed.py
│   ├── Procfile
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── deps.py
│   ├── models/
│   │   ├── usuario.py
│   │   ├── categoria.py
│   │   ├── producto.py
│   │   └── venta.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── venta.py
│   │   └── categoria.py
│   └── routers/
│       ├── auth.py
│       ├── productos.py
│       ├── ventas.py
│       ├── categorias.py
│       ├── reportes.py
│       └── usuarios.py
└── frontend/
    └── index.html
```

## Metodología RAD aplicada

| Fase | Duración | Entregable |
|------|----------|-----------|
| Requisitos | Día 1 | RF/RNF, historias de usuario |
| Prototipo | Día 1 | Wireframes + diseño UI |
| Iteración 1 | Día 2 | Estructura base + login |
| Iteración 2 | Día 3 | Módulos principales funcionales |
| Iteración 3 | Día 4 | Integración + despliegue |
| Pruebas | Día 5 | Plan + evidencias + correcciones |
