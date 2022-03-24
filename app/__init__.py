from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask.cli import AppGroup
from http import HTTPStatus

api = Api()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_name=None):
    from config import config
    from app import db, auth, login, ticket

    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    auth.init_app(api)
    login.init_app(api)
    ticket.init_app(api)

    @app.route('/')
    def index():
        return {
            'status': 'OK'
        }

    @jwt.unauthorized_loader
    def unauthorized_callback(e):
        return jsonify({'message': e}), HTTPStatus.UNAUTHORIZED

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({'message': 'Expired Access Token'}), HTTPStatus.UNAUTHORIZED

    db_cli = AppGroup('db')

    @db_cli.command('create_all')
    def create_all():
        from app.db import db
        with app.app_context():
            db.drop_all()
            db.create_all()

    app.cli.add_command(db_cli)

    return app
