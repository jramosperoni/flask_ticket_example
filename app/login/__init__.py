from .routes import Login


def init_app(api):
    api.add_resource(Login, '/login/')
