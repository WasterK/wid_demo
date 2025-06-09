from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify

blp = Blueprint("Health", __name__, description="Health Check")

@blp.route("/health")
class HealthCheck(MethodView):
    def get(self):
        return jsonify({"status": "ok"})

@blp.route("/version")
class Version(MethodView):
    def get(self):
        return jsonify({"version": "1.0.0"})