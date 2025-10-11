import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
if 'cmip6_2050to2074_temp' not in st.session_state:
    st.session_state.cmip6_2050to2074_temp = None
if 'cmip6_2075to2099_temp' not in st.session_state:
    st.session_state.cmip6_2075to2099_temp = None
if '1983to2024_precip' not in st.session_state:
    st.session_state['1983to2024_precip'] = None
if 'mid_century_tws' not in st.session_state:
    st.session_state.mid_century_tws = None
if 'late_century_tws' not in st.session_state:
    st.session_state.late_century_tws = None



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

def plot_tws_map(filePath, label, session_state_label):

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

    custom_levels = [-300, -200, -100, -50, -10, 10, 50, 100, 200, 300]

    # Define a list of colors
    custom_colors = ['darkred', 'red', 'orange', 'yellow', 'lightgray', 'cyan', 'blue', 'darkblue', 'purple']

    # Create a ListedColormap
    custom_cmap = mcolors.ListedColormap(custom_colors)

    # Create a BoundaryNorm instance
    # cmap.N should match the number of colors in custom_cmap
    norm = mcolors.BoundaryNorm(custom_levels, custom_cmap.N)

    mappable = ax.contourf(lon_cyclic, lats, np.clip(data_cyclic, -299.9, 299.9), 60, vmin = -300, vmax = 300, cmap=custom_cmap,
                 transform=ccrs.PlateCarree(), levels=custom_levels, norm=norm)

    ax.coastlines()

    fig.colorbar(mappable, label='label', orientation='horizontal', pad=0.01, shrink=0.6) # Add a colorbar

    st.pyplot(fig, width='stretch')
    
    st.session_state[session_state_label] = fig

st.sidebar.header("Maps")

st.markdown("# Global spatial distributions of various climate indicators and projections")

#################### Change in surface temperature #############################
st.write("")

col1, col2 = st.columns(2)

with col1:
    selected_years = st.selectbox("Select year range:", ['1950-1993', '1994-2024', '2025-2049 (projected)', 
        '2050-2074 (projected)', '2075-2099 (projected)'])

st.markdown(f"##### Graph 1: Change in surface temperature for {selected_years}")

