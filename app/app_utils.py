import mysql.connector
import streamlit as st


def connection():
    return mysql.connector.connect(
        **st.secrets["weather-db"]
    )


def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
