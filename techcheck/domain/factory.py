from __future__ import annotations

from typing import Any, Dict

from .quiz import Quiz, OpenSourceQuiz, FinTechQuiz, BigDataQuiz


class QuizFactory:
    """Fábrica de quizzes."""

    @staticmethod
    def create_quiz(config: Dict[str, Any]) -> Quiz:
        tech_stack = config.get("tech_stack", "opensource")
        difficulty = config.get("difficulty", "medium")
        num_questions = config.get("num_questions", 10)

        if tech_stack == "opensource":
            return OpenSourceQuiz(tech_stack, difficulty, num_questions)
        if tech_stack == "fintech":
            return FinTechQuiz(tech_stack, difficulty, num_questions)
        if tech_stack == "bigdata":
            return BigDataQuiz(tech_stack, difficulty, num_questions)

        return Quiz(tech_stack, difficulty, num_questions)
