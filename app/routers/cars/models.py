from typing import Union, Dict, List

from app.database_execute import execute_query
from app.routers.cars.schemas import GetAdminCarRequest, UpdateCarDataRequest, GetAvailableCarsRequest, \
    AddCarDataRequest
from app.routers.cars.services import create_user_car_query, create_admin_car_query


class Cars:
    @staticmethod
    def create(data: AddCarDataRequest) -> None:
        execute_query(
            f"""INSERT INTO rental_car.cars (license_plate, status, car_type) VALUES (%s, %s, %s);""",
            (data.license_plate, data.status, data.car_type)
        )

    @staticmethod
    def get(data: GetAvailableCarsRequest) -> List[Dict[str, str]]:
        return execute_query(
            create_user_car_query(data),
            fetch_all=True
        )

    @staticmethod
    def update(data: UpdateCarDataRequest) -> None:
        execute_query(
            """UPDATE rental_car.cars SET status = %s WHERE id = %s""",
            (data.status, data.id)
        )

    @staticmethod
    def delete(car_id: Union[int, str]) -> None:
        execute_query(f"DELETE FROM rental_car.cars WHERE id = %s", car_id)

    @staticmethod
    def get_all_cars(data: GetAdminCarRequest) -> List[Dict[str, str]]:
        return execute_query(
            create_admin_car_query(data),
            fetch_all=True
        )
