from internetspeedtest import SpeedTest


def run_speed_test() -> dict:
    try:
        speed_test = SpeedTest()

        servers = speed_test.get_servers()
        best_server = speed_test.find_best_server(servers)

        ping_ms, jitter_ms = speed_test.ping(best_server)
        download_mbps, bytes_downloaded = speed_test.download(best_server)
        upload_mbps, bytes_uploaded = speed_test.upload(best_server)

        return {
            "status": "success",
            "server": best_server.name,
            "sponsor": best_server.sponsor_name,
            "ping_ms": round(ping_ms, 2),
            "jitter_ms": round(jitter_ms, 2),
            "download_mbps": round(download_mbps, 2),
            "upload_mbps": round(upload_mbps, 2),
            "bytes_downloaded": bytes_downloaded,
            "bytes_uploaded": bytes_uploaded,
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }