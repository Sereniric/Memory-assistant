from flask import Blueprint, render_template, session, request

from app.games.sequence_recall import (
    generate_sequence,
    calculate_score,
    next_difficulty
)


games = Blueprint("games", __name__, url_prefix="/game")


@games.route("/")
def start():
    session["difficulty"] = "easy"

    return render_template(
        "games/start.html"
    )

@games.route("/remember")
def remember():
    difficulty = session.get("difficulty", "easy")

    sequence = generate_sequence(difficulty)

    session["sequence"] = sequence

    return render_template(
        "games/remember.html",
        sequence=sequence,
        difficulty=difficulty
    )

@games.route("/answer")
def answer():
    return render_template(
        "games/answer.html"
    )

@games.route("/submit", methods=["POST"])
def submit():
    sequence = session.get("sequence", [])
    difficulty = session.get("difficulty", "easy")

    answer_text = request.form.get("answer", "")

    try:
        answer = [
            int(number)
            for number in answer_text.split()
        ]
    except ValueError:
        return "Please enter numbers only."

    correct, accuracy = calculate_score(
        sequence,
        answer
    )

    new_difficulty = next_difficulty(
        difficulty,
        accuracy
    )

    session["difficulty"] = new_difficulty

    return render_template(
        "games/result.html",
        sequence=sequence,
        answer=answer,
        correct=correct,
        accuracy=accuracy,
        difficulty=difficulty,
        new_difficulty=new_difficulty
    )