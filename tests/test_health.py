from unittest.mock import patch

from app.services.health import get_network_health


@patch("app.services.health.measure_ping")
def test_health_healthy(mock_ping):
    mock_ping.return_value = {
        "host": "8.8.8.8",
        "status": "reachable",
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss_percent": 0.0,
        "min_latency_ms": 10.0,
        "max_latency_ms": 20.0,
        "avg_latency_ms": 15.0,
    }

    result = get_network_health()

    assert result["status"] == "healthy"


@patch("app.services.health.measure_ping")
def test_health_degraded_due_to_latency(mock_ping):
    mock_ping.return_value = {
        "host": "8.8.8.8",
        "status": "reachable",
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss_percent": 0.0,
        "min_latency_ms": 140.0,
        "max_latency_ms": 190.0,
        "avg_latency_ms": 160.0,
    }

    result = get_network_health()

    assert result["status"] == "degraded"


@patch("app.services.health.measure_ping")
def test_health_degraded_due_to_packet_loss(mock_ping):
    mock_ping.return_value = {
        "host": "8.8.8.8",
        "status": "reachable",
        "packets_sent": 4,
        "packets_received": 3,
        "packet_loss_percent": 25.0,
        "min_latency_ms": 10.0,
        "max_latency_ms": 20.0,
        "avg_latency_ms": 15.0,
    }

    result = get_network_health()

    assert result["status"] == "degraded"


@patch("app.services.health.measure_ping")
def test_health_offline(mock_ping):
    mock_ping.return_value = {
        "host": "8.8.8.8",
        "status": "unreachable",
        "packets_sent": 4,
        "packets_received": 0,
        "packet_loss_percent": 100.0,
        "min_latency_ms": None,
        "max_latency_ms": None,
        "avg_latency_ms": None,
    }

    result = get_network_health()

    assert result["status"] == "offline"