from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.db import db
from app.utils.models import BaseModel


class Role:
    ADMIN = 0
    ADVISER = 1
    CLIENT = 2


class User(BaseModel):
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, nullable=True, default=Role.CLIENT)
    username = db.Column(db.String(20), nullable=False, unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
