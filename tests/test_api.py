from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "Pulse" in response.text


def test_docs_load():
    response = client.get("/docs")

    assert response.status_code == 200