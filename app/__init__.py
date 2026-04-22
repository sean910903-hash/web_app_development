from flask import Flask

from app.models import db
from app.routes import task_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "task-manager-secret-key"

    db.init_app(app)
    app.register_blueprint(task_bp)

    with app.app_context():
        db.create_all()

    return app
    