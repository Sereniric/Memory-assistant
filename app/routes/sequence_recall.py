from flask import Blueprint, render_template, session, request

from app.games.sequence_recall import (
    generate_sequence,
    calculate_score,
    next_difficulty
)

sequence_recall = Blueprint(
    "sequence_recall",
    __name__,
    url_prefix="/game/sequence"
)

games = Blueprint("games", __name__, url_prefix="/game")

@sequence_recall.route("/")
def intro():

    return render_template(
        "games/sequence_recall/start.html"
    )



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

    history = session.get("game_history", [])
    history.append({
        "game": "Sequence Recall",
        "accuracy": round(accuracy),
        "score": f"{round(accuracy)}%",
        "difficulty": difficulty.title(),
        "message": "Completed"
    })
    session["game_history"] = history[-20:]

    return render_template(
        "games/result.html",
        sequence=sequence,
        answer=answer,
        correct=correct,
        accuracy=accuracy,
        difficulty=difficulty,
        new_difficulty=new_difficulty
    )