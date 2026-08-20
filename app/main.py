from fastapi import FastAPI

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