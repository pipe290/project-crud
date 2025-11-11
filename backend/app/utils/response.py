"""
Utility to standardize API responses.
"""

from typing import Any, Optional, Dict

def build_response(message: str, status: str = "success", data: Optional[Any] = None) -> Dict[str, Any]:
    """
    Standard response format.
    - message: human readable message
    - status: 'success'|'error'
    - data: optional; payload (can be dict, list, None)
    """
    payload = {"message": message, "status": status}
    if data is not None:
        payload["data"] = data
    return payload
