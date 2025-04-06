from typing import Dict

# Assuming you have a database client instance initialized elsewhere, e.g.:
# from app.db.firebase import db

async def create_user(user_id: str, profile_data: Dict) -> str:
    try:
        await db.collection("Users").document(user_id).set({"profile": profile_data})
        return user_id
    except Exception as e:
        raise Exception(f"Failed to create user: {e}")
