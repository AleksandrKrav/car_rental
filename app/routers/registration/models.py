from typing import Dict

from app.database_execute import execute_query
from app.routers.registration.schemas import LoginRequest


class Auth:
    @staticmethod
    def login(data: LoginRequest) -> Dict[str, str]:
        return execute_query("""SELECT * FROM rental_car.users WHERE email = %s;""", data.email, fetch_one=True)
