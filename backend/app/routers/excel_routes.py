# app/routers/excel_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from app.database import get_db
from app.services.excel_service import ExcelService
from app.utils.response import build_response
from app.services.validator_service import ExcelValidator

router = APIRouter()


# ============================================================
#   1️⃣ LISTAR HOJAS DEL EXCEL
# ============================================================
@router.post("/sheets")
async def list_sheets(file: UploadFile = File(...)):
    contents = await file.read()
    xl = ExcelService.load_excel(contents)
    return {"sheets": ExcelService.list_sheets(xl)}


# ============================================================
#   2️⃣ PREVISUALIZAR HOJA
# ============================================================
@router.post("/preview/{sheet}")
async def preview_sheet(sheet: str, file: UploadFile = File(...)):
    contents = await file.read()
    xl = ExcelService.load_excel(contents)

    preview = ExcelService.preview_sheet(xl, sheet)
    return {"preview": preview}


# ============================================================
#   3️⃣ IMPORTAR UNA HOJA COMPLETA
# ============================================================
@router.post("/import/{sheet}")
async def import_sheet(sheet: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    xl = ExcelService.load_excel(contents)

    count = await ExcelService.import_sheet(xl, sheet, db)

    return build_response(
        message=f"{count} productos importados",
        status="success",
        data={"count": count}
    )


# ============================================================
#   4️⃣ ENDPOINT ANTIGUO (RESPALDO)
# ============================================================
@router.post("/upload-basic")
async def upload_basic(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Archivo inválido")

    contents = await file.read()
    excel_data = BytesIO(contents)

    df = pd.read_excel(excel_data)
    df.columns = [c.lower().strip() for c in df.columns]

    ExcelValidator.run_all(df)

    for _, row in df.iterrows():
        product_in = {
            "name": str(row["name"]),
            "description": str(row["description"]),
            "price": float(row["price"])
        }
        print("Producto cargado:", product_in)

    return build_response("Archivo procesado (modo básico)", "success")


@router.post("/upload")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint NUEVO para cargar archivos Excel desde el frontend.
    """
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Archivo inválido. Solo se aceptan .xls o .xlsx")

    contents = await file.read()
    xl = ExcelService.load_excel(contents)

    # Obtenemos la primera hoja automáticamente
    sheets = ExcelService.list_sheets(xl)
    if not sheets:
        raise HTTPException(status_code=400, detail="El archivo no contiene hojas.")

    default_sheet = sheets[0]

    count = await ExcelService.import_sheet(xl, default_sheet, db)

    return build_response(
        message=f"{count} productos importados correctamente",
        status="success",
        data={"count": count}
    )

