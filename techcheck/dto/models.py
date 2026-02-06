from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class QuizConfig:
    tech_stack: str = "opensource"
    difficulty: str = "medium"
    num_questions: int = 10


@dataclass(frozen=True)
class DeployRequest:
    instance_id: str
    config: QuizConfig


@dataclass(frozen=True)
class DeployResult:
    instance_id: str
    quiz: Dict[str, Any]
    message: str = "TechCheck deploy efectuado com sucesso"
