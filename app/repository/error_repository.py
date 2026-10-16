from app.models.error_record import ErrorRecord
from datetime import datetime

class ErrorRepository:
    def __init__(self):
        self.errors_by_id : dict[int, ErrorRecord] = {}
        self._next_error_id = 1

    def save_error (
        self,
        cycle_id: int,
        timestamp: datetime,
        error_code: str,
        message: str,
        ) -> ErrorRecord:
        error = ErrorRecord(
            error_id = self._next_error_id,
            cycle_id = cycle_id,
            timestamp = timestamp,
            error_code = error_code,
            message = message,
            )
        self.errors_by_id[error.error_id] = error
        self._next_error_id += 1

        return error

    def get_recent_errors(self, limit: int=10) -> list[ErrorRecord]:
        recent_errors = list(self.errors_by_id.values())
        recent_errors.reverse()
        return recent_errors[:limit]
