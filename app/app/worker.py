from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings

from app.businesslogics.weatherapi import WeatherAPI
from app.schemas import Location

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def create_weather_data(location_data:list[Location]):
    weatherapi_obj = WeatherAPI()
    for location in location_data:
        weatherapi_obj.fetch_batch_data(latitude=location.centroid_latitude, longitude=location.centroid_longitude)