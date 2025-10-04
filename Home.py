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





