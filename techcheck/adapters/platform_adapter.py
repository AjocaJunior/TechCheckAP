from __future__ import annotations

from typing import Any, Dict

from ..dto.models import DeployRequest, DeployResult, QuizConfig


class PlatformRequestAdapter:
    """Adapter: converte payload externo (JSON HTTP) em DTO interno estável."""

    @staticmethod
    def to_deploy_request(payload: Dict[str, Any]) -> DeployRequest:
        instance_id = payload.get("instanceId")
        if not instance_id or not isinstance(instance_id, str):
            raise ValueError("instanceId é obrigatório")

        raw_cfg = payload.get("config") or {}
        if not isinstance(raw_cfg, dict):
            raw_cfg = {}

        tech_stack = raw_cfg.get("tech_stack", "opensource")
        difficulty = raw_cfg.get("difficulty", "medium")
        num_questions = raw_cfg.get("num_questions", 10)

        if not isinstance(tech_stack, str):
            tech_stack = "opensource"
        if not isinstance(difficulty, str):
            difficulty = "medium"
        try:
            num_questions = int(num_questions)
        except (TypeError, ValueError):
            num_questions = 10

        if num_questions < 1:
            num_questions = 1
        if num_questions > 200:
            num_questions = 200

        return DeployRequest(
            instance_id=instance_id,
            config=QuizConfig(
                tech_stack=tech_stack,
                difficulty=difficulty,
                num_questions=num_questions,
            ),
        )


class PlatformResponseAdapter:
    """Adapter responsável por converter resultados internos em JSON"""

    @staticmethod
    def deploy_ok(result: DeployResult) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": result.message,
            "instanceId": result.instance_id,
            "quiz": result.quiz,
        }

    @staticmethod
    def error(message: str) -> Dict[str, Any]:
        return {"error": message}
