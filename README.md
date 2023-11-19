# Weather forecast dashboard

This repository allows to retrieve climate data through the 
[OpenWeatherMap API](https://openweathermap.org/api), save it into a MySQL database, and 
display the retrieved data on a dashboard made in [streamlit](https://streamlit.io/).

## How to run

To retrieve the data and run the dashboard you need to install the dependencies. 
You can use pipenv to create the virtual environment and install everything with 
the following command:

```shell
pipenv install
```

Use the following command to start the virtual environment with pipenv:

```shell
pipenv shell
```

Alternatively, you can use the [requirements.txt](requirements.txt) file to install 
the dependencies.

### How to retrieve the data

The data is going to be retrieved through the API referenced above.

Two scripts are used in order to retrieve the data and store it into a MySQL database:

- [create_tables.py](create_tables.py)
- [retriever.py](retriever.py)

The first script simply creates the table necessary to store the data in the database. 
You can find the schema and the DDL in the [database_info](database_info) directory.

The script [retriever.py](retriever.py) is used in order to:

- Get the data every hour through the OpenWeatherMap API
- Save the data into a MySQL database

To do this you need a **.env** file at the root level of the repository 
with the following information:

```dotenv
api_key="api_key"
# Database credentials
host="host"
port=3306
user="user"
password="password"
database="database"
```

Additionally, the script makes use of the provided [params.yaml](configs/params.yaml) 
file where you can define the following parameters:

- **save_data_locally**: whether to save the data retrieved from the API in a compressed parquet file.
  It can be True or False.
- **filename**: the name of the parquet file you want to save. This is going to be used only if 
  'save_data_locally' is set to True.
- **log**: whether to log the operations made during the script in a log file that will be saved 
  at 'log/retriever.log'. It can be True or False.
- **cities**: a list of dictionaries with the cities you want to retrieve the data from.

To run the scripts just run the shell script provided:

```shell
./run_retriever.sh
```

or

```shell
bash ./run_retriever.sh
```

Alternatively, you can run the python scripts directly in your virtual environment:

```shell
python3 create_tables.py
python3 retriever.py
```

Or if you have Windows as OS:

```shell
python create_tables.py
python retriever.py
```

### How to run the dashboard

To run the dashboard you need to add a **secrets.toml** file in the 
[app/.streamlit](app/.streamlit) directory with the following information:

```toml
[weather-db]
host="host"
port=3306
user="user"
password="password"
database="database"
```

It seems a bit redundant since this information is already added in the .env file, 
but following the streamlit documentation it seems to be the right way to do it. 
Please, suggest whether it would be better to use just the .env file or any 
other solution.

After having provided the **secrets.toml** file, run the shell script while in the 
[app](app) directory:

```shell
./run.sh
```

or

```shell
bash ./run.sh
```

Alternatively you can run the following command from the terminal in your virtual 
environment:

```shell
streamlit run Home.py --server.port=8501
```

You can obviously change the port to whatever you prefer.

#### Use docker to run the dashboard

To use docker to run the dashboard you need to build the image with the 
[dashboard.Dockerfile](dashboard.Dockerfile) provided with the following command:

```shell
docker build -t dashboard-image -f dashboard.Dockerfile .
```

Once the image is built, you can run it using the following command:

```shell
docker run -d --name dashboard-container dashboard-image
```

## Queries in SQL and python

There are questions about the data that were answered both in SQL and in python. 
The SQL queries can be found in the [data_information.sql](database_info/data_information.sql) file.

The same answers were given using python in the [data_information.py](data_information.py) 
script.

To run the python script you can simply run the following command in the terminal in 
your virtual environment:

```shell
python3 data_information.py
```

Or if you have Windows as OS:

```shell
python data_information.py
```

## Possible improvements

1. [ ] Use docker to run the scripts to retrieve the data (maybe using [cron](https://www.man7.org/linux/man-pages/man8/cron.8.html))
2. [ ] Expand the DB to be able to add data with a different granularity or additional climate information
3. [ ] Train and add a model to forecast temperature and climate conditions
4. [ ] Host both the retriever and the dashboard so that they can be easily accessed