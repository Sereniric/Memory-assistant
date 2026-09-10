from io import BytesIO

from flask import Blueprint, abort, redirect, render_template, request, send_file, url_for

from app.extensions import db
from app.models import Condition, Medicine, Reminder, get_patient
from app.services import text_to_speech

patient = Blueprint(
    "patient",
    __name__,
    url_prefix="/patient"
)


@patient.route("/")
def index():
    current_patient = get_patient()

    return render_template(
        "patient/index.html",
        patient=current_patient,
        medicines=current_patient.medicines,
        conditions=current_patient.conditions
    )


@patient.route("/reminder/<int:reminder_id>/voice")
def reminder_voice(reminder_id):
    current_patient = get_patient()
    reminder = Reminder.query.filter_by(
        id=reminder_id,
        patient_id=current_patient.id,
    ).first()

    if reminder is None:
        abort(404)

    try:
        audio = text_to_speech.generate_reminder_audio(reminder)
    except text_to_speech.TextToSpeechError as error:
        return str(error), 503

    if isinstance(audio, bytes):
        audio = BytesIO(audio)

    return send_file(audio, mimetype="audio/wav", download_name="reminder.wav")


@patient.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    current_patient = get_patient()

    if request.method == "POST":
        age_raw = request.form.get("age", "").strip()

        current_patient.name = request.form.get("name", "").strip() or "Patient"
        current_patient.age = int(age_raw) if age_raw.isdigit() else None
        current_patient.gender = request.form.get("gender", "").strip()
        current_patient.dementia_stage = request.form.get("dementia_stage", "mild")
        current_patient.diagnosis_date = request.form.get("diagnosis_date", "").strip()
        current_patient.caregiver_name = request.form.get("caregiver_name", "").strip()
        current_patient.caregiver_phone = request.form.get("caregiver_phone", "").strip()
        current_patient.emergency_contact = request.form.get("emergency_contact", "").strip()
        current_patient.notes = request.form.get("notes", "").strip()

        db.session.commit()

        return redirect(url_for("patient.index"))

    return render_template(
        "patient/edit_profile.html",
        patient=current_patient
    )


@patient.route("/medicine/add", methods=["GET", "POST"])
def add_medicine():
    current_patient = get_patient()

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            medicine = Medicine()
            medicine.patient_id = current_patient.id
            medicine.name = name
            medicine.dosage = request.form.get("dosage", "").strip()
            medicine.frequency = request.form.get("frequency", "").strip()
            medicine.notes = request.form.get("notes", "").strip()

            db.session.add(medicine)
            db.session.commit()

        return redirect(url_for("patient.index"))

    return render_template(
        "patient/add_medicine.html",
        patient=current_patient
    )


@patient.route("/medicine/<int:medicine_id>/delete", methods=["POST"])
def delete_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)

    db.session.delete(medicine)
    db.session.commit()

    return redirect(url_for("patient.index"))


@patient.route("/condition/add", methods=["GET", "POST"])
def add_condition():
    current_patient = get_patient()

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            condition = Condition()
            condition.patient_id = current_patient.id
            condition.name = name
            condition.status = request.form.get("status", "active")
            condition.diagnosed_date = request.form.get("diagnosed_date", "").strip()
            condition.notes = request.form.get("notes", "").strip()

            db.session.add(condition)
            db.session.commit()

        return redirect(url_for("patient.index"))

    return render_template(
        "patient/add_condition.html",
        patient=current_patient
    )


@patient.route("/condition/<int:condition_id>/delete", methods=["POST"])
def delete_condition(condition_id):
    condition = Condition.query.get_or_404(condition_id)

    db.session.delete(condition)
    db.session.commit()

    return redirect(url_for("patient.index"))
