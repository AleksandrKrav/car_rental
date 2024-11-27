from functools import wraps
from http import HTTPStatus

from flask import session, jsonify


def auth_validator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'msg': "Not auth."}), HTTPStatus.UNAUTHORIZED
        return f(*args, **kwargs)
    return decorated_function


def admin_validator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'msg': "Not auth."}), HTTPStatus.UNAUTHORIZED
        if session['user']['role'] != 'admin':
            return jsonify({'msg': 'User is not an admin'}), HTTPStatus.FORBIDDEN
        return f(*args, **kwargs)
    return decorated_function
