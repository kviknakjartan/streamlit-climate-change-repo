import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

from get_data import (
    get_sea_ice_data,
    get_ice_sheet_data,
    get_glaciers_data,
    get_snow_data
)

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Climate Change in Graphs: Ice',
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
t = (x.dt.to_period('M') - x.iloc[0].to_period('M')).apply(lambda x: x.n)
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
        line=dict(color='black', width=1))
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
st.caption(f"""Graph 5: {selected_hemisphere} monthly sea Ice {selected_variable.lower()} from satellite data. 
    Also shown are the 12 month moving average and a trendline.
    Sea ice extent is the total area of ocean with at least 15% sea ice concentration, while sea ice area is the actual 
    amount of ice present, accounting for the fractional coverage within each grid cell. Data from 
    [National Snow and Ice Data Center](https://nsidc.org/data/g02135/versions/4).""")


fig2 = make_subplots()

df = get_ice_sheet_data()

# Add traces
fig2.add_trace(
    go.Scatter(x=df.loc[df['Source'] == 'NASA - Antarctica land ice mass','Date'],
        y=df.loc[df['Source'] == 'NASA - Antarctica land ice mass','Value'] * 1000000000, 
        name='Antarctica (NASA JPL)',
        hovertemplate =
        'Value: %{y:.2e} tons'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='blue', width=1))
)
fig2.add_trace(
    go.Scatter(x=df.loc[df['Source'] == 'NASA - Greenland land ice mass','Date'],
        y=df.loc[df['Source'] == 'NASA - Greenland land ice mass','Value'] * 1000000000, 
        name='Greenland (NASA JPL)',
        hovertemplate =
        'Value: %{y:.2e} tons'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='red', width=1))
)
fig2.add_trace(
    go.Scatter(x=df.loc[df['Source'] == 'IMBIE - Antarctica cumulative mass balance','Date'],
        y=df.loc[df['Source'] == 'IMBIE - Antarctica cumulative mass balance','Value'] * 1000000000, 
        name='Antarctica (Combined data)',
        hovertemplate =
        'Value: %{y:.2e} tons'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='darkblue', width=4))
)
fig2.add_trace(
    go.Scatter(x=df.loc[df['Source'] == 'IMBIE - Greenland cumulative mass balance','Date'],
        y=df.loc[df['Source'] == 'IMBIE - Greenland cumulative mass balance','Value'] * 1000000000, 
        name='Greenland (Combined data)',
        hovertemplate =
        'Value: %{y:.2e} tons'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='darkred', width=4))
)
# Uncertainties
x = df.loc[df['Source'] == 'IMBIE - Antarctica cumulative mass balance uncertainty','Date']
y = df.loc[df['Source'] == 'IMBIE - Antarctica cumulative mass balance','Value'].reset_index(drop=True) * 1000000000
y_unc = df.loc[df['Source'] == 'IMBIE - Antarctica cumulative mass balance uncertainty','Value'].reset_index(drop=True) * 1000000000
y_lower = y - y_unc
y_upper = y + y_unc
fig2.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Antarctica uncertainty (Combined data)',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)
x = df.loc[df['Source'] == 'IMBIE - Greenland cumulative mass balance uncertainty','Date']
y = df.loc[df['Source'] == 'IMBIE - Greenland cumulative mass balance','Value'].reset_index(drop=True) * 1000000000
y_unc = df.loc[df['Source'] == 'IMBIE - Greenland cumulative mass balance uncertainty','Value'].reset_index(drop=True) * 1000000000
y_lower = y - y_unc
y_upper = y + y_unc

fig2.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Greenland uncertainty (Combined data)',
        fill='toself',
        fillcolor='rgba(255,0,0,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(255,0,0,0.2)', width=0.1))
)
fig2.update_layout(
        title_text="Graph 6: Cumulative Mass Balance of Greenland and Antarctica",
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.1  # y-position (0.9 is near top)
        )
)

