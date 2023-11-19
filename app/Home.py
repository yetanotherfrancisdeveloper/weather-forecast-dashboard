import pandas as pd
import streamlit as st
from app_utils import connection, run_query

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="images/weather-icon.png",
    layout="wide"
)

conn = connection()
st.markdown('# Weather Dashboard')

st.write('This dashboard provides a visual representation of temperature history for various cities '
         'and some related KPIs.')

# Load temperature data
temperature_data_rows = run_query(conn, "SELECT * FROM temperature;")
temperature_data_columns = ['temperature_id', 'city_id', 'date', 'temperature_c', 'feels_temp_c']
temperature_df = pd.DataFrame(data=temperature_data_rows, columns=temperature_data_columns)
# Change type for temperatures to float to plot them
temperature_df['temperature_c'] = temperature_df['temperature_c'].astype(float)
temperature_df['feels_temp_c'] = temperature_df['feels_temp_c'].astype(float)

# Load city data
city_data_rows = run_query(conn, "SELECT * FROM city;")
city_data_columns = ['city_id', 'country_code', 'name', 'state']
city_df = pd.DataFrame(data=city_data_rows, columns=city_data_columns)

# Merge city and temperature data
merged_df = pd.merge(temperature_df, city_df, on='city_id', how='inner')

# Display line plots for each city
unique_cities = merged_df['city_id'].unique()

for city in unique_cities:
    city_data = merged_df[merged_df['city_id'] == city]
    city_name = city_data.iloc[0]['name']
    st.subheader(f'Temperature history for {city_name}')
    st.line_chart(city_data.set_index('date')[['temperature_c', 'feels_temp_c']])

# Close the database connection
conn.close()
