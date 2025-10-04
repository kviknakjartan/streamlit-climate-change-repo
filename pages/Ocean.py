import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_sea_level_hist_data,
    get_sea_level_latest_data,
    get_ph_data,
    get_ohc_data
)

st.sidebar.header("Ocean")

st.markdown("# Global mean sea level anomaly and ocean acidification")

fig5 = make_subplots()

df = get_sea_level_hist_data()

# Add traces
fig5.add_trace(
    go.Scatter(x=df.Year,
        y=df.Value, 
        name='Global mean sea level anomaly',
        hovertemplate =
        'Value: %{y:.1f} mm'+
        '<br>Year: %{x:.0f}',
        line=dict(color='blue'))
)
x = df.Year
y_lower = df.Value - df.Unc
y_upper = df.Value + df.Unc

fig5.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Uncertainty',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)

fig5.update_layout(
    title_text=f"Graph 1: Reconstructed global mean sea level anomaly",
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# Set x-axis title
fig5.update_xaxes(title_text="Year")

# Set y-axes titles
fig5.update_yaxes(title_text=f"Sea level anomaly (mm)")
st.plotly_chart(fig5, use_container_width=True)
st.caption(f"""Graph 1: Reconstructed global mean sea level anomaly relative to 1990. The reconstruction is based on 
    satellite data and tide gauge records. 
    Data from [CSIRO](https://www.cmar.csiro.au/sealevel/sl_data_cmar.html).""")


fig6 = make_subplots()

df = get_sea_level_latest_data()
x=df.Date
y=df["Mean Sea Level (cm)"] * 10

# Add traces
fig6.add_trace(
    go.Scatter(x=x,
        y=y, 
        name='Global mean sea level anomaly',
        hovertemplate =
        'Value: %{y:.1f} mm'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='blue'))
)
y_lower = y - df["90% C.L. uncertainty"] * 10
y_upper = y + df["90% C.L. uncertainty"] * 10

fig6.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='90% Confidence level',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)

fig6.add_trace(
    go.Scatter(x=x,
        y=df["OLS fit"] * 10, 
        name='Trendline',
        customdata = df["Trendslope"],
        hovertemplate =
        'Slope: %{customdata:.2f} mm/yr'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='black', width = 1, dash='dash'))
)

fig6.update_layout(
    title_text=f"Graph 2: Latest global mean sea level anomaly",
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# Set x-axis title
fig6.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig6.update_yaxes(title_text=f"Sea level anomaly (mm)")
st.plotly_chart(fig6, use_container_width=True)
st.caption(f"""Graph 2: Global mean sea level anomaly from satellite altimetry. 30% of the global mean sea 
    level rise is due to thermal expansion in the ocean while remaining contribution mainly comes from the melting of 
    glaciers and ice sheets. The rise in global mean sea level has increased by 46%, from a trend of 2.9 mm/year over 
    1999–2009 to a trend of 4.2 mm/year over 2014–2024 (Copernicus Climate Change Service).
    Data from [Copernicus Climate Change Service](https://climate.copernicus.eu/climate-indicators/sea-level).""")

df_global, df_aloha = get_ph_data()

# Create figure with secondary y-axis
fig7 = make_subplots()

x = df_global['date']
y = df_global['value']

# Add traces
fig7.add_trace(
    go.Scatter(x=x,
        y=y,
        name="Estimated global average pH",
        hovertemplate =
        'Value: %{y:.1f}'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='blue', width=2))
)

y_lower = y - df_global["uncertainty"]
y_upper = y + df_global["uncertainty"]

fig7.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Global pH uncertainty',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)

fig7.add_trace(
    go.Scatter(x=df_aloha.date,
        y=df_aloha['pHcalc_25C'],
        name="Hawaii measured pH",
        hovertemplate =
        'Value: %{y:.1f}'+
        '<br>Date: %{x|%B %d, %Y}',
        line=dict(color='red'))
)

fig7.update_layout(
    title_text="Graph 3: Estimated global average and measured (Hawaii) ocean pH level",
    legend=dict(
        x=0.1,  # x-position (0.1 is near left)
        y=0.7,  # y-position (0.9 is near top)
        xref="container",
        yref="container",
        orientation = 'h'
    )
)

# Set x-axis title
fig7.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig7.update_yaxes(title_text="Acidity (pH)")
st.plotly_chart(fig7, use_container_width=True)
st.caption("""Graph 3: Estimated global average and measured (Hawaii) ocean pH level. The ocean has absorbed roughly 20-30% of 
    total anthropogenic carbon dioxide emissions since the 1980’s. 
    This is causing acidification of the oceans at a rate faster than any time in the past 300 million years (Copernicus). 
    pH is measured on a logarithmic scale which means that ocean acidity has increased by 40% since the pre-industrial era. 
    Global average estimation data from [Copernicus](https://marine.copernicus.eu/ocean-climate-portal/ocean-acidification). 
    Measured pH data from [Hawaii Ocean Time-series (HOT)](https://hahana.soest.hawaii.edu/hot/hotco2/hotco2.html).""")


df_300, df_700, df_2000, df_700_2000 = get_ohc_data()

fig8 = make_subplots()

