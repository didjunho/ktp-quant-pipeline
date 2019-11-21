"""Insta485 development configuration."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = "postgres://ktp:ktpiscool1!@stonks.c2kcelme0thw.us-east-1.rds.amazonaws.com:5432/stonks"

COGNITO_REGION = 'us-east-1'
COGNITO_USERPOOL_ID = 'us-east-1_2KCYSyxTd'

# optional
COGNITO_APP_CLIENT_ID = '5ca5t271qvu3j99q0qqf0qdsa6'  # client ID you wish to verify user is authenticated against
COGNITO_CHECK_TOKEN_EXPIRATION = False  # disable token expiration checking for testing purposes
COGNITO_JWT_HEADER_NAME = 'X-MyApp-Authorization'
COGNITO_JWT_HEADER_PREFIX = 'Bearer'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'mike-is-coder-boi'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
