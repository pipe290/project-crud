"""
FastAPI application with CRUD endpoints and Excel uploader module.
Includes CORS configuration, DB session management, and error handling.
"""

from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

# --- Imports internos ---
from app import models, schemas, crud
from app.database import engine, get_db
from app.utils.response import build_response
from app.routers import excel_routes

# --- Inicializar la app ---
app = FastAPI(
    title="CRUD FastAPI - Profesional con Cargador Excel",
    version="2.0.0",
    description="API con endpoints CRUD de productos y módulo de carga de archivos Excel."
)

# --- Configuración CORS ---
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Crear tablas en la BD ---
models.Base.metadata.create_all(bind=engine)

# --- Importar router Excel ---
app.include_router(excel_routes.router, prefix="/excel", tags=["Excel"])

# ---------------------------------------------------------
#                   ENDPOINTS CRUD PRODUCTOS
# ---------------------------------------------------------

@app.get("/", summary="Health check")
def health():
    return {"status": "ok"}

@app.post("/products", response_model=schemas.ProductOut, status_code=201)
def create_product_endpoint(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_product(db, product_in)
        return JSONResponse(
            status_code=201,
            content=build_response(
                "Product created successfully", 
                "success", 
                data=jsonable_encoder(created)
            )
        )
    except Exception as e:
        print("[ERROR create_product]", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/products", summary="List products")
def list_products(skip: int = Query(0, ge=0), limit: int = Query(20000, ge=1, le=50000),
                  db: Session = Depends(get_db)):
    try:
        items = crud.get_products(db, skip=skip, limit=limit)
        return build_response(
            "Products fetched successfully", 
            "success", 
            data=jsonable_encoder(items)
        )
    except Exception as e:
        print("[ERROR list_products]", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/products/{product_id}", summary="Get a product by ID")
def get_product_by_id(product_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        return build_response(
            "Product fetched successfully", 
            "success", 
            data=jsonable_encoder(item)
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        print("[ERROR get_product_by_id]", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/products/{product_id}", summary="Update product")
def update_product(product_id: int, payload: schemas.ProductUpdate, db: Session = Depends(get_db)):
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        updated = crud.update_product(db, item, payload)
        return build_response(
            "Product updated successfully", 
            "success", 
            data=jsonable_encoder(updated)
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        print("[ERROR update_product]", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/products/{product_id}", summary="Delete product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        crud.delete_product(db, item)
        return build_response("Product deleted successfully", "success")
    except HTTPException as he:
        raise he
    except Exception as e:
        print("[ERROR delete_product]", e)
        raise HTTPException(status_code=500, detail="Internal server error")
