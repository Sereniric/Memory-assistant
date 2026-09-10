from flask import Blueprint, redirect, render_template, request, session, url_for

from app.models import User, ensure_default_users, get_current_user

main = Blueprint("main", __name__)


@main.route("/")
def home():
    if get_current_user() is None:
        return redirect(url_for("main.login"))

    return render_template("home.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    ensure_default_users()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_role"] = user.role

            if user.role == "caregiver":
                return redirect(url_for("caregiver.dashboard"))

            return redirect(url_for("patient.index"))

        return render_template("login.html", error="Invalid username or password.")

    current_user = get_current_user()

    if current_user is not None:
        if current_user.role == "caregiver":
            return redirect(url_for("caregiver.dashboard"))

        return redirect(url_for("patient.index"))

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))