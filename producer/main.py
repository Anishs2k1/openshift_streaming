#Home base of the application responsible for
# - Creates the FASTAPI app instance
# - Registers all routes onto that app
# - Owns the lifespan of the application - startup + shutdown
import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager #lets me write startup and shutdown logic easily in 1 function
from generator import generate_random_event
from state import event_history, MAX_HISTORY

from routes.health import router as health_router
from routes.events import router as event_router
from routes.stream import router as event_router


async def produce_events():
    interval = int(os.getenv("EVENT_INTERVAL_SECONDS", "2"))
    while True:
        event = generate_random_event()
        if len(event_history) >= MAX_HISTORY:
            event_history.pop(0)
        event_history.append(event)
        await asyncio.sleep(interval)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(produce_events())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Cluster Event Producer",
    description="Generates and streams fake kubernetes events to a consumer",
    version = "0.1.0",
    lifespan = lifespan
)

app.include_router(health_router, tags=["ops"])
app.include_router(event_history, tags=["stream"])
app.include_router(event_router, tags=['events'])
