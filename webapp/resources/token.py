from flask import g
from flask_restful import Resource
from ..auth import auth, auth_token

class ApiToken(Resource):
    @auth.login_required
    def get(self):
        token = auth_token(g.user)
        return { 'token': token }
