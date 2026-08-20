from fastapi import FastAPI

from app.services.bandwidth import get_bandwidth_usage
from app.services.ping import measure_ping


app = FastAPI(
    title="Pulse",
    description="A lightweight network monitoring and diagnostics API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Pulse",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/ping")
def ping_host(host: str = "8.8.8.8"):
    return measure_ping(host)


@app.get("/bandwidth")
def bandwidth():
    return get_bandwidth_usage()