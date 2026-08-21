from unittest.mock import patch

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


@patch("app.main.measure_ping")
def test_ping_endpoint(mock_ping):
    mock_ping.return_value = {
        "host": "example.com",
        "status": "reachable",
        "avg_latency_ms": 20.0,
    }

    response = client.get("/ping?host=example.com")

    assert response.status_code == 200
    assert response.json()["host"] == "example.com"

    mock_ping.assert_called_once_with("example.com")


@patch("app.main.get_bandwidth_usage")
def test_bandwidth_endpoint(mock_bandwidth):
    mock_bandwidth.return_value = {
        "upload_rate_mbps": 1.2,
        "download_rate_mbps": 8.4,
    }

    response = client.get("/bandwidth")

    assert response.status_code == 200
    assert response.json()["download_rate_mbps"] == 8.4

    mock_bandwidth.assert_called_once()


@patch("app.main.run_speed_test")
def test_speed_endpoint(mock_speed):
    mock_speed.return_value = {
        "status": "success",
        "download_mbps": 100.0,
        "upload_mbps": 20.0,
    }

    response = client.get("/speed")

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    mock_speed.assert_called_once()


@patch("app.main.get_network_health")
def test_health_endpoint(mock_health):
    mock_health.return_value = {
        "status": "healthy",
        "host": "1.1.1.1",
    }

    response = client.get("/health?host=1.1.1.1")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    mock_health.assert_called_once_with("1.1.1.1")


@patch("app.main.get_bandwidth_usage")
@patch("app.main.get_network_health")
def test_metrics_endpoint(mock_health, mock_bandwidth):
    mock_health.return_value = {
        "status": "healthy",
    }

    mock_bandwidth.return_value = {
        "download_rate_mbps": 5.0,
        "upload_rate_mbps": 1.0,
    }

    response = client.get("/metrics?host=8.8.8.8")

    assert response.status_code == 200

    body = response.json()

    assert body["health"]["status"] == "healthy"
    assert body["bandwidth"]["download_rate_mbps"] == 5.0

    mock_health.assert_called_once_with("8.8.8.8")
    mock_bandwidth.assert_called_once()