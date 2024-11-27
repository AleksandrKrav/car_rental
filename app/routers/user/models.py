from typing import Dict

from app.database_execute import execute_query
from app.routers.registration.schemas import UserRegistrationRequest
from app.routers.user.schemas import UpdateUserDataRequest


class Users:
    @staticmethod
    def create(data: UserRegistrationRequest) -> None:
        execute_query(
            """INSERT INTO rental_car.users (first_name, last_name, email, password, role)
             VALUES (%s, %s, %s, %s, %s); """,
            (data.first_name, data.last_name, data.email, data.password, 'client')
        )

    @staticmethod
    def get(user_id: int) -> Dict[str, str]:
        return execute_query("""SELECT * FROM rental_car.users WHERE id = %s;""", user_id, fetch_one=True)

    @staticmethod
    def update(data: UpdateUserDataRequest, user_id: int) -> None:
        execute_query(
            """UPDATE rental_car.users SET first_name = %s, last_name = %s,
             password = %s WHERE id = %s""",
            (data.first_name, data.last_name, data.password, user_id)
        )

    @staticmethod
    def delete(user_id: int) -> None:
        execute_query("DELETE FROM rental_car.users WHERE id = %s", user_id)
