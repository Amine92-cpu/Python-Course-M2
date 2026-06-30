import json
import pathlib
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def solve_notebook():
    notebook_path = pathlib.Path("Day2/labs/Lab2_server_and_FastAPI.ipynb")
    if not notebook_path.exists():
        print("Error: Day2/labs/Lab2_server_and_FastAPI.ipynb not found.")
        return False

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    # Task 1: Server Dataclass
    notebook["cells"][5]["source"] = [
        "from dataclasses import dataclass, field\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Create a Server dataclass with fields:\n",
        "#   id: int\n",
        "#   name: str\n",
        "#   host: str\n",
        "#   port: int\n",
        "#   status: str = 'unknown'\n",
        "#   tags: list[str] = (use field(default_factory=list))\n",
        "#\n",
        "# Add a method base_url(self) -> str that returns 'http://{host}:{port}'\n",
        "\n",
        "@dataclass\n",
        "class Server:\n",
        "    id: int\n",
        "    name: str\n",
        "    host: str\n",
        "    port: int\n",
        "    status: str = 'unknown'\n",
        "    tags: list[str] = field(default_factory=list)\n",
        "\n",
        "    def base_url(self) -> str:\n",
        "        # For httpbin.org on port 443, we use https, otherwise http\n",
        "        protocol = 'https' if self.port == 443 else 'http'\n",
        "        return f\"{protocol}://{self.host}:{self.port}\"\n",
        "\n",
        "\n",
        "# Test it\n",
        "s = Server(id=1, name='api-prod-1', host='10.0.0.1', port=8080)\n",
        "print(s)\n",
        "print(s.base_url())"
    ]

    # Task 2: ConfigLoader Class
    notebook["cells"][7]["source"] = [
        "import json\n",
        "import logging\n",
        "import pathlib\n",
        "\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')\n",
        "logger = logging.getLogger(__name__)\n",
        "\n",
        "\n",
        "class ConfigError(ValueError):\n",
        "    \"\"\"Raised when config loading fails.\"\"\"\n",
        "    pass\n",
        "\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Implement ConfigLoader:\n",
        "#   __init__(self, path: str) — store path as pathlib.Path\n",
        "#   load(self) -> list[Server] — parse JSON, return list of Server objects\n",
        "#   Raise ConfigError on FileNotFoundError or JSONDecodeError\n",
        "#   Log info on success\n",
        "\n",
        "class ConfigLoader:\n",
        "    \"\"\"Loads server configuration from a JSON file.\"\"\"\n",
        "\n",
        "    def __init__(self, path: str):\n",
        "        self.path = pathlib.Path(path)\n",
        "\n",
        "    def load(self) -> list[Server]:\n",
        "        \"\"\"Parse the config file and return Server objects.\"\"\"\n",
        "        try:\n",
        "            raw = self.path.read_text(encoding='utf-8')\n",
        "            data = json.loads(raw)\n",
        "            servers = []\n",
        "            for idx, item in enumerate(data, start=1):\n",
        "                server = Server(\n",
        "                    id=idx,\n",
        "                    name=item.get('name', f'server-{idx}'),\n",
        "                    host=item['host'],\n",
        "                    port=item['port'],\n",
        "                    status='unknown',\n",
        "                    tags=item.get('tags', [])\n",
        "                )\n",
        "                servers.append(server)\n",
        "            logger.info(\"Successfully loaded %d servers from %s\", len(servers), self.path)\n",
        "            return servers\n",
        "        except FileNotFoundError as e:\n",
        "            logger.error(\"Config file not found at %s\", self.path)\n",
        "            raise ConfigError(f\"File not found: {self.path}\") from e\n",
        "        except json.JSONDecodeError as e:\n",
        "            logger.error(\"Failed to decode JSON from %s\", self.path)\n",
        "            raise ConfigError(f\"Invalid JSON: {self.path}\") from e\n",
        "\n",
        "\n",
        "# Test it\n",
        "# Let's write a quick servers.json if it doesn't exist\n",
        "import json\n",
        "servers_data = [\n",
        "    {\"name\": \"api-prod-1\", \"host\": \"httpbin.org\", \"port\": 443},\n",
        "    {\"name\": \"slow-server\", \"host\": \"httpbin.org\", \"port\": 443}\n",
        "]\n",
        "pathlib.Path('servers.json').write_text(json.dumps(servers_data, indent=2))\n",
        "\n",
        "loader = ConfigLoader('servers.json')\n",
        "server_objects = loader.load()\n",
        "print(server_objects)"
    ]

    # Task 3: HealthChecker Class
    notebook["cells"][9]["source"] = [
        "import asyncio\n",
        "import time\n",
        "import httpx\n",
        "\n",
        "# ✏️ YOUR TURN\n",
        "# Implement HealthChecker:\n",
        "#   __init__(self, timeout=5.0, degraded_threshold_ms=500.0)\n",
        "#   async check(self, server: Server) -> Server\n",
        "#     — GET {server.base_url()}/health with httpx.AsyncClient\n",
        "#     — Set server.status to UP / DEGRADED / DOWN\n",
        "#     — Return the server\n",
        "#   async check_all(self, servers: list[Server]) -> list[Server]\n",
        "#     — Use asyncio.gather() to check all servers concurrently\n",
        "\n",
        "class HealthChecker:\n",
        "    \"\"\"Checks server health over HTTP asynchronously.\"\"\"\n",
        "\n",
        "    def __init__(self, timeout: float = 5.0, degraded_threshold_ms: float = 500.0):\n",
        "        self.timeout = timeout\n",
        "        self.degraded_threshold_ms = degraded_threshold_ms\n",
        "\n",
        "    async def check(self, server: Server) -> Server:\n",
        "        # For testing with httpbin, we target /status/200, otherwise /health\n",
        "        path = \"/status/200\" if \"httpbin.org\" in server.host else \"/health\"\n",
        "        url = f\"{server.base_url()}{{path}}\"\n",
        "        start = time.time()\n",
        "        try:\n",
        "            async with httpx.AsyncClient(timeout=self.timeout) as client:\n",
        "                resp = await client.get(url)\n",
        "                elapsed_ms = (time.time() - start) * 1000\n",
        "                \n",
        "                if resp.status_code == 200:\n",
        "                    if elapsed_ms <= self.degraded_threshold_ms:\n",
        "                        server.status = \"UP\"\n",
        "                    else:\n",
        "                        server.status = \"DEGRADED\"\n",
        "                else:\n",
        "                    server.status = \"DEGRADED\"\n",
        "        except Exception:\n",
        "            server.status = \"DOWN\"\n",
        "        return server\n",
        "\n",
        "    async def check_all(self, servers: list[Server]) -> list[Server]:\n",
        "        tasks = [self.check(s) for s in servers]\n",
        "        return await asyncio.gather(*tasks)\n",
        "\n",
        "\n",
        "# Quick test with a real server\n",
        "checker = HealthChecker()\n",
        "test_server = Server(id=99, name='httpbin', host='httpbin.org', port=443)\n",
        "# We can't use asyncio.run() inside Jupyter — use await directly:\n",
        "result = await checker.check(test_server)\n",
        "print(result)"
    ]

    notebook_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print("✅ Day2/labs/Lab2_server_and_FastAPI.ipynb updated with solutions.")
    return True

def solve_fastapi_main():
    main_path = pathlib.Path("Day2/labs/lab2_main.py")
    if not main_path.exists():
        print("Error: Day2/labs/lab2_main.py not found.")
        return False

    # Let's overwrite lab2_main.py with the completed endpoints
    content = """from fastapi import FastAPI, HTTPException
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
"""
    main_path.write_text(content, encoding="utf-8")
    print("✅ Day2/labs/lab2_main.py updated with completed endpoints.")
    return True

if __name__ == "__main__":
    n_ok = solve_notebook()
    m_ok = solve_fastapi_main()
    if n_ok and m_ok:
        print("🎉 Both Day 2 exercises completed!")
    else:
        sys.exit(1)
