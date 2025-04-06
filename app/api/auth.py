from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import Dict
from app.core.session import create_session

router = APIRouter()

class LoginRequest(BaseModel):
    token: str


@router.post("/login")
async def login_user(request: LoginRequest, response: Response):
    try:
        user_id = "default_user"
        role = "student"

        session_id = await create_session(user_id, role)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,  # Set to False for local development without HTTPS
        )
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


# You'll need to include this router in your main app
