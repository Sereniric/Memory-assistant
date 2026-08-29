import os

from flask import Flask

from app.extensions import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, "dementia_care.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app.routes.sequence_recall import games
    from app.routes.shopping_memory import shopping_memory
    from app.routes.picture_recall import picture_recall

    app.register_blueprint(games)
    app.register_blueprint(shopping_memory)
    app.register_blueprint(picture_recall)

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