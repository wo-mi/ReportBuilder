from flask_restful import Resource
from ..auth import auth

class ApiAdmin(Resource):
    @auth.login_required(role="admin")
    def get(self):
        return {"user":"admin"}
