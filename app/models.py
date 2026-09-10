from datetime import datetime
from functools import wraps

from flask import redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    name = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False, default="Patient")
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    dementia_stage = db.Column(db.String(20), default="mild")
    diagnosis_date = db.Column(db.String(20))

    caregiver_name = db.Column(db.String(120))
    caregiver_phone = db.Column(db.String(30))
    emergency_contact = db.Column(db.String(120))

    notes = db.Column(db.Text)

    medicines = db.relationship(
        "Medicine",
        backref="patient",
        cascade="all, delete-orphan",
        order_by="Medicine.created_at"
    )

    conditions = db.relationship(
        "Condition",
        backref="patient",
        cascade="all, delete-orphan",
        order_by="Condition.created_at"
    )

    reminders = db.relationship(
        "Reminder",
        backref="patient",
        cascade="all, delete-orphan",
        order_by="Reminder.created_at.desc()"
    )


class Medicine(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(60))
    frequency = db.Column(db.String(120))
    notes = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Condition(db.Model):
    __tablename__ = "conditions"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="active")
    diagnosed_date = db.Column(db.String(20))
    notes = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    title = db.Column(db.String(120), nullable=False)
    day = db.Column(db.String(20))
    time = db.Column(db.String(20))
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def ensure_default_users():
    if User.query.count() > 0:
        return

    patient_user = User(username="patient", role="patient", name="Patient")
    patient_user.set_password("patient123")

    caregiver_user = User(username="caregiver", role="caregiver", name="Caregiver")
    caregiver_user.set_password("caregiver123")

    db.session.add_all([patient_user, caregiver_user])
    db.session.commit()


def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return db.session.get(User, user_id)


def require_roles(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if user is None:
                return redirect(url_for("main.login"))

            if allowed_roles and user.role not in allowed_roles:
                if user.role == "patient":
                    return redirect(url_for("patient.index"))
                return redirect(url_for("main.home"))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_patient():
    """
    This MVP tracks a single patient profile (no login system yet),
    so we always work with the first patient record, creating a
    blank one the first time the app is used.
    """
    patient = Patient.query.first()

    if patient is None:
        patient = Patient()
        patient.name = "Patient"
        patient.dementia_stage = "mild"

        db.session.add(patient)
        db.session.commit()

    return patient
