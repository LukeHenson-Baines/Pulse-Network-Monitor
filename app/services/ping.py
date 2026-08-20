from ping3 import ping


def measure_ping(host: str, count: int = 4) -> dict:
    latencies = []

    for _ in range(count):
        response = ping(host, timeout=2)

        if response is not None:
            latencies.append(response * 1000)

    packets_received = len(latencies)
    packet_loss = ((count - packets_received) / count) * 100

    if not latencies:
        return {
            "host": host,
            "status": "unreachable",
            "packets_sent": count,
            "packets_received": 0,
            "packet_loss_percent": 100.0,
            "min_latency_ms": None,
            "max_latency_ms": None,
            "avg_latency_ms": None,
        }

    return {
        "host": host,
        "status": "reachable",
        "packets_sent": count,
        "packets_received": packets_received,
        "packet_loss_percent": round(packet_loss, 2),
        "min_latency_ms": round(min(latencies), 2),
        "max_latency_ms": round(max(latencies), 2),
        "avg_latency_ms": round(sum(latencies) / packets_received, 2),
    }