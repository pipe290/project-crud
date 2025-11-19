# app/routers/logs_routes.py
from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

LOG_PATH = "app/logs/excel_logs.json"

@router.get("/excel", summary="Get Excel logs")
def get_excel_logs():
    if not os.path.exists(LOG_PATH):
        return {"logs": []}

    try:
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
            return {"logs": data}
    except:
        raise HTTPException(status_code=500, detail="Error leyendo logs")
