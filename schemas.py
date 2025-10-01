from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str = Field(... , min_length=8, max_length=72)


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class BoardBase(BaseModel):
    name: str

class BoardCreate(BoardBase):
    pass 

class Board(BoardBase):
    id: int
    user_id: int 
    model_config = ConfigDict(from_attributes=True)

class ColumnBase(BaseModel):
    name: str

class ColumnCreate(ColumnBase):
    pass 

class Column(ColumnBase):
    id: int
    board_id: int
    model_config = ConfigDict(from_attributes=True)

class CardBase(BaseModel):
    title: str
    content: Optional[str] = None
    position: int

class CardCreate(CardBase):
    pass 

class Card(CardBase):
    id: int
    column_id: int
    model_config = ConfigDict(from_attributes=True)