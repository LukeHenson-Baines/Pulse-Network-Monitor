from types import SimpleNamespace
from unittest.mock import patch

from app.services.bandwidth import get_bandwidth_usage


@patch("app.services.bandwidth.time.sleep")
@patch("app.services.bandwidth.psutil.net_io_counters")
def test_get_bandwidth_usage(mock_counters, mock_sleep):
    start = SimpleNamespace(
        bytes_sent=1_000_000,
        bytes_recv=2_000_000,
        packets_sent=100,
        packets_recv=200,
        errin=0,
        errout=0,
        dropin=0,
        dropout=0,
    )

    end = SimpleNamespace(
        bytes_sent=2_000_000,
        bytes_recv=5_000_000,
        packets_sent=150,
        packets_recv=350,
        errin=1,
        errout=2,
        dropin=3,
        dropout=4,
    )

    mock_counters.side_effect = [start, end]

    result = get_bandwidth_usage(interval=2.0)

    mock_sleep.assert_called_once_with(2.0)

    assert result["total_bytes_sent"] == 2_000_000
    assert result["total_bytes_received"] == 5_000_000

    # 1,000,000 bytes over 2 sec = 500,000 bytes/sec = 4 Mbps
    assert result["upload_rate_mbps"] == 4.0

    # 3,000,000 bytes over 2 sec = 1,500,000 bytes/sec = 12 Mbps
    assert result["download_rate_mbps"] == 12.0

    assert result["packets_sent"] == 150
    assert result["packets_received"] == 350
    assert result["errors_in"] == 1
    assert result["errors_out"] == 2
    assert result["dropped_in"] == 3
    assert result["dropped_out"] == 4