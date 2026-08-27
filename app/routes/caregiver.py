from flask import Blueprint, render_template, session


caregiver = Blueprint(
    "caregiver",
    __name__,
    url_prefix="/caregiver"
)


@caregiver.route("/dashboard")
def dashboard():
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
        activities=list(reversed(activities[-8:])),
        total_games=len(activities),
        average_accuracy=average_accuracy,
        current_difficulty=session.get("difficulty", "easy").title()
    )
