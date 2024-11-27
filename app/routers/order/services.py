from app.exceptions import BadRequestError
from app.routers.cars.models import Cars
from app.routers.cars.schemas import GetAvailableCarsRequest
from app.routers.order.models import Orders, Payments
from app.routers.order.schemas import CreateOrder
from app.routers.user.models import Users
from app.tasks import send_email_task


def create_order(user_id: int, data: CreateOrder) -> None:
    Orders.create(user_id, data)
    order_data = Orders.get_by_user_id(user_id)
    data = GetAvailableCarsRequest(id=data.car_id)
    car_data = Cars.get(data)[0]

    try:
        if not car_data:
            raise BadRequestError('Car id not valid')
        if car_data['status'] != 'READY_TO_GO':
            raise BadRequestError('Bad car status')

        Payments.create(order_data['id'], order_data['price'])
        Orders.update_payment_status(order_data['id'])
        user_data = Users.get(user_id)

        send_email_task.delay("Order details", [user_data['email']], 'Order complete')
    except Exception as e:
        Orders.delete(order_data['id'])
        raise BadRequestError(e)
