import os
from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import db

    db.init_app(app)
    init_db(app)

    with app.app_context():
        from . import main
        app.register_blueprint(main.bp)

    return app

