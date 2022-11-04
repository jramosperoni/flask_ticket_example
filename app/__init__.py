from flask import Flask, jsonify
from flask_authorize import Authorize
from flask_jwt_extended import JWTManager, current_user
from flask_restx import Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask.cli import AppGroup
from http import HTTPStatus
from werkzeug.exceptions import HTTPException, NotFound, Unauthorized


api = Api()
authorize = Authorize(current_user=lambda: current_user)
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name=None):
    from config import config
    from app import auth, login, ticket
    from app.db import db

    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    authorize.init_app(app)
    auth.init_app(api)
    login.init_app(api)
    ticket.init_app(api)

    @app.route('/')
    def index():
        return {
            'status': 'OK'
        }

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({'message': 'error'}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.errorhandler(NotFound)
    def url_not_found_handle_exception(e):
        """Url Not Found"""
        return jsonify({'message': 'error'}), HTTPStatus.NOT_FOUND

    @api.errorhandler(NotFound)
    def not_found_handle_exception(e):
        """
        Element Not Found
        """
        return {'message': 'error api'}, HTTPStatus.NOT_FOUND

    @api.errorhandler(Unauthorized)
    def unauthorized_handle_exception(e):
        """
        Permission
        """
        return {'message': 'error api'}, HTTPStatus.UNAUTHORIZED

    @jwt.invalid_token_loader
    def invalid_token_loader_callback(e):
        """Header Without JWT"""
        return jsonify({'message': e}), HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def unauthorized_callback(e):
        return jsonify({'message': e}), HTTPStatus.UNAUTHORIZED

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({'message': 'Expired Access Token'}), HTTPStatus.UNAUTHORIZED

    db_cli = AppGroup('app-db')

    @db_cli.command('create_all')
    def create_all():
        from app.db import db
        with app.app_context():
            db.drop_all()
            db.create_all()

    app.cli.add_command(db_cli)

    return app
