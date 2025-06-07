from pydantic import BaseModel

class UserBase(BaseModel):
    login: str
    name: str | None = None

class UserCreate(UserBase):
    password: str


class UserInDB(UserCreate):
    hashed_password: str