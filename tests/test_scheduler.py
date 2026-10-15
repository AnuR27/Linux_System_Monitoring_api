from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from app.scheduler.scheduler import MonitoringScheduler

def test_scheduler_rejects_non_positive_interval():
    with pytest.raises(ValueError):
        MonitoringScheduler(
            monitoring_service = Mock(),
            interval_seconds = 0,
            )

def test_scheduler_continues_after_cycle_failure(monkeypatch):
    monitoring_service = Mock()
    monitoring_service.run_cycle.side_effect = [
        RuntimeError("temporary failure"),
        (
            SimpleNamespace(
                cycle_id=2,
                status="SUCCESS",
                severity="HEALTHY",
                ),
            [],
            ),
        ]
    scheduler = MonitoringScheduler(
        monitoring_service = monitoring_service,
        interval_seconds = 30,
        )

    wait_calls = []

    def fake_wait(seconds):
        wait_calls.append(seconds)
        if len(wait_calls) == 2:
            scheduler.stop_event.set()
        return scheduler.stop_event.is_set()

    monkeypatch.setattr(
        scheduler.stop_event, "wait",
        fake_wait,
        )

    scheduler.run_forever()

    assert monitoring_service.run_cycle.call_count == 2
    assert wait_calls == [30,30]


def test_stop_prevents_next_cycle():
    monitoring_service = Mock()

    scheduler = MonitoringScheduler(
        monitoring_service=monitoring_service,
        interval_seconds=30,
        )
    scheduler.stop()
    scheduler.run_forever()

    monitoring_service.run_cycle.assert_not_called()
