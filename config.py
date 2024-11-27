import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')


class Config:
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    DEFAULT_SENDER = os.getenv('DEFAULT_SENDER')


class Database:
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE = os.getenv('DB_DATABASE')
    CURSOR_CLASS = pymysql.cursors.DictCursor
