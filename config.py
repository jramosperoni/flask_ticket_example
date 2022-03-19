# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Secret-Key!')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'JWT-Secret-Key!')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_INCLUDE_MESSAGE = False
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = os.environ.get('TESTING') or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = os.environ.get('TESTING') or True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = os.environ.get('DEBUG') or False
    TESTING = os.environ.get('DEBUG') or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
