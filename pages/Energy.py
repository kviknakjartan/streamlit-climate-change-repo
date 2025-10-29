import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_energy_consumption_data,
    get_electricity_data,
    get_energy_sector_data,
    get_energy_per_cap_data
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
df_energy = get_energy_consumption_data()

min_value = df_energy['Year'].min()
max_value = df_energy['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'ec_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

fig1 = make_subplots()

for col in ['Traditional biomass','Coal','Oil','Gas','Nuclear','Hydropower','Wind','Solar','Other renewables','Biofuels']:

    # Add traces
    fig1.add_trace(
        go.Scatter(x=df_energy.Year,
            y=df_energy[col], 
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

############################################# Historic electricity by source plot ###########################################################
df_el = get_electricity_data()

df = df_el[(df_el.Year > 1999) & (df_el.Entity == 'World')]
df = df.sort_values(by='Year')

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'el_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

fig2 = make_subplots()

for col in ['Coal','Gas','Oil','Nuclear','Hydro','Solar','Wind','Bioenergy','Other renewables']:

    # Add traces
    fig2.add_trace(
        go.Scatter(x=df.Year,
            y=df[col], 
            name=col,
            hovertemplate =
            'Value: %{y:.2e} TWh'+
            '<br>Year: %{x:.0f}',
            stackgroup='one')
    )

fig2.update_layout(
    title_text=f"Graph 2: World electricity generation by source 2000-2024",
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
fig2.update_xaxes(title_text="Year")

# # Set y-axes titles
fig2.update_yaxes(title_text="Electricity generation (TWh)")
st.plotly_chart(fig2, use_container_width=True)
st.caption("""Graph 2: World electricity generation by source 2000-2024. Data 
    from [Our World in Data](https://ourworldindata.org/grapher/electricity-production-by-source).""")

############################################# Historic energy by sector plot ###########################################################
df = get_energy_sector_data()

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'sector_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

fig3 = make_subplots()

for sector in ['Industry','Transport','Non-energy use','Commercial and Public Services','Agriculture and forestry',
    'Residential','Other non-specified','Fishing']:

    df_sector = df[df['total final consumption in World'] == sector]
    # Add traces
    fig3.add_trace(
        go.Scatter(x=df_sector.Year,
            y=df_sector.Value/3600, 
            name=sector,
            hovertemplate =
            'Value: %{y:.2e} TWh'+
            '<br>Year: %{x:.0f}',
            stackgroup='one')
    )

fig3.update_layout(
    title_text=f"Graph 3: World final energy consumption by sector 2000-2023",
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
fig3.update_xaxes(title_text="Year")

# # Set y-axes titles
fig3.update_yaxes(title_text="Electricity generation (TWh)")
st.plotly_chart(fig3, use_container_width=True)
st.caption("""Graph 3: World final energy consumption by sector 2000-2023. Data 
    from [IEA](https://www.iea.org/world/energy-mix).""")

############################################# Historic per capita energy by source plot ###########################################################
df = get_energy_per_cap_data()

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
    'pp_historical', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))

fig4 = make_subplots()

col1, col2 = st.columns(2)

with col1:
    selected_source = st.selectbox("Choose an energy source:", ['Hydro','Nuclear','Gas','Oil','Coal','Wind','Total','Solar'])

selected_countries = st.multiselect(
        'Select Countries',
        df.Entity.unique(),
        default = ['United States','China','Russia','European Union (27)'],
        placeholder = "Choose at least one"
)
for country in selected_countries:
    fig4.add_trace(
        go.Scatter(x=df.loc[df.Entity == country, 'Year'],
            y=df.loc[df.Entity == country, selected_source], 
            name=country,
            hovertemplate =
            'Value: %{y:.2e} kWh'+
            '<br>Year: %{x:.0f}')
    )

fig4.update_layout(
    title_text=f"Graph 4: Per capita primary energy consumption by source 1965-2024",
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
fig4.update_xaxes(title_text="Year")

# # Set y-axes titles
fig4.update_yaxes(title_text="Energy consumption (kWh)")
st.plotly_chart(fig4, use_container_width=True)
st.caption("""Graph 4: Per capita primary energy consumption by source 1965-2024. Data 
    from [Our World in Data](https://ourworldindata.org/energy).""")

############################################# Historic per capita 2023 map ###########################################################
df = df.merge(df_el.loc[df_el.Year == 2023, ['Entity','Code']], on='Entity', how='left')

col1, col2 = st.columns(2)

with col1:
    selected_source = st.selectbox("Choose an energy source:", ['Hydro','Nuclear','Gas','Oil','Coal','Wind','Total','Solar'], 
        key='source')

fig5 = px.choropleth(df[df.Year == 2023], locations="Code",
                    color=selected_source, 
                    hover_name="Entity", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.turbid,
                    title=f'Graph 5: Per capita primary energy consumption by source 2023')

fig5.update_layout(
    coloraxis_colorbar=dict(
        orientation="h",  # Horizontal orientation
        yanchor="bottom", # Anchor the legend's bottom to the specified y-coordinate
        y=-0.3,           # Position below the plot area (adjust as needed)
        xanchor="left",   # Anchor the legend's left to the specified x-coordinate
        x=0.13,               # Position at the left edge of the plot area
        title=f'{selected_source} (kWh)'
    )
)
st.plotly_chart(fig5, use_container_width=True)
st.caption("""Graph 5: Per capita primary energy consumption by source 2023. Data 
    from [Our World in Data](https://ourworldindata.org/energy).""")
###########################################################################################################################
st.markdown("### References")

st.markdown(
    """*World energy consumption by year (Graph 1)*  \nSmil, V. (2016). Energy Transitions: Global and National Perspectives 
    (2nd Edition). Praeger."""
)
st.markdown(
    """*World energy consumption by year (Graph 1)*  \nEnergy Institute - Statistical Review of World Energy (2025) – with major 
    processing by Our World in Data [dataset]. Accessed 2025-10-27."""
)
st.markdown(
    """*World electricity generation by source (Graph 2)*  \nEnergy Institute - Statistical Review of World Energy (2025) – with 
    major processing by Our World in Data [dataset]. Accessed 2025-10-28."""
)
st.markdown(
    """*World electricity generation by source (Graph 2)*  \nEmber - Yearly Electricity Data Europe (2025) – with major 
    processing by Our World in Data [dataset]. Accessed 2025-10-28."""
)
st.markdown(
    """*World electricity generation by source (Graph 2)*  \nEmber - Yearly Electricity Data (2025) – with major 
    processing by Our World in Data [dataset]. Accessed 2025-10-28."""
)
st.markdown(
    """*World energy consumption by year (Graph 3)*  \nInternational Energy Agency (2024); World - IEA, 
    https://www.iea.org/world/energy-mix [dataset], License: CC BY 4.0; Accessed 2025-10-27."""
)
st.markdown(
    """*Primary energy consumption per capida (Graphs 4 and 5)*  \nEnergy Institute - Statistical Review of World Energy (2025) – with 
    major processing by Our World in Data [dataset]. Accessed 2025-10-28."""
)