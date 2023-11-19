import pandas as pd
import streamlit as st
from app_utils import connection, run_query


def data_info_page():
    st.set_page_config(
        page_title='Data information',
        page_icon='images/weather-icon.png',
        layout='wide'
    )

    conn = connection()

    st.markdown('# Data information')
    st.sidebar.markdown('# Data information')
    st.sidebar.write('This page provides some more information on the data collected.')

    # Load data
    # Load temperature data
    temperature_data_rows = run_query(conn, "SELECT * FROM temperature;")
    temperature_data_columns = ['temperature_id', 'city_id', 'date', 'temperature_c', 'feels_temp_c']
    temperature_df = pd.DataFrame(data=temperature_data_rows, columns=temperature_data_columns)
    # Change type for temperatures to floats
    temperature_df['temperature_c'] = temperature_df['temperature_c'].astype(float)
    temperature_df['feels_temp_c'] = temperature_df['feels_temp_c'].astype(float)

    # Load city data
    city_data_rows = run_query(conn, "SELECT * FROM city;")
    city_data_columns = ['city_id', 'country_code', 'name', 'state']
    city_df = pd.DataFrame(data=city_data_rows, columns=city_data_columns)

    # Load climate_condition data
    climate_condition_data_rows = run_query(conn, "SELECT * FROM climate_condition;")
    climate_condition_data_columns = ['climate_condition_id', 'city_id', 'date', 'weather_condition', 'wind_speed',
                                      'wind_deg', 'humidity', 'clouds']
    climate_condition_df = pd.DataFrame(data=climate_condition_data_rows, columns=climate_condition_data_columns)
    # Change decimal types to floats
    climate_condition_df['wind_speed'] = climate_condition_df['wind_speed'].astype(float)
    climate_condition_df['humidity'] = climate_condition_df['humidity'].astype(float)
    climate_condition_df['clouds'] = climate_condition_df['clouds'].astype(float)

    # Plot average temperature per city in a given period of time
    first_available_date = climate_condition_df['date'].min()
    last_available_date = climate_condition_df['date'].max()
    d = st.date_input(
        'Select the desired period of time',
        (first_available_date, last_available_date),
        first_available_date,
        last_available_date,
    )

    st.subheader(f'Average temperature per city in the period {str(d[0])} - {str(d[1])}')
    # To correctly display data for the days selected
    second_date = d[1] + pd.Timedelta(hours=24)
    temperature_df = temperature_df.loc[(temperature_df['date'] > str(d[0])) & (temperature_df['date'] < str(second_date))]
    cities = temperature_df['city_id'].unique()
    avg_temps = []
    cities_names = []
    for city in cities:
        avg_temps.append(temperature_df.loc[temperature_df['city_id'] == city]['temperature_c'].mean())
        cities_names.append(city_df.loc[city_df['city_id'] == city].iloc[0]['name'])

    avg_temp_df = pd.DataFrame({'city': cities_names, 'avg_temperature_c': avg_temps})
    st.bar_chart(avg_temp_df, x='city', y='avg_temperature_c')

    for city in cities:
        climate_condition_df_city = climate_condition_df.loc[climate_condition_df['city_id'] == city]
        city_name = city_df.loc[city_df['city_id'] == city].iloc[0]['name']
        st.subheader(f'Wind speed for {city_name} in the period {str(d[0])} - {str(d[1])}')
        st.line_chart(climate_condition_df_city.set_index('date')[['wind_speed']])

    conn.close()


data_info_page()
