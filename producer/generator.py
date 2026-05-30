#produces the random streamted events on command
#produces randomized ClusterEvent
#contains all the different types of messages that can be sent
import uuid
import random
from datetime import datetime, timezone

from models import ClusterEvents, EventType, Severity


NAMESPACES = [
    "payments",
    "auth",
    "frontend",
    "data-pipeline",
    "monitoring",
    "api-gateway",
]

RESOURCE_NAMES = [
    "api-server-7d9f4b-xkq2p",
    "token-service-5c8d2a-mnr7t",
    "web-app-6f3b1c-pqz9s",
    "event-processor-4a7e8d-rvw3k",
    "cache-proxy-9b2f5c-lmn4j",
    "db-migration-job-8x2p1",
]

MESSAGES = {
    EventType.POD_CRASH: [
        "Container exited with code 1 — application error",
        "Container exited with code 137 — process killed",
        "Back-off restarting failed container",
        "Liveness probe failed — container will be restarted",
    ],
    EventType.OOM_KILL: [
        "Container exceeded memory limit of 512Mi and was killed",
        "Container exceeded memory limit of 256Mi and was killed",
        "OOMKilled — container used more memory than its limit allows",
        "Memory limit exceeded — process terminated by kernel OOM killer",
    ],
    EventType.NODE_PRESSURE: [
        "Node has memory pressure condition — new pods will not be scheduled",
        "Node has disk pressure condition — eviction may occur",
        "Node has PID pressure condition — process limit approaching",
        "Kubelet evicting pods due to memory pressure on node",
    ],
    EventType.DEPLOYMENT_ROLLOUT: [
        "Scaled up replica set web-app-v2 to 1",
        "Scaled down replica set web-app-v1 to 2",
        "Successfully rolled out deployment — all replicas updated",
        "Waiting for deployment rollout to finish — 1 of 3 updated",
    ],
    EventType.IMAGE_PULL_ERROR: [
        "Failed to pull image — manifest unknown",
        "Failed to pull image — unauthorized: authentication required",
        "Back-off pulling image quay.io/myapp/api:v2.1.0",
        "ErrImagePull — image not found in registry",
    ],
}

SEVERITY_MAP = {
    EventType.POD_CRASH: [Severity.CRITICAL, Severity.WARNING],
    EventType.OOM_KILL: [Severity.CRITICAL],
    EventType.NODE_PRESSURE: [Severity.CRITICAL, Severity.WARNING],
    EventType.DEPLOYMENT_ROLLOUT: [Severity.INFO],
    EventType.IMAGE_PULL_ERROR: [Severity.WARNING],
}

def generate_random_event() -> ClusterEvents:
    event_type = random.choice(list(EventType))
    