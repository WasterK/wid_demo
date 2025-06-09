from flask import Flask, jsonify, request
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import datetime, os

from blocklist import BLOCKLIST

from resources.users import blp as userBlueprint
from resources.health import blp as healthBlueprint
from resources.media import blp as mediaBlueprint
from resources.parts import blp as partsBlueprint
from resources.slideshow import blp as slideshowBlueprint

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,  
    origins=[
        "http://localhost:4200",
        "https://krill-popular-molly.ngrok-free.app",
        "https://kws-pmd-web-jwt.onrender.com"
    ],
    methods=["GET", "POST", "DELETE", "OPTIONS"],  
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "WID REST API"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Use Environment Variable for JWT Secret Key
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=7)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Enable CSRF Protection
app.config["JWT_COOKIE_SECURE"] = True  # Ensure it's True since using HTTPS
app.config["JWT_COOKIE_SAMESITE"] = "None"  # Required for cross-origin cookies
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Disable CSRF protection for testing (can enable later)

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has been revoked.", "error": "token_revoked"}, 401)

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}, 401)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}, 401)

api.register_blueprint(userBlueprint)
api.register_blueprint(healthBlueprint)
api.register_blueprint(mediaBlueprint)
api.register_blueprint(partsBlueprint)
api.register_blueprint(slideshowBlueprint)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
