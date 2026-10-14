from datetime import datetime

from app.models.raw_metrics import RawMetrics
from app.services.metrics_service import MetricsService

def make_raw_metrics(**overrides) -> RawMetrics:
    data = {
        "timestamp": datetime(2026,10,14,10,0,0),
        "cpu_percent": 25.0,
        "memory_percent": 50.0,
        "disk_percent": 60.0,
        "process_count": 100,
        "collection_time_ms": 12.5,
        "collection_errors": [],
        }
    data.update(overrides)
    return RawMetrics(**data)

def test_all_metrics_present_without_errors_is_success():
    service = MetricsService()
    status = service.compute_status(make_raw_metrics())
    assert status == "SUCCESS"

def test_missing_metric_results_in_partial_status():
    service = MetricsService()
    raw = make_raw_metrics(cpu_percent=None)
    status = service.compute_status(raw)
    assert status == "PARTIAL"

def test_All_metrics_missing_results_in_failed_status():
    service = MetricsService()
    raw = make_raw_metrics(
        cpu_percent = None,
        memory_percent = None,
        disk_percent = None,
        process_count = None,
        )
    status = service.compute_status(raw)
    assert status == "FAILED"

def test_collection_error_results_in_partial_status():
    service = MetricsService()
    raw = make_raw_metrics(collection_errors=["CPU_COLLECTION_TIMEOUT"])
    status = service.compute_status(raw)
    assert status == "PARTIAL"

def test_low_cpu_and_memory_are_healthy():
    service = MetricsService()
    raw = make_raw_metrics(cpu_percent=30, memory_percent=50)
    assert service.compute_severity(raw) == "HEALTHY"

def test_cpu_at_80_percent_is_warning():
    service = MetricsService()
    raw = make_raw_metrics(cpu_percent=80, memory_percent=50)
    assert service.compute_severity(raw) == "WARNING"

def test_memory_at_95_percent_is_critical():
    service = MetricsService()
    raw = make_raw_metrics(cpu_percent=30, memory_percent=95)

    assert service.compute_severity(raw) == "CRITICAL"


def test_missing_cpu_means_health_is_unknown():
    service = MetricsService()
    raw = make_raw_metrics(cpu_percent=None, memory_percent=50)

    assert service.compute_severity(raw) == "UNKNOWN"


def test_health_is_independent_of_collection_errors():
    service = MetricsService()
    raw = make_raw_metrics(
        cpu_percent=98,
        memory_percent=50,
        collection_errors=["DISK_COLLECTION_FAILED"],
    )














