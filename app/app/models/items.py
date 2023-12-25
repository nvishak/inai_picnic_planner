from typing import Union

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel
from app.models import User
# Shared properties
class ItemBase(SQLModel):
    title: str
    description: Union[str, None] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: Union[str, None] = None


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    title: str
    owner_id: Union[int, None] = Field(
        default=None, foreign_key="user.id", nullable=False
    )
    owner: Union[User, None] = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int