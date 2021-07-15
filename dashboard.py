import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components

from make_plots import plotly_plot
from db_interface import get_db_connection, load_dataset
from queries import dashboard_queries

st.set_page_config(layout="wide")

def load_datasets(connection):
    data = []
    for entry in dashboard_queries:
        df = load_dataset(entry['query'], entry['dtype'], connection)
        data.append(df)
    return data

host    =st.secrets['pg_host']
database=st.secrets['pg_dbname']
user    =st.secrets['pg_user']
password=st.secrets['pg_pass']
port    =st.secrets['pg_port']

# Cache a database connection. Connection parameters taken from secrets
db_connection = get_db_connection(host, database, user, password, port)

plot_types = (
#    "Scatter",
#    "Histogram",
    "Bar",
    "Line",
#    "3D Scatter",
) 

libs = (
#    "Matplotlib",
#    "Seaborn",
    "Plotly Express",
#    "Altair",
#    "Pandas Matplotlib",
    "Bokeh",
)

dictionary = {
    "key": "Value",
    "key2": "Value2"
}

#st.write(dictionary)

st.sidebar.write("Controls")

df = pd.DataFrame(
    np.random.randn(50, 20), 
    columns=('col %d' % i for i in range(20)))

#st.dataframe(df)

#st.image("https://cdn.mos.cms.futurecdn.net/BQwukuZwwwXrg27B9Le2Q6-970-80.png.webp")

option = st.sidebar.selectbox("Select a Dashboard", ("Community", "ZilSwap", "Adhoc"), 0)

if option == "Community":
    with st.beta_container():
        st.title("Zilliqa Community Dashboard")
        st.write("""Visualizing ecosystem growth since inception.""")

    #ticker = st.sidebar.text_input("Ticker","TSLA", 5)
    columns = st.beta_columns(2)

    col_data = [ dashboard_queries[:len(dashboard_queries)//2], dashboard_queries[len(dashboard_queries)//2:] ]

    for col, data in zip(columns, col_data):
        with col:
            for entry in data:
                st.subheader(entry['name'])
                df = load_dataset(entry['query'], entry['dtype'], db_connection)
                fig = plotly_plot(entry["chart"], df, entry['x'], entry['y'], entry['name'], entry['color'])
                st.plotly_chart(fig, use_container_width=True)

if option == "ZilSwap":
    st.subheader("ZilSwap Dashboard")

if option == "Adhoc":
    st.subheader("Adhoc Query Dashboard")

