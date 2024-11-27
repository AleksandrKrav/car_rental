from datetime import timedelta, datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class GetOrder(BaseModel):
    car_type: Optional[str] = None
    rental_start_date: Optional[datetime] = None
    rental_end_date: Optional[datetime] = None


class CreateOrder(BaseModel):
    car_id: str
    price: int
    rental_start_date: datetime
    rental_end_date: datetime

    @model_validator(mode="after")
    def model_data_validator(cls, values):
        start_date = values.rental_start_date
        end_date = values.rental_end_date

        if end_date <= start_date:
            raise ValueError('rental_end_date must be after rental_start_date.')

        if end_date - start_date > timedelta(days=7):
            raise ValueError('The maximum rental period is 7 days.')

        return values


class GetOrderByIdRequest(BaseModel):
    order_id: str
