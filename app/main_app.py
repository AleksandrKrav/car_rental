from http import HTTPStatus
from typing import Tuple

from celery import Celery
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from app import routers
from config import SWAGGER_URL, API_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, FLASK_SECRET_KEY


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery


def create_app() -> Tuple[Flask, Celery]:
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
    app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND

    app.secret_key = FLASK_SECRET_KEY

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Car Rental API"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(routers.main_bp)

    @app.errorhandler(Exception)
    def handle_exception(error):
        if hasattr(error, 'code') and hasattr(error, 'description'):
            return jsonify({'error': error.description}), error.code
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), HTTPStatus.INTERNAL_SERVER_ERROR

    return app, make_celery(app)
