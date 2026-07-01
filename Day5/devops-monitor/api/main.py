# api/main.py
import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from api.auth import verify_api_key
from api.metrics import get_system_metrics
from api.models import Server, ServerIn, ServerOut
from api.poller import run_poll_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# In-memory store
_store: dict[int, Server] = {}
_counter = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start background polling loop on startup."""
    task = asyncio.create_task(run_poll_loop(_store))
    logger.info("Background poller started.")
    yield
    task.cancel()
    logger.info("Background poller stopped.")


app = FastAPI(
    title="DevOps Monitoring API",
    version="1.0.0",
    description="Real-time server monitoring and system metrics API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── System Routes ────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health():
    """Liveness probe — returns ok when the API is running."""
    return {"status": "ok", "servers_monitored": len(_store)}


@app.get("/metrics", tags=["System"])
async def metrics():
    """Return a real-time snapshot of CPU, memory and disk usage."""
    return get_system_metrics()


# ─── Server CRUD Routes ───────────────────────────────────────────────────────

@app.post(
    "/servers",
    response_model=ServerOut,
    status_code=201,
    tags=["Servers"],
)
async def register_server(
    server: ServerIn,
    _: str = Depends(verify_api_key),
):
    """Register a new server to monitor. Requires X-API-Key header."""
    global _counter
    _counter += 1
    record = Server(
        id=_counter,
        name=server.name,
        host=server.host,
        port=server.port,
        tags=server.tags,
    )
    _store[_counter] = record
    logger.info("Registered server %s (id=%d)", server.name, _counter)
    return record


@app.get("/servers", response_model=list[ServerOut], tags=["Servers"])
async def list_servers(status: str | None = None):
    """List all monitored servers. Optionally filter by status (UP/DEGRADED/DOWN)."""
    servers = list(_store.values())
    if status:
        servers = [s for s in servers if s.status.upper() == status.upper()]
    return servers


@app.get("/servers/{server_id}", response_model=ServerOut, tags=["Servers"])
async def get_server(server_id: int):
    """Get a single server by ID."""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204, tags=["Servers"])
async def delete_server(
    server_id: int,
    _: str = Depends(verify_api_key),
):
    """Delete a server from monitoring. Requires X-API-Key header."""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    del _store[server_id]
    logger.info("Deleted server id=%d", server_id)


@app.post("/servers/{server_id}/check", response_model=ServerOut, tags=["Servers"])
async def trigger_check(server_id: int):
    """Manually trigger a health check on a specific server."""
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    import httpx
    import time

    server = _store[server_id]
    url = f"{server.base_url()}/health"
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
        elapsed_ms = (time.time() - start) * 1000
        server.status = (
            "UP" if resp.status_code == 200 and elapsed_ms <= 500 else "DEGRADED"
        )
    except Exception:
        server.status = "DOWN"
    return server


# ─── WebSocket ────────────────────────────────────────────────────────────────

@app.websocket("/ws/metrics")
async def ws_metrics(websocket: WebSocket):
    """Stream system metrics as JSON every second until client disconnects."""
    await websocket.accept()
    logger.info("WebSocket client connected.")
    try:
        while True:
            data = get_system_metrics()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
