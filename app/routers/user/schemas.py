from pydantic import BaseModel, constr


class UpdateUserDataRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: constr(min_length=8, max_length=16)
