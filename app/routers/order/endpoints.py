from http import HTTPStatus

from flask import Blueprint, jsonify, session
from flask_pydantic import validate

from app.decorators import auth_validator
from app.exceptions import BadRequestError
from app.routers.order.models import Orders
from app.routers.order.schemas import CreateOrder, GetOrderByIdRequest, GetOrder
from app.routers.order.services import create_order

order_bp = Blueprint('order', __name__)


@order_bp.route('/', methods=['POST'])
@validate()
@auth_validator
def create(body: CreateOrder):
    try:
        create_order(session['user']['id'], body)
    except BadRequestError as e:
        return jsonify({'message': "Can't create order", 'error': e}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': 'Order created'}), HTTPStatus.CREATED


@order_bp.route('/all', methods=['GET'])
@validate()
@auth_validator
def get_user_orders(query: GetOrder):
    orders_data = Orders.get(session['user']['id'], query)
    return jsonify(orders_data), HTTPStatus.OK


@order_bp.route('/', methods=['GET'])
@validate()
@auth_validator
def get_user_order_by_id(query: GetOrderByIdRequest):
    order_data = Orders.get_by_id(session['user']['id'], query.order_id)
    if not order_data:
        return jsonify({'message': 'Order not found'}), HTTPStatus.NOT_FOUND
    return jsonify(order_data), HTTPStatus.OK
