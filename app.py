"""
TechCheck Activity Provider — uso de Adapter (PlatformRequestAdapter/PlatformResponseAdapter) e Facade (TechCheckFacade)
Endpoints:
- GET  /
- GET  /config
- GET  /config/params
- POST /deploy
- GET  /analytics/list
- GET  /analytics  
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from flask import Flask, request, jsonify

app = Flask(__name__)

class Quiz:
    """Classe principal de quiz genérico."""

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
    pass  # Lógica de quiz sobre open source projects

class FinTechQuiz(Quiz):
    pass  # Lógica de quiz sobre tecnologias para finanças

class BigDataQuiz(Quiz):
    pass  # Lógica de quiz sobre alto volume de dados

class QuizFactory:
    # Fábrica de quizzes

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


# Repositórios para persistência em memória

class ActivityRepository:
    """Persistência de activities em memória."""

    def __init__(self):
        self._activities: Dict[str, Dict[str, Any]] = {}

    def save(self, instance_id: str, payload: Dict[str, Any]) -> None:
        self._activities[instance_id] = payload

    def get(self, instance_id: str) -> Optional[Dict[str, Any]]:
        return self._activities.get(instance_id)

class AnalyticsRepository:
    """Persistência de analytics em memória."""

    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def get(self, instance_id: str) -> Optional[List[Dict[str, Any]]]:
        return self._store.get(instance_id)

    def save(self, instance_id: str, analytics: List[Dict[str, Any]]) -> None:
        self._store[instance_id] = analytics

# DTOs internos (modelo do domínio / aplicação)

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

# Adapter (Request/Response) — traduz contrato externo <-> interno

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

        # normalizar tipos
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
    """
    Adapter: converte resultados internos em JSON esperado pela plataforma.
    """

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

# Facade — orquestra subsistemas e expõe operações simples

class TechCheckFacade:
    def __init__(self, activity_repository: ActivityRepository, analytics_repository: AnalyticsRepository):
        self.activity_repository = activity_repository
        self.analytics_repository = analytics_repository

    def deploy(self, req: DeployRequest) -> DeployResult:
        cfg_dict = {
            "tech_stack": req.config.tech_stack,
            "difficulty": req.config.difficulty,
            "num_questions": req.config.num_questions,
        }

        quiz = QuizFactory.create_quiz(cfg_dict)

        self.activity_repository.save(
            req.instance_id,
            {"config": cfg_dict, "quiz": quiz.to_dict()},
        )

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

activity_repository = ActivityRepository()
analytics_repository = AnalyticsRepository()
facade = TechCheckFacade(activity_repository, analytics_repository)

@app.route("/")
def home():
    return "TechCheck Activity Provider online!"

@app.route("/config")
def config_page():
    return """
    <!DOCTYPE html>
    <html lang="pt">
      <head>
        <meta charset="UTF-8" />
        <title>TechCheck - Configuração</title>
      </head>
      <body>
        <h1>TechCheck - Configuração</h1>
        <p>Parâmetros de atividades TechCheck.</p>
      </body>
    </html>
    """

@app.route("/config/params")
def config_params():
    return jsonify(facade.get_config_params())

@app.route("/deploy", methods=["POST"])
def deploy_activity():
    payload = request.get_json(silent=True) or {}

    try:
        deploy_req = PlatformRequestAdapter.to_deploy_request(payload)
        result = facade.deploy(deploy_req)
        return jsonify(PlatformResponseAdapter.deploy_ok(result))
    except ValueError as e:
        return jsonify(PlatformResponseAdapter.error(str(e))), 400
    except Exception:
        return jsonify(PlatformResponseAdapter.error("Erro interno ao processar deploy")), 500

@app.route("/analytics/list")
def analytics_list():
    return jsonify(facade.analytics_catalog())

@app.route("/analytics")
def analytics_values():
    instance_id = request.args.get("instanceId", "")
    try:
        return jsonify(facade.analytics_values(instance_id))
    except ValueError as e:
        return jsonify(PlatformResponseAdapter.error(str(e))), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
