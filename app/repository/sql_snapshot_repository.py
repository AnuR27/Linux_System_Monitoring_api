from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.core.database import SessionLocal
from app.models.db_snapshot import SnapshotDB
from app.models.snapshot import Snapshot, SnapshotDraft

class SQLSnapshotRepository:
    def __init__(self, session_factory: sessionmaker = SessionLocal):
        self.session_factory = session_factory

    def save_snapshot(self, snapshot: SnapshotDraft) -> Snapshot:
        with self.session_factory() as session:
            db_snapshot = SnapshotDB(**snapshot.model_dump())
            session.add(db_snapshot)
            session.commit()
            session.refresh(db_snapshot)

            return Snapshot(
                cycle_id = db_snapshot.cycle_id,
                timestamp = db_snapshot.timestamp,
                cpu_percent= db_snapshot.cpu_percent,
                memory_percent = db_snapshot.memory_percent,
                disk_percent = db_snapshot.disk_percent,
                process_count = db_snapshot.process_count,
                status = db_snapshot.status,
                severity = db_snapshot.severity,
                collection_time_ms = db_snapshot.collection_time_ms,
                )
    def get_latest_snapshot(self) -> Snapshot | None:
        with self.session_factory() as session:
            statement = (
                select(SnapshotDB).order_by(SnapshotDB.cycle_id.desc()).limit(1))
            db_snapshot = session.scalars(statement).first()

            if db_snapshot is None:
                return None

            return self._to_snapshot(db_snapshot)

    def get_recent_snapshots(self, limit: int= 10) -> list[Snapshot]:
        with self.session_factory() as session:
            statement = (select(SnapshotDB).order_by(SnapshotDB.cycle_id.desc()).limit(limit))
            rows = session.scalars(statement).all()
            return [self._to_snapshot(row) for row in rows]

    @staticmethod
    def _to_snapshot(row: SnapshotDB) -> Snapshot:
        return Snapshot(
            cycle_id = row.cycle_id,
            timestamp = row.timestamp,
            cpu_percent = row.cpu_percent,
            memory_percent = row.memory_percent,
            disk_percent = row.disk_percent,
            process_count = row.process_count,
            status = row.status,
            severity = row.severity,
            collection_time_ms = row.collection_time_ms,
            )
