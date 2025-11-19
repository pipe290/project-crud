# app/services/excel_service.py
import pandas as pd
from io import BytesIO
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.validator_service import ExcelValidator
from app.utils.websocket_manager import ws_manager
from app import schemas, crud
from app.utils.logger import log_excel_event


class ExcelService:

    @staticmethod
    async def notify(step: str, progress: int):
        await ws_manager.broadcast({"step": step, "progress": progress})

    @staticmethod
    def load_excel(contents: bytes):
        try:
            return pd.ExcelFile(BytesIO(contents))
        except Exception:
            raise HTTPException(400, "No se pudo leer el archivo Excel.")

    @staticmethod
    def list_sheets(xl: pd.ExcelFile):
        return xl.sheet_names

    @staticmethod
    def preview_sheet(xl: pd.ExcelFile, sheet: str):
        if sheet not in xl.sheet_names:
            raise HTTPException(400, f"La hoja '{sheet}' no existe.")

        df = xl.parse(sheet).fillna("")

        # Previsualizamos solo 10 filas máximas
        return df.head(10).to_dict(orient="records")

    @staticmethod
    async def import_sheet(xl: pd.ExcelFile, sheet: str, db: Session):
        if sheet not in xl.sheet_names:
            raise HTTPException(400, f"La hoja '{sheet}' no existe.")

        df = xl.parse(sheet)
        df.columns = [c.lower().strip() for c in df.columns]

        await ExcelService.notify("Validando columnas", 10)
        ExcelValidator.validate_columns(df)

        await ExcelService.notify("Validando valores", 20)
        ExcelValidator.run_all(df)

        await ExcelService.notify("Importando", 40)

        created_count = 0
        for _, row in df.iterrows():
            product = schemas.ProductCreate(
                name=str(row["name"]),
                description=str(row.get("description", "")),
                price=float(row["price"]),
            )
            crud.create_product(db, product)
            created_count += 1

        await ExcelService.notify("Completado", 100)
        log_excel_event("import_completed", {"sheet": sheet, "count": created_count})

        return created_count
