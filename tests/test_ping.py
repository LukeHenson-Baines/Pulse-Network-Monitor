from unittest.mock import patch

from app.services.ping import measure_ping


@patch("app.services.ping.ping")
def test_measure_ping_reachable(mock_ping):
    mock_ping.side_effect = [0.01, 0.02, 0.015, 0.025]

    result = measure_ping("example.com")

    assert result["status"] == "reachable"
    assert result["packets_sent"] == 4
    assert result["packets_received"] == 4
    assert result["packet_loss_percent"] == 0.0
    assert result["min_latency_ms"] == 10.0
    assert result["max_latency_ms"] == 25.0
    assert result["avg_latency_ms"] == 17.5


@patch("app.services.ping.ping")
def test_measure_ping_unreachable(mock_ping):
    mock_ping.return_value = None

    result = measure_ping("example.com")

    assert result["status"] == "unreachable"
    assert result["packets_received"] == 0
    assert result["packet_loss_percent"] == 100.0
    assert result["avg_latency_ms"] is None


@patch("app.services.ping.ping")
def test_measure_ping_partial_packet_loss(mock_ping):
    mock_ping.side_effect = [0.01, None, 0.02, None]

    result = measure_ping("example.com")

    assert result["status"] == "reachable"
    assert result["packets_received"] == 2
    assert result["packet_loss_percent"] == 50.0
    assert result["avg_latency_ms"] == 15.0