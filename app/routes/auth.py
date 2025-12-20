from flask import Blueprint, request, jsonify, current_app
from app.db import db
from app.models import User
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists."}), 400
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials."}), 401
    
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, current_app.config.get("JWT_SECRET"), algorithm="HS256")

    return jsonify({"token": token}), 200