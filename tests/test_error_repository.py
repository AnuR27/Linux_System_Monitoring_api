from datetime import datetime, timezone

from app.repository.error_repository import ErrorRepository


def test_save_error_returns_and_stores_error():
    repository = ErrorRepository()
    timestamp = datetime.now(timezone.utc)

    error = repository.save_error(
        cycle_id=1,
        timestamp=timestamp,
        error_code="CPU_METRIC_MISSING",
        message="CPU metric could not be collected",
    )

    assert error.error_id == 1
    assert error.cycle_id == 1
    assert error.timestamp == timestamp
    assert error.error_code == "CPU_METRIC_MISSING"
    assert error.message == "CPU metric could not be collected"
    assert repository.errors_by_id[1] == error


def test_error_ids_increment():
    repository = ErrorRepository()
    timestamp = datetime.now(timezone.utc)

    first = repository.save_error(
        cycle_id=1,
        timestamp=timestamp,
        error_code="CPU_METRIC_MISSING",
        message="CPU unavailable",
    )
    second = repository.save_error(
        cycle_id=2,
        timestamp=timestamp,
        error_code="MEMORY_METRIC_MISSING",
        message="Memory unavailable",
    )

    assert first.error_id == 1
    assert second.error_id == 2


def test_recent_errors_returns_newest_first_and_respects_limit():
    repository = ErrorRepository()
    timestamp = datetime.now(timezone.utc)

    for cycle_id in range(1, 4):
        repository.save_error(
            cycle_id=cycle_id,
            timestamp=timestamp,
            error_code="TEST_ERROR",
            message=f"Error from cycle {cycle_id}",
        )

    recent = repository.get_recent_errors(limit=2)

    assert len(recent) == 2
    assert [error.cycle_id for error in recent] == [3, 2]
