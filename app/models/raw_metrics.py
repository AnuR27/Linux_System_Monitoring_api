from pydantic import BaseModel, Field
from datetime import datetime

class RawMetrics(BaseModel):
    timestamp: datetime

    cpu_percent: float | None = None
    memory_percent: float | None = None
    disk_percent: float | None = None
    process_count: int | None = None

    collection_time_ms: float | None = None
    collection_errors: list[str] = Field(default_factory=list)
