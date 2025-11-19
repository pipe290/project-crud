# backend/app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional, List, Tuple

def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    """
    Crea un producto y lo retorna.
    """
    product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_name(db: Session, name: str) -> Optional[models.Product]:
    """
    Busca un producto por nombre (case-insensitive).
    Normaliza el nombre para hacer una búsqueda segura.
    """
    if not name:
        return None
    # búsqueda case-insensitive
    return db.query(models.Product).filter(func.lower(models.Product.name) == name.strip().lower()).first()


def product_exists_by_name(db: Session, name: str) -> bool:
    return get_product_by_name(db, name) is not None


def create_product_if_not_exists(db: Session, product_in: schemas.ProductCreate) -> Tuple[models.Product, bool]:
    """
    Crea un producto solo si no existe uno con el mismo nombre.
    Retorna (product_obj, created_flag)
    """
    existing = get_product_by_name(db, product_in.name)
    if existing:
        return existing, False
    created = create_product(db, product_in)
    return created, True


def update_product(db: Session, product: models.Product, updates: schemas.ProductUpdate) -> models.Product:
    if updates.name is not None:
        product.name = updates.name
    if updates.description is not None:
        product.description = updates.description
    if updates.price is not None:
        product.price = updates.price
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: models.Product) -> None:
    db.delete(product)
    db.commit()
