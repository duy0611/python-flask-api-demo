from flask import Flask


def create_app():
    app = Flask(__name__)

    from .api import api_v1
    app.register_blueprint(api_v1)

    return app
