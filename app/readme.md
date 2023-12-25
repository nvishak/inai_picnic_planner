The project is using fastapi for the backend server.
I have used poetry for the package management. 

To Setup poetry
python3 -m pip install poetry 

Alembic is used to manage the revision.
the database configuration has to be updated in two places in the project.
alembic/env.py // get_url method
app/core/config.py //SQLALCHEMY_DATABASE_URI

Create a database and update the configs in above mentioned files. 

to set up the table run the following command
poetry run alembic upgrade head

This will create all the tables required for the project.

The app can be started by running: 
poetry run uvicorn app.main:app --reload 

--reload is used for hot reload can be skipped if not required. 

Though process for the porject was: 
Problem statemnt was to create an app which can be used to determin and plan picnic location based on weather data. 
Location data is coming from the below mentioned url: 
https://open-meteo.com/en/docs

I have used two tables essentially to manage the weather and location data. 
I have used h3 library to manage the geospatial aspect of the data.
I have used index 9 and index 5. Which cover 26 Acre and 62493.90435058099 Acre area.
The location table has to be prefilled with location data as in country, state, district, zipcode, locality. Once single h9 can conver atleast 3-5 locality based on the are of the place and weather don't tend to defer to change based on the area of a h9. 
This is used to avaoid duplication of data on lat, long level as it would create issues in scaling up of the project on a global scale. 
h5_index and h9_index can be used to partition later on along with the country column to do sharing on the table.
The weather data follows same principal but has two added column of date and hour of the day. 
An ideal scenario of the project would be to trigger the celery task on a daily basics and added the 7th day data to the table and to delete data of 7 days prior as historic data won't be useful for planning purposes.
I have added few varaible from the weather api which can be further extended to add more support. Alembic will help us with the adding migration to the database and to maintain consistent state of the table schema. 

