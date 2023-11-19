-- How many distinct weather conditions were observed (rain/snow/clear/…) in a certain period?
SELECT COUNT(DISTINCT(weather_condition)) AS distinct_weather_conditions FROM climate_condition WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00';

-- Can you rank the most common weather conditions in a certain period of time per city?
SELECT city.name AS city_name, climate_condition.weather_condition AS weather_condition, RANK() OVER (PARTITION BY city.name ORDER BY weather_condition) AS weather_condition_rank FROM city INNER JOIN climate_condition ON city.city_id = climate_condition.city_id WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00' GROUP BY climate_condition.city_id, climate_condition.weather_condition ORDER BY climate_condition.city_id;

-- What are the temperature averages observed in a certain period per city?
SELECT city.name AS city_name, AVG(temperature.temperature_c) AS avg_temperature_c FROM city INNER JOIN temperature ON city.city_id = temperature.city_id WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00' GROUP BY temperature.city_id ORDER BY avg_temperature_c DESC;

-- What city had the highest absolute temperature in a certain period of time?
SELECT city.name AS city_name, MAX(ABS(temperature.temperature_c)) AS max_abs_temperature_c FROM city INNER JOIN temperature ON city.city_id = temperature.city_id WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00' GROUP BY temperature.city_id ORDER BY max_abs_temperature_c DESC LIMIT 1;

-- Which city had the highest daily temperature variation in a certain period of time?
SELECT city.city_id AS city_id, city.name AS city_name, DATE(temperature.date) AS date, FORMAT(STD(temperature.temperature_c), 2) AS daily_temp_variation FROM city INNER JOIN temperature ON city.city_id = temperature.city_id WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00' GROUP BY city_id, city_name, DATE(temperature.date) ORDER BY daily_temp_variation DESC LIMIT 1;

-- What city had the strongest wind in a certain period of time?
SELECT city.name AS city_name, MAX(climate_condition.wind_speed) AS max_wind_speed FROM city INNER JOIN climate_condition ON city.city_id = climate_condition.city_id WHERE date > '2023-11-18 01:00:00' AND date < '2023-11-19 18:00:00' GROUP BY climate_condition.city_id ORDER BY max_wind_speed DESC LIMIT 1;
