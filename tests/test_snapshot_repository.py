from app.models.snapshot import SnapshotDraft
from app.repository.snapshot_repository import SnapshotRepository


def make_snapshot() -> SnapshotDraft:
    return SnapshotDraft(
        timestamp="2026-10-13T10:00:00",
        cpu_percent=25.0,
        memory_percent=50.0,
        disk_percent=60.0,
        process_count=100,
        status="SUCCESS",
        severity="LOW",
        collection_time_ms=12.5,
    )


def test_latest_snapshot_is_none_when_repository_is_empty():
    repository = SnapshotRepository()

    assert repository.get_latest_snapshot() is None


def test_latest_snapshot_returns_most_recent_saved_snapshot():
    repository = SnapshotRepository()

    first = repository.save_snapshot(make_snapshot())
    second = repository.save_snapshot(make_snapshot())

    latest = repository.get_latest_snapshot()

    assert latest is second
    assert latest.cycle_id == 2
    assert first.cycle_id == 1

def test_saving_snapshot_assigns_id_without_modifying_draft():
    repository = SnapshotRepository()
    draft = make_snapshot()

    saved = repository.save_snapshot(draft)

    assert saved.cycle_id == 1
    assert not hasattr(draft, "cycle_id")
    assert saved is not draft

def test_get_recent_snapshots_returns_newest_first():
    repository = SnapshotRepository()

    first = repository.save_snapshot(make_snapshot())
    second = repository.save_snapshot(make_snapshot())
    third = repository.save_snapshot(make_snapshot())

    recent = repository.get_recent_snapshots(limit=2)

    assert recent == [third, second]
    assert first not in recent

def test_get_recent_snapshots_returns_empty_list_when_repository_is_empty():
    repository = SnapshotRepository()

    assert repository.get_recent_snapshots() == []
