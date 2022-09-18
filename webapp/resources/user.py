from flask_restful import Resource, fields, marshal_with, reqparse, abort
from ..model import db, User
from ..auth import auth
from werkzeug.security import generate_password_hash


user_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'role': fields.String
}

class ApiUsers(Resource):
    @auth.login_required(role='admin')   
    @marshal_with(user_resource_fields)
    def get(self):
        users = User.query.all()
        return users

    @auth.login_required(role='admin')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',required=True, help="Email cannot be blank!", location='json')
        parser.add_argument('password',required=True, help="Password cannot be blank!", location='json')
        parser.add_argument('role', location='json')
        args = parser.parse_args()

        email = args['email']
        password = args['password']
        role = args['role']

        if User.get_user_by_email(email) is not None:
            abort(404, message="A user with that username already exists")

        user = User(email=email,
                    password_hash=generate_password_hash(password),
                    role=role)

        db.session.add(user)
        db.session.commit()

        return {"message": "success"}


class ApiUser(Resource):
    @auth.login_required(role='admin')
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user
        
    @auth.login_required(role='admin')
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "success"}

