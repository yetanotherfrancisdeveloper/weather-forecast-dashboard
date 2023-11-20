import mysql.connector
import streamlit as st


def connection():
    """
    It establishes a connection to a MySQL database.
    """
    
    return mysql.connector.connect(
        **st.secrets["weather-db"]
    )


def run_query(conn: mysql.connector.connection.MySQLConnection, query: str):
    """
    It runs a given query.

    :param conn: MySQL database connection.
    :param query: string with the query to execute.
    :return: the result from the executed query.
    """
    
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
