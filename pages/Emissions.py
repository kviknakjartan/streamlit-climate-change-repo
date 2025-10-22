import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_historic_ghg_data
)

st.set_page_config(
    page_title='Climate Change in Graphs: Emissions',
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

st.sidebar.header("Emissions")

st.markdown("# Greenhouse gas emissions")
############################################# Historic GHG plot ###########################################################
df = get_historic_ghg_data()

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'ghg_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

col1, col2 = st.columns(2)

with col1:
    selected_graph = st.selectbox("Choose a graph:", ['World total GHG emissions by substance', 'GHG emissions by country'])

fig1 = make_subplots()

if selected_graph == 'World total GHG emissions by substance':

    df_world = df[df.Entity == 'World']
    # Add traces
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.annual_emissions_co2_total, 
            name='CO<sub>2</sub>',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue'),
            stackgroup='one')
    )
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.annual_emissions_ch4_total_co2eq, 
            name='CH<sub>4</sub>',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red'),
            stackgroup='one')
    )
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.annual_emissions_n2o_total_co2eq, 
            name='N<sub>2</sub>O',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green'),
            stackgroup='one')
    )

fig1.update_layout(
    title_text=f"Graph 1: {selected_graph} by year in CO<sub>2</sub> equivalent",
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
fig1.update_yaxes(title_text="Emissions (tons of CO<sub>2</sub> equivalent)")
st.plotly_chart(fig1, use_container_width=True)
st.caption("""Graph 1: World total GHG emissions by substance and GHG emissions by country, by year in CO<sub>2</sub> 
    equivalent. Data from [Our World in Data](https://ourworldindata.org/grapher/ghg-emissions-by-gas).""")

###########################################################################################################################
st.markdown("### References")

st.markdown(
    f"""*Greenhouse gas emissions, world total and by country (Graph 1)*  \nJones, M. W., Peters, G. P., Gasser, T., Andrew, 
    R. M., Schwingshackl, C., Gütschow, J., Houghton, R. A., Friedlingstein, P., Pongratz, J., & Le Quéré, C. (2024) – with major 
    processing by Our World in Data. “Annual carbon dioxide, methane and nitrous oxide emissions including land use” [dataset]. 
    Jones et al., “National contributions to climate change 2024.2” [original data].
    Accessed {date.today()}."""
)
