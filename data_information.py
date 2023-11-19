import pandas
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=pandas.errors.SettingWithCopyWarning)


if __name__ == '__main__':
    # Load saved data from parquet
    response_data = pd.read_parquet('data/response.parquet.gz')

    print('-- How many distinct weather conditions were observed (rain/snow/clear/…) in a certain period?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 11:00:00')
        ]
    print(len(response_data_question['weather_condition'].unique()))

    print('\n-- Can you rank the most common weather conditions in a certain period of time per city?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 19:00:00')
        ]

    cities = response_data_question['city_id'].unique()
    for city in cities:
        response_data_question_city = response_data_question.loc[response_data_question['city_id'] == city]
        response_data_question_city = response_data_question_city.groupby(['city_id', 'city_name', 'weather_condition'], as_index=True)['weather_condition'].count().to_frame()
        response_data_question_city = response_data_question_city.rename(columns={'weather_condition': 'count'})
        response_data_question_city['rank'] = response_data_question_city['count'].rank(ascending=False)
        response_data_question_city = response_data_question_city.sort_values(by=['rank'], ascending=True)
        print(response_data_question_city)

    print('\n-- What are the temperature averages observed in a certain period per city?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 13:00:00')
        ]
    response_data_question = response_data_question.groupby(['city_id', 'city_name'], as_index=True)['temperature_c'].mean().to_frame()
    response_data_question = response_data_question.rename(columns={'temperature_c': 'avg_temperature_c'})
    print(response_data_question)

    print('\n-- What city had the highest absolute temperature in a certain period of time?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 13:00:00')
        ]
    response_data_question['abs_temperature_c'] = response_data_question['temperature_c'].abs()
    response_data_question = response_data_question.iloc[response_data_question['abs_temperature_c'].argmax()]['city_name']
    print(response_data_question)

    print('\n-- Which city had the highest daily temperature variation in a certain period of time?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 13:00:00')
        ]
    response_data_question['day'] = response_data_question['date'].apply(lambda x: x.date())
    response_data_question = response_data_question.groupby(by=['city_id', 'city_name', 'day'], as_index=True)['temperature_c'].std().to_frame()
    response_data_question = response_data_question.rename(columns={'temperature_c': 'daily_temperature_c_std'})
    response_data_question = response_data_question.iloc[response_data_question['daily_temperature_c_std'].argmax()].name[1]
    print(response_data_question)

    print('\n-- What city had the strongest wind in a certain period of time?')
    response_data_question = response_data.loc[
        (response_data['date'] > '2023-11-19 10:00:00') &
        (response_data['date'] < '2023-11-19 13:00:00')
        ]
    response_data_question = response_data_question.iloc[response_data_question['wind_speed'].argmax()]['city_name']
    print(response_data_question)
