from http import HTTPStatus

from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.routers.cars.models import Cars
from app.routers.cars.schemas import GetAvailableCarsRequest

cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/', methods=['GET'])
@validate()
def get_all_available_cars(query: GetAvailableCarsRequest):
    cars_data = Cars.get(query)
    return jsonify(cars_data), HTTPStatus.OK
