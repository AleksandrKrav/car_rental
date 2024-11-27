from typing import Dict, List, Union

from app.database_execute import execute_query
from app.routers.order.schemas import CreateOrder, GetOrder


def get_order_query(user_id: int, data: GetOrder) -> str:
    query = f"""
       SELECT o.*
       FROM rental_car.orders o
       JOIN rental_car.cars c ON o.car_id = c.id
       WHERE user_id = '{user_id}'
    """

    if data.car_type:
        query += f"AND (c.car_type = '{data.car_type}')"
    if data.rental_end_date and data.rental_start_date:
        query += f"""AND (o.rental_start_date >= '{data.rental_start_date}' 
        AND o.rental_end_date <= '{data.rental_end_date}') AND DATEDIFF(o.rental_end_date, o.rental_start_date) 
        BETWEEN 1 AND 7"""

    return query


class Orders:
    @staticmethod
    def create(user_id: int, data: CreateOrder) -> None:
        execute_query(
            f"""INSERT INTO rental_car.orders (user_id, car_id, price, payment_status, rental_start_date,
             rental_end_date) VALUES (%s, %s, %s, FALSE, %s, %s);""",
            (user_id, data.car_id, data.price, data.rental_start_date, data.rental_end_date)
        )

    @staticmethod
    def get(user_id: int, data: GetOrder) -> List[Dict[str, str]]:
        return execute_query(
            get_order_query(user_id, data),
            fetch_all=True
        )

    @staticmethod
    def update_payment_status(order_id: Union[int, str]) -> None:
        execute_query(
            """UPDATE rental_car.orders SET payment_status = TRUE WHERE id = %s;""",
            order_id
        )

    @staticmethod
    def get_by_user_id(user_id: int) -> Dict[str, str]:
        return execute_query(
            """SELECT * FROM rental_car.orders WHERE user_id = %s ORDER BY order_date DESC LIMIT 1;""",
            user_id,
            fetch_one=True
        )

    @staticmethod
    def get_all() -> List[Dict[str, str]]:
        return execute_query("""SELECT * FROM rental_car.orders;""", fetch_all=True)

    @staticmethod
    def get_by_id(user_id: int, order_id: Union[int, str]) -> Dict[str, str]:
        return execute_query(
            """SELECT * FROM rental_car.orders WHERE user_id = %s AND id = %s;""",
            (user_id, order_id),
            fetch_one=True
        )

    @staticmethod
    def delete(order_id: Union[int, str]):
        execute_query(
            """DELETE FROM rental_car.orders WHERE id = %s;""",
            order_id
        )


class Payments:
    @staticmethod
    def create(order_id: Union[int, str], price: Union[int, str]) -> None:
        execute_query(
            """INSERT INTO rental_car.payments (order_id, amount) VALUES (%s, %s);""",
            (order_id, price)
        )
