from typing import Union

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Shared properties
class LocationBase(SQLModel):
    country: str
    state: str
    district: str
    city: str
    zipcode:str
    locality: str
    centroid_latitude:float
    centroid_longitude:float
    h9_index: int
    h5_index:int

# Properties to receive on Location creation
class LocationCreate(LocationBase):
    pass


# Properties to receive on Location update
class LocationUpdate(LocationBase):
    pass


# Database model, database table inferred from class name
class Location(LocationBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    h9_index: int = Field(index=True)
    h5_index:int = Field(index=True)
    

# Properties to return via API, id is always required
class LocationOut(LocationBase):
    id: int
    country: str
    state: str
    district: str
    city: str
    zipcode:str
    locality: str
    centroid_latitude:float
    centroid_longitude:float
    h9_index: int
    h5_index:int