from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
from app.models import User

def login_required(fn):
    """Decorator to protect routes that require authentication."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"message": "Authorization header is missing"}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid authorization header"}), 401
        
        token = parts[1]
        try:
            payload = jwt.decode(token, current_app.config.get("SECRET_KEY", 'dev'), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401
        
        # Attach the user to flask.g for route handlers to use
        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        g.current_user = user
        return fn(*args, **kwargs)
    
    return wrapper