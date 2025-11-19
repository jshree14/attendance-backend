from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: int | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
