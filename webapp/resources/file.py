from flask import g
from flask_restful import Resource, reqparse, abort
from ..model import db
from ..auth import auth
from ..upload import save_file
from werkzeug import datastructures


class ApiFiles(Resource):
    @auth.login_required
    def post(self, project_id):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()
        uploaded_file = args['file']

        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(404, message="Incorect project id")

        for file in project.files:
            if file.name == uploaded_file.filename:
                abort(400, message="File name already exists")

        if not save_file(project, uploaded_file):
            return abort(400, message="Incorrect file")
        
        return {"message": "success"}


class ApiFile(Resource):
    @auth.login_required
    def delete(self, project_id, file_id):
        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(404, message="Incorect project id")

        if file_id>0 and file_id <= len(project.files):
            file = project.files[file_id-1]
        else:
            abort(404, message="Incorect file id")
        
        file.remove_upload()
        db.session.delete(file)
        db.session.commit()
        
        return {"message": "success"}
        