# Set x-axis title
fig2.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig2.update_yaxes(title_text="Cumulative mass change (tons)")
st.plotly_chart(fig2, use_container_width=True)
st.caption("""Graph 6: Cumulative Mass Balance of Greenland and Antarctica from 1992. 
    The dark lines show combined data that is based on more than 20 different studies where data has been combined 
    over multiple region. Shading shows the uncertainty estimates that is cumulated from uncertainties calculated for each study.
    The two thin lines show data from one commonly cited analysis where seasonal variations can be seen. 
    All estimates are centered at zero in 2002. A downward slope indicates a net loss of ice and snow. 
    For reference, 1,000 billion metric tons (one Teraton) is equal to about 260 cubic miles of ice which is enough to raise sea 
    level by about 3 millimeters (IPCC, 2013 as cited in US EPA, 2021). 
    Graph adopted from [EPA](https://www.epa.gov/climate-indicators/climate-change-indicators-ice-sheets).
    Data from [EPA](https://www.epa.gov/climate-indicators/climate-change-indicators-ice-sheets).""")

df = get_glaciers_data()

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig3.add_trace(
    go.Scatter(x=df['Year'],
        y=df['Mean cumulative mass balance'],
        name="Glaciers mass balance",
        hovertemplate =
        'Value: %{y:.1f} m'+
        '<br>Year: %{x:.0f}',
        line=dict(color='blue')),
    secondary_y=False,
)
fig3.add_trace(
    go.Bar(x=df['Year'],
        y=df['Number of observations'],
        orientation='v',
        name="Number of glaciers observed",
        hovertemplate =
        'Value: %{y:.0f}'+
        '<br>Year: %{x:.0f}',
        marker=dict(
                color='rgba(255,0,0,0.2)'
    )),
    secondary_y=True,
)
fig3.update_layout(
        title_text="Graph 7: Cumulative change in mass balance for observed glaciers around the world",
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.8,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)

# Set x-axis title
fig3.update_xaxes(title_text="Year")

# Set y-axes titles
fig3.update_yaxes(title_text="Cumulative mass balance (meters of water equivalent)", secondary_y=False)
fig3.update_yaxes(title_text="Number of glaciers observed", secondary_y=True)
st.plotly_chart(fig3, use_container_width=True)
st.caption("""Graph 7: Cumulative change in mass balance for a world wide set of reference glaciers. 
    The line on the graph shows the average mass balance of all the glaciers that were measured in a given year.
    Negative values indicate a net loss of ice and snow since the base year of 1956. Measurements are in meters 
    of water equivalent representing changes in the average thickness of the glaciers. The barplot shows how many 
    glaciers were measured in a given year. Data from [EPA](https://www.epa.gov/climate-indicators/climate-change-indicators-glaciers).""")

df, df_yearly = get_snow_data()

selected_season = st.selectbox("Choose a season:", ['Spring', 'Summer', 'Autumn', 'Winter', 'Yearly average'])

fig4 = make_subplots()

if selected_season == 'Yearly average':

    x = df_yearly.index
    y = df_yearly

else:

    x = df.loc[df['season'] == selected_season, 's_year']
    y = df.loc[df['season'] == selected_season, 'value']

# Add traces
fig4.add_trace(
    go.Scatter(x=x,
        y=y, 
        name=selected_season,
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Year: %{x:.0f}')
)

# Generate a trendlince

# Coefficients: [slope, intercept]
coefficients = np.polyfit(x[~y.isna()], y[~y.isna()], 1)
trendline_function = np.poly1d(coefficients)
trendline_y = trendline_function(x)

fig4.add_trace(
    go.Scatter(x=x,
        y=trendline_y, 
        name="Trendline",
        hovertemplate =
        'Value: %{y:.2e} km<sup>2</sup>'+
        '<br>Year: %{x:.0f}'+
        f'<br>{coefficients[0]:.2e} * years + {coefficients[1]:.2e}',
        line=dict(color='black', width=1))
)

yearly_or_seasonal = "yearly" if selected_season == "Yearly average" else "seasonal"

fig4.update_layout(
    title_text=f"Graph 8: Northern hemisphere {yearly_or_seasonal} average snow cover extent",
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# Set x-axis title
fig4.update_xaxes(title_text="Year")

# Set y-axes titles
fig4.update_yaxes(title_text=f"Snow cover extent (km<sup>2</sup>)")
st.plotly_chart(fig4, use_container_width=True)
st.caption(f"""Graph 8: Northern hemisphere seasonal and yearly average snow cover extent by year.
    Snow cover extent is calculated at the Rutgers Global Snow Lab (GSL). The indicator is derived from maps
    produced daily by meteorologists at the US National Ice Center. Satellite images are used to construct the maps. 
    Data from [Rutgers University Global Snow Lab](https://climate.rutgers.edu/snowcover/table_area.php?ui_set=2&ui_sort=0).""")