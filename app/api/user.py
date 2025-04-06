from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()

@router.get("/me")
async def get_current_user(request: Request):
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user


@router.put("/me")
async def update_profile(request: Request, profile_data):
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user_id = user["user_id"]  # Assuming user ID is in the session data
    # In a full implementation, this would call a service function to update the user's profile
    # await update_user_profile(user_id, profile_data)
    return {"message": "Profile updated successfully"}


@router.get("/me/preferences")
async def get_preferences(request: Request):
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user_id = user["user_id"]
    # In a full implementation, this would call a service function to get the user's preferences
    # preferences = await get_user_preferences(user_id)
    # return preferences
    return {"preferences": {}}  # Placeholder for preferences


@router.put("/me/preferences")
async def update_preferences(request: Request, preferences):
    user = request.scope.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user_id = user["user_id"]
    # In a full implementation, this would call a service function to update the user's preferences
    # await update_user_preferences(user_id, preferences)
    return {"message": "Preferences updated successfully"}