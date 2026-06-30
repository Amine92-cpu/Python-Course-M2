from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dataclasses import dataclass, field as dc_field

app = FastAPI(title="DevOps Monitoring API", version="1.0")


# ─── Internal model ─────────────────────────────────────────────────────────

@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = dc_field(default_factory=list)

    def base_url(self) -> str:
        protocol = "https" if self.port == 443 else "http"
        return f"{protocol}://{self.host}:{self.port}"


# ─── Pydantic schemas ────────────────────────────────────────────────────────

class ServerIn(BaseModel):
    name: str
    host: str
    port: int = Field(default=8080, ge=1, le=65535)
    tags: list[str] = []


class ServerOut(BaseModel):
    id: int
    name: str
    host: str
    port: int
    status: str
    tags: list[str] = []
    model_config = {"from_attributes": True}


# ─── In-memory store ─────────────────────────────────────────────────────────

_store: dict[int, Server] = {}
_counter = 0


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "servers": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    global _counter
    _counter += 1
    record = Server(id=_counter, name=server.name, host=server.host,
                    port=server.port, tags=server.tags)
    _store[_counter] = record
    return record


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    servers = list(_store.values())
    if status:
        return [s for s in servers if s.status.upper() == status.upper()]
    return servers


@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail=f"Server with ID {server_id} not found")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail=f"Server with ID {server_id} not found")
    del _store[server_id]
    return


@app.post("/servers/{server_id}/check", response_model=ServerOut)
async def trigger_check(server_id: int):
    import httpx
    if server_id not in _store:
        raise HTTPException(404, "Server not found")
    server = _store[server_id]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            path = "/status/200" if "httpbin" in server.host else "/health"
            resp = await client.get(f"{server.base_url()}{path}")
            server.status = "UP" if resp.status_code == 200 else "DEGRADED"
    except Exception:
        server.status = "DOWN"
    return server
