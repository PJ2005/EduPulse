from typing import List, Dict, Optional
from datetime import timedelta, datetime
import time
# This service handles break scheduling and reminders.
# It could integrate with a notification system for reminders.

# Pomodoro settings (configurable)
POMODORO_WORK_DURATION = timedelta(minutes=25)
SHORT_BREAK_DURATION = timedelta(minutes=5)
LONG_BREAK_DURATION = timedelta(minutes=15)

#  In-memory storage for active breaks (replace with database)
active_breaks: Dict[str, Dict] = {}


async def start_pomodoro(user_id: str) -> Dict:
    # Starts a Pomodoro timer
    if user_id in active_breaks:
        raise ValueError("Pomodoro already active")
    
    start_time = datetime.now()
    active_breaks[user_id] = {
        "start_time": start_time,
        "work_end_time": start_time + POMODORO_WORK_DURATION,
        "type": "work",
    }
    return {"message": "Pomodoro started", "work_duration": POMODORO_WORK_DURATION.total_seconds(), "end_time": active_breaks[user_id]["work_end_time"].isoformat()}

async def check_break_status(user_id: str) -> Dict:
    # Checks the status of the current break (if any)
    break_data = active_breaks.get(user_id)
    if not break_data:
        return {"status": "idle"}

    now = datetime.now()
    if break_data["type"] == "work":
        if now >= break_data["work_end_time"]:
            # Time for a break
            break_data["type"] = "short_break"
            break_data["break_end_time"] = now + SHORT_BREAK_DURATION
            return {"status": "short_break", "duration": SHORT_BREAK_DURATION.total_seconds(), "end_time": break_data["break_end_time"].isoformat()}
        else:
            remaining_time = (break_data["work_end_time"] - now).total_seconds()
            return {"status": "work", "remaining": remaining_time}
    elif break_data["type"] == "short_break":
        if now >= break_data["break_end_time"]:
            # Break over
            del active_breaks[user_id]
            return {"status": "break_over"}
        else:
            remaining_time = (break_data["break_end_time"] - now).total_seconds()
            return {"status": "short_break", "remaining": remaining_time}

    return {"status": "unknown"} # Should not reach here

async def stop_pomodoro(user_id: str) -> Dict:
    # Stops the current Pomodoro or break
    if user_id not in active_breaks:
        raise ValueError("No active Pomodoro")
    del active_breaks[user_id]
    return {"message": "Pomodoro stopped"}


# TODO: Implement break scheduling algorithms and break compliance tracking
#  Break scheduling could consider:
#   - Task duration and complexity.
#   - User's historical work patterns (if available).
#   - Time of day.
#  Break compliance tracking could monitor:
#   - Whether the user takes breaks as scheduled.
#   - The duration of breaks.
#   - Provide feedback or adjust schedules accordingly.