from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from db import db
from flask import jsonify

blp = Blueprint("Slideshow", __name__, description="Slideshow API")

@blp.route("/slideshow/<int:part_id>")
class Slideshow(MethodView):
    @jwt_required()
    def get(self, part_id):
        media = db.get_media_by_part(part_id)
        return jsonify({"slideshow": media})

@blp.route("/slideshow/<int:part_id>/thumbnail-bar")
class Thumbnails(MethodView):
    @jwt_required()
    def get(self, part_id):
        media = db.get_media_by_part(part_id)
        thumbnails = [
            {"id": m["id"], "name": m["media_name"], "type": m["media_type"]}
            for m in media
        ]
        return jsonify({"thumbnails": thumbnails})
