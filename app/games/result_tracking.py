from datetime import datetime, timezone

from flask import session


RESULTS_SESSION_KEY = "game_results"


def record_result(game_name, score, accuracy, difficulty, **details):
    """Save one completed game round in the current user's session."""
    results = session.get(RESULTS_SESSION_KEY, [])

    result = {
        "game": game_name,
        "score": score,
        "accuracy": round(float(accuracy), 2),
        "difficulty": difficulty,
        "completed_at": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
    }
    result.update(details)

    results.append(result)
    session[RESULTS_SESSION_KEY] = results

    return result


def get_results():
    """Return completed game rounds, newest result last."""
    return session.get(RESULTS_SESSION_KEY, [])