# Add traces
fig8.add_trace(
    go.Scatter(x=df_300.time,
        y=df_300.ohc_mean/10**21,
        name="0-300 m",
        hovertemplate =
        'Value: %{y:.2f} ZJ'+
        '<br>Date: %{x|%B %Y}',
        line=dict(color='blue'))
)

fig8.add_trace(
    go.Scatter(x=pd.concat([df_300.time, df_300.time[::-1]]),
        y=pd.concat([df_300.ohc_max/10**21, df_300.ohc_min[::-1]/10**21]), 
        name='0-300 m uncertainty',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)

fig8.add_trace(
    go.Scatter(x=df_700.time,
        y=df_700.ohc_mean/10**21,
        name="0-700 m",
        hovertemplate =
        'Value: %{y:.2f} ZJ'+
        '<br>Date: %{x|%B %Y}',
        line=dict(color='red'))
)

fig8.add_trace(
    go.Scatter(x=pd.concat([df_700.time, df_700.time[::-1]]),
        y=pd.concat([df_700.ohc_max/10**21, df_700.ohc_min[::-1]/10**21]), 
        name='0-700 m uncertainty',
        fill='toself',
        fillcolor='rgba(255,0,0,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(255,0,0,0.2)', width=0.1))
)

fig8.add_trace(
    go.Scatter(x=df_2000.time,
        y=df_2000.ohc_mean/10**21,
        name="0-2000 m",
        hovertemplate =
        'Value: %{y:.2f} ZJ'+
        '<br>Date: %{x|%B %Y}',
        line=dict(color='green'))
)

fig8.add_trace(
    go.Scatter(x=pd.concat([df_2000.time, df_2000.time[::-1]]),
        y=pd.concat([df_2000.ohc_max/10**21, df_2000.ohc_min[::-1]/10**21]), 
        name='0-2000 m uncertainty',
        fill='toself',
        fillcolor='rgba(0,255,0,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,255,0,0.2)', width=0.1))
)

fig8.add_trace(
    go.Scatter(x=df_700_2000.time,
        y=df_700_2000.ohc_mean/10**21,
        name="700-2000 m",
        hovertemplate =
        'Value: %{y:.2f} ZJ'+
        '<br>Date: %{x|%B %Y}',
        line=dict(color='gray', dash='dash'))
)

fig8.add_trace(
    go.Scatter(x=pd.concat([df_700_2000.time, df_700_2000.time[::-1]]),
        y=pd.concat([df_700_2000.ohc_max/10**21, df_700_2000.ohc_min[::-1]/10**21]), 
        name='700-2000 m uncertainty',
        fill='toself',
        fillcolor='rgba(128,128,128,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(128,128,128,0.2)', width=0.1))
)

fig8.update_layout(
    title_text="Graph 4: Ocean heat content anomalies of the ocean for various depth ranges",
    legend=dict(
        x=0.1,  # x-position (0.1 is near left)
        y=0.7,  # y-position (0.9 is near top)
        xref="container",
        yref="container",
        orientation = 'h'
    )
)

# Set x-axis title
fig8.update_xaxes(title_text="Observation time")

# Set y-axes titles
fig8.update_yaxes(title_text="Heat content (ZJ)")
st.plotly_chart(fig8, use_container_width=True)
st.caption("""Graph 4: Ocean heat content anomalies of the ocean for various depth ranges. The ocean absorbes and stores up to 
    90% of the excess heat that is received by Earth and interned by the greenhouse effect. This heat is distributed by ocean 
    circulation from low to mid and high latitudes, and from the surface to deeper layers (Copernicus). The heat content is 
    measured in zettajoules (ZJ), which represents a factor of 10 to the power of 21.
    Data and graph adopted from [Copernicus](https://climate.copernicus.eu/climate-indicators/ocean-heat-content).""")

st.markdown("# References")

st.markdown(
    """*Global mean sea level reconstruction (Graph 1)*  \nChurch, J.A. and N.J. White (2011), Sea-level rise from the late 19th 
    to the early 21st century. Surveys in Geophysics, 32, 585-602, doi:10.1007/s10712-011-9119-1."""
)
st.markdown(
    f"""*Global mean sea level anomaly (Graph 2)*  \nCopernicus Climate Change Service. 
    Climate indicators - Sea level: Figure 1. Daily change in global mean sea level 
    [Dataset]. https://climate.copernicus.eu/climate-indicators/sea-level.
    Date Accessed {date.today()}."""
)
st.markdown(
    """*Global average pH estimation (Graph 3)*  \nCopernicus Marine Service. 
    Ocean Climate Portal - Ocean Acidification. [Dataset]. https://marine.copernicus.eu/ocean-climate-portal/ocean-acidification.
    Date Accessed 2025-10-04."""
)
st.markdown(
    f"""*Measured pH levels from Aloha Station Hawaii (Graph 3)*  \nHawaii Ocean Time-series (HOT).  
    [Dataset]. https://hahana.soest.hawaii.edu/hot/hotco2/hotco2.html.
    Date Accessed {date.today()}."""
)
st.markdown(
    """*Global ocean heat content anomalies (Graph 4)*  \nCopernicus Climate Change Service. 
    CLIMATE INDICATORS - Ocean heat content. [Dataset]. https://climate.copernicus.eu/climate-indicators/ocean-heat-content.
    Date Accessed 2025-10-04."""
)