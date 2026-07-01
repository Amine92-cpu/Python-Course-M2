# api/poller.py
import asyncio
import logging
import time
import httpx
from api.models import Server

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 10
TIMEOUT_SECONDS = 5.0
DEGRADED_THRESHOLD_MS = 500.0


async def poll_server(server: Server) -> None:
    """Check one server's /health endpoint and update its status in-place.

    Status rules:
      UP       - HTTP 200 and response time <= DEGRADED_THRESHOLD_MS
      DEGRADED - HTTP 200 but slow, OR non-200 HTTP response
      DOWN     - connection error or timeout
    """
    url = f"{server.base_url()}/health"
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            resp = await client.get(url)
        elapsed_ms = (time.time() - start) * 1000
        if resp.status_code == 200 and elapsed_ms <= DEGRADED_THRESHOLD_MS:
            server.status = "UP"
        elif resp.status_code == 200:
            server.status = "DEGRADED"
        else:
            server.status = "DEGRADED"
        logger.info("%-20s %s  (%.0f ms)", server.name, server.status, elapsed_ms)
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        server.status = "DOWN"
        logger.warning("%-20s DOWN - %s", server.name, exc)


async def run_poll_loop(store: dict) -> None:
    """Continuously poll all servers in *store* every POLL_INTERVAL_SECONDS.

    This coroutine is designed to run as a background task started during
    the FastAPI lifespan startup event.
    """
    while True:
        if store:
            await asyncio.gather(*[poll_server(s) for s in store.values()])
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
