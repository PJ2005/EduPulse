from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Break(BaseModel):
    start_time: datetime
    end_time: datetime
    # Add other relevant fields as needed, e.g.:
    # activity: Optional[str] = None
    # location: Optional[str] = None
    # notes: Optional[str] = None