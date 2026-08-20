from fastapi import FastAPI

from app.services.bandwidth import get_bandwidth_usage
from app.services.ping import measure_ping
from app.services.speed import run_speed_test
from app.services.health import get_network_health

from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Pulse",
    description="A lightweight network monitoring and diagnostics API.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/ping")
def ping_host(host: str = "8.8.8.8"):
    return measure_ping(host)

@app.get("/bandwidth")
def bandwidth():
    return get_bandwidth_usage()

@app.get("/speed")
def speed():
    return run_speed_test()

@app.get("/health")
def health(host: str = "8.8.8.8"):
    return get_network_health(host)

@app.get("/metrics")
def metrics(host: str = "8.8.8.8"):
    return {
        "health": get_network_health(host),
        "bandwidth": get_bandwidth_usage(),
    }