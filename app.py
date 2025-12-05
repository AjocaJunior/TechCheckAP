from flask import Flask, request, jsonify

app = Flask(__name__)

class Quiz:
    #Classe principal de quiz genérico
    def __init__(self, tech_stack, difficulty, num_questions):
        self.tech_stack = tech_stack
        self.difficulty = difficulty
        self.num_questions = num_questions

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "tech_stack": self.tech_stack,
            "difficulty": self.difficulty,
            "num_questions": self.num_questions
        }


class OpenSourceQuiz(Quiz):
    pass  # Lógica de quiz sobre open source projects


class FinTechQuiz(Quiz):
    pass  # Lógica de quiz sobre tecnologias para finanças


class BigDataQuiz(Quiz):
    pass  # Lógica de quiz sobre alto volume de dados

class QuizFactory:
    # Fábrica

    @staticmethod
    def create_quiz(config):

        tech_stack = config.get("tech_stack", "opensource")
        difficulty = config.get("difficulty", "medium")
        num_questions = config.get("num_questions", 10)

        if tech_stack == "opensource":
            return OpenSourceQuiz(tech_stack, difficulty, num_questions)
        elif tech_stack == "fintech":
            return FinTechQuiz(tech_stack, difficulty, num_questions)
        elif tech_stack == "bigdata":
            return BigDataQuiz(tech_stack, difficulty, num_questions)
        else:
            # fallback simples
            return Quiz(tech_stack, difficulty, num_questions)


# Persistência em memória
activities = {}
analytics_store = {}


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
    return jsonify({
        "activity": "TechCheck",
        "version": "1.0",
        "params": [
            {
                "name": "num_questions",
                "label": "Número de questões",
                "type": "integer",
                "min": 5,
                "max": 50,
                "default": 10
            },
            {
                "name": "difficulty",
                "label": "Nível de dificuldade",
                "type": "enum",
                "values": ["easy", "medium", "hard", "super", "geek"],
                "default": "medium"
            },
            {
                "name": "tech_stack",
                "label": "Área de TICs",
                "type": "enum",
                "values": ["opensource", "fintech", "bigdata"],
                "default": "opensource"
            }
        ]
    })


@app.route("/deploy", methods=["POST"])
def deploy_activity():

    data = request.get_json(silent=True) or {}
    instance_id = data.get("instanceId")
    config = data.get("config", {})

    if not instance_id:
        return jsonify({"error": "instanceId é obrigatório"}), 400


    quiz = QuizFactory.create_quiz(config)

    activities[instance_id] = {
        "config": config,
        "quiz": quiz.to_dict()
    }

    return jsonify({
        "status": "ok",
        "message": "TechCheck deploy efectuado com sucesso",
        "instanceId": instance_id,
        "quiz": quiz.to_dict()
    })


@app.route("/analytics/list")
def analytics_list():
    return jsonify({
        "activity": "TechCheck",
        "analytics": [
            {
                "name": "score",
                "label": "Pontuação final",
                "type": "number"
            },
            {
                "name": "completion_time",
                "label": "Tempo de conclusão (s)",
                "type": "number"
            },
            {
                "name": "correct_answers",
                "label": "Respostas correctas",
                "type": "integer"
            }
        ]
    })


@app.route("/analytics")
def analytics_values():
    instance_id = request.args.get("instanceId")
    if not instance_id:
        return jsonify({"error": "instanceId é obrigatório"}), 400

    analytics = analytics_store.get(instance_id) or [
        {"userId": "student1", "score": 85, "completion_time": 320, "correct_answers": 17},
        {"userId": "student2", "score": 60, "completion_time": 450, "correct_answers": 12}
    ]

    return jsonify({
        "instanceId": instance_id,
        "analytics": analytics
    })


@app.route("/")
def home():
    return "TechCheck Activity Provider online!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
