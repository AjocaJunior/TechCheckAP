from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..adapters.platform_adapter import PlatformRequestAdapter, PlatformResponseAdapter
from ..services.facade import TechCheckFacade


def create_routes_blueprint(facade: TechCheckFacade) -> Blueprint:
    bp = Blueprint("techcheck", __name__)

    @bp.get("/")
    def home():
        return "TechCheck Activity Provider online!"

    @bp.get("/config")
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

    @bp.get("/config/params")
    def config_params():
        return jsonify(facade.get_config_params())

    @bp.post("/deploy")
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

    @bp.get("/analytics/list")
    def analytics_list():
        return jsonify(facade.analytics_catalog())

    @bp.get("/analytics")
    def analytics_values():
        instance_id = request.args.get("instanceId", "")
        try:
            return jsonify(facade.analytics_values(instance_id))
        except ValueError as e:
            return jsonify(PlatformResponseAdapter.error(str(e))), 400

    return bp
