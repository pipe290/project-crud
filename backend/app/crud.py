"""
CRUD operations for Product.
"""

from sqlalchemy.orm import Session
from app import models, schemas

# -------------------------
# CREATE
# -------------------------
def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# -------------------------
# READ
# -------------------------
def get_product(db: Session, product_id: int) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()

# -------------------------
# UPDATE
# -------------------------
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

# -------------------------
# DELETE
# -------------------------
def delete_product(db: Session, product: models.Product) -> None:
    db.delete(product)
    db.commit()
