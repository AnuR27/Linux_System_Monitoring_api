from datetime import datetime, timezone

from app.models.raw_metrics import RawMetrics
from app.models.snapshot import SnapshotDraft
from app.services.monitoring_service import MonitoringService
from app.repository.error_repository import ErrorRepository

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


class FailingFakeCollector:
    def collect(self):
        return RawMetrics(
            timestamp=datetime.now(timezone.utc),
            cpu_percent=None,
            memory_percent=60.0,
            disk_percent=45.0,
            process_count=4,
            collection_time_ms=10.0,
            collection_errors=[
                "CPU_COLLECTION_FAILED: test failure"
            ],
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

class FailingFakeMetricsService(FakeMetricsService):
    def process(self, raw_metrics):
        draft, _ = super().process(raw_metrics)
        return draft, list(raw_metrics.collection_errors) + [
            "CPU_METRIC_MISSING"
        ]

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
    error_repository = ErrorRepository()

    monitoring_service = MonitoringService(
        collector=collector,
        metrics_service=metrics_service,
        snapshot_repository=repository,
        error_repository=error_repository
        )

    snapshot, errors = monitoring_service.run_cycle()

    assert snapshot.cycle_id == 1
    assert snapshot.cpu_percent == 85.0
    assert snapshot.severity == "WARNING"
    assert errors == []
    assert len(repository.saved_drafts) == 1


def test_run_cycle_persists_collection_errors():
    collector = FailingFakeCollector()
    metrics_service = FailingFakeMetricsService()
    snapshot_repository = FakeSnapshotRepository()
    error_repository = ErrorRepository()

    monitoring_service = MonitoringService(
        collector = collector,
        metrics_service = metrics_service,
        snapshot_repository = snapshot_repository,
        error_repository = error_repository,
        )
    snapshot, errors = monitoring_service.run_cycle()

    saved_errors = error_repository.get_recent_errors()

    assert len(saved_errors) == 2
    assert all(error.cycle_id == snapshot.cycle_id for error in saved_errors)
    assert saved_errors[0].error_code == "CPU_METRIC_MISSING"
