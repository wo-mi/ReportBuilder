import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .model import db
from .resources.user import ApiUser, ApiUsers
from .resources.project import ApiProject, ApiProjects
from .resources.token import ApiToken
from .resources.config import ApiConfig
from .resources.file import ApiFile, ApiFiles
from .resources.admin import ApiAdmin

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

    if not os.path.exists(database_path):
        with app.app_context():
            db.create_all()
            add_temp_admin()


    CORS(app, resources={r"/api/*": {"origins": "*"}})

    api = Api()
    api.add_resource(ApiToken,    '/api/token/')
    api.add_resource(ApiAdmin,    '/api/admin/')
    api.add_resource(ApiUsers,    '/api/users/')
    api.add_resource(ApiUser,     '/api/users/<int:user_id>')
    api.add_resource(ApiProjects, '/api/projects/')
    api.add_resource(ApiProject,  '/api/projects/<int:project_id>')
    api.add_resource(ApiConfig,   '/api/projects/<int:project_id>/config/')    
    api.add_resource(ApiFiles,    '/api/projects/<int:project_id>/files/')
    api.add_resource(ApiFile,     '/api/projects/<int:project_id>/files/<int:file_id>')
    api.init_app(app)

    return app


def add_temp_admin():
    from .model import User
    admin = User(email='admin', password_hash='pbkdf2:sha256:260000$Pp4idTDrJOLVqDZd$3f8c79885629e93898590c06fecf580d3719f279820546731fad360ab0acffdd', role='admin user')
    db.session.add(admin)
    db.session.commit()