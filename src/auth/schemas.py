from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    login: str
    name: str | None = None

class UserCreate(UserBase):
    password: str


class UserInDB(UserCreate):
    hashed_password: str