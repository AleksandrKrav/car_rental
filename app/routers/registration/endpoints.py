from http import HTTPStatus

from flask import Blueprint, jsonify, session
from flask_pydantic import validate

from app.routers.registration.models import Auth
from app.routers.registration.schemas import UserRegistrationRequest, LoginRequest
from app.routers.user.models import Users

registration_bp = Blueprint('register', __name__)


@registration_bp.route('/registration', methods=['POST'])
@validate()
def registration(body: UserRegistrationRequest):
    Users.create(body)
    return jsonify({'message': 'User registered successfully'}), HTTPStatus.CREATED


@registration_bp.route('/login', methods=['POST'])
@validate()
def login(body: LoginRequest):
    user = Auth.login(body)

    if not user:
        return jsonify({'message': 'User not found.'}), HTTPStatus.BAD_REQUEST
    if user['password'] != body.password:
        return jsonify({'message': 'Invalid password.'}), HTTPStatus.FORBIDDEN

    session['user'] = {'id': user['id'], 'role': user['role']}
    return jsonify({'message': 'Login successful'}), HTTPStatus.OK


@registration_bp.route('/logout', methods=['POST'])
def logout():
    # removed user from web session
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), HTTPStatus.OK
