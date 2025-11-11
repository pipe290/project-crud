"""
FastAPI application with CRUD endpoints.
Each endpoint uses try/except/finally and closes the DB session.
CORS enabled for frontend requests.
"""

from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import List

from app import models, schemas, crud
from app.database import SessionLocal, engine, Base
from app.utils.response import build_response

# Create tables on startup if not present. In production use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD FastAPI - Profesional", version="1.0.0")

# --- CORS middleware ---
origins = [
    "http://localhost:8080",  # tu frontend
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# --- Health check ---
@app.get("/", summary="Health check")
def health():
    return {"status": "ok"}

# --- Create product ---
@app.post("/products", response_model=schemas.ProductOut, status_code=201)
def create_product(product_in: schemas.ProductCreate):
    db = SessionLocal()
    try:
        created = crud.create_product(db, product_in)
        data = jsonable_encoder(created)
        response = build_response("Product created", "success", data=data)
        return JSONResponse(status_code=201, content=response)
    except Exception as e:
        print(e)  # Debug
        return JSONResponse(status_code=500, content=build_response("Internal server error", "error"))
    finally:
        db.close()

# --- List products ---
@app.get("/products", summary="List products")
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    db = SessionLocal()
    try:
        items = crud.get_products(db, skip=skip, limit=limit)
        data = jsonable_encoder(items)
        return build_response("Products fetched", "success", data=data)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content=build_response("Internal server error", "error"))
    finally:
        db.close()

# --- Get product by ID ---
@app.get("/products/{product_id}", summary="Get a product by id")
def get_product_by_id(product_id: int = Path(..., ge=1)):
    db = SessionLocal()
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        data = jsonable_encoder(item)
        return build_response("Product fetched", "success", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content=build_response("Internal server error", "error"))
    finally:
        db.close()

# --- Update product ---
@app.put("/products/{product_id}", summary="Update product")
def update_product(product_id: int, payload: schemas.ProductUpdate):
    db = SessionLocal()
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        updated = crud.update_product(db, item, payload)
        data = jsonable_encoder(updated)
        return build_response("Product updated", "success", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content=build_response("Internal server error", "error"))
    finally:
        db.close()

# --- Delete product ---
@app.delete("/products/{product_id}", summary="Delete product")
def delete_product(product_id: int):
    db = SessionLocal()
    try:
        item = crud.get_product(db, product_id=product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        crud.delete_product(db, item)
        return build_response("Product deleted", "success")
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content=build_response("Internal server error", "error"))
    finally:
        db.close()
