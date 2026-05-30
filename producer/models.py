#This file defines the shape of the json datastructures ... the events that are going to be streamed.
#What are the variety of events being used
#What are the variety of severities that will be streamed
#Just defining the structure of the models
from pydantic import BaseModel, Field #handing validation and linting of data structures
from datetime import datetime
from enum import Enum #enumerating numbers with variables to represent them
from typing import Optional

class EventType(str, Enum):
    POD_CRASH           = "PodCrash"
    OOM_KILL            = "OOMKill"
    NODE_PRESSURE       = "NodePressure"
    DEPLOYMENT_ROLLOUT  = "DeploymentRollout"
    IMAGE_PULL_ERROR    = "ImagePullError"


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING  = "warning"
    INFO     = "info"


class ClusterEvent(BaseModel):
    id: str = Field(
        description = "Unique Identifier for this Field",
        example = "ID-2321-JRT321A"
    )

    timestamp: datetime = Field(
        description = "Time when the event was created",
        example = "10:20:02 02-12-2026"
    )

    event_type: EventType = Field(
        description = "The type of event thats being streamed",
        example = "Pod Crash"

    )

    severity: Severity = Field(
        description = "Severity of the event thats coming through",
        example = "CRITICAL"
    )

    namespace: str = Field(
        description = "Namespace within Openshift this is occurring in",
        example = "visavms"
    )

    resource_name: str = Field(
        description = "The application this event is coming from",
        example = "Web-app-3210"
    )

    message: str = Field(
        description = "What is actually happening to the app",
        example = "everything is fucked"
    )

class EventSummary(BaseModel):
    total_received: int = Field(

    )

    counts_by_severity: dict[str : int] = Field(

    )

    counts_by_type: dict[str : int] = Field(
        
    )




