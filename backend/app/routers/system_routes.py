# app/routers/system_routes.py
from fastapi import APIRouter, Request
import os
import sys

router = APIRouter()

@router.get("/routes", summary="List all API routes")
async def list_routes(request: Request):
    routes_info = []
    for route in request.app.routes:
        routes_info.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods)
        })
    return {"routes": routes_info}

@router.post("/restart", summary="Restart backend server")
async def restart_server():
    python = sys.executable
    os.execl(python, python, *sys.argv)
