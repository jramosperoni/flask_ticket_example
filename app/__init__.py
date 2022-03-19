from flask import Flask
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask.cli import AppGroup

api = Api()
ma = Marshmallow()


def create_app(config_name=None):
    from config import config
    from app import db, auth, ticket

    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    auth.init_app(api)
    ticket.init_app(api)

    @app.route('/')
    def index():
        return {
            'status': 'OK'
        }

    db_cli = AppGroup('db')

    @db_cli.command('create_all')
    def create_all():
        from app.db import db
        with app.app_context():
            db.drop_all()
            db.create_all()

    app.cli.add_command(db_cli)

    return app
