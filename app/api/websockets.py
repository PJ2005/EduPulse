from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.websockets.websocket_manager import WebSocketManager  # Import the manager (adjust path if needed)
from app.core.middleware import get_current_user  # Add this import
import json

router = APIRouter()

# Initialize the manager (ideally, this should be done in a central location, like your app startup)
websocket_manager = WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user = Depends(get_current_user)):
    user_id = user["user_id"]
    await websocket_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                event = message.get("event")
                #  Handle different event types from the client, e.g.:
                #  if event == "ping":
                #      await websocket_manager.send_personal_message(json.dumps({"event": "pong"}), websocket)
                #  else:
                #      print(f"Unknown event: {event}")
                await websocket_manager.send_personal_message(f"You wrote: {data}", websocket)  # Echo for now
            except json.JSONDecodeError:
                print("Invalid JSON received")
                await websocket_manager.send_personal_message("Invalid message format", websocket)
            except Exception as e:
                print(f"Error handling message: {e}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user_id)
        print(f"User {user_id} disconnected")
