from datetime import datetime, timezone
import time

import psutil

from app.models.raw_metrics import RawMetrics

class SystemCollector:
    def collect(self) -> RawMetrics:
        start_time = time.perf_counter()
        timestamp = datetime.now(timezone.utc)

        cpu_percent = None
        memory_percent = None
        disk_percent = None
        process_count = None
        errors = []

        #collect CPU
        try:
            cpu_percent = psutil.cpu_percent(interval = 0.1)
        except Exception as exc:
            errors.append(f"CPU_COLLECTION_FAILED: {exc}")

        #collect memory
        try:
            memory_percent = psutil.virtual_memory().percent
        except Exception as exc:
            errors.append(f"MEMORY_COLLECTION_FAILED: {exc}")

        # collect disk usage
        try:
            disk_percent = psutil.disk_usage("/").percent
        except Exception as exc:
            errors.append(f"DISK_COLLECTION_FAILED: {exc}")

        #collect process count
        try:
            process_count = len(psutil.pids())
        except Exception as exc:
            errors.append(f"PROCESS_COUNT_COLLECTION_FAILED: {exc}")

        collection_time_ms = (time.perf_counter() - start_time) * 1000

        return RawMetrics(
            timestamp=timestamp,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            process_count=process_count,
            collection_time_ms=collection_time_ms,
            collection_errors=errors,)
