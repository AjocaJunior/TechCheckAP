from __future__ import annotations

from typing import Any, Dict, List

from ..domain.factory import QuizFactory
from ..dto.models import DeployRequest, DeployResult
from ..observers.deploy_analytics import ActivityObserver
from ..repositories.activity_repo import ActivityRepository
from ..repositories.analytics_repo import AnalyticsRepository


class TechCheckFacade:
    """
    Facade responsável por orquestrar subsistemas e expor operações simples.
    """

    def __init__(self, activity_repository: ActivityRepository, analytics_repository: AnalyticsRepository):
        self.activity_repository = activity_repository
        self.analytics_repository = analytics_repository
        self._observers: List[ActivityObserver] = []

    def attach(self, observer: ActivityObserver) -> None:
        self._observers.append(observer)

    def notify(self, event: str, instance_id: str, payload: Dict[str, Any]) -> None:
        for obs in list(self._observers):
            obs.update(event, instance_id, payload)

    def deploy(self, req: DeployRequest) -> DeployResult:
        cfg_dict = {
            "tech_stack": req.config.tech_stack,
            "difficulty": req.config.difficulty,
            "num_questions": req.config.num_questions,
        }

        quiz = QuizFactory.create_quiz(cfg_dict)
        payload = {"config": cfg_dict, "quiz": quiz.to_dict()}

        self.activity_repository.save(req.instance_id, payload)

        self.notify("DEPLOYED", req.instance_id, payload)

        return DeployResult(instance_id=req.instance_id, quiz=quiz.to_dict())

    def get_config_params(self) -> Dict[str, Any]:
        return {
            "activity": "TechCheck",
            "version": "1.0",
            "params": [
                {
                    "name": "num_questions",
                    "label": "Número de questões",
                    "type": "integer",
                    "min": 5,
                    "max": 50,
                    "default": 10,
                },
                {
                    "name": "difficulty",
                    "label": "Nível de dificuldade",
                    "type": "enum",
                    "values": ["easy", "medium", "hard", "super", "geek"],
                    "default": "medium",
                },
                {
                    "name": "tech_stack",
                    "label": "Área de TICs",
                    "type": "enum",
                    "values": ["opensource", "fintech", "bigdata"],
                    "default": "opensource",
                },
            ],
        }

    def analytics_catalog(self) -> Dict[str, Any]:
        return {
            "activity": "TechCheck",
            "analytics": [
                {"name": "score", "label": "Pontuação final", "type": "number"},
                {"name": "completion_time", "label": "Tempo de conclusão (s)", "type": "number"},
                {"name": "correct_answers", "label": "Respostas correctas", "type": "integer"},
            ],
        }

    def analytics_values(self, instance_id: str) -> Dict[str, Any]:
        if not instance_id:
            raise ValueError("instanceId é obrigatório")

        existing = self.analytics_repository.get(instance_id)

        analytics = existing or [
            {"userId": "student1", "score": 85, "completion_time": 320, "correct_answers": 17},
            {"userId": "student2", "score": 60, "completion_time": 450, "correct_answers": 12},
        ]
        return {"instanceId": instance_id, "analytics": analytics}
