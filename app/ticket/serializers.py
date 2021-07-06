from .models import Ticket, Message
from app import ma


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
