from datetime import datetime, timezone

from app.models.raw_metrics import RawMetrics
from app.models.snapshot import SnapshotDraft
from app.services.monitoring_service import MonitoringService

class FakeCollector:
    def collect(self):
        return RawMetrics(
            timestamp = datetime.now(timezone.utc),
            cpu_percent = 85.0,
            memory_percent=60.0,
            disk_percent=45.0,
            process_count=4,
            collection_time_ms=10.0,
            collection_errors=[],
            )

class FakeMetricsService:
    def process(self, raw_metrics):
        draft = SnapshotDraft(
            timestamp=raw_metrics.timestamp,
            cpu_percent=raw_metrics.cpu_percent,
            memory_percent=raw_metrics.memory_percent,
            disk_percent=raw_metrics.disk_percent,
            process_count=raw_metrics.process_count,
            status="SUCCESS",
            severity="WARNING",
            collection_time_ms=raw_metrics.collection_time_ms,
        )
        return draft, []

class FakeSnapshotRepository:
    def __init__(self):
        self.saved_drafts = []

    def save_snapshot(self, draft):
        self.saved_drafts.append(draft)
        from app.models.snapshot import Snapshot

        return Snapshot(
            cycle_id = len(self.saved_drafts),
            **draft.model_dump(),
            )

def test_run_cycle_collects_processes_and_saves_snapshot():
    collector = FakeCollector()
    metrics_service = FakeMetricsService()
    repository = FakeSnapshotRepository()

    monitoring_service = MonitoringService(
        collector=collector,
        metrics_service=metrics_service,
        snapshot_repository=repository,
        )

    snapshot, errors = monitoring_service.run_cycle()

    assert snapshot.cycle_id == 1
    assert snapshot.cpu_percent == 85.0
    assert snapshot.severity == "WARNING"
    assert errors == []
    assert len(repository.saved_drafts) == 1

