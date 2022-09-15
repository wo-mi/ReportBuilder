from datetime import datetime, timezone, timedelta
from flask import g, current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import check_password_hash
from .model import User
import jwt


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
auth = MultiAuth(basic_auth, token_auth)


@basic_auth.get_user_roles
def get_user_roles(user):
    return user.roles

@token_auth.get_user_roles
def get_user_roles(user):
    return user.roles

@basic_auth.verify_password
def verify_password(email_or_token, password):
    user = User.get_user_by_email(email_or_token)
    if user is not None and check_password_hash(user.password_hash, password):
        g.user = user
        return user
    else:
        return False

@token_auth.verify_token
def verify_auth_token(token):
    try:
        secret = current_app.config['SECRET_KEY']
        data = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidSignatureError:
        return False
    except Exception:
        return False
    
    user = User.query.get(data['id'])
    
    if user is not None:
        g.user = user
        return user
    
    return False

def auth_token(user, duration = 60):
    expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=duration)   
    
    payload = { 'id': user.id, "exp": expiration}
    secret = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, secret, algorithm="HS256")

    return token