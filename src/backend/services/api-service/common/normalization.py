from __future__ import annotations

from typing import List

from app.schemas import Event


def dedupe_events(events: List[Event]) -> List[Event]:
    """Remove duplicate events by event_id, keeping the first occurrence."""
    seen = {}
    for event in events:
        if event.event_id not in seen:
            seen[event.event_id] = event
    return list(seen.values())


def sort_events(events: List[Event]) -> List[Event]:
    """Sort events by start time then title for deterministic responses."""
    return sorted(events, key=lambda evt: (evt.start_at, evt.title))


def normalize_events(events: List[Event]) -> List[Event]:
    return sort_events(dedupe_events(events))
