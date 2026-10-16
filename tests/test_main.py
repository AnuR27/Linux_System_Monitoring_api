from fastapi.testclient import TestClient
from app.main import app

from app.repository.snapshot_repository import SnapshotRepository
from app.repository.error_repository import ErrorRepository


from datetime import datetime, timezone
from app.models.snapshot import SnapshotDraft

def create_test_repositories():
    return SnapshotRepository(), ErrorRepository()

app.state.repository_factory = create_test_repositories

def test_root_endpoint_and_application_lifecycle():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "System Monitoring API is running"
            }

        assert app.state.scheduler is not None

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "status" : "ok",
            "service": "system-monitoring-api",
            }


def test_latest_metrics_endpoint():
    with TestClient(app) as client:
        repository = app.state.snapshot_repository

        repository.save_snapshot(
            SnapshotDraft(
                timestamp=datetime.now(timezone.utc),
                cpu_percent=25.0,
                memory_percent=50.0,
                disk_percent=60.0,
                process_count=100,
                status="SUCCESS",
                severity="HEALTHY",
                collection_time_ms=12.5,
            )
        )

        response = client.get("/metrics/latest")

        assert response.status_code == 200

        data = response.json()
        assert data["cycle_id"] >= 1
        assert data["cpu_percent"] == 25.0
        assert data["memory_percent"] == 50.0
        assert data["status"] == "SUCCESS"
        assert data["severity"] == "HEALTHY"


def test_latest_metrics_returns_404_when_no_snapshot_exists():
    with TestClient(app) as client:
        repository = app.state.snapshot_repository

        repository.snapshots_by_cycle.clear()
        repository.cycle_order.clear()

        response = client.get("/metrics/latest")

        assert response.status_code == 404
        assert response.json() == {
            "detail": "No metrics snapshot available"
            }

def test_metrics_history_endpoint():
    with TestClient(app) as client:
        repository = app.state.snapshot_repository
        repository.snapshots_by_cycle.clear()
        repository.cycle_order.clear()

        repository.save_snapshot(
            SnapshotDraft(
                timestamp=datetime.now(timezone.utc),
                cpu_percent=25.0,
                memory_percent=50.0,
                disk_percent=60.0,
                process_count=100,
                status="SUCCESS",
                severity="HEALTHY",
                collection_time_ms=12.5,
            )
        )
        response = client.get("/metrics/history?limit=5")

        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 1
        assert data[0]["cpu_percent"] == 25.0

def test_errors_endpoint_returns_saved_errors():
    with TestClient(app) as client:
        repository = app.state.error_repository
        repository.errors_by_id.clear()
        repository._next_error_id = 1

        repository.save_error(
            cycle_id = 1,
            timestamp = datetime.now(timezone.utc),
            error_code="CPU_COLLECTION_FAILED",
            message = "Test CPU failure",
            )

        response = client.get("/errors")

        assert response.status_code == 200
        data = response.json()
        assert any(
            error["error_code"] == "CPU_COLLECTION_FAILED"
            for error in data
            )

def test_errors_endpoint_rejects_invalid_limit():
    with TestClient(app) as client:
        response = client.get("/errors?limit=0")

        assert response.status_code == 422
