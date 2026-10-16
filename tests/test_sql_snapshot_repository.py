from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.db_snapshot import SnapshotDB
from app.models.snapshot import SnapshotDraft
from app.repository.sql_snapshot_repository import SQLSnapshotRepository

def test_save_and_read_snapshot_from_postgres():
    repository = SQLSnapshotRepository()

    draft = SnapshotDraft(
        timestamp = datetime.now(timezone.utc),
        cpu_percent=23.5,
        memory_percent=61.2,
        disk_percent=45.0,
        process_count=120,
        status="SUCCESS",
        severity="HEALTHY",
        collection_time_ms=12.5,
        )

    saved = repository.save_snapshot(draft)

    try:
        assert saved.cycle_id is not None
        assert saved.cpu_percent == 23.5
        assert repository.get_latest_snapshot().cycle_id == saved.cycle_id

        recent = repository.get_recent_snapshots(limit=10)
        assert any(item.cycle_id == saved.cycle_id for item in recent)
    finally:
        # Remove this test's row so repeated runs dont accumulate test data
        with SessionLocal() as session:
            session.query(SnapshotDB).filter_by(
                cycle_id=saved.cycle_id
                ).delete()
            session.commit()
