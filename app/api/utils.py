from typing import Any, Dict, Optional

def create_response(success: bool, data: Any = None, message: str = "", error: Optional[Dict] = None) -> Dict:
    """Creates a standardized API response."""
    response: Dict[str, Any] = {"success": success, "message": message}
    if data is not None:
        response["data"] = data
    else:
        response["data"] = {}  # Ensure data is always present
    if error:
        response["error"] = error
    return response

#  Example usage (you don't need this in the utils.py file, it's just for illustration):
# from fastapi import APIRouter
# router = APIRouter()

# @router.get("/example")
# async def example_endpoint():
#   # ... your logic ...
#   if success:
#     return create_response(success=True, data={"result": "Operation successful"}, message="Success!")
#   else:
#     return create_response(success=False, error={"code": 500, "message": "Something went wrong"}, message="An error occurred.")
