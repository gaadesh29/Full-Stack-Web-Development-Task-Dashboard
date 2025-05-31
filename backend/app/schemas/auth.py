from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(UserLogin):
    name: str 