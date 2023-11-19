import logging
import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def connection(log: bool = False) -> mysql.connector.connection.MySQLConnection:
    """
    It establishes a connection to a MySQL database.

    :param log: saves messages into the file at 'log/retriever.log' for the performed operations.
    :return: the MySQL database connection.
    """

    try:
        db_conn = mysql.connector.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            port=os.getenv('port'),
            password=os.getenv('password'),
            database=os.getenv('database')
        )
    except mysql.connector.Error as err:
        if log:
            logging.error(f'Could not establish connection to DB: {err}')
        else:
            print(f'Could not establish connection to DB: {err}')
    else:
        if log:
            logging.info('Connection to DB established successfully')
        else:
            print('Connection to DB established successfully')

        return db_conn


def run_query(conn: mysql.connector.connection.MySQLConnection, query: str, log: bool = False) -> list:
    """
    It runs a given query.

    :param conn: MySQL database connection.
    :param query: string with the query to execute.
    :param log: saves messages into the file at 'log/retriever.log' for the performed operations.
    :return: the result from the executed query.
    """

    with conn.cursor() as cur:
        try:
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            if log:
                logging.error(f'An error occurred: {e}')
            else:
                print(f'An error occurred: {e}')


def insert_query(conn: mysql.connector.connection.MySQLConnection,
                 table_name: str,
                 fields: list,
                 values: list,
                 log: bool = False):
    """
    Insert values into a table in a MySQL database.

    :param conn: MySQL database connection.
    :param table_name: name of the table to insert values into.
    :param fields: list of column names in the table.
    :param values: list of lists, each containing values for a single row.
    :param log: saves messages into the file at 'log/retriever.log' for the performed operations.
    """

    cursor = conn.cursor()

    # Prepare the placeholders for the values
    value_placeholders = ', '.join(['%s' for _ in fields])

    # Construct the SQL query
    query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({value_placeholders})"

    try:
        # Execute the query for each set of values
        cursor.executemany(query, values)

        # Commit the changes to the database
        conn.commit()
        if log:
            logging.info(f'Successfully inserted {cursor.rowcount} rows into {table_name}.')
        else:
            print(f'Successfully inserted {cursor.rowcount} rows into {table_name}.')

    except mysql.connector.Error as err:
        if log:
            logging.error(f'Error: {err}')
        else:
            print(f'Error: {err}')
        conn.rollback()

    finally:
        # Close the cursor to release resources
        cursor.close()


def save_to_parquet(filename: str, data_to_save: dict, log: bool = False):
    """
    Saves given data to a parquet file compressed with gzip.

    :param filename: name of the file.
    :param data_to_save: dictionary containing the data to save.
    :param log: saves messages into the file at 'log/retriever.log' for the performed operations.
    """

    if not os.path.isdir('data'):
        os.makedirs('data')
        logging.info(f'Created data directory.')
    if not os.path.isfile('data/response.parquet.gz'):
        response_df = pd.DataFrame(data_to_save)
        response_df.to_parquet(f'data/{filename}.parquet.gz', compression='gzip')
        logging.info(f'Saved "data/{filename}.parquet.gz" file successfully.')
    else:
        response_df = pd.read_parquet(f'data/{filename}.parquet.gz')
        data_to_add_df = pd.DataFrame(data_to_save)
        response_df = pd.concat([response_df, data_to_add_df], ignore_index=True)
        response_df.to_parquet(f'data/{filename}.parquet.gz', compression='gzip')
        logging.info(f'Updated "data/{filename}.parquet.gz" file successfully.')
