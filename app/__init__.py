import os

from flask import Flask, redirect, request, session, url_for

from app.extensions import db
from app.localization import get_active_language, translate_text


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, "dementia_care.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.before_request
    def set_default_language():
        session.setdefault("lang", "as")
        session["lang"] = get_active_language(session.get("lang"))

    @app.context_processor
    def inject_translation_helpers():
        def t(key, **kwargs):
            text = translate_text(key, session.get("lang", "as"))
            for placeholder, value in kwargs.items():
                text = text.replace(f"{{{{{placeholder}}}}}", str(value))
            return text

        return {
            "t": t,
            "current_lang": get_active_language(session.get("lang", "as")),
            "session": session,
        }

    @app.route("/set_language/<lang>", methods=["POST"])
    def set_language(lang):
        if lang in {"en", "as"}:
            session["lang"] = lang
        return redirect(request.referrer or url_for("main.home"))

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app.routes.sequence_recall import games
    from app.routes.shopping_memory import shopping_memory
    from app.routes.picture_recall import picture_recall
    from app.routes.results import results

    app.register_blueprint(games)
    app.register_blueprint(shopping_memory)
    app.register_blueprint(picture_recall)
    app.register_blueprint(results)

    from app.routes.caregiver import caregiver
    app.register_blueprint(caregiver)

    from app.routes.sequence_recall import sequence_recall
    app.register_blueprint(sequence_recall)

    from app.routes.patient import patient
    app.register_blueprint(patient)

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app