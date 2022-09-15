import os, json
from flask import g, request, jsonify, send_file
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from .model import db, User, Project
from .auth import auth, auth_token
from .upload import save_file
from werkzeug.security import generate_password_hash
from werkzeug import datastructures
from ReportBuilder import Project as ReportBuilderProject

api = Api()



user_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password_hash': fields.String,
    'role': fields.String
}

class Users(Resource):
    @auth.login_required(role='admin')   
    @marshal_with(user_resource_fields)
    def get(self):
        users = User.query.all()
        return users

    @auth.login_required(role='admin')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',required=True, help="Email cannot be blank!")
        parser.add_argument('password',required=True, help="Password cannot be blank!")
        parser.add_argument('role')
        args = parser.parse_args()

        email = args['email']
        password = args['password']
        role = args['role']

        if User.get_user_by_email(email) is not None:
            abort(409, message="A user with that username already exists")

        user = User(email=email,
                    password_hash=generate_password_hash(password),
                    role=role)

        db.session.add(user)
        db.session.commit()

        return {"message": "success"}

api.add_resource(Users, '/api/users/')




project_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'docs': fields.String,
    'config': fields.String
}

class Projects(Resource):
    @auth.login_required    
    @marshal_with(project_resource_fields)
    def get(self):
        projects = g.user.projects
        # project = Project.query.get_or_404(id)
        
        # return jsonify(projects.config)
        return projects.config

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',required=True, help="Name cannot be blank!")
        parser.add_argument('docs')
        parser.add_argument('config')
        args = parser.parse_args()

        name = args['name']
        docs = args['docs']
        config = args['config']
        project = Project(name=name,docs=docs,config=config)

        g.user.projects.append(project)
        db.session.commit()

        return {"message": "success"}

api.add_resource(Projects, '/api/projects/')




class Project(Resource):
    @auth.login_required    
    def get(self, project_id):

        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(400, message="Incorect project id")

        files = []
        for file in project.files:
            files.append((file.name,file.relative_path))
        
        config = project.config
        
        rb_project = ReportBuilderProject()
        rb_project.build_from_dir("Test project")
        rb_project.merge()
        rb_project.save()

        print(files)
        print()
        print(config)

        return send_file('test.pdf')
        # return {"message": "success"}

api.add_resource(Project, '/api/projects/<int:project_id>')




class Config(Resource):
    @auth.login_required
    def get(self, project_id):
        
        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(400, message="Incorect project id")

        return project.config

    @auth.login_required
    def post(self, project_id):

        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(400, message="Incorect project id")

        try:
            jsonData = request.get_json()            
            parsed = json.loads(jsonData)
            project.config = str(parsed)
            db.session.commit()

            return {"message": "success"}            

        except ValueError as err:
            abort(400, message="Invalid json")

api.add_resource(Config, '/api/projects/<int:project_id>/config/')



class Files(Resource):
    @auth.login_required
    def post(self, project_id):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()
        uploaded_file = args['file']

        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(400, message="Incorect project id")

        if not save_file(project, uploaded_file):
            return abort(400, message="Incorrect file")
        
        return {"message": "success"}

api.add_resource(Files, '/api/projects/<int:project_id>/files/')




class Token(Resource):
    @auth.login_required
    def get(self):
        token = auth_token(g.user)
        return { 'token': token }

api.add_resource(Token, '/api/token/')




class Admin(Resource):
    @auth.login_required(role="admin")
    def get(self):
        return "hello admin"

api.add_resource(Admin, '/api/admin/')


# class Home(Resource):
#     def get(self):
#         return {"total":"world"}

# api.add_resource(Home, '/')




