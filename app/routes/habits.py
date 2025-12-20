from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from app.db import db
from app.models import Habit
from app.utils.auth_middleware import login_required

habits_bp = Blueprint("habits", __name__)


# Create a new habit
@habits_bp.route("", methods=["POST"])
@login_required
def create_habit():
    data = request.get_json() or {}
    title = data.get("title")
    frequency = data.get("frequency", "daily")

    if not title:
        return jsonify({"message": "Title is required."}), 400
    
    new_habit = Habit(title=title, frequency=frequency, user_id=g.current_user.id)

    try:
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({
            "message": "Habit created successfully.",
            "habit": new_habit.to_dict()
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error creating habit.", "error": str(e)}), 500
    