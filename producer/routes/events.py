from fastapi import APIRouter, Query
from typing import Optional

from models import ClusterEvent, Severity, EventType
from state import event_history


router = APIRouter()

@router.get('/events', response_model=list[ClusterEvent])
async def get_events(
    severity: Optional[Severity] = Query(
        default = None,
        description="Filter events by severity level"
    ),
    event_type: Optional[EventType] = Query(
        default = None,
        description="Filter received events by event type"        
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=50,
        description="Number of recent events to return"
    )


):
    filtering_events = event_history

    if severity:
        filtering_events = [e for e in filtering_events if e.severity == severity]

    if event_type:
        filtering_events = [e for e in filtering_events if e.event_type == event_type]

    return list(filtering_events[-limit:])
            

