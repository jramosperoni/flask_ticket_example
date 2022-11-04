from flask import request
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, current_user
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import HTTPException, Unauthorized
from app import authorize
from .models import Ticket, Message
from .serializers import TicketSchema, MessageSchema


class TicketList(Resource):
    serializer = TicketSchema()

    @jwt_required()
    def get(self):
        queryset = Ticket.query
        if authorize.has_role('Client'):
            queryset = queryset.filter_by(owner_id=current_user.id)
        tickets = self.serializer.dump(queryset.all(), many=True)
        return tickets

    @jwt_required()
    @authorize.create(Ticket)
    def post(self):
        json_data = request.get_json()
        try:
            ticket = self.serializer.load(json_data)
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        ticket.save()
        return self.serializer.dump(ticket), HTTPStatus.CREATED


class TicketDetail(Resource):
    serializer = TicketSchema()

    def get_object(self, id, permission=None):
        try:
            ticket = Ticket.query.filter_by(id=id).one()
            if permission and not getattr(authorize, permission)(ticket)\
                    or authorize.has_role('Client') and ticket.owner_id != current_user.id:
                raise Unauthorized
            return ticket
        except NoResultFound:
            abort(HTTPStatus.NOT_FOUND)

    @jwt_required()
    def get(self, id):
        ticket = self.get_object(id, 'read')
        return self.serializer.dump(ticket)

    @jwt_required()
    def put(self, id):
        ticket_instance = self.get_object(id, 'update')
        json_data = request.get_json()
        try:
            ticket = self.serializer.load(json_data, instance=ticket_instance)
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        ticket.save()
        return self.serializer.dump(ticket)

    @jwt_required()
    def delete(self, id):
        ticket = self.get_object(id, 'delete')
        ticket.delete()
        return HTTPStatus.NO_CONTENT.phrase, HTTPStatus.NO_CONTENT


class MessageList(Resource):
    serializer = MessageSchema()

    def get(self):
        messages = self.serializer.dump(Message.query.all(), many=True)
        return messages

    def post(self):
        json_data = request.get_json()
        try:
            message = self.serializer.load(json_data)
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        message.save()
        return self.serializer.dump(message), HTTPStatus.CREATED


class MessageDetail(Resource):
    serializer = MessageSchema()

    def get_object(self, id):
        try:
            return Message.query.filter_by(id=id).one()
        except NoResultFound:
            abort(HTTPStatus.NOT_FOUND)

    def get(self, id):
        ticket = self.get_object(id)
        return self.serializer.dump(ticket)

    def put(self, id):
        message_instance = self.get_object(id)
        json_data = request.get_json()
        try:
            message = self.serializer.load(json_data, instance=message_instance)
        except ValidationError as e:
            return e.messages, HTTPStatus.BAD_REQUEST
        message.save()
        return self.serializer.dump(message)

    def delete(self, id):
        message = self.get_object(id)
        message.delete()
        return HTTPStatus.NO_CONTENT.phrase, HTTPStatus.NO_CONTENT
