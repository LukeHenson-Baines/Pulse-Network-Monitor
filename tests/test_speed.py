from unittest.mock import MagicMock, patch

from app.services.speed import run_speed_test


@patch("app.services.speed.SpeedTest")
def test_speed_test_success(mock_speed_test_class):
    mock_speed_test = MagicMock()
    mock_speed_test_class.return_value = mock_speed_test

    server = MagicMock()
    server.name = "London Test Server"
    server.sponsor_name = "Test Sponsor"

    mock_speed_test.get_servers.return_value = ["server"]
    mock_speed_test.find_best_server.return_value = server
    mock_speed_test.ping.return_value = (15.123, 2.456)
    mock_speed_test.download.return_value = (120.987, 15_000_000)
    mock_speed_test.upload.return_value = (35.432, 4_000_000)

    result = run_speed_test()

    assert result == {
        "status": "success",
        "server": "London Test Server",
        "sponsor": "Test Sponsor",
        "ping_ms": 15.12,
        "jitter_ms": 2.46,
        "download_mbps": 120.99,
        "upload_mbps": 35.43,
        "bytes_downloaded": 15_000_000,
        "bytes_uploaded": 4_000_000,
    }

    mock_speed_test.get_servers.assert_called_once()
    mock_speed_test.find_best_server.assert_called_once_with(["server"])
    mock_speed_test.ping.assert_called_once_with(server)
    mock_speed_test.download.assert_called_once_with(server)
    mock_speed_test.upload.assert_called_once_with(server)


@patch("app.services.speed.SpeedTest")
def test_speed_test_error(mock_speed_test_class):
    mock_speed_test_class.side_effect = Exception("Speed test unavailable")

    result = run_speed_test()

    assert result == {
        "status": "error",
        "message": "Speed test unavailable",
    }