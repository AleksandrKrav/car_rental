from datetime import timedelta, datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from app.constants import CAR_TYPES, CAR_STATUSES


class AddCarDataRequest(BaseModel):
    license_plate: str
    status: str = "READY_TO_GO"
    car_type: str

    @model_validator(mode="after")
    def model_data_validator(cls, values):
        car_type = values.car_type
        status = values.status

        if car_type not in CAR_TYPES:
            raise ValueError(f'Car type can be only {CAR_TYPES}')

        if status not in CAR_STATUSES:
            raise ValueError(f'Car status can be only {CAR_STATUSES}')

        return values


class CarIdRequest(BaseModel):
    id: str


class UpdateCarDataRequest(CarIdRequest):
    status: str


class GetAvailableCarsRequest(BaseModel):
    id: Optional[str] = None
    car_type: Optional[str] = None
    rental_start_date: Optional[datetime] = None
    rental_end_date: Optional[datetime] = None
    license_plate: Optional[str] = None

    @model_validator(mode="after")
    def model_data_validator(cls, values):
        car_type = values.car_type
        start_date = values.rental_start_date
        end_date = values.rental_end_date

        if start_date and end_date:
            if end_date <= start_date:
                raise ValueError('rental_end_date must be after rental_start_date.')

            if end_date - start_date > timedelta(days=7):
                raise ValueError('The maximum rental period is 7 days.')

        elif start_date or end_date:
            raise ValueError('Must be rental_start_date and rental_end_date ')

        if car_type and car_type not in CAR_TYPES:
            raise ValueError(f'Car type can be only {CAR_TYPES}')

        return values


class GetAdminCarRequest(GetAvailableCarsRequest):
    status: Optional[str] = None

    @model_validator(mode="after")
    def model_data_validator(cls, values):
        status = values.status

        if status and status not in CAR_STATUSES:
            raise ValueError(f'Car status can be only {CAR_STATUSES}')

        return values

