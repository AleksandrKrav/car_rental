from http import HTTPStatus

from flask import Blueprint, jsonify
from flask_pydantic import validate

from app.decorators import admin_validator
from app.routers.cars.models import Cars
from app.routers.cars.schemas import UpdateCarDataRequest, GetAdminCarRequest, AddCarDataRequest, CarIdRequest
from app.routers.order.models import Orders

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/cars', methods=['GET'])
@validate()
@admin_validator
def get_all_cars(query: GetAdminCarRequest):
    cars_data = Cars.get_all_cars(query)
    return jsonify(cars_data), HTTPStatus.OK


@admin_bp.route('/cars', methods=['POST'])
@validate()
@admin_validator
def add_car_data(body: AddCarDataRequest):
    try:
        Cars.create(body)
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": e.args[0]}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': 'Car added successfully'}), HTTPStatus.CREATED


@admin_bp.route('/cars', methods=['PUT'])
@validate()
@admin_validator
def update_data(body: UpdateCarDataRequest):
    try:
        Cars.update(body)
        return jsonify({"message": "User data updated successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": e.args[0]}), HTTPStatus.BAD_REQUEST


@admin_bp.route('/cars', methods=['DELETE'])
@validate()
@admin_validator
def delete_car(body: CarIdRequest):
    try:
        Cars.delete(body.id)
        return jsonify({"message": "User deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": e.args[0]}), HTTPStatus.BAD_REQUEST


@admin_bp.route('/orders', methods=['GET'])
@admin_validator
def get_all_orders():
    orders_data = Orders.get_all()
    return jsonify(orders_data), HTTPStatus.OK
