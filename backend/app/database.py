"""
database.py
Configuración de la conexión a PostgreSQL con SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# --- Cargar variables de entorno desde .env ---
load_dotenv()  # Esto permite usar un archivo .env en backend/

# --- Configuración de la base de datos ---
POSTGRES_USER = os.getenv("DB_USER", "crud_user")
POSTGRES_PASSWORD = os.getenv("DB_PASS", "1234")
POSTGRES_DB = os.getenv("DB_NAME", "crud_db")
POSTGRES_HOST = os.getenv("DB_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("DB_PORT", "5432")

# URL de conexión
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# --- Crear motor SQLAlchemy ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Cambia a False en producción
    pool_pre_ping=True  # Evita errores de conexión inactiva
)

# --- Crear sesión ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base para modelos ---
Base = declarative_base()

# --- Dependencia para inyectar la sesión en endpoints ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
