from pydantic import BaseModel
from datetime import datetime


class Snapshot(BaseModel):
    cycle_id: int
    timestamp: datetime

    cpu_percent: float | None = None
    memory_percent: float | None = None
    disk_percent: float | None = None
    process_count: int | None = None

    status: str
    severity: str

    collection_time_ms: float | None = None
