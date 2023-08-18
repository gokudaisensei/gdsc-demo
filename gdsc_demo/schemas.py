from pydantic import BaseModel

from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: float
    description: str


class ProductDB(ProductBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Product(ProductDB):
    pass


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserDBBase:
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserDBBase):
    pass


class UserDB(UserDBBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
