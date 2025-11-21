from flask import Flask, request

app = Flask(__name__)

@app.route("/config")
def config_page():
    return """
    <h1>TechCheck - Configuração</h1>
    """


@app.route("/")
def home():
    return "TechCheck Activity Provider online!"
