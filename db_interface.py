import psycopg2
import os
import numpy as np
import pandas as pd 
import streamlit as st
import pandas.io.sql as sqlio

@st.cache(allow_output_mutation=True)
def get_db_connection(host, database, user, password, port=5432):
    # Setup the db connection using commandline parameters  
    client = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)

    return client


def run_query(query="select * from transactions limit 10", connection=None):
    '''
    Greedy query that assumes a limited number of records returned
    '''
    conn = None
    if not connection:
        conn = get_db_connection()
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        # If no connection was provided, close the local connection
        if not connection:
            conn.close()

    results = np.array(results)
    return results


def run_query_serverside(query="select * from transactions limit 10", connection=None, limit=1000):
    conn = None
    if not connection:
        conn = get_db_connection()
    results = []
    try:
        cursor = conn.cursor(name="ipython_reporting")
        cursor.execute(query)
        rows = cursor.fetchmany(limit)
        while not len(rows) == 0:
            results = results+rows
            rows = cursor.fetchmany(1000)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        # If no connection was provided, close the local connection
        if not connection:
            conn.close()

    results = np.array(results)
    return results

@st.cache(hash_funcs={psycopg2.extensions.connection : id})
def load_dataset(query, dtypes, connection=None):
    df = sqlio.read_sql_query(query, connection, dtype=dtypes)
    return df
