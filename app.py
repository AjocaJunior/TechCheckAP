"""
TechCheck Activity Provider — remoção do antipadrão Blob

Padrões existentes:
- Factory (QuizFactory)
- Adapter (PlatformRequestAdapter / PlatformResponseAdapter)
- Facade (TechCheckFacade)
- Observer (DeployAnalyticsObserver)

Endpoints:
- GET  /
- GET  /config
- GET  /config/params
- POST /deploy
- GET  /analytics/list
- GET  /analytics
"""

from __future__ import annotations

from flask import Flask

from techcheck.observers.deploy_analytics import DeployAnalyticsObserver
from techcheck.repositories.activity_repo import ActivityRepository
from techcheck.repositories.analytics_repo import AnalyticsRepository
from techcheck.services.facade import TechCheckFacade
from techcheck.web.routes import create_routes_blueprint


def create_app() -> Flask:
    app = Flask(__name__)

    activity_repository = ActivityRepository()
    analytics_repository = AnalyticsRepository()
    facade = TechCheckFacade(activity_repository, analytics_repository)

    facade.attach(DeployAnalyticsObserver(analytics_repository))

    app.register_blueprint(create_routes_blueprint(facade))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
