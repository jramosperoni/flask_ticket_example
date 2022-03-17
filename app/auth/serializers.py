from marshmallow import validate
from .models import User
from app import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'deleted', 'password', 'role', 'username')
        load_instance = True

    password = ma.String(load_only=True, required=True)
    username = ma.auto_field(validate=validate.Length(min=3))
