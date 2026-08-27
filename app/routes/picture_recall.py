from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.games.picture_recall import (
    calculate_points,
    check_answer,
    create_round,
)


picture_recall = Blueprint(
    "picture_recall",
    __name__,
    url_prefix="/game/picture",
)


@picture_recall.route("/")
def start():
    session["level"] = 1
    session["score"] = 0
    session["lives"] = 3
    session["state"] = "remember"

    round_data = create_round(session["level"])
    session["remember_items"] = round_data["remember_items"]
    session["options"] = round_data["options"]

    return redirect(url_for("picture_recall.remember"))


@picture_recall.route("/remember")
def remember():
    if "level" not in session:
        return redirect(url_for("picture_recall.start"))

    return render_template(
        "games/picture_recall/remember.html",
        items=session["remember_items"],
        level=session["level"],
    )


@picture_recall.route("/select")
def select():
    if "level" not in session:
        return redirect(url_for("picture_recall.start"))

    return render_template(
        "games/picture_recall/select.html",
        options=session["options"],
        level=session["level"],
        score=session["score"],
        lives=session["lives"],
    )


@picture_recall.route("/submit", methods=["POST"])
def submit():
    if "level" not in session:
        return redirect(url_for("picture_recall.start"))

    selected = request.form.getlist("items")
    remember_items = session.get("remember_items", [])

    correct = check_answer(selected, remember_items)

    if correct:
        points = calculate_points(session["level"])
        session["score"] += points
        session["level"] += 1
        session["last_result"] = "correct"
        session["last_points"] = points
    else:
        session["lives"] -= 1
        session["last_result"] = "wrong"
        session["last_points"] = 0
        if session["lives"] <= 0:
            session["state"] = "game_over"

    history = session.get("game_history", [])
    history.append({
        "game": "Picture Recall",
        "accuracy": 100 if correct else 0,
        "score": f"+{session.get('last_points', 0)} points",
        "difficulty": f"Level {session['level']}",
        "message": "Completed" if correct else "Needs practice"
    })
    session["game_history"] = history[-20:]

    return redirect(url_for("picture_recall.result"))


@picture_recall.route("/result")
def result():
    if "level" not in session:
        return redirect(url_for("picture_recall.start"))

    return render_template(
        "games/picture_recall/result.html",
        level=session["level"],
        score=session["score"],
        lives=session["lives"],
        result=session.get("last_result"),
        points=session.get("last_points", 0),
        game_over=session.get("state") == "game_over",
    )


@picture_recall.route("/next", methods=["POST"])
def next_round():
    if "level" not in session:
        return redirect(url_for("picture_recall.start"))

    if session.get("state") == "game_over":
        return redirect(url_for("picture_recall.start"))

    round_data = create_round(session["level"])
    session["remember_items"] = round_data["remember_items"]
    session["options"] = round_data["options"]
    session["state"] = "remember"

    return redirect(url_for("picture_recall.remember"))
