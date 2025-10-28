import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_energy_consumption_data
)

st.set_page_config(
    page_title='Climate Change in Graphs: Energy',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

def range_slider_with_inputs(title, label, min_bound, max_bound, default_range):
    """
    Creates a Streamlit range slider with associated number input fields.

    Args:
        label (str): The label for the slider and input fields.
        min_bound (int/float): The minimum value for the range.
        max_bound (int/float): The maximum value for the range.
        default_range (tuple/list): The initial selected range (e.g., (low, high)).

    Returns:
        tuple: A tuple containing the selected lower and upper bounds.
    """
    st.write(title)

    def update_slider_value():
        updated_lower_value = st.session_state[f"{label}_lower_input"]
        updated_upper_value = st.session_state[f"{label}_upper_input"]
        st.session_state[f"{label}_slider"] = (updated_lower_value,updated_upper_value)

    if f"{label}_slider" not in st.session_state:
        st.session_state[f"{label}_slider"] = default_range

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # Create the range slider
        selected_range = st.slider(
            "Lower bound",
            min_value=min_bound,
            max_value=max_bound,
            format="%0.0f",
            label_visibility='collapsed',
            key=f"{label}_slider" # Unique key for the slider
        )
    
    with col1:
        lower_bound = st.number_input(
            "Slider",
            min_value=min_bound,
            max_value=max_bound,
            value=selected_range[0],
            on_change=update_slider_value,
            format="%0.0f",
            step=1.0,
            label_visibility='collapsed',
            key=f"{label}_lower_input" # Unique key for the lower input
        )

    with col3:
        upper_bound = st.number_input(
            "Upper bound",
            min_value=min_bound,
            max_value=max_bound,
            value=selected_range[1],
            on_change=update_slider_value,
            format="%0.0f",
            step=1.0,
            label_visibility='collapsed',
            key=f"{label}_upper_input" # Unique key for the upper input
        )

    # Ensure consistency between slider and input values
    if lower_bound != selected_range[0] or upper_bound != selected_range[1]:
        # If input fields are modified, update the slider's session state
        # This requires using st.session_state to manage the slider's value
        st.session_state[f"{label}_slider"] = (lower_bound, upper_bound)
        selected_range = (lower_bound, upper_bound)

    return selected_range

st.sidebar.header("Energy")

st.markdown("# World energy consumption and production")
############################################# Historic energy consumption plot ###########################################################
df = get_energy_consumption_data()

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'ec_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

fig1 = make_subplots()

for col in ['Traditional biomass','Coal','Oil','Gas','Nuclear','Hydropower','Wind','Solar','Other renewables','Biofuels']:

    # Add traces
    fig1.add_trace(
        go.Scatter(x=df.Year,
            y=df[col], 
            name=col,
            hovertemplate =
            'Value: %{y:.2e} TWh'+
            '<br>Year: %{x:.0f}',
            stackgroup='one')
    )

fig1.update_layout(
    title_text=f"Graph 1: World energy consumption by year 1800-2024",
    xaxis=dict(range=[from_year, to_year]),
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# # Set x-axis title
fig1.update_xaxes(title_text="Year")

# # Set y-axes titles
fig1.update_yaxes(title_text="Energy consumption (TWh)")
st.plotly_chart(fig1, use_container_width=True)
st.caption("""Graph 1: World energy consumption by year 1800-2024 in terms of direct primary energy. Primary energy is the 
    energy found in natural resources that has not yet been converted into other forms. In the absence of more recent data, 
    traditional biomass is assumed constant since 2015. Data 
    from [Our World in Data](https://ourworldindata.org/grapher/global-primary-energy).""")


###########################################################################################################################
st.markdown("### References")

st.markdown(
    """*World energy consumption by year (Graph 1)*  \nSmil, V. (2016). Energy Transitions: Global and National Perspectives 
    (2nd Edition). Praeger."""
)
st.markdown(
    """*World energy consumption by year (Graph 1)*  \nStatistical Review of World Energy (2025) – with major 
    processing by Our World in Data [dataset]. Accessed 2025-10-27."""
)

