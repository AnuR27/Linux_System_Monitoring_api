from app.collector.system_collector import SystemCollector
from app.services.metrics_service import MetricsService
from app.repository.snapshot_repository import SnapshotRepository

class MonitoringService:
    def __init__(
        self,
        collector: SystemCollector,
        metrics_service: MetricsService,
        snapshot_repository: SnapshotRepository,
        ):
        self.collector = collector
        self.metrics_service = metrics_service
        self.snapshot_repository = snapshot_repository

    def run_cycle(self):
        # 1.  collect raw system metrics
        raw_metrics = self.collector.collect()

        #2. process metrics into a snapshot draft and errors
        snapshot_draft, errors = self.metrics_service.process(raw_metrics)

        # 3. save the snapshot and receive the saved snapshot
        saved_snapshot = self.snapshot_repository.save_snapshot(
            snapshot_draft
            )

        # 4. Return the results of this cycle
        return saved_snapshot, errors
