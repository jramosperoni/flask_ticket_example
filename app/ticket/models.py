from datetime import datetime
from app.db import db


class Priority:
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Ticket(BaseModel):
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=Priority.LOW)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


class Message(BaseModel):
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', name='fk_message_ticket_id'))
    ticket = db.relationship('Ticket', foreign_keys=[ticket_id], backref=db.backref('messages', lazy='dynamic'))
    text = db.Column(db.String(200), nullable=False)
