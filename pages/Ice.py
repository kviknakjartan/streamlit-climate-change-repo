import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
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
with col2:
    selected_variable = st.selectbox("Choose a variable:", ['Extent', 'Area'])

fig1 = make_subplots()

df = get_sea_ice_data()
x = df.loc[df['region'] == selected_hemisphere[0], 'date']
y = df.loc[df['region'] == selected_hemisphere[0], selected_variable.lower()]*1000000

# Add traces
fig1.add_trace(
    go.Scatter(x=x,
        y=y, 
        name=selected_variable,
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Date: %{x|%Y-%B}',
        line=dict(color='blue'))
)
fig1.add_trace(
    go.Scatter(x=x,
        y=df.loc[df['region'] == selected_hemisphere[0], f'ma_{selected_variable.lower()}']*1000000, 
        name="12 month moving average",
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Date: %{x|%Y-%B}',
        line=dict(color='red'))
)

# Generate a trendlince
t = (x.dt.to_period('M') - x[0].to_period('M')).apply(lambda x: x.n)
# Coefficients: [slope, intercept]
coefficients = np.polyfit(t, y, 1)
trendline_function = np.poly1d(coefficients)
trendline_y = trendline_function(t)

fig1.add_trace(
    go.Scatter(x=x,
        y=trendline_y, 
        name="Trendline",
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Date: %{x|%Y-%B}'+
        f'<br>{coefficients[0]:.2e} * months + {coefficients[1]:.2e}',
        line=dict(color='magenta', width=0.7))
)

fig1.update_layout(
    title_text=f"Graph 5: {selected_hemisphere} sea ice {selected_variable.lower()} with 12 month moving average",
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# Set x-axis title
fig1.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig1.update_yaxes(title_text=f"{selected_variable} (km<sup>2</sup>)")
st.plotly_chart(fig1, use_container_width=True)
st.caption(f"""Graph 5: {selected_hemisphere} monthly sea Ice {selected_variable.lower()} from satelite data. 
    Also shown is the 12 month moving average.
    Sea ice extent is the total area of ocean with at least 15% sea ice concentration, while sea ice area is the actual 
    amount of ice present, accounting for the fractional coverage within each grid cell. Data from 
    [National Snow and Ice Data Center](https://nsidc.org/data/g02135/versions/4).""")