if selected_years == '1950-1993':
    plot_map(Path("data/df_be_wide_1950to1993_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'be_1950to1993_temp')
elif selected_years == '1994-2024':
    plot_map(Path("data/df_be_wide_1994to2024_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'be_1994to2024_temp')
elif selected_years == '2025-2049 (projected)':
    plot_map(Path("data/df_cmip6_wide_2025to2049_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'cmip6_2025to2049_temp')
elif selected_years == '2050-2074 (projected)':
    plot_map(Path("data/df_cmip6_wide_2050to2074_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'cmip6_2050to2074_temp')
else:
    plot_map(Path("data/df_cmip6_wide_2075to2099_temp.csv"), 'Temperature change (°C per decade)', -2, 2, 'RdBu_r', 
        'cmip6_2075to2099_temp')

st.caption("""Graph 1: Global temperature trends in °C per decade in the past (instrumental record) and for future projections 
    based on 23 CMIP6 model outputs. For CMIP6 projections the median trend for all model outputs is shown for 
    scenario [SSP2-4.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways).
    CMIP6 data from [Copernicus Climate Change Service, Climate Data Store](https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview).
    Temperature instrumental record from [The Berkeley Earth Land/Ocean Temperature Record](https://doi.org/10.5194/essd-12-3469-2020).""")

#################### Change in monthly average precipitation #############################
st.write("")

col1, col2 = st.columns(2)

with col1:
    selected_years = st.selectbox("Select year range:", ['1983-2024'])

st.markdown(f"##### Graph 2: Change in monthly average precipitation for {selected_years}")

if selected_years == '1983-2024':
    plot_map(Path("data/df_wide_1983to2024_precip.csv"), 'Precipitation change (mm/day per decade)', -1.6, 1.6, 'RdBu',
        '1983to2024_precip')
# elif selected_years == '2025-2049':
#     plot_map(Path("data/df_cmip6_wide_2025to2049_precip.csv"), 'Precipitation change (mm/day per decade)', -1.6, 1.6, 'RdBu',
#         '2025to2049_precip')
# else:
#     plot_map(Path("data/df_cmip6_wide_2050to2099_precip.csv"), 'Precipitation change (mm/day per decade)', -1.6, 1.6, 'RdBu',
#         '2050to2099_precip')

st.caption("""Graph Graph 2: Trend in monthly average precipitation for 1983-2024. Units are (mm/day)/decade.
         Monthly average precipitation data derived from satellite measurements 
         from [Copernicus Climate Change Service, Climate Data Store](https://cds.climate.copernicus.eu/datasets/satellite-precipitation?tab=download).""")

#################### TWS and drought #############################
st.write("")

col1, col2 = st.columns(2)

with col1:
    selected_indicator = st.selectbox("Select indicator:", ['Changes in terrestrial water storage 2030-2059', 
        'Changes in terrestrial water storage 2070-2099'])

st.markdown(f"##### Graph 3: {selected_indicator}")

if selected_indicator == 'Changes in terrestrial water storage 2030-2059':
    plot_tws_map(Path("data/df_wide_mid_century_tws.csv"), 'TWS (mm)', 'mid_century_tws')
elif selected_indicator == 'Changes in terrestrial water storage 2070-2099':
    plot_tws_map(Path("data/df_wide_late_century_tws.csv"), 'TWS (mm)', 'late_century_tws')

st.caption("""Graph 3:  The changes (multi-model weighted mean) in terrestrial water storage (TWS), averaged for the 
    mid- (2030–2059) and the late (2070–2099) twenty-first century under future 
    scenario [RCP6.0](https://en.wikipedia.org/wiki/Representative_Concentration_Pathway). The changes are relative to the 
    average for the historical baseline period (1976–2005). Terrestrial water storage is the sum of continental water 
    stored in canopies, snow and ice, rivers, lakes and reservoirs, wetlands, soil and groundwater. It plays a key role in
    determining water resource availability. Changes in TWS are linked to droughts, floods and global sea level change. 
    Graph adopted from and data from [Nature Climate Change](https://doi.org/10.1038/s41558-020-00972-w).""")

#################### Loss in biodiversity #############################
st.write("")

col1, col2 = st.columns(2)

with col1:
    selected_map = st.selectbox("Select indicator:", ['Magnitude', 'Abruptness', 'Timing'])

def show_map(title, map_path, colorbar_path):

    st.markdown(title)

    with st.container(gap = None):

        with rasterio.open(map_path) as src:
                
                fig, ax = plt.subplots(figsize=(20, 15))
                ax.set_frame_on(False)
                ax.set_axis_off()
                show(src, ax=ax)
                st.pyplot(fig)

        co1, col2, col3 = st.columns([1.5,1,1.5])

        with col2:
            st.image(colorbar_path)

if selected_map == "Magnitude":
    show_map("##### Graph 3: Percentage of species exposed to potentially dangerous climate by 2100",
        Path("data/MagnitudeEckertGGplot.tiff"), Path("data/Fig2_ScaleBarMagnitude.svg"))
elif selected_map == "Abruptness":
    show_map("##### Graph 3: Percentage of species exposed to potentially dangerous climate at a time of maximum exposure",
        Path("data/AbruptnessEckertGGplot.tiff"), Path("data/Fig2_ScaleBarAbruptness.svg"))
else:
    show_map("##### Graph 3: Median year of species exposed to potentially dangerous climate",
        Path("data/TimingEckertGGplot.tiff"), Path("data/Fig2_ScaleBarTiming.svg"))

st.caption("""Graph 3: Three different indicators quantifying potential loss of biodiversity in the future based on 
    scenario [SSP2-4.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) and data on over 30,000 marine and 
    terrestrial species. *Magnitude* indicates what percentage of
    local species will be subjected to climate conditions threatening to their survival by the year 2100. *Abruptness* indicates 
    what percentage of local species will be subjected to these conditions at the same time interval (a decade), the interval at 
    which most of the species in question will be exposed. *Timing* then indicates the median year of exposure for all local species
    that will be exposed by the year 2100. Data and plots from [Nature](https://doi.org/10.1038/s41586-020-2189-9).""")

#################### References #############################
st.markdown("# References")

st.markdown(
    """*Instrumental temperature record (Graph 1)*  \nRohde, R. A. and Hausfather, Z.: 
    The Berkeley Earth Land/Ocean Temperature Record, Earth Syst. Sci. Data, 12, 3469-3479, 
    https://doi.org/10.5194/essd-12-3469-2020, 2020. 
    (Accessed on 2025-10-08)."""
)
st.markdown(
    """*CMIP6 model output data (Graph 1)*  \nCopernicus Climate Change Service, Climate Data Store, 
    (2021): CMIP6 climate projections. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). 
    DOI: 10.24381/cds.c866074c. (Accessed on 2025-10-08)."""
)
st.markdown(
    """*Precipitation data 1983-2024 (Graph 2)*  \nCopernicus Climate Change Service (2021): Precipitation monthly and daily 
    gridded data from 1979 to present derived from satellite measurement. Copernicus Climate Change Service (C3S) Climate 
    Data Store (CDS). DOI: 10.24381/cds.c14d9324.
    (Accessed on 2025-10-07)."""
)
st.markdown(
    """*GPCP Version 3.2 Satellite-Gauge (SG) Combined Precipitation Data Set (Graph 2)*  \nHuffman, G.J., A. Behrangi, 
    D.T. Bolvin, E.J. Nelkin (2022), GPCP Version 3.2 Satellite-Gauge (SG) Combined Precipitation Data Set, Edited by 
    Huffman, G.J., A. Behrangi, D.T. Bolvin, E.J. Nelkin, Greenbelt, Maryland, USA, Goddard Earth Sciences Data and 
    Information Services Center (GES DISC), Accessed: [2025-10-07], 10.5067/MEASURES/GPCP/DATA304."""
)
st.markdown(
    """*Changes in TWS and drought severity (Graph 3)*  \nPokhrel, Y., Felfelani, F., Satoh, Y. et al. Global terrestrial 
    water storage and drought severity under climate change. Nat. Clim. Chang. 11, 226–233 
    (2021). https://doi.org/10.1038/s41558-020-00972-w.
    (Accessed on 2025-10-06)"""
)
st.markdown(
    """*Indicators quantifying potential loss of biodiversity (Graph 3)*  \nTrisos, C.H., Merow, C. & Pigot, A.L. 
    The projected timing of abrupt ecological disruption from climate change. 
    Nature 580, 496–501 (2020). https://doi.org/10.1038/s41586-020-2189-9.
    (Accessed on 2025-10-06)"""
)