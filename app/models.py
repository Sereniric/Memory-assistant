from datetime import datetime

from app.extensions import db


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
