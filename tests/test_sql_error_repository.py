from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.db_error import ErrorDB
from app.models.db_snapshot import SnapshotDB
from app.models.snapshot import SnapshotDraft
from app.repository.sql_error_repository import SQLErrorRepository
from app.repository.sql_snapshot_repository import SQLSnapshotRepository

def test_save_and_read_error_from_postgres():
    snapshot_repository = SQLSnapshotRepository()
    error_repository = SQLErrorRepository()

    draft = SnapshotDraft(
        timestamp = datetime.now(timezone.utc),
        status = "PARTIAL",
        severity="WARNING",
        )

    snapshot = snapshot_repository.save_snapshot(draft)

    try:
        saved_error = error_repository.save_error(
            cycle_id = snapshot.cycle_id,
            timestamp = datetime.now(timezone.utc),
            error_code = "TEST_ERROR",
            message = "Test error for repository integration",
            )

        assert saved_error.error_id is not None
        assert saved_error.cycle_id == snapshot.cycle_id
        assert saved_error.error_code == "TEST_ERROR"

        recent = error_repository.get_recent_errors(limit=10)
        assert any(item.error_id == saved_error.error_id for item in recent)

    finally:
        with SessionLocal() as session:
            session.query(ErrorDB).filter_by(
                cycle_id = snapshot.cycle_id
                ).delete()
            session.query(SnapshotDB).filter_by(
                cycle_id=snapshot.cycle_id
                ).delete()
            session.commit()
