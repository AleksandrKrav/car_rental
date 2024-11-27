from flask import Blueprint
from app.routers.registration.endpoints import registration_bp
from app.routers.user.endpoints import user_bp
from app.routers.order.endpoints import order_bp
from app.routers.cars.endpoints import cars_bp
from app.routers.admin.endpoints import admin_bp

main_bp = Blueprint('main', __name__)

main_bp.register_blueprint(registration_bp, url_prefix='/auth')
main_bp.register_blueprint(user_bp, url_prefix='/user')
main_bp.register_blueprint(order_bp, url_prefix='/order')
main_bp.register_blueprint(cars_bp, url_prefix='/cars')
main_bp.register_blueprint(admin_bp, url_prefix='/admin')
