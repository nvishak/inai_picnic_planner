from typing import Optional
from datetime import date

from pydantic import BaseModel


# Shared properties
class WeatherdataBase(BaseModel):
    date: date
    hour_of_the_day:str
    temperature_2m:float
    apparent_temperature:float
    precipitation_probability:float
    rain:float
    cloud_cover:float
    h9_index: int
    h5_index: int


# Properties to receive on Weatherdata creation
class WeatherdataCreate(WeatherdataBase):
    pass


# Properties to receive on Weatherdata update
class WeatherdataUpdate(WeatherdataBase):
    pass


# Properties shared by models stored in DB
class WeatherdataInDBBase(WeatherdataBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Weatherdata(WeatherdataInDBBase):
    pass


# Properties properties stored in DB
class WeatherdataInDB(WeatherdataInDBBase):
    pass
