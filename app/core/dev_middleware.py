from fastapi import Request, HTTPException, status
import logging

# Configure logger
logger = logging.getLogger(__name__)

async def dev_authenticate_user(request: Request, call_next):
    """
    Development middleware that bypasses authentication.
    Use this only for development and testing purposes.
    """
    # Add mock user to the request
    request.scope["user"] = {
        "uid": "test-user-id",
        "user_id": "test-user-id",
        "email": "test@example.com",
        "name": "Test User",
        "is_admin": True,
        "firebase_user": {"uid": "test-user-id"}
    }
    
    logger.debug(f"Development middleware: Added test user for path {request.url.path}")
    return await call_next(request)
