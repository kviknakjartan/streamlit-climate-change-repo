import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Climate Change in Graphs',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.sidebar.header("Home")

st.title("Climate Change in Graphs:")
st.subheader("""Interactive graphs and maps showing past, present and future (?) climate and climatic indicators.""")

st.write("---")

col1, col2 = st.columns([1,4])

with col1:
    if st.button("Emissions", icon=":material/factory:", width = "stretch", help = "World greenhouse gas emissions"):
        st.switch_page("pages/Emissions.py")
    if st.button("Ice", icon=":material/ac_unit:", width = "stretch", help = "Ice and snowcover extent"):
        st.switch_page("pages/Ice.py")
    if st.button("Maps", icon=":material/map:", width = "stretch", 
        help = "Global spatial distributions of various climate indicators and projections"):
        st.switch_page("pages/Maps.py")
    if st.button("Ocean", icon=":material/water:", width = "stretch", 
        help = "Global mean sea level anomaly and ocean acidification"):
        st.switch_page("pages/Ocean.py")
    if st.button("Quantities", icon=":material/special_character:", width = "stretch", 
        help = "Physical quantities"):
        st.switch_page("pages/Ocean.py")
    if st.button("Temperature", icon=":material/device_thermostat:", width = "stretch", 
        help = "Global average temperature and greenhouse gas concentration"):
        st.switch_page("pages/Temperature.py")





