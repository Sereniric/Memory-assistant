from flask import Blueprint, redirect, render_template, session, url_for

from app.games.result_tracking import get_results


results = Blueprint("results", __name__, url_prefix="/game/results")


@results.route("/")
def history():
    if session.get("user_role") != "patient":
        return redirect(url_for("main.login"))

    return render_template(
        "games/results.html",
        results=get_results(),
    )