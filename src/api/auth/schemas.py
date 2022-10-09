from pydantic import BaseModel


class RegistrationData(BaseModel):
    login: str
    password: str
    name: str


class LoginResponse(BaseModel):
    user_id: int
    access_token: str
    token_type: str = "bearer"
