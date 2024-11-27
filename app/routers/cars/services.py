from typing import Union

from app.routers.cars.schemas import GetAvailableCarsRequest, GetAdminCarRequest


def create_car_query(data: Union[GetAvailableCarsRequest, GetAdminCarRequest]) -> str:
    query_part = ""

    if data.car_type:
        query_part += f"AND car_type = '{data.car_type}'"
    if data.license_plate:
        query_part += f"AND license_plate = '{data.license_plate}'"
    if data.id:
        query_part += f"AND id = '{data.id}'"
    if data.rental_start_date and data.rental_end_date:
        query_part += """AND NOT EXISTS (
            SELECT 1
            FROM rental_car.orders o
            WHERE o.car_id = c.id
            AND (
                (o.rental_start_date < '{0}' AND o.rental_end_date > '{1}') OR
                (o.rental_start_date BETWEEN '{0}' AND '{1}') OR
                (o.rental_end_date BETWEEN '{0}' AND '{1}')
            )
        )""".format(data.rental_start_date, data.rental_end_date)

    return query_part


def create_user_car_query(data: GetAvailableCarsRequest) -> str:
    return f"""SELECT c.id, c.license_plate, c.status, c.car_type FROM rental_car.cars c 
    WHERE status = 'READY_TO_GO' {create_car_query(data)};"""


def create_admin_car_query(data: GetAdminCarRequest) -> str:
    query_part = create_car_query(data)

    if data.status:
        query_part += f"AND status = '{data.status}'"

    if query_part:
        query_part = "WHERE " + query_part[4:]

    return f"""SELECT c.id, c.license_plate, c.status, c.car_type FROM rental_car.cars c {query_part};"""
