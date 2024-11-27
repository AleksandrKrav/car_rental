from pydantic import BaseModel, constr


class UserRegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    password: constr(min_length=8, max_length=16)
    email: str


class LoginRequest(BaseModel):
    password: constr(min_length=8, max_length=16)
    email: str
