from .routes import UserList, UserDetail


def init_app(api):
    api.add_resource(UserList, '/users/')
    api.add_resource(UserDetail, '/users/<int:id>')
