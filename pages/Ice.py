import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from get_data import (
    get_sea_ice_data
)

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Climate Past and Future',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)
col1, col2 = st.columns(2)

with col1:
    selected_hemisphere = st.selectbox("Choose a hemisphere:", ['Northern hemisphere', 'Southern hemisphere'])
with col1:
    selected_variable = st.selectbox("Choose a variable:", ['Extent', 'Area'])

fig1 = make_subplots()

df = get_sea_ice_data()

# Add traces
fig1.add_trace(
    go.Scatter(x=df.loc[df['region'] == selected_hemisphere[0], 'date'], \
        y=df.loc[df['region'] == selected_hemisphere[0], selected_variable.lower()]*1000000, 
        name=selected_variable,
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Date: %{x|%Y-%B}',
        line=dict(color='blue'))
)