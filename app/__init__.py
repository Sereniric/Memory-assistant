from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"

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

    return app