import openmeteo_requests
import json
import requests_cache
import pandas as pd
from retry_requests import retry
import logging 
from logging import Logger
from sqlmodel import Session
from app.db.engine import engine
import h3

class WeatherAPI():
    
    def __init__(self) -> None:
        self.__logger__:Logger = logging.getLogger('fastapi')
        # Setup the Open-Meteo API client with cache and retry on error
        self.__cache_session__ = requests_cache.CachedSession('.cache', expire_after = 3600)
        self.__retry_session__ = retry(self.__cache_session__, retries = 5, backoff_factor = 0.2)
        self.__openmeteo__ = openmeteo_requests.Client(session = self.__retry_session__)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        self.__url__ = "https://api.open-meteo.com/v1/forecast"

    def __create_h3_index(self, lat, long, index):
        '''
        Create h3 index for inde
        '''
        hex_index =h3.geo_to_h3(lat=lat, lng=long, resolution=index) 
        return h3.string_to_h3(hex_index)

    def __process_response__(self, type, is_batch, h5_index, h9_index):
        type_temperature_2m = type.Variables(0).ValuesAsNumpy()
        type_apparent_temperature = type.Variables(1).ValuesAsNumpy()
        type_precipitation_probability = type.Variables(2).ValuesAsNumpy()
        type_rain = type.Variables(3).ValuesAsNumpy()
        type_cloud_cover = type.Variables(4).ValuesAsNumpy()
        type_data = {"datetime": pd.date_range(
        	start = pd.to_datetime(type.Time(), unit = "s"),
        	end = pd.to_datetime(type.TimeEnd(), unit = "s"),
        	freq = pd.Timedelta(seconds = type.Interval()),
        	inclusive = "left"
        )}
        type_data["temperature_2m"] = type_temperature_2m
        type_data["apparent_temperature"] = type_apparent_temperature
        type_data["precipitation_probability"] = type_precipitation_probability
        type_data["rain"] = type_rain
        type_data["cloud_cover"] = type_cloud_cover
        type_dataframe = pd.DataFrame(data = type_data)
        # convert datetime column to just date
        type_dataframe['date'] = pd.to_datetime(type_dataframe['datetime']).dt.date
        type_dataframe['hour_of_the_day'] = pd.to_datetime(type_dataframe['datetime']).dt.time
        type_dataframe['h5_index'] = h5_index
        type_dataframe['h9_index'] = h9_index        
        type_dataframe= type_dataframe.drop(columns=['datetime'], axis=1)
        
        if(is_batch == True):
            try:
                type_dataframe.to_sql('weatherdata', con=engine,if_exists='append', index=False, chunksize=500)
            except Exception as e:
                self.__logger__.error(str(e), stack_info=True)
                self.__logger__.info("Existing entries found already")

        json_res = type_dataframe.to_json(orient='records', date_format='iso')
        variable_list = json.loads(json_res)
        return variable_list
   
    def fetch_batch_data(self,latitude:float, longitude:float):
        if latitude is not None and longitude is not None:  
            params = {
    	        "latitude": latitude,
    	        "longitude": longitude,
    	        "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "rain", "cloud_cover"],
                "timezone": "auto",
                "forecast_days": 7
            }
            responses = self.__openmeteo__.weather_api(self.__url__, params=params)

            res = []

            h5_index = self.__create_h3_index(lat=latitude, long=longitude, index=5)
            h9_index = self.__create_h3_index(lat=latitude, long=longitude, index=9)

            # Process first location. Add a for-loop for multiple locations or weather models
            for response in responses:
                # Process hourly data. The order of variables needs to be the same as requested.
                hourly = response.Hourly()
                processed_response = self.__process_response__(type=hourly, is_batch=True, h5_index=h5_index, h9_index=h9_index)
                res.append({
                "Coordinates":f"{response.Latitude()}°E {response.Longitude()}°N",
                "Elevation":f"{response.Elevation()} m asl",
                "Timezone": f"{response.Timezone()} {response.TimezoneAbbreviation()}",
                "weather_varaibles":processed_response
                })
            return res
            

    def get_current_weather(self,latitude:float, longitude:float):
        '''
        Get Weather based on the current time for the given latitude and longitude
        '''
        params = {
    	    "latitude": latitude,
    	    "longitude": longitude,
    	    "current": ["temperature_2m", "apparent_temperature", "precipitation_probability", "rain", "cloud_cover"],
            "timezone": "auto",
        }

        h5_index = self.__create_h3_index(lat=latitude, long=longitude, index=5)
        h9_index = self.__create_h3_index(lat=latitude, long=longitude, index=9)
        try:
            responses = self.__openmeteo__.weather_api(self.__url__, params=params)
            res = []
            for response in responses:
                current = response.Current()
                processed_response = self.__process_response__(type=current, is_batch=False, h9_index=h9_index, h5_index=h5_index)
                res.append({
                "coordinates":f"{response.Latitude()}°E {response.Longitude()}°N",
                "elevation":f"{response.Elevation()} m asl",
                "timezone": f"{response.Timezone()} {response.TimezoneAbbreviation()}",
                "weather_varaibles":processed_response
                })
            return res
        except Exception as e:
            self.__logger__.error(str(e), stack_info=True)
            return e