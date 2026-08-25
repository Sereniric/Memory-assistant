from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"

    from app.routes.games import games

    app.register_blueprint(games)

    return app