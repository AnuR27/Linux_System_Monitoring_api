from fastapi.testclient import TestClient
from app.main import app

def test_root_endpoint_and_application_lifecycle():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "System Monitoring API is running"
            }

        assert app.state.scheduler is not None
