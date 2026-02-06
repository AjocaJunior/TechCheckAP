from __future__ import annotations

from typing import Any, Dict, List, Optional


class AnalyticsRepository:
    """Persistência de analytics em memória."""

    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def get(self, instance_id: str) -> Optional[List[Dict[str, Any]]]:
        return self._store.get(instance_id)

    def save(self, instance_id: str, analytics: List[Dict[str, Any]]) -> None:
        self._store[instance_id] = analytics
