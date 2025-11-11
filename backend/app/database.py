"""
Database utilities: engine and SessionLocal creation.
All imports at top as required.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres123")
DB_NAME = os.getenv("DB_NAME", "crud_db")
DB_HOST = os.getenv("DB_HOST", "postgres_crud")
DB_PORT = os.getenv("DB_PORT", "5432")

# Standard SQLAlchemy DB URL for Postgres
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# create engine with pool_pre_ping to avoid stale connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal factory used to create DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
