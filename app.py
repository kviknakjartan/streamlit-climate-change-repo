import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from get_data import (
    get_cmip6_data,
    get_be_global_data,
    get_osman_data,
    get_parrenin_data,
    get_co2_latest_data,
    get_ch4_latest_data,
    get_n2o_latest_data,
    get_co2_hist_data,
    get_ch4_hist_data,
    get_n2o_hist_data
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


def get_and_combine_ghg_data():
    df = pd.concat([get_co2_hist_data(), get_ch4_hist_data(), get_n2o_hist_data(), \
        get_co2_latest_data(), get_ch4_latest_data(), get_n2o_latest_data(), get_parrenin_data()])
    return df

def get_and_combine_temp_data():
    df = pd.concat([get_osman_data(), get_be_global_data(), get_co2_hist_data(), get_co2_latest_data()])
    return df

def create_ghg_section():
    df = get_and_combine_ghg_data()

    min_value = df['Year'].min()
    max_value = df['Year'].max()

    from_year, to_year = range_slider_with_inputs("What timescale are you interested in? (Negative values are years BCE)", \
        'ghg', min_value, max_value, (min_value, max_value))

    # GREENHOUSE GAS PLOT
    # Create figure with secondary y-axis
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CO2_hist', 'Year'], \
            y=df.loc[df['Name'] == 'CO2_hist', 'Value'], name="CO<sub>2</sub> icecore",
            hovertemplate =
            'Value: %{y:.1f} ppm'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue')),
        secondary_y=False,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CO2_latest', 'Year'], \
            y=df.loc[df['Name'] == 'CO2_latest', 'Value'], name="CO<sub>2</sub> measurements",
            line=dict(color='lightblue'),
            hovertemplate =
            'Value: %{y:.1f} ppm'+
            '<br>Year: %{x:.0f}'),
        secondary_y=False,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CH4_hist', 'Year'], \
            y=df.loc[df['Name'] == 'CH4_hist', 'Value'], name="Methane (CH<sub>4</sub>) icecore",
            hovertemplate =
            'Value: %{y:.1f} ppb'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red')),
        secondary_y=True,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CH4_latest', 'Year'], \
            y=df.loc[df['Name'] == 'CH4_latest', 'Value'], name="Methane (CH<sub>4</sub>) measurements", 
            line=dict(color='pink'),
            hovertemplate =
            'Value: %{y:.1f} ppb'+
            '<br>Year: %{x:.0f}'),
        secondary_y=True,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'N2O_hist', 'Year'], \
            y=df.loc[df['Name'] == 'N2O_hist', 'Value'], name="N<sub>2</sub>O icecore",
            hovertemplate =
            'Value: %{y:.1f} ppb'+
            '<br>Year: %{x:.0f}',
            line=dict(color='gray')),
        secondary_y=True,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'N2O_latest', 'Year'], \
            y=df.loc[df['Name'] == 'N2O_latest', 'Value'], name="N<sub>2</sub>O measurements",
            line=dict(color='lightgray'),
            hovertemplate =
            'Value: %{y:.1f} ppb'+
            '<br>Year: %{x:.0f}'),
        secondary_y=True,
    )

    fig1.update_layout(
        title_text="Graph 1: Atmospheric concentrations for selected greenhouse gases",
        xaxis=dict(range=[from_year, to_year]),
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
    )

    # Set x-axis title
    fig1.update_xaxes(title_text="Year (negative = BCE)")

    # Set y-axes titles
    fig1.update_yaxes(title_text="CO<sub>2</sub> (ppm)", secondary_y=False)
    fig1.update_yaxes(title_text="CH<sub>4</sub> (ppb) / N<sub>2</sub>O (ppb)", secondary_y=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("""Graph 1: Estimated atmospheric concentration levels of three greenhouse gases for the past ~800,000 years.
        Based on Antarctic icecore data. Also shown are modern measured annual average levels (instrumental record).""")

    # CO2 VS. TEMPERATURE PLOT
    # Create figure with secondary y-axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig2.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CO2_hist', 'Year'], \
            y=df.loc[df['Name'] == 'CO2_hist', 'Value'], name="CO<sub>2</sub> icecore",
            hovertemplate =
            'Value: %{y:.1f} ppm'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue')),
        secondary_y=False,
    )

    fig2.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'Temp_parrenin', 'Year'], \
            y=df.loc[df['Name'] == 'Temp_parrenin', 'Value'], name="Temperature change icecore",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green')),
        secondary_y=True,
    )

    # Add figure title
    fig2.update_layout(
        title_text="Graph 2: Antarctic average air temperature change and global CO<sub>2</sub> concentration",
        xaxis=dict(range=[from_year, to_year]),
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h')
    )

    # Set x-axis title
    fig2.update_xaxes(title_text="Year (negative = BCE)")

    # Set y-axes titles
    fig2.update_yaxes(title_text="CO<sub>2</sub> (ppm)", secondary_y=False)
    fig2.update_yaxes(title_text="Temperature change (°C)", secondary_y=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("""Graph 2: Recostruction of Antarctic temperature change for the past ~800,000 years, based on Antarctic 
        icecore data and estimation of past carbon dioxide levels based on Antarctic icecore data.""")
    st.write("")
    st.write("")

def create_ghg_section2():
    df = get_and_combine_temp_data()

    min_value = df.loc[df['Name'] == 'Temp_hist', 'Year'].min()
    max_value = df['Year'].max()

    df = df[df['Year'] >= min_value]

    from_year, to_year = range_slider_with_inputs("What timescale are you interested in? (Negative values are years BCE)", \
        'temp', min_value, max_value, (min_value, max_value))

    # Create figure with secondary y-axis
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CO2_hist', 'Year'], \
            y=df.loc[df['Name'] == 'CO2_hist', 'Value'], name="CO<sub>2</sub> icecore",
            hovertemplate =
            'Value: %{y:.1f} ppm'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue')),
        secondary_y=False,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'CO2_latest', 'Year'], \
            y=df.loc[df['Name'] == 'CO2_latest', 'Value'], name="CO<sub>2</sub> measurements",
            line=dict(color='lightblue'),
            hovertemplate =
            'Value: %{y:.1f} ppm'+
            '<br>Year: %{x:.0f}'),
        secondary_y=False,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'Temp_hist', 'Year'], \
            y=df.loc[df['Name'] == 'Temp_hist', 'Value'], name="Reconstructed temperature",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green')),
        secondary_y=True,
    )

    fig1.add_trace(
        go.Scatter(x=df.loc[df['Name'] == 'Temp_latest', 'Year'], \
            y=df.loc[df['Name'] == 'Temp_latest', 'Value'], name="Temperature measurements", 
            line=dict(color='lightgreen'),
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}'),
        secondary_y=True,
    )

    fig1.update_layout(
        title_text="Graph 3: Annual global average surface temperature and CO<sub>2</sub> concentration",
        xaxis=dict(range=[from_year, to_year]),
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
    )

    # Set x-axis title
    fig1.update_xaxes(title_text="Year (negative = BCE)")

    # Set y-axes titles
    fig1.update_yaxes(title_text="CO<sub>2</sub> (ppm)", secondary_y=False)
    fig1.update_yaxes(title_text="Temperature (°C)", secondary_y=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("""Graph 3: Recostruction of annual global average temperature for the past ~24,000 years based on climate modeling and geochemical proxy data,
         estimation of past carbon dioxide levels based on Antarctic icecore data and modern measured temperature and 
         carbon dioxide levels (instrumental record).""")

def create_cmip6_section():
    df = get_cmip6_data()
    df_instrumental = get_be_global_data()
    df_historical = df[df['experiment'] == 'historical']
    df_ssp126 = df[df['experiment'] == 'ssp126']
    df_ssp245 = df[df['experiment'] == 'ssp245']
    df_ssp585 = df[df['experiment'] == 'ssp585']

    # Create figure
    fig1 = make_subplots()

    # Add traces
    fig1.add_trace(
        go.Scatter(x=df_historical.loc[df['quantile'] == 0.5, 'year'], \
            y=df_historical.loc[df['quantile'] == 0.5, 'tas'], name="historical 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black'))
    )
    fig1.add_trace(
        go.Scatter(x=df_historical.loc[df['quantile'] == 0.9, 'year'], \
            y=df_historical.loc[df['quantile'] == 0.9, 'tas'], name="historical 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_historical.loc[df['quantile'] == 0.1, 'year'], \
            y=df_historical.loc[df['quantile'] == 0.1, 'tas'], name="historical 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 0, 0, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df['quantile'] == 0.5, 'year'], \
            y=df_ssp126.loc[df['quantile'] == 0.5, 'tas'], name="SSP1-2.6 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df['quantile'] == 0.9, 'year'], \
            y=df_ssp126.loc[df['quantile'] == 0.9, 'tas'], name="SSP1-2.6 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df['quantile'] == 0.1, 'year'], \
            y=df_ssp126.loc[df['quantile'] == 0.1, 'tas'], name="SSP1-2.6 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 0, 255, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df['quantile'] == 0.5, 'year'], \
            y=df_ssp245.loc[df['quantile'] == 0.5, 'tas'], name="SSP2-4.5 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df['quantile'] == 0.9, 'year'], \
            y=df_ssp245.loc[df['quantile'] == 0.9, 'tas'], name="SSP2-4.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df['quantile'] == 0.1, 'year'], \
            y=df_ssp245.loc[df['quantile'] == 0.1, 'tas'], name="SSP2-4.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 255, 0, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df['quantile'] == 0.5, 'year'], \
            y=df_ssp585.loc[df['quantile'] == 0.5, 'tas'], name="SSP5-8.5 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df['quantile'] == 0.9, 'year'], \
            y=df_ssp585.loc[df['quantile'] == 0.9, 'tas'], name="SSP5-8.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df['quantile'] == 0.1, 'year'], \
            y=df_ssp585.loc[df['quantile'] == 0.1, 'tas'], name="SSP5-8.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(255, 0, 0, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_instrumental['Year'], \
            y=df_instrumental['Value'], name="Instrumental record",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='magenta', width=0.5))
    )
    fig1.update_layout(
        title_text="Graph 4: CMIP6 model ensemble annual global average temperature quantiles and instrumental record",
        legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
    )
    # Set x-axis title
    fig1.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig1.update_yaxes(title_text="Temperature (°C)")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("""Graph 4: Climate model ensemble annual global average temperature quantiles for four different scenarios 
        from year 1850 to year 2100. 
        For each of the three scenarios [SSP1-2.6](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways), 
        [SSP2-4.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) and 
        [SSP5-8.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) each model outputs forecast based on 
        parameters governed by assumptions about socioeconomic factors in the future as well as physical quantities.
        Each model also outputs estimation of historical global average temperatures based on physical quantities
        as well as data from past atmospheric records and proxies. The instrumental record is shown for comparison.""")

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Climate Past and Future',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)
st.title("Global Average Temperature and Greenhouse Gas Concentration:")
st.subheader("""Four interactive graphs showing past and future temperatures as well as atmospheric greenhouse gas concentrations based on paleoclimatic data and climate modeling.""")

st.write("---")

create_ghg_section()
create_ghg_section2()
create_cmip6_section()




