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
fig1.update_layout(
    title_text=f"Graph 5: {selected_hemisphere} sea ice {selected_variable.lower()}, 12 month moving average"
)
# Set x-axis title
fig1.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig1.update_yaxes(title_text=f"{selected_variable} (km<sup>2</sup>)")
st.plotly_chart(fig1, use_container_width=True)
st.caption("""Graph 4: Climate model ensemble annual global average temperature quantiles for four different scenarios 
    from year 1850 to year 2100. 
    For each of the three scenarios [SSP1-2.6](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways), 
    [SSP2-4.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) and 
    [SSP5-8.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) each model outputs forecast based on 
    parameters governed by assumptions about socioeconomic factors in the future as well as physical quantities.
    Each model also outputs estimation of historical global average temperatures based on physical quantities
    as well as data from past atmospheric records and proxies. The instrumental record is shown for comparison.""")