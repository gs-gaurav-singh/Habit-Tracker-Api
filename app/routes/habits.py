from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from app.db import db
from app.models import Habit
from app.utils.auth_middleware import login_required

habits_bp = Blueprint("habits", __name__)


# Create a new habit
@habits_bp.route("/add_habits", methods=["POST"])
@login_required
def create_habit():
    data = request.get_json() or {}
    title = data.get("title")
    frequency = data.get("frequency", "daily")

    if not title:
        return jsonify({"Message": "Title is required."}), 400
    
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
    
# Get all habits
@habits_bp.route("/", methods=["GET"])
@login_required
def get_habits():
    habits = Habit.query.filter_by(user_id=g.current_user.id).all()
    if len(habits) == 0:
        return jsonify({"Message": "Habit not found."}), 404
    else:
        return jsonify([habit.to_dict() for habit in habits]), 200

# Get a single habit
@habits_bp.route('/<int:habit_id>', methods=["GET"])
@login_required
def get_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=g.current_user.id).first()
    if not habit:
        return jsonify({"message": "Habit not found."}), 404
    
    return jsonify(habit.to_dict()), 200

# Update the habit
@habits_bp.route("/update/<int:habit_id>", methods=["PUT"])
@login_required
def update_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=g.current_user.id).first()
    if not habit:
        return jsonify({"message": "Habit not found."}), 404
    
    data = request.get_json() or {}
    habit.title = data.get("title", habit.title)
    habit.frequency = data.get("frequency", habit.frequency)

    try:
        db.session.commit()
        return jsonify({
            "message": "Updated habit successfully.",
            "habit": habit.to_dict()
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error updating habit.", "error": str(e)}), 500
    
# Delete a habit
@habits_bp.route("/ /<int:habit_id>", methods=["DELETE"])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=g.current_user.id).first()
    if not habit:
        return jsonify({"message": "Habit not found."}), 404

    try:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({"message": "Deleted habit successfully."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting habit.", "error": str(e)}), 500
