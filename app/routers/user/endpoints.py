from http import HTTPStatus

from flask import Blueprint, jsonify, session
from flask_pydantic import validate

from app.decorators import auth_validator
from app.routers.user.models import Users
from app.routers.user.schemas import UpdateUserDataRequest

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
@auth_validator
def get_user_data():
    user_data = Users.get(session['user']['id'])

    if not user_data:
        return jsonify({'message': 'User not found'}), HTTPStatus.BAD_REQUEST

    return jsonify(user_data), HTTPStatus.OK


@user_bp.route('/', methods=['PUT'])
@validate()
@auth_validator
def update_user_data(body: UpdateUserDataRequest):
    Users.update(body, session['user']['id'])
    return jsonify({"message": "User data updated successfully"}), HTTPStatus.OK


@user_bp.route('/', methods=['DELETE'])
@auth_validator
def delete_user():
    Users.delete(session['user']['id'])
    # remove user from web session
    session.pop('', None)
    return jsonify({"message": "User deleted successfully"}), HTTPStatus.OK
