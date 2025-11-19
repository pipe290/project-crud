# app/services/validator_service.py
import pandas as pd
from fastapi import HTTPException

class ExcelValidator:

    REQUIRED_COLUMNS = {"name", "description", "price"}

    @staticmethod
    def validate_columns(df: pd.DataFrame):
        cols = set(df.columns)
        if not ExcelValidator.REQUIRED_COLUMNS.issubset(cols):
            raise HTTPException(
                status_code=400,
                detail=f"El Excel debe contener columnas: {ExcelValidator.REQUIRED_COLUMNS}"
            )

    @staticmethod
    def validate_empty_values(df: pd.DataFrame):
        if df.isnull().any().any():
            raise HTTPException(
                status_code=400,
                detail="El Excel contiene valores vacíos. Revísalo."
            )

    @staticmethod
    def validate_numeric(df: pd.DataFrame):
        try:
            df["price"] = pd.to_numeric(df["price"])
        except:
            raise HTTPException(
                status_code=400,
                detail="La columna 'price' contiene valores no numéricos."
            )

    @staticmethod
    def run_all(df: pd.DataFrame):
        ExcelValidator.validate_columns(df)
        ExcelValidator.validate_empty_values(df)
        ExcelValidator.validate_numeric(df)
