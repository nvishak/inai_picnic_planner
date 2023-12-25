from typing import Optional

from pydantic import BaseModel


# Shared properties
class LocationBase(BaseModel):
    country: str
    state: str 
    district: str 
    city: str 
    zipcode: str 
    locality: str 
    centroid_latitude: float
    centroid_longitude: float
    h9_index: int
    h5_index: int


# Properties to receive on Location creation
class LocationCreate(LocationBase):
    pass


# Properties to receive on Location update
class LocationUpdate(LocationBase):
    pass


# Properties shared by models stored in DB
class LocationInDBBase(LocationBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Location(LocationInDBBase):
    pass


# Properties properties stored in DB
class LocationInDB(LocationInDBBase):
    pass
