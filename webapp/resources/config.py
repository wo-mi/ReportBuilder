import json
from flask import g, request
from flask_restful import Resource, abort
from ..model import db
from ..auth import auth


class ApiConfig(Resource):
    @auth.login_required
    def get(self, project_id):
        
        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(404, message="Incorect project id")

        return project.config

    @auth.login_required
    def post(self, project_id):

        if project_id>0 and project_id <= len(g.user.projects):
            project = g.user.projects[project_id-1]
        else:
            abort(404, message="Incorect project id")

        try:
            jsonData = request.get_json()            
            parsed = json.dumps(json.loads(jsonData))
            project.config = str(parsed)
            db.session.commit()

            return {"message": "success"}            

        except ValueError as err:
            abort(400, message="Invalid json")
