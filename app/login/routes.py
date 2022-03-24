from flask import request
from flask_restx import Resource, abort
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from sqlalchemy.exc import NoResultFound
from ..auth.models import User
from app import jwt


def get_user(username):
    try:
        return User.query.filter_by(username=username).one()
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, 'User not found')


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data['sub']
    return get_user(identity)


class Login(Resource):
    def post(self):
        json_data = request.get_json()
        user = get_user(json_data['username'])
        if user.verify_password(json_data['password']):
            return create_access_token(identity=user.username)
        else:
            return 'Invalid password', HTTPStatus.UNAUTHORIZED
