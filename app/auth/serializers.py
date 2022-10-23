from marshmallow import fields, validate
from .models import Role, User
from app import ma


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        fields = ('id', 'name')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'deleted', 'password', 'roles', 'username')
        load_instance = True

    password = ma.String(load_only=True, required=True)
    roles = fields.Nested(RoleSchema(many=True))
    username = ma.auto_field(validate=validate.Length(min=3))
