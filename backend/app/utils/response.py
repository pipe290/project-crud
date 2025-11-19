def build_response(message: str, status: str, data=None):
    """
    Devuelve un formato de respuesta estándar para toda la API.
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }
