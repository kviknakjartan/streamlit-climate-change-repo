import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import rasterio
from rasterio.plot import show

st.set_page_config(
    page_title='Climate Change in Graphs: Maps',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown(
    """
    <style>
    .st-emotion-cache-1jicfl2 { /* This class targets the main content area */
        max-width: initial; /* Remove max-width constraint */
        padding: 0rem 1rem; /* Adjust padding as needed */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'be_1950to1993_temp' not in st.session_state:
    st.session_state.be_1950to1993_temp = None
if 'be_1994to2024_temp' not in st.session_state:
    st.session_state.be_1994to2024_temp = None
if 'cmip6_2025to2049_temp' not in st.session_state:
    st.session_state.cmip6_2025to2049_temp = None
if '1983to2024_precip' not in st.session_state:
    st.session_state['1983to2024_precip'] = None

st.sidebar.header("Maps")

st.markdown("# Global mean sea level anomaly and ocean acidification")

def plot_map(filePath, label, vmin, vmax, cmap, session_state_label):

    if st.session_state[session_state_label] is not None:
        st.pyplot(st.session_state[session_state_label], width='stretch')
        return

    df = pd.read_csv(filePath)

    lats = df.latitude
    df = df.drop(columns=['latitude'])
    lons = df.columns
    data = df.values

    data_cyclic, lon_cyclic = add_cyclic_point(data, coord=pd.to_numeric(lons))

    fig = plt.figure(figsize=(16, 12))
    ax = plt.axes(projection=ccrs.Mollweide(central_longitude=0, globe=None))

    mappable = ax.contourf(lon_cyclic, lats, data_cyclic * 120, 60, vmin = vmin, vmax = vmax, cmap=cmap,
                 transform=ccrs.PlateCarree())

    ax.coastlines()

    fig.colorbar(mappable, label=label, orientation='horizontal', pad=0.01, shrink=0.6) # Add a colorbar

    st.pyplot(fig, width='stretch')
    
    st.session_state[session_state_label] = fig

col1, col2 = st.columns(2)

with col1:
    selected_years = st.selectbox("Select year range:", ['1950-1993', '1994-2024', '2025-2049'])

st.markdown(f"##### Graph 1: Change in surface temperature for {selected_years}")

if selected_years == '1950-1993':
    plot_map(Path("data/df_be_wide_1950to1993_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'be_1950to1993_temp')
elif selected_years == '1994-2024':
    plot_map(Path("data/df_be_wide_1994to2024_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'be_1994to2024_temp')
elif selected_years == '2025-2049':
    plot_map(Path("data/df_cmip6_wide_2025to2049_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'cmip6_2025to2049_temp')

st.caption("""Graph 3: Recostruction of annual global average temperature for the past ~24,000 years based on climate modeling and geochemical proxy data,
         estimation of past carbon dioxide levels based on Antarctic icecore data and modern measured temperature and 
         carbon dioxide levels (instrumental record). Temperature reconstruction data from [NOAA](https://doi.org/10.25921/njxd-hg08).
         Temperature instrumental record from [The Berkeley Earth Land/Ocean Temperature Record](https://doi.org/10.5194/essd-12-3469-2020).""")

col1, col2 = st.columns(2)

with col1:
    selected_years = st.selectbox("Select year range:", ['1983-2024'])

st.markdown(f"##### Graph 2: Change in daily precipitation for {selected_years}")

if selected_years == '1983-2024':
    plot_map(Path("data/df_wide_1983to2024_precip.csv"), 'Precipitation change (mm/day per decade)', -1.6, 1.6, 'RdBu',
        '1983to2024_precip')

st.caption("""Graph 3: Recostruction of annual global average temperature for the past ~24,000 years based on climate modeling and geochemical proxy data,
         estimation of past carbon dioxide levels based on Antarctic icecore data and modern measured temperature and 
         carbon dioxide levels (instrumental record). Temperature reconstruction data from [NOAA](https://doi.org/10.25921/njxd-hg08).
         Temperature instrumental record from [The Berkeley Earth Land/Ocean Temperature Record](https://doi.org/10.5194/essd-12-3469-2020).""")


st.markdown(f"##### Graph 2: Change in daily precipitation for {selected_years}")

with st.container(gap = None):

    with rasterio.open(Path("data/MagnitudeEckertGGplot.tiff")) as src:
            
            fig, ax = plt.subplots(figsize=(20, 15))
            ax.set_frame_on(False)
            ax.set_axis_off()
            show(src, ax=ax)
            st.pyplot(fig)

    co1, col2, col3 = st.columns([2,1,2])

    with col2:
        st.image(Path("data/Fig2_ScaleBarMagnitude.svg"))

st.caption("""Graph 3: Recostruction of annual global average temperature for the past ~24,000 years based on climate modeling and geochemical proxy data,
         estimation of past carbon dioxide levels based on Antarctic icecore data and modern measured temperature and 
         carbon dioxide levels (instrumental record). Temperature reconstruction data from [NOAA](https://doi.org/10.25921/njxd-hg08).
         Temperature instrumental record from [The Berkeley Earth Land/Ocean Temperature Record](https://doi.org/10.5194/essd-12-3469-2020).""")

