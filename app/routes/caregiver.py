from flask import Blueprint, redirect, render_template, request, session, url_for

from app.extensions import db
from app.models import Reminder, get_patient


caregiver = Blueprint(
    "caregiver",
    __name__,
    url_prefix="/caregiver"
)


@caregiver.route("/dashboard")
def dashboard():
    patient = get_patient()
    activities = session.get("game_history", [])
    accuracy_values = [
        activity["accuracy"]
        for activity in activities
        if activity.get("accuracy") is not None
    ]
    average_accuracy = round(
        sum(accuracy_values) / len(accuracy_values)
    ) if accuracy_values else 0

    return render_template(
        "caregiver/dashboard.html",
        patient=patient,
        reminders=patient.reminders,
        activities=list(reversed(activities[-8:])),
        total_games=len(activities),
        average_accuracy=average_accuracy,
        current_difficulty=session.get("difficulty", "easy").title()
    )


@caregiver.route("/reminder/add", methods=["GET", "POST"])
def add_reminder():
    current_patient = get_patient()

    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if title:
            reminder = Reminder()
            reminder.patient_id = current_patient.id
            reminder.title = title
            reminder.day = request.form.get("day", "").strip()
            reminder.time = request.form.get("time", "").strip()
            reminder.message = request.form.get("message", "").strip()

            db.session.add(reminder)
            db.session.commit()

        return redirect(url_for("caregiver.dashboard"))

    return render_template(
        "caregiver/add_reminder.html",
        patient=current_patient
    )


@caregiver.route("/reminders")
def list_reminders():
    current_patient = get_patient()
    return render_template(
        "caregiver/add_reminder.html",
        patient=current_patient,
        reminders=current_patient.reminders
    )
