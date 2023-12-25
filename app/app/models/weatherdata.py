from typing import Union
from datetime import date
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Shared properties
class WeatherdataBase(SQLModel):
    h5_index:int = Field(index=True)
    h9_index:int = Field(index=True)
    date:date = Field(index=True)
    hour_of_the_day: str = Field(index=True)
    temperature_2m:float
    apparent_temperature:float
    precipitation_probability:float
    rain:float
    cloud_cover:float

# Properties to receive on Weatherdata creation
class WeatherdataCreate(WeatherdataBase):
    pass


# Properties to receive on Weatherdata update
class WeatherdataUpdate(WeatherdataBase):
    pass


# Database model, database table inferred from class name
class Weatherdata(WeatherdataBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)

    

# Properties to return via API, id is always required
class WeatherdataOut(WeatherdataBase):
    id: int
    