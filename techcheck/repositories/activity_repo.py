from __future__ import annotations

from typing import Any, Dict, Optional


class ActivityRepository:
    """Persistência de activities em memória."""

    def __init__(self):
        self._activities: Dict[str, Dict[str, Any]] = {}

    def save(self, instance_id: str, payload: Dict[str, Any]) -> None:
        self._activities[instance_id] = payload

    def get(self, instance_id: str) -> Optional[Dict[str, Any]]:
        return self._activities.get(instance_id)
