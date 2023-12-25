import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemOut, ItemUpdate
from app.businesslogics import weatherapi
from app.worker import create_weather_data
from app.crud import location
from app.schemas import Weatherdata

router = APIRouter()
logger = logging.getLogger('fastapi')

@router.get("/batch_start")
def save_batch_data(
    session: SessionDep
):
    
    """
    Store data for all locations.
    """
    location_data = location.get_all(db=session)
    task = create_weather_data.delay(location_data)
    return {"task_id": task.id}

@router.get("/current")
def get_current_weather_data(
    session: SessionDep, latitude:float, longitude: float
):
    """
    Retrieve items.
    """

    weather_obj =  weatherapi.WeatherAPI()
    res = weather_obj.get_current_weather(latitude=latitude, longitude=longitude)
    return res

@router.get("/")
def get_weather_data(
    session: SessionDep, h5_index, h9_index, date
)-> list[Weatherdata]:
   try:
        logger.info("")
        statement = select(Weatherdata)\
            .filter(Weatherdata.h5_index == h5_index, Weatherdata.h9_index == h9_index, Weatherdata.date == date)\
            .offset(0).limit(100)
        weather_data = session.exec(statement).all()
        logger.info(f"Feteche data for h5={h5_index},h9={h9_index} and date={h9_index}")
   except Exception as e:
       logger.error(str(e))
       raise HTTPException(status_code=400, detail=str(e))
   
   return weather_data