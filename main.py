from fastapi import FastAPI
import logging
from app.core.middleware import authenticate_user
from app.core.config import settings
from app.api import auth, user, websockets, test_integration
from app.api import questions, tests, analytics, adaptive_learning
from app.api import content, notes
from app.api import calendar, tasks, breaks, ai_planning, study_planner
from app.api import home
from app.websockets.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="EduPulse API",
    description="API for the EduPulse educational platform",
    version="1.0.0",
)

# Add authentication middleware
app.middleware("http")(authenticate_user)

# Initialize websocket manager
websocket_manager = WebSocketManager()

# Include all routers
# Core API endpoints
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(websockets.router)

# Test Dashboard API endpoints
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(tests.router, prefix="/api/tests", tags=["tests"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(adaptive_learning.router, prefix="/api/adaptive", tags=["adaptive learning"])
app.include_router(test_integration.router)

# Content Management API endpoints
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])

# Scheduler Dashboard API endpoints
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(breaks.router, prefix="/api/breaks", tags=["breaks"])
app.include_router(ai_planning.router, prefix="/api/ai_planning", tags=["ai planning"])
app.include_router(study_planner.router, prefix="/api/study_planner", tags=["study planner"])

# Home Page API endpoints
app.include_router(home.router, prefix="/api/home", tags=["home"])

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to EduPulse API!"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up EduPulse application...")
    # Add startup logic here (e.g., database connections)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down EduPulse application...")
    # Add cleanup logic here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)