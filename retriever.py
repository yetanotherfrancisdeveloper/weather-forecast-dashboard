import json
import logging
import os
import pandas as pd
import pycountry
import requests
import schedule
import time
import yaml
from datetime import datetime
from dotenv import load_dotenv
from utils import connection, insert_query, run_query


def get_and_save_data(cities_to_retrieve: list, save_data_locally=False, filename='', log: bool = False):
    # Getting API key from .env file
    api_key = os.getenv('api_key')

    conn = connection(log=log)
    for city_info in cities_to_retrieve:
        country_alpha_2 = pycountry.countries.get(name=city_info['country']).alpha_2
        country_code = int(pycountry.countries.get(name=city_info['country']).numeric)

        # Check if the country was already inserted in the table
        is_country_code = run_query(
            conn=conn,
            query=f"SELECT * FROM country "
                  f"WHERE "
                  f"country_code = {country_code};",
            log=log
        )
        # If the country isn't in the table, add it
        if not is_country_code:
            insert_query(
                conn=conn,
                table_name='country',
                fields=['country_code', 'country', 'country_alpha_2'],
                values=[[country_code, city_info['country'], country_alpha_2]],
                log=log
            )

        # Check if the city was already inserted in the table
        is_city = run_query(
            conn=conn,
            query=f"SELECT * FROM city "
                  f"WHERE "
                  f"name = '{city_info['city']}' AND "
                  f"country_code = {country_code} AND "
                  f"state = '{city_info['state']}';",
            log=log
        )
        # If the city isn't in the table, add it
        if not is_city:
            insert_query(
                conn=conn,
                table_name='city',
                fields=['country_code', 'name', 'state'],
                values=[[country_code, city_info['city'], city_info['state']]],
                log=log
            )

        limit = 1
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?'
            f'q={city_info["city"]},{city_info["state"]},{country_alpha_2},{country_code}&limit={limit}&appid={api_key}'
        )

        geo_data = response.json()
        city_lat = geo_data[0]['lat']
        city_lon = geo_data[0]['lon']
        to_exclude = 'minutely,daily,hourly,alerts'

        # Retrieve city ID
        city_id = run_query(
            conn=conn,
            query=f"SELECT city_id FROM city "
                  f"WHERE "
                  f"name = '{city_info['city']}' AND "
                  f"country_code = {country_code} AND "
                  f"state = '{city_info['state']}';",
            log=log
        )
        city_id = city_id[0][0]

        # Check if the city's coordinates were already inserted in the table
        is_location = run_query(
            conn=conn,
            query=f"SELECT * FROM location "
                  f"WHERE "
                  f"city_id = {city_id} AND "
                  f"latitude = {city_lat} AND "
                  f"longitude = {city_lon};",
            log=log
        )
        # If the coordinates aren't in the table, add them
        if not is_location:
            insert_query(
                conn=conn,
                table_name='location',
                fields=['city_id', 'latitude', 'longitude'],
                values=[[city_id, city_lat, city_lon]],
                log=log
            )

        # Retrieve weather data
        response_weather = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?'
            f'lat={city_lat}&lon={city_lon}&units=metric&exclude={to_exclude}&appid={api_key}'
        )
        weather_data_json = response_weather.json()

        current_data = weather_data_json['current']
        current_data_weather = current_data['weather'][0]
        # Insert values into the 'climate_condition' table
        timestamp = datetime.utcfromtimestamp(current_data['dt'])
        weather_condition = current_data_weather['main']
        wind_speed = round(float(current_data['wind_speed']), 2)
        wind_deg = int(current_data['wind_deg'])
        humidity = round(float(current_data['humidity']), 2)
        clouds = round(float(current_data['clouds']), 2)
        insert_query(
            conn=conn,
            table_name='climate_condition',
            fields=['city_id', 'date', 'weather_condition', 'wind_speed', 'wind_deg', 'humidity', 'clouds'],
            values=[[city_id, timestamp, weather_condition, wind_speed, wind_deg, humidity, clouds]],
            log=log
        )

        # Insert values into the 'temperature' table
        temp_c = round(float(current_data['temp']), 2)
        feels_temp_c = round(float(current_data['feels_like']), 2)
        insert_query(
            conn=conn,
            table_name='temperature',
            fields=['city_id', 'date', 'temperature_c', 'feels_temp_c'],
            values=[[city_id, timestamp, temp_c, feels_temp_c]],
            log=log
        )

        if save_data_locally:
            data_to_save = {
                'city_id': [city_id],
                'city_name': [city_info['city']],
                'city_state': [city_info['state']],
                'city_country': [city_info['country']],
                'date': [timestamp],
                'weather_condition': [weather_condition],
                'wind_speed': [wind_speed],
                'wind_deg': [wind_deg],
                'humidity': [humidity],
                'clouds': [clouds],
                'temperature_c': [temp_c],
                'feels_temp_c': [feels_temp_c]
            }
            if not os.path.isdir('data'):
                os.makedirs('data')
            if not os.path.isfile('data/response.parquet.gz'):
                response_df = pd.DataFrame(data_to_save)
                response_df.to_parquet(f'data/{filename}.parquet.gz', compression='gzip')
            else:
                response_df = pd.read_parquet(f'data/{filename}.parquet.gz')
                data_to_add_df = pd.DataFrame(data_to_save)
                response_df = pd.concat([response_df, data_to_add_df], ignore_index=True)
                response_df.to_parquet(f'data/{filename}.parquet.gz', compression='gzip')

    conn.close()


if __name__ == '__main__':
    # Load variables from .env file
    load_dotenv()
    # Load parameters for the script
    download_params = yaml.safe_load(open(f'configs/params.yaml'))['download']
    cities = yaml.safe_load(open(f'configs/params.yaml'))['cities']
    # Configure logging to write messages to a file
    if download_params['log']:
        if not os.path.isdir('log'):
            os.mkdir('log')
        logging.basicConfig(
            filename='log/retriever.log',
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s"
        )
        logging.info('Starting scheduler')
    else:
        print('Starting scheduler')

    # Get data through the API, update the tables in the DB and save data locally (if requested) every hour
    schedule.every().hour.at(":00").do(
        get_and_save_data,
        cities_to_retrieve=cities,
        save_data_locally=download_params['save_data_locally'],
        filename=str(download_params['filename']),
        log=download_params['log']
    )
    while True:
        schedule.run_pending()
        time.sleep(1)
