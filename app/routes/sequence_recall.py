import re

from flask import Blueprint, render_template, session, request

from app.games.sequence_recall import (
    generate_sequence,
    calculate_score,
    next_difficulty
)
from app.games.result_tracking import record_result
from app.services.speech_to_text import SpeechToTextError, transcribe_audio

sequence_recall = Blueprint(
    "sequence_recall",
    __name__,
    url_prefix="/game/sequence"
)

games = Blueprint("games", __name__, url_prefix="/game")

NUMBER_WORDS = {
    "zero": 0,
    "oh": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def normalize_answer(answer_text):
    """Convert typed digits or simple spoken digits into game input."""
    tokens = re.findall(r"[a-z]+|\d+", answer_text.lower())

    if not tokens:
        raise ValueError

    answer = []
    for token in tokens:
        if token.isdigit():
            answer.append(int(token))
        elif token in NUMBER_WORDS:
            answer.append(NUMBER_WORDS[token])
        else:
            raise ValueError

    return answer

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

@games.route("/voice", methods=["POST"])
def voice_answer():
    audio_file = request.files.get("voice_answer")

    if audio_file is None or not audio_file.filename:
        return render_template(
            "games/answer.html",
            voice_error="Please record or choose an audio answer.",
        )

    try:
        transcript = transcribe_audio(audio_file, language="en-IN")
        normalized_answer = " ".join(
            str(number) for number in normalize_answer(transcript)
        )
    except (SpeechToTextError, ValueError):
        return render_template(
            "games/answer.html",
            voice_error="We could not understand the numbers. Please try again or type your answer.",
        )

    return render_template(
        "games/answer.html",
        voice_transcript=transcript,
        voice_answer=normalized_answer,
    )

@games.route("/submit", methods=["POST"])
def submit():
    sequence = session.get("sequence", [])
    difficulty = session.get("difficulty", "easy")

    answer_text = request.form.get("answer", "")

    try:
        answer = normalize_answer(answer_text)
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

    record_result(
        "Sequence Recall",
        score=correct,
        accuracy=accuracy,
        difficulty=difficulty,
        correct=correct,
        total=len(sequence),
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