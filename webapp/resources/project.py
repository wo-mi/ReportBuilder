import json
from flask import g, send_file
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from ..model import db, Project
from ..auth import auth
from ReportBuilder import Project as ReportBuilderProject


project_resource_fields = {
    'name': fields.String,
    'config': fields.String
}

class ApiProjects(Resource):
    @auth.login_required    
    @marshal_with(project_resource_fields)
    def get(self):
        projects = g.user.projects
        return projects

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="Name cannot be empty", location='json')
        parser.add_argument('config',location='json')
        args = parser.parse_args()

        name = args['name']
        config = args['config']

        for project in g.user.projects:
            if project.name == name:
                abort(404, message="Project name already exists")

        if config != "":
            try:
                config = json.dumps(json.loads(config)) 
            except ValueError as err:
                abort(404, message="Invalid json")

        project = Project(name=name,config=config)

        g.user.projects.append(project)
        db.session.commit()

        return {"message": "success"}


class ApiProject(Resource):
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
        rb_project.build_from_database(config, files)
        rb_project.merge()
        path = rb_project.save()
        rb_project.close_documents()

        return send_file(path)

        
    @auth.login_required
    def delete(self, project_id):
        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(404, message="Incorect project id")

        for file in project.files:
            file.remove_upload()
            db.session.delete(file)

        db.session.delete(project)
        db.session.commit()
        
        return {"message": "success"}