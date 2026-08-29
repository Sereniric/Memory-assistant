from flask import Blueprint, render_template

from app.games.result_tracking import get_results


results = Blueprint("results", __name__, url_prefix="/game/results")


@results.route("/")
def history():
    return render_template(
        "games/results.html",
        results=get_results(),
    )