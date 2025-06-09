import base64

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db

blp = Blueprint("Media", __name__, description="Operations on media")

@blp.route("/parts/<int:part_id>/media")
class MediaList(MethodView):

    @jwt_required(optional=True)
    def get(self, part_id):
        media = db.get_media_by_part(part_id)

        # Convert bytes to base64 string for JSON safety
        for m in media:
            if isinstance(m.get("media_data"), bytes):
                m["media_data"] = base64.b64encode(m["media_data"]).decode("utf-8")

        return jsonify(media)


    @jwt_required(optional=True)
    def post(self, part_id):
        # Media file from Bruno or frontend
        file = request.files.get("media_file")
        if not file:
            return {"message": "media_file is required"}, 400

        # Other metadata from form fields
        media_name = request.form.get("media_name", file.filename)
        media_type = request.form.get("media_type", "video")
        duration = int(request.form.get("duration", 5))
        display_order = int(request.form.get("display_order", 0))

        # Read binary file content
        media_data = file.read()

        db.add_media(
            part_id=part_id,
            media_name=media_name,
            media_data=media_data,
            media_type=media_type,
            duration=duration,
            display_order=display_order
        )
        return {"message": "Media uploaded successfully."}, 201


@blp.route("/media/<int:media_id>")
class MediaResource(MethodView):
    @jwt_required()
    def delete(self, media_id):
        db.delete_media(media_id)
        return {"message": "Media deleted."}, 200

    @jwt_required()
    def patch(self, media_id):
        data = request.get_json()
        display_order = data.get("display_order")
        if display_order is None:
            abort(400, message="display_order is required")
        db.update_media_order(media_id, display_order)
        return {"message": "Media updated."}, 200
