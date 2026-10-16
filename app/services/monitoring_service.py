from app.collector.system_collector import SystemCollector
from app.services.metrics_service import MetricsService
from app.repository.snapshot_repository import SnapshotRepository
from app.repository.error_repository import ErrorRepository
from app.models.raw_metrics import RawMetrics

class MonitoringService:
    def __init__(
        self,
        collector: SystemCollector,
        metrics_service: MetricsService,
        snapshot_repository: SnapshotRepository,
        error_repository: ErrorRepository,
        ):
        self.collector = collector
        self.metrics_service = metrics_service
        self.snapshot_repository = snapshot_repository
        self.error_repository = error_repository

    def run_cycle(self):
        # 1.  collect raw system metrics
        raw_metrics = self.collector.collect()

        #2. process metrics into a snapshot draft and errors
        snapshot_draft, errors = self.metrics_service.process(raw_metrics)

        # 3. save the snapshot and receive the saved snapshot
        saved_snapshot = self.snapshot_repository.save_snapshot(
            snapshot_draft
            )

        for error in errors:
            error_code, _, message = error.partition(": ")

            self.error_repository.save_error(
                cycle_id = saved_snapshot.cycle_id,
                timestamp = raw_metrics.timestamp,
                error_code = error_code,
                message = message or error,
                )

        # 4. Return the results of this cycle
        return saved_snapshot, errors
