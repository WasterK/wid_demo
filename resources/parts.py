from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db

blp = Blueprint("Parts", __name__, description="Operations on parts")

@blp.route("/parts")
class PartList(MethodView):
    @jwt_required(optional=True)
    def get(self):
        parts = db.get_all_parts()
        return jsonify(parts)

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get("name")
        if not name:
            abort(400, message="Part name is required")
        db.add_part(name)
        return {"message": f"Part '{name}' added."}, 201

@blp.route("/parts/<int:part_id>")
class PartResource(MethodView):
    @jwt_required()
    def delete(self, part_id):
        db.delete_part(part_id)
        return {"message": "Part deleted"}, 200

@blp.route("/parts/search")
class PartSearch(MethodView):
    @jwt_required(optional=True)
    def get(self):
        query = request.args.get("q", "")
        all_parts = db.get_all_parts()
        filtered = [p for p in all_parts if query.lower() in p["name"].lower()]
        return jsonify(filtered)