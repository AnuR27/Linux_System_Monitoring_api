from app.models.raw_metrics import RawMetrics
from app.models.snapshot import SnapshotDraft

class MetricsService:
    def compute_status(self, raw: RawMetrics) -> str:
        metrics = [
            raw.cpu_percent,
            raw.memory_percent,
            raw.disk_percent,
            raw.process_count
            ]
        missing = sum(1 for m in metrics if m is None)
        if missing == 0 and not raw.collection_errors:
            return "SUCCESS"
        if missing == len(metrics):
            return "FAILED"
        return "PARTIAL"


    def compute_severity(self, raw: RawMetrics) -> str:
        # CPU and memory are required to assess host health.
        if raw.cpu_percent is None or raw.memory_percent is None:
            return "UNKNOWN"

        # Critical takes priority over warning.
        if raw.cpu_percent >= 95 or raw.memory_percent >= 95:
            return "CRITICAL"

        if raw.cpu_percent >= 80 or raw.memory_percent >= 80:
            return "WARNING"

        return "HEALTHY"


    def generate_errors(self, raw:RawMetrics) -> list[str]:
        errors = list(raw.collection_errors)
        if raw.cpu_percent is None:
            errors.append("CPU_METRIC_MISSING")
        if raw.memory_percent is None:
            errors.append("MEMORY_METRIC_MISSING")
        if raw.disk_percent is None:
            errors.append("DISK_METRIC_MISSING")
        if raw.process_count is None:
            errors.append("PROCESS_COUNT_MISSING")
        return errors


    def build_snapshot(self, raw: RawMetrics) -> SnapshotDraft:
        status = self.compute_status(raw)
        severity = self.compute_severity(raw)

        return SnapshotDraft(
            timestamp=raw.timestamp,
            cpu_percent=raw.cpu_percent,
            memory_percent=raw.memory_percent,
            disk_percent=raw.disk_percent,
            process_count=raw.process_count,
            status=status,
            severity=severity,
            collection_time_ms=raw.collection_time_ms,
        )

    def process(self, raw: RawMetrics) -> tuple[SnapshotDraft, list[str]]:
        snapshot = self.build_snapshot(raw)
        errors = self.generate_errors(raw)
        return snapshot, errors
