
from types import SimpleNamespace

from app.collector.system_collector import SystemCollector


def test_collect_returns_all_metrics(monkeypatch):
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.cpu_percent",
        lambda interval: 25.0,
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.virtual_memory",
        lambda: SimpleNamespace(percent=60.0),
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.disk_usage",
        lambda path: SimpleNamespace(percent=45.0),
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.pids",
        lambda: [1, 2, 3, 4],
    )

    collector = SystemCollector()
    result = collector.collect()

    assert result.cpu_percent == 25.0
    assert result.memory_percent == 60.0
    assert result.disk_percent == 45.0
    assert result.process_count == 4
    assert result.collection_errors == []
    assert result.collection_time_ms >= 0
    assert result.timestamp.tzinfo is not None

def test_cpu_failure_does_not_stop_other_metrics(monkeypatch):
    def fail_cpu(interval):
        raise OSError("CPU unavailable")

    monkeypatch.setattr(
        "app.collector.system_collector.psutil.cpu_percent",
        fail_cpu,
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.virtual_memory",
        lambda: SimpleNamespace(percent=60.0),
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.disk_usage",
        lambda path: SimpleNamespace(percent=45.0),
    )
    monkeypatch.setattr(
        "app.collector.system_collector.psutil.pids",
        lambda: [1, 2, 3],
    )

    collector = SystemCollector()
    result = collector.collect()

    assert result.cpu_percent is None
    assert result.memory_percent == 60.0
    assert result.disk_percent == 45.0
    assert result.process_count == 3
    assert len(result.collection_errors) == 1
    assert result.collection_errors[0].startswith(
        "CPU_COLLECTION_FAILED:"
    )
