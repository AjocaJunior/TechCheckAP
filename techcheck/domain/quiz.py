from __future__ import annotations

from typing import Any, Dict


class Quiz:

    def __init__(self, tech_stack: str, difficulty: str, num_questions: int):
        self.tech_stack = tech_stack
        self.difficulty = difficulty
        self.num_questions = num_questions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "tech_stack": self.tech_stack,
            "difficulty": self.difficulty,
            "num_questions": self.num_questions,
        }


class OpenSourceQuiz(Quiz):
    """Lógica de quiz sobre projetos open source."""
    pass


class FinTechQuiz(Quiz):
    """Lógica de quiz sobre tecnologias para finanças."""
    pass


class BigDataQuiz(Quiz):
    """Lógica de quiz sobre alto volume de dados."""
    pass
