from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ..repositories.analytics_repo import AnalyticsRepository


class ActivityObserver(Protocol):
    """
    Observer responsável por receber notificações de eventos do ciclo de vida da activity
    """

    def update(self, event: str, instance_id: str, payload: Dict[str, Any]) -> None:
        ...


class DeployAnalyticsObserver:
    """
    Ao ocorrer um deploy, inicializa/regista analytics base
    no AnalyticsRepository (mantendo coerência com /analytics e /analytics/list).
    """

    def __init__(self, analytics_repository: AnalyticsRepository):
        self.analytics_repository = analytics_repository

    def update(self, event: str, instance_id: str, payload: Dict[str, Any]) -> None:
        if event != "DEPLOYED":
            return

        cfg = payload.get("config", {}) if isinstance(payload, dict) else {}
        difficulty = cfg.get("difficulty", "medium")

        base_score = {"easy": 70, "medium": 60, "hard": 50, "super": 45, "geek": 40}.get(difficulty, 60)
        base_time = {"easy": 300, "medium": 420, "hard": 540, "super": 650, "geek": 720}.get(difficulty, 420)

        initial_analytics: List[Dict[str, Any]] = [
            {"userId": "student1", "score": base_score + 25, "completion_time": base_time - 80, "correct_answers": 17},
            {"userId": "student2", "score": base_score, "completion_time": base_time, "correct_answers": 12},
        ]

        self.analytics_repository.save(instance_id, initial_analytics)
