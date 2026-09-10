from flask import Blueprint, redirect, render_template, url_for

from app.extensions import db
from app.models import EmergencyAlert, get_patient

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/sos/confirm")
def sos_confirm():
    patient = get_patient()

    if not patient.caregiver_phone:
        return redirect(url_for("patient.edit_profile", sos_setup="1"))

    return render_template("sos/confirm.html", patient=patient)


@main.route("/sos/send")
def sos_send():
    patient = get_patient()

    if not patient.caregiver_phone:
        return redirect(url_for("patient.edit_profile", sos_setup="1"))

    recipient_name = patient.caregiver_name or "Family member"
    message = (
        f"Emergency alert from MemoryCare: {patient.name} may need immediate help."
    )
    alert = EmergencyAlert(
        patient_id=patient.id,
        recipient_name=recipient_name,
        recipient_phone=patient.caregiver_phone,
        message=message,
    )
    db.session.add(alert)
    db.session.commit()

    return render_template(
        "sos/sent.html",
        patient=patient,
        alert=alert,
        message=message,
    )