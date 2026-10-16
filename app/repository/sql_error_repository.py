from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.core.database import SessionLocal
from app.models.db_error import ErrorDB
from app.models.error_record import ErrorRecord


class SQLErrorRepository:
    def __init__(self, session_factory: sessionmaker = SessionLocal):
        self.session_factory = session_factory

    def save_error(
        self,
        cycle_id: int,
        timestamp: datetime,
        error_code: str,
        message: str,
        ) -> ErrorRecord:
        with self.session_factory() as session:
            db_error = ErrorDB(
                cycle_id = cycle_id,
                timestamp=timestamp,
                error_code=error_code,
                message=message,
                )
            session.add(db_error)
            session.commit()
            session.refresh(db_error)

            return self._to_error_record(db_error)

    def get_recent_errors(self, limit: int=10) -> list[ErrorRecord]:
        with self.session_factory() as session:
            statement = (
                select(ErrorDB).order_by(ErrorDB.error_id.desc()).limit(limit)
                )
            rows = session.scalars(statement).all()
            return [self._to_error_record(row) for row in rows]

    @staticmethod
    def _to_error_record(row: ErrorDB) -> ErrorRecord:
        return ErrorRecord(
            error_id=row.error_id,
            cycle_id=row.cycle_id,
            timestamp=row.timestamp,
            error_code=row.error_code,
            message=row.message,
            )
