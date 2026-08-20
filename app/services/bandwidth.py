import time
import psutil


def get_bandwidth_usage(interval: float = 1.0) -> dict:
    start = psutil.net_io_counters()

    time.sleep(interval)

    end = psutil.net_io_counters()

    bytes_sent_per_second = (end.bytes_sent - start.bytes_sent) / interval
    bytes_received_per_second = (end.bytes_recv - start.bytes_recv) / interval

    upload_mbps = (bytes_sent_per_second * 8) / 1_000_000
    download_mbps = (bytes_received_per_second * 8) / 1_000_000

    return {
        "total_bytes_sent": end.bytes_sent,
        "total_bytes_received": end.bytes_recv,
        "total_megabytes_sent": round(end.bytes_sent / (1024 ** 2), 2),
        "total_megabytes_received": round(end.bytes_recv / (1024 ** 2), 2),
        "upload_rate_mbps": round(upload_mbps, 2),
        "download_rate_mbps": round(download_mbps, 2),
        "packets_sent": end.packets_sent,
        "packets_received": end.packets_recv,
        "errors_in": end.errin,
        "errors_out": end.errout,
        "dropped_in": end.dropin,
        "dropped_out": end.dropout,
    }