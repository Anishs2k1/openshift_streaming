from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import os

from models import ClusterEvent
from state import event_history, MAX_HISTORY
from generator import generate_random_event

router = APIRouter()


async def generate_stream():
    interval = int(os.getenv("EVENT_INTERVAL_SECONDS", "2"))
    event = generate_random_event()
    if len(event_history) > MAX_HISTORY:
        event_history.pop(0)
    event_history.append(event)
    yield f"data: {event.model_dump_json()}\n\n"
    await asyncio.sleep(interval)

@router.get('/stream')
async def stream():
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )