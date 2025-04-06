from fastapi import Request, HTTPException, status
import jwt
import logging
from app.core.config import settings
from app.auth.firebase_auth import verify_id_token

# Configure logger
logger = logging.getLogger(__name__)

exempt_paths = [
    "/api/auth/login",
    "/api/auth/register",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/swagger-ui.css",
    "/swagger-ui-bundle.js",
    "/favicon-32x32.png", 
    "/favicon-16x16.png",
    "/swagger-ui-standalone-preset.js",
    "/_static",
]

async def authenticate_user(request: Request, call_next):
    """
    Middleware to authenticate users via Firebase ID token.
    Checks for a valid token in the Authorization header.
    """
    # Skip authentication for exempt paths
    if any(request.url.path.startswith(path) for path in exempt_paths):
        logger.debug(f"Skipping authentication for exempt path: {request.url.path}")
        return await call_next(request)
    
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        if request.url.path.startswith("/api/"):
            logger.warning(f"Missing Authorization header for {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Authorization header",
            )
        # For other paths, proceed without authentication
        logger.debug(f"No auth header for non-API path: {request.url.path} - proceeding")
        return await call_next(request)
    
    try:
        # Extract the token
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )
            
        # Verify Firebase token
        decoded_token = verify_id_token(token)
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        
        # Add the user information to the request scope
        request.scope["user"] = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "is_admin": decoded_token.get("admin", False),  # Set to True for admin users in Firebase custom claims
            "firebase_user": decoded_token
        }
        
    except (ValueError, Exception) as e:
        logger.warning(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    # Proceed with the request
    return await call_next(request)

# Function to get the current admin user (for admin-only endpoints)
def get_current_admin_user(request: Request):
    """
    Dependency function to check if a user is an admin.
    Used in API endpoints that require admin privileges.
    """
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
        
    # Check if user is an admin
    if not user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
        
    return user

# Function to get the current user (for authenticated endpoints)
def get_current_user(request: Request):
    """
    Dependency function to get the current authenticated user.
    Used in API endpoints that require authentication.
    """
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user