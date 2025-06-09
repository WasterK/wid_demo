from flask import make_response, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

import time

from blocklist import BLOCKLIST

from db import db
from schemas import UserSchema, LoginSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data: dict):
        if db.is_user_already_exists(user_data["username"]):
            abort(400, message="Username is already exists.")

        user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
        # if user_data.get("email", None):
        user = db.add_user(user_data)
        if user == -1:
            return {"message": "Something went wrong in database. please try again later"}, 500
        #     return {"message": "user created successfully."}, 201
        # else: 
        # user = db.add_user_without_email(user_data)
        return {"message": "user created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200)
    def post(self, user_data):
        # Check if the user exists
        if not db.is_user_already_exists(user_data["username"]):
            abort(400, message="User does not exist. Please create an account first.")

        # Validate user credentials
        user = db.get_user_by_username(user_data["username"])
        if user and pbkdf2_sha256.verify(user_data["password"], user["password"]):
            # Generate JWT tokens
            access_token = create_access_token(identity=str(user["user_id"]), fresh=True)
            refresh_token = create_refresh_token(identity=str(user["user_id"]))

            # Create the response object
            response = make_response(jsonify({'message': f'Logged in successfully.', "username": user["username"], "access_token": access_token, "refresh_token": refresh_token}))

            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            
            return response, 200
        else:
            # Invalid credentials
            abort(401, message="Invalid Credentials.")

@blp.route("/token-expiration")
class CheckTokenValidity(MethodView):
    @jwt_required(locations=["cookies"])
    @blp.response(200)
    def get(self):
        return jsonify({"message": "Token is valid."}, 200)

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(locations=["cookies"], refresh=True)
    @blp.response(200)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=str(current_user), fresh=False)

        response = make_response(jsonify({'message': 'token refreshed'}))
        
        set_access_cookies(response, access_token)
        return response, 200 

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = db.get_user(user_id)
        if user:
            return {"username": user[0]}, 200
        else:
            abort(404, message="User not found.")

    def delete(self, user_id):
        try:
            db.delete_user(user_id)
            return {"message": "User deleted."}
        except Exception:
            abort(404, message=f"Error occurred while deleting user.")

@blp.route("/logout")
class Logout(MethodView):
    @jwt_required(locations=["cookies"])
    @blp.response(200)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200