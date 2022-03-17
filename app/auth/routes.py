from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource, abort
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError
from .models import User
from .serializers import UserSchema


class UserList(Resource):
    serializer = UserSchema()

    def get(self):
        users = self.serializer.dump(User.query.all(), many=True)
        return users

    def post(self):
        json_data = request.get_json()
        try:
            user = self.serializer.load(json_data)
            user.save()
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        except IntegrityError as e:
            return e.orig.args[0], HTTPStatus.CONFLICT
        return self.serializer.dump(user), HTTPStatus.CREATED


class UserDetail(Resource):
    serializer = UserSchema()

    def get_object(self, id):
        try:
            return User.query.filter_by(id=id).one()
        except NoResultFound:
            abort(HTTPStatus.NOT_FOUND, 'User not found')

    def get(self, id):
        user = self.get_object(id)
        return self.serializer.dump(user)

    def put(self, id):
        user_instance = self.get_object(id)
        json_data = request.get_json()
        try:
            user = self.serializer.load(json_data, instance=user_instance, partial=True)
            user.save()
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        except IntegrityError as e:
            return e.orig.args[0], HTTPStatus.CONFLICT
        return self.serializer.dump(user)

    def delete(self, id):
        user = self.get_object(id)
        user.delete()
        return HTTPStatus.NO_CONTENT.phrase, HTTPStatus.NO_CONTENT
