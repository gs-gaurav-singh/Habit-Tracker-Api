from .db import db
from datetime import datetime
from .db import db
from datetime import datetime
from passlib.hash import bcrypt


class User(db.Model):
    """User model for storing user account details."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    habits = db.relationship('Habit', backref='owner', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        return bcrypt.verify(password, self.password_hash)


class Habit(db.Model):
    """Habit model for storing habit details."""

    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300))
    frequency = db.Column(db.String(20), default="daily")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    checkins = db.relationship("Checkin", back_populates="habit", cascade="all, delete-orphan")


class Checkin(db.Model):
    """Checkin model for storing habit check-in details."""

    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    habit = db.relationship("Habit", back_populates="checkins")

    __table_args__ = (db.UniqueConstraint("habit_id", "date", name="unique_checkin_per_day"),)