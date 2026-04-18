---
name: event-system-coherence
description: >-
  Verify that every emitted event has a corresponding consumer, logger, or metric.
  Detects orphan events, missing audit trails, and unexposed event endpoints.
  Ensures events are not silently created and forgotten.
license: MIT
metadata:
  category: architecture
  author: ecos
  targets: [python, observability]
---

# Event System Coherence Checker

Ensure every event emitted has a route to consumption, logging, or metrics.

---

## Triggers

Use this skill when:
- "audit event system"
- "check event consumption"
- "find orphan events"
- "verify event logging"
- "event traceability"

---

## Quick Reference

| Check | Required |
|-------|----------|
| Event created | Has consumer/log/metric |
| Event emitted | Has audit trail |
| Event type | Exposed via /metrics |
| Event handler | Never silent |

---

## Process

### Phase 1: Find Event Definitions

Search for event classes and event emission:

```python
# Event definitions
class ActivityEvent(BaseModel):
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]

class RouteEvent(BaseModel):
    backend_id: str
    server_id: str
    tool_name: str

# Event emission
self._activity_history.append(event)
await self.dispatcher.dispatch(event)
```

### Phase 2: Find Event Consumers

Check for:
- Event handlers that process events
- Logging of events
- Metrics export of events
- Storage/persistence of events

### Phase 3: Check Coherence

For each event type:
- ✓ Has at least one consumer
- ✓ Logged with structured info
- ✓ Exposed in /metrics endpoint
- ✓ Stored for audit (if critical)

---

## Common Issues

### Issue 1: Orphan Event
```python
# Created but never consumed
class ActivityEvent:
    pass

# In Watchdog:
def record_activity(self, event_type: str, **data):
    event = ActivityEvent(...)
    self._activity_history.append(event)  # ← Appended, never read!
```

### Issue 2: Silent Logging
```python
# Logged but not actionable
async def dispatch(self, event: Event):
    logger.info(f"Event: {event}")  # ← Just info, no metric
```

### Issue 3: Missing Metrics
```python
# Event emitted but no prometheus counter
def on_request(self, request):
    event_counter.inc()  # ← Not implemented!
```

---

## Audit Report Template

```markdown
## Event System Coherence Audit

### ORPHAN EVENTS (created but never consumed)
- ActivityEvent (watchdog.py) - appended to list, never read
- RouteEvent (temporal_router.py) - created, no handler

### MISSING METRICS
- /metrics/events?type=activity - NOT IMPLEMENTED
- /metrics/routes/history - NOT IMPLEMENTED

### PARTIAL LOGGING
- VerificationResult - logged but no structured fields
```

---

## Fix Patterns

### Pattern 1: Event Consumer
```python
class EventConsumer:
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
    
    def register(self, event_type: str, handler: Callable):
        self._handlers[event_type] = handler
    
    async def consume(self, event: Event):
        if event.event_type in self._handlers:
            await self._handlers[event.event_type](event)
```

### Pattern 2: Event Metrics
```python
from prometheus_client import Counter

event_counter = Counter(
    'gateway_events_total',
    'Total events emitted',
    ['event_type', 'source']
)

def emit_event(event: Event):
    event_counter.labels(
        event_type=event.event_type,
        source=event.source
    ).inc()
```

### Pattern 3: Event Audit Log
```python
import structlog

logger = structlog.get_logger()

def emit_event(event: Event):
    logger.info(
        "event_emitted",
        event_type=event.event_type,
        event_id=event.id,
        source=event.source,
        **event.data
    )
```

---

## Implementation Checklist

For each event type:
- [ ] Define event class with pydantic
- [ ] Register event type in registry
- [ ] Add handler method
- [ ] Add prometheus counter
- [ ] Add structured log
- [ ] Expose /metrics endpoint