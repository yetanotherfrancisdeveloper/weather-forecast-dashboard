import logging
import numpy as np
import os
import yaml
from utils import connection, run_query


if __name__ == '__main__':
    # Load parameters for the script
    download_params = yaml.safe_load(open(f'configs/params.yaml'))['download']
    # Establish connection with DB
    conn = connection()
    # Retrieve tables in the DB
    created_tables = run_query(
        conn=conn,
        query="SHOW TABLES;",
        log=download_params['log']
    )
    if created_tables:
        created_tables = np.concatenate(created_tables)

    newly_created_tables = []
    # Create table for countries
    if 'country' not in created_tables:
        run_query(
            conn=conn,
            query="CREATE TABLE country ( "
                  "country_code SMALLINT NOT NULL PRIMARY KEY, "
                  "country VARCHAR(255) NOT NULL, "
                  "country_alpha_2 CHAR(2) NOT NULL);",
            log=download_params['log']
        )
        newly_created_tables.append('country')
    # Create table for cities
    if 'city' not in created_tables:
        run_query(
            conn=conn,
            query="CREATE TABLE city ( "
                  "city_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                  "country_code SMALLINT NOT NULL, "
                  "name VARCHAR(255) NOT NULL, "
                  "state VARCHAR(255) NULL, "
                  "CONSTRAINT city UNIQUE (country_code, name, state));",
            log=download_params['log']
        )
        # Add foreign key
        run_query(
            conn=conn,
            query="ALTER TABLE city "
                  "ADD CONSTRAINT cities_country_foreign FOREIGN KEY(country_code) REFERENCES country(country_code);",
            log=download_params['log']
        )
        newly_created_tables.append('city')
    # Create table for location
    if 'location' not in created_tables:
        run_query(
            conn=conn,
            query="CREATE TABLE location ("
                  "location_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                  "city_id BIGINT UNSIGNED NOT NULL, "
                  "latitude DECIMAL(10, 8) NOT NULL, "
                  "longitude DECIMAL(11, 8) NOT NULL, "
                  "CONSTRAINT location UNIQUE (city_id, latitude, longitude))",
            log=download_params['log']
        )
        run_query(
            conn=conn,
            query="ALTER TABLE location "
                  "ADD CONSTRAINT location_city_id_foreign FOREIGN KEY(city_id) REFERENCES city(city_id);",
            log=download_params['log']
        )
        newly_created_tables.append('location')
    # Create table for climate conditions
    if 'climate_condition' not in created_tables:
        run_query(
            conn=conn,
            query="CREATE TABLE climate_condition ( "
                  "climate_condition_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                  "city_id BIGINT UNSIGNED NOT NULL, "
                  "date TIMESTAMP NOT NULL, "
                  "weather_condition VARCHAR(255), "
                  "wind_speed DECIMAL(8, 2), "
                  "wind_deg SMALLINT, "
                  "humidity DECIMAL(5, 2), "
                  "clouds DECIMAL(8, 2));",
            log=download_params['log']
        )
        # Add foreign key
        run_query(
            conn=conn,
            query="ALTER TABLE climate_condition "
                  "ADD CONSTRAINT climate_conditions_city_id_foreign FOREIGN KEY(city_id) REFERENCES city(city_id);",
            log=download_params['log']
        )
        newly_created_tables.append('climate_condition')
    # Create table for temperatures
    if 'temperature' not in created_tables:
        run_query(
            conn=conn,
            query="CREATE TABLE temperature ( "
                  "temperature_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                  "city_id BIGINT UNSIGNED NOT NULL, "
                  "date TIMESTAMP NOT NULL, "
                  "temperature_c DECIMAL(5, 2), "
                  "feels_temp_c DECIMAL(5, 2));",
            log=download_params['log']
        )
        # Add foreign key
        run_query(
            conn=conn,
            query="ALTER TABLE temperature "
                  "ADD CONSTRAINT temperatures_city_id_foreign FOREIGN KEY(city_id) REFERENCES city(city_id);",
            log=download_params['log']
        )
        newly_created_tables.append('temperature')

    # Print newly created tables to verify that everything went smoothly
    if newly_created_tables:
        if not os.path.isdir('log'):
            os.mkdir('log')
        logging.basicConfig(
            filename='log/retriever.log',
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s"
        )

        for table in newly_created_tables:
            logging.info(f'Created table {table}')
