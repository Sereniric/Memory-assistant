from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request
)

from app.games.shopping_memory import (
    create_round,
    calculate_points,
    check_answer
)
from app.games.result_tracking import record_result


shopping_memory = Blueprint(
    "shopping_memory",
    __name__,
    url_prefix="/game/shopping"
)



@shopping_memory.route("/")
def start():

    session["level"] = 1
    session["score"] = 0
    session["lives"] = 3
    session["state"] = "remember"

    round_data = create_round(
        session["level"]
    )

    session["remember_items"] = (
        round_data["remember_items"]
    )

    session["options"] = (
        round_data["options"]
    )

    return redirect(
        url_for("shopping_memory.remember")
    )


@shopping_memory.route("/remember")
def remember():

    if "level" not in session:
        return redirect(
            url_for("shopping_memory.start")
        )

    return render_template(
        "games/shopping/remember.html",
        items=session["remember_items"],
        level=session["level"]
    )


@shopping_memory.route("/select")
def select():

    if "level" not in session:
        return redirect(
            url_for("shopping_memory.start")
        )

    return render_template(
        "games/shopping/select.html",
        options=session["options"],
        level=session["level"],
        score=session["score"],
        lives=session["lives"]
    )


@shopping_memory.route(
    "/submit",
    methods=["POST"]
)
def submit():

    if "level" not in session:
        return redirect(
            url_for("shopping_memory.start")
        )

    selected = request.form.getlist("items")

    remember_items = session.get(
        "remember_items",
        []
    )

    correct = check_answer(
        selected,
        remember_items
    )

    if correct:

        points = calculate_points(
            session["level"]
        )

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

    record_result(
        "Shopping Memory",
        score=session["last_points"],
        accuracy=100 if correct else 0,
        difficulty=f"level {session['level']}",
        correct=correct,
    )

    return redirect(
        url_for("shopping_memory.result")
    )


@shopping_memory.route("/result")
def result():

    if "level" not in session:
        return redirect(
            url_for("shopping_memory.start")
        )

    return render_template(
        "games/shopping/result.html",
        level=session["level"],
        score=session["score"],
        lives=session["lives"],
        result=session.get("last_result"),
        points=session.get("last_points", 0),
        game_over=session.get("state") == "game_over"
    )


@shopping_memory.route(
    "/next",
    methods=["POST"]
)
def next_round():

    if "level" not in session:
        return redirect(
            url_for("shopping_memory.start")
        )

    if session.get("state") == "game_over":
        return redirect(
            url_for("shopping_memory.start")
        )

    round_data = create_round(
        session["level"]
    )

    session["remember_items"] = (
        round_data["remember_items"]
    )

    session["options"] = (
        round_data["options"]
    )

    session["state"] = "remember"

    return redirect(
        url_for("shopping_memory.remember")
    )