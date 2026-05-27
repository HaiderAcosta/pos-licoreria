"""Script para poblar la base de datos con datos iniciales."""
from core.database import SessionLocal, engine, Base
from models.usuario import Usuario
from models.categoria import Categoria
from models.producto import Producto
from core.security import get_password_hash

import models.usuario, models.categoria, models.producto, models.venta

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        if db.query(Usuario).first():
            print("Base de datos ya tiene datos. Omitiendo seed.")
            return

        # Usuarios
        admin = Usuario(nombre="Admin Licorería", email="admin@licoreria.com",
                        password=get_password_hash("admin123"), rol="admin")
        cajero = Usuario(nombre="Juan Cajero", email="cajero@licoreria.com",
                         password=get_password_hash("cajero123"), rol="cajero")
        db.add_all([admin, cajero])
        db.flush()

        # Categorías
        cats = ["Aguardiente", "Cerveza", "Ron", "Whisky", "Vino", "Otros"]
        categorias = {}
        for nombre in cats:
            c = Categoria(nombre=nombre)
            db.add(c)
            db.flush()
            categorias[nombre] = c.id

        # Productos
        productos = [
            ("Aguardiente Nectar 750ml", 28000, 20000, 24, categorias["Aguardiente"]),
            ("Aguardiente Antioqueño 750ml", 27000, 19500, 18, categorias["Aguardiente"]),
            ("Cerveza Club Colombia 330ml", 4200, 2800, 120, categorias["Cerveza"]),
            ("Cerveza Poker 330ml", 3500, 2400, 96, categorias["Cerveza"]),
            ("Ron Medellín 700ml", 45000, 32000, 15, categorias["Ron"]),
            ("Whisky Old Parr 750ml", 89000, 65000, 8, categorias["Whisky"]),
            ("Vino Santa Helena 750ml", 22000, 15000, 10, categorias["Vino"]),
            ("Cerveza Heineken 330ml", 5500, 3800, 60, categorias["Cerveza"]),
            ("Ron Bacardí 700ml", 52000, 38000, 3, categorias["Ron"]),
            ("Aguardiente Nectar Naranja 750ml", 28500, 20500, 12, categorias["Aguardiente"]),
        ]

        for nombre, precio_venta, precio_costo, stock, cat_id in productos:
            p = Producto(
                nombre=nombre,
                precio_venta=precio_venta,
                precio_costo=precio_costo,
                stock=stock,
                stock_minimo=5,
                categoria_id=cat_id
            )
            db.add(p)

        db.commit()
        print("✅ Seed completado exitosamente")
        print("   Admin: admin@licoreria.com / admin123")
        print("   Cajero: cajero@licoreria.com / cajero123")
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
