from fastapi import APIRouter
from typing import Dict, Any
from faker import Faker
import json

router = APIRouter(prefix="/test_integration")

@router.get("/mock_profile", response_model=Dict[str, Any])
async def get_mock_profile():
    fake = Faker()
    return {
        "success": True,
        "data": {
            "user_id": fake.uuid4(),
            "username": fake.user_name(),
            "email": fake.email(),
            "full_name": fake.name(),
            # ... add other profile fields with fake data ...
        },
        "message": ""
    }

@router.get("/error_500", response_model=Dict[str, Any])
async def simulate_server_error():
    return {
        "success": False,
        "data": {},
        "error": {"code": 500, "message": "Simulated server error"},
        "message": "Error!"
    }

# Example of a test endpoint that might interact with a specific service:
# @router.post("/create_mock_task", response_model=Dict[str, Any])
# async def create_mock_task():
#     # ... (if you have a task creation service) ...
#     from app.services.tasks import create_task  # Adjust import
#     task_data = generate_mock_task()
#     #  You might need to adapt this depending on your service's API:
#     # new_task = await create_task(**task_data, user_id="test_user_id")
#     return {"success": True, "data": task_data, "message": "Mock task created"}

def generate_mock_task():
    fake = Faker()
    return {
        "task_id": fake.uuid4(),
        "title": fake.sentence(),
        "description": fake.paragraph(),
        # ... add other task fields ...
    }
