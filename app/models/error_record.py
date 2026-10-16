from datetime import datetime

from pydantic import BaseModel

class ErrorRecord(BaseModel):
    error_id : int
    cycle_id : int
    timestamp : datetime
    error_code : str
    message: str
