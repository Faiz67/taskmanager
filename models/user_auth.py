from pydantic import BaseModel


class Login(BaseModel):
    user_name: str
    password: str


class Register(Login):
    email_id: str


class Logout(Login):
    pass
