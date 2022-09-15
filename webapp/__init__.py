import os
from flask import Flask
from flask_cors import CORS
from .model import db
from .resource import api

basedir = os.path.dirname(os.path.abspath(__file__))


def create_app():
    database_path = os.path.join(basedir, "database.db")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        'test_dev_w4euht789'

    db.init_app(app)
    api.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    if not os.path.exists(database_path):

        with app.app_context():
            db.create_all()

            fill_with_temp_data()

    return app


def fill_with_temp_data():

    from .model import User, Project
    
    admin = User(email='admin', password_hash='pbkdf2:sha256:260000$Pp4idTDrJOLVqDZd$3f8c79885629e93898590c06fecf580d3719f279820546731fad360ab0acffdd', role='admin user')
    user = User(email='guest@example.com', password_hash='pbkdf2:sha256:260000$gEtVMz8RFtL3Fo9e$72206a21f7a22277216103ae359f5784a05f357b8cf01b7f1b46c79f9eee8ff0', role='user')
    proj = Project(name='Hello Python!', user=admin)

    db.session.add(admin)
    db.session.add(user)
    db.session.add(proj)

    db.session.commit()