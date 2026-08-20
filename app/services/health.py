from app.services.ping import measure_ping


def get_network_health(host: str = "8.8.8.8") -> dict:
    ping_result = measure_ping(host)

    if ping_result["status"] == "unreachable":
        return {
            "status": "offline",
            "host": host,
            "reason": "Target host could not be reached.",
            "ping": ping_result,
        }

    packet_loss = ping_result["packet_loss_percent"]
    avg_latency = ping_result["avg_latency_ms"]

    if packet_loss >= 25:
        status = "degraded"
        reason = "High packet loss detected."
    elif avg_latency is not None and avg_latency >= 150:
        status = "degraded"
        reason = "High latency detected."
    else:
        status = "healthy"
        reason = "Network connection is operating normally."

    return {
        "status": status,
        "host": host,
        "reason": reason,
        "ping": ping_result,
    }