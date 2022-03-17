from datetime import datetime
from app.db import db
from app.utils.models import BaseModel


class Priority:
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Ticket(BaseModel):
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=Priority.LOW)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


class Message(BaseModel):
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', name='fk_message_ticket_id'))
    ticket = db.relationship('Ticket', foreign_keys=[ticket_id], backref=db.backref('messages', lazy='dynamic'))
    text = db.Column(db.String(200), nullable=False)
