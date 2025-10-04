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
    if st.button("Ice", icon=":material/ac_unit:", width = "stretch", help = "Ice and snowcover extent"):
        st.switch_page("pages/Ice.py", icon=":material/ac_unit:", width = "stretch")
    if st.button("Ocean", icon=":material/water:", width = "stretch", 
        help = "Global mean sea level anomaly and ocean acidification"):
        st.switch_page("pages/Ocean.py")
    if st.button("Temperature", icon=":material/device_thermostat:", width = "stretch", 
        help = "Global average temperature and greenhouse gas concentration"):
        st.switch_page("pages/Temperature.py")





