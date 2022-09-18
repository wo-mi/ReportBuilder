import os, uuid
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Text)

    projects = db.relationship('Project', back_populates='user')

    @property
    def roles(self):
        return self.role.split()

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email = email).first()
        return user

    def __repr__(self):
        return f'<User {self.email}>'


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    config = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='projects')
    files = db.relationship('File', back_populates='project')

    def __repr__(self):
        return f'<Project {self.name}>'


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    uuid = db.Column(db.String(32))

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))#, nullable=False)
    project = db.relationship('Project', back_populates='files')

    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.uuid = uuid.uuid4().hex

    @property
    def relative_path(self):
        return os.path.join("webapp\\upload", self.uuid[0], self.uuid[1], self.uuid)

    def remove_upload(self):
        if os.path.exists(self.relative_path):
            os.remove(self.relative_path)

    def __repr__(self):
        return f'<File {self.name}>'
