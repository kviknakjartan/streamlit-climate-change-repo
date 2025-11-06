import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_cmip6_data,
    get_be_global_data,
    get_be_global_data2,
    get_gistemp_global_data,
    get_hadcrut_global_data,
    get_osman_data,
    get_parrenin_data,
    get_co2_latest_data,
    get_ch4_latest_data,
    get_n2o_latest_data,
    get_co2_hist_data,
    get_ch4_hist_data,
    get_n2o_hist_data,
    get_noaa_global_data
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
        #st.session_state[f"{label}_slider"] = (lower_bound, upper_bound)
        selected_range = (lower_bound, upper_bound)

    return selected_range


def get_and_combine_ghg_data():
    df = pd.concat([get_co2_hist_data(), get_ch4_hist_data(), get_n2o_hist_data(), \
        get_co2_latest_data(), get_ch4_latest_data(), get_n2o_latest_data(), get_parrenin_data()])
    return df

def get_and_combine_temp_data():
    df = pd.concat([get_osman_data(), get_be_global_data(), get_co2_hist_data(), get_co2_latest_data()])
    return df

def create_instrumental_temperature_section():
    df = get_be_global_data2()

    min_value = df['Year'].min()
    max_value = df['Year'].max()

    from_year, to_year = range_slider_with_inputs("What timescale are you interested in?", \
        'instrumental', min_value*1.0, max_value*1.0, (min_value*1.0, max_value*1.0))


    # Instrumental temperature plot
    fig0 = make_subplots()

    selected_graph = st.selectbox("Select graph:", ['Global mean surface temperature with uncertainty 1850 to present', 
            'Global mean surface temperature anomaly for four different datasets 1850 to present'])

    if selected_graph == 'Global mean surface temperature with uncertainty 1850 to present':

        # Add traces
        fig0.add_trace(
            go.Scatter(x=df['Year'], \
                y=df['Five-year Anomaly'] + 14.102, 
                name="Five-year moving average",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='blue'))
        )
        y_max = df['Five-year Anomaly'] + df['Five-year Unc.'] + 14.102
        y_min = df['Five-year Anomaly'] - df['Five-year Unc.'] + 14.102
        fig0.add_trace(
            go.Scatter(x=df['Year'], \
                y=y_max, 
                name="Five-year uncertainty",
                hoverinfo = 'skip',
                line=dict(color='blue', width=0.1),
                showlegend=False)
        )
        fig0.add_trace(
            go.Scatter(x=df['Year'], \
                y=y_min, 
                name="Five-year uncertainty",
                hoverinfo = 'skip',
                line=dict(color='blue', width=0.1),
                fill='tonexty',
                fillcolor = 'rgba(0, 0, 255, 0.2)')
        )
        fig0.add_trace(
            go.Scatter(x=df['Year'], \
                y=df['Annual Anomaly'] + 14.102, 
                name="Annual average",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='magenta', width=1))
        )
    else:
        df_gistemp = get_gistemp_global_data()
        df_hadcrut = get_hadcrut_global_data()
        df_noaa = get_noaa_global_data()

        # Add traces
        fig0.add_trace(
            go.Scatter(x=df['Year'],
                y=df['Five-year Anomaly'], 
                name="Berkeley Earth",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='blue'))
        )
        fig0.add_trace(
            go.Scatter(x=df_gistemp['Year'],
                y=df_gistemp['Five-year Anomaly'], 
                name="GISTEMPv4",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='red'))
        )
        fig0.add_trace(
            go.Scatter(x=df_hadcrut['Time'],
                y=df_hadcrut['Five-year Anomaly'], 
                name="HADCRUT5",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='green'))
        )
        fig0.add_trace(
            go.Scatter(x=df_noaa['Year'],
                y=df_noaa['Five-year Anomaly'], 
                name="NOAAGlobalTempv6",
                hovertemplate =
                'Value: %{y:.1f} °C'+
                '<br>Year: %{x:.0f}',
                line=dict(color='magenta'))
        )
    fig0.update_layout(
        title_text="Graph 1: Global mean surface temperature (instrumental record) 1850 to present",
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
    fig0.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig0.update_yaxes(title_text="Global mean temperature (°C)")
    st.plotly_chart(fig0, use_container_width=True)
    st.caption("""Graph 1: Global mean surface temperature with uncertainty and global mean temperature anomaly for four different 
        datasets, 1850 to present. On the former graph a 5-year moving average is shown as well as annual average and 
        uncertainty for the 5-year average. On the latter graph 5-year moving averages are shown for each dataset.
        See references for data access.""")

def create_ghg_section():
    st.write("")

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
        title_text="Graph 2: Global atmospheric concentrations for selected greenhouse gases",
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
    st.caption("""Graph 2: Estimated global atmospheric concentration levels of three greenhouse gases for the past ~800,000 years.
        Based on Antarctic icecore data. Also shown are modern measured annual average levels (instrumental record).
        See references for data access.""")

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
        title_text="Graph 3: Estimated Antarctic air temperature change and global CO<sub>2</sub> concentration",
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
    st.caption("""Graph 3: Recostruction of Antarctic air temperature change for the past ~800,000 years, based on Antarctic 
        icecore data from five different sites, and estimation of past carbon dioxide levels based on Antarctic icecore data. Temperature data from
        [PANGAEA](https://doi.org/10.1594/PANGAEA.810188).""")
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
        title_text="Graph 4: Estimated annual global mean surface temperature and CO<sub>2</sub> concentration",
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
    st.caption("""Graph 4: Recostruction of annual global mean temperature for the past ~24,000 years based on climate modeling and geochemical proxy data,
         estimation of past carbon dioxide levels based on Antarctic icecore data and modern measured temperature and 
         carbon dioxide levels (instrumental record). Temperature reconstruction data from [NOAA](https://doi.org/10.25921/njxd-hg08).
         Temperature instrumental record from [The Berkeley Earth Land/Ocean Temperature Record](https://doi.org/10.5194/essd-12-3469-2020).""")

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
        go.Scatter(x=df_historical.loc[df_historical['quantile'] == 0.5, 'year'], \
            y=df_historical.loc[df_historical['quantile'] == 0.5, 'tas'], name="historical 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black'))
    )
    fig1.add_trace(
        go.Scatter(x=df_historical.loc[df_historical['quantile'] == 0.9, 'year'], \
            y=df_historical.loc[df_historical['quantile'] == 0.9, 'tas'], name="historical 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_historical.loc[df_historical['quantile'] == 0.1, 'year'], \
            y=df_historical.loc[df_historical['quantile'] == 0.1, 'tas'], name="historical 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='black', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 0, 0, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df_ssp126['quantile'] == 0.5, 'year'], \
            y=df_ssp126.loc[df_ssp126['quantile'] == 0.5, 'tas'], name="SSP1-2.6 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df_ssp126['quantile'] == 0.9, 'year'], \
            y=df_ssp126.loc[df_ssp126['quantile'] == 0.9, 'tas'], name="SSP1-2.6 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp126.loc[df_ssp126['quantile'] == 0.1, 'year'], \
            y=df_ssp126.loc[df_ssp126['quantile'] == 0.1, 'tas'], name="SSP1-2.6 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 0, 255, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df_ssp245['quantile'] == 0.5, 'year'], \
            y=df_ssp245.loc[df_ssp245['quantile'] == 0.5, 'tas'], name="SSP2-4.5 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df_ssp245['quantile'] == 0.9, 'year'], \
            y=df_ssp245.loc[df_ssp245['quantile'] == 0.9, 'tas'], name="SSP2-4.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp245.loc[df_ssp245['quantile'] == 0.1, 'year'], \
            y=df_ssp245.loc[df_ssp245['quantile'] == 0.1, 'tas'], name="SSP2-4.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green', width=0.1),
            fill='tonexty',
            fillcolor = 'rgba(0, 255, 0, 0.2)')
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df_ssp585['quantile'] == 0.5, 'year'], \
            y=df_ssp585.loc[df_ssp585['quantile'] == 0.5, 'tas'], name="SSP5-8.5 50th quantile",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red'))
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df_ssp585['quantile'] == 0.9, 'year'], \
            y=df_ssp585.loc[df_ssp585['quantile'] == 0.9, 'tas'], name="SSP5-8.5 10th/90th quantiles",
            hovertemplate =
            'Value: %{y:.1f} °C'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red', width=0.1),
            showlegend=False)
    )
    fig1.add_trace(
        go.Scatter(x=df_ssp585.loc[df_ssp585['quantile'] == 0.1, 'year'], \
            y=df_ssp585.loc[df_ssp585['quantile'] == 0.1, 'tas'], name="SSP5-8.5 10th/90th quantiles",
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
        title_text="Graph 5: CMIP6 model ensemble annual global mean temperature quantiles and instrumental record 1850-2100",
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
    st.caption("""Graph 5: Climate model ensemble annual global mean temperature quantiles for four different scenarios 
        from year 1850 to year 2100. Shown are quantiles for the output of 37 models.
        For each of the three scenarios [SSP1-2.6](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways), 
        [SSP2-4.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) and 
        [SSP5-8.5](https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways) each model outputs forecast based on 
        parameters governed by assumptions about socioeconomic factors in the future as well as physical quantities.
        Each model also outputs estimation of historical global mean temperatures based on physical quantities
        as well as data from past atmospheric records and proxies. The instrumental record is shown for comparison. 
        Graph adopted from [Copernicus Climate Change Service (C3S) Data Tutorials](https://ecmwf-projects.github.io/copernicus-training-c3s/intro.html).
        CMIP6 data from [Copernicus Climate Change Service, Climate Data Store](https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview).""")

st.set_page_config(
    page_title='Climate Change in Graphs: Temperature',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.sidebar.header("Temperature")

st.markdown("# Global Mean Temperature and Greenhouse Gas Concentration")

create_instrumental_temperature_section()
create_ghg_section()
create_ghg_section2()
create_cmip6_section()


st.markdown("### References")

st.markdown(
    f"""*Global mean surface instrumental temperature (Graph 1)*  \nGISTEMP Team, 2025: GISS Surface Temperature Analysis 
    (GISTEMP), version 4. NASA Goddard Institute for Space Studies. 
    Dataset accessed {date.today()} at https://data.giss.nasa.gov/gistemp/."""
)
st.markdown(
    """*Global mean surface instrumental temperature (Graph 1)*  \nLenssen, N., G.A. Schmidt, M. Hendrickson, P. Jacobs, 
    M. Menne, and R. Ruedy, 2024: A GISTEMPv4 observational uncertainty ensemble. J. Geophys. Res. Atmos., 129, no. 17, 
    e2023JD040179, doi:10.1029/2023JD040179."""
)
st.markdown(
    f"""*Global mean surface instrumental temperature (Graph 1)*  \nMorice, C. P., Kennedy, J. J., Rayner, N. A., Winn, 
    J. P., Hogan, E., Killick, R. E., et al. (2021). An updated assessment of near-surface temperature change from 1850: 
    the HadCRUT5 data set. Journal of Geophysical Research: Atmospheres, 126, 
    e2019JD032361. https://doi.org/10.1029/2019JD032361.
    Accessed {date.today()}."""
)
st.markdown(
    f"""*Global mean surface instrumental temperature (Graph 1)*  \nHuang, B., X. Yin, M. J. Menne, R. Vose, and H. 
    Zhang, NOAA Global Surface Temperature Dataset (NOAAGlobalTemp), Version 6.0.0 
    [aravg.ann.land_ocean.90S.90N.v6.0.0.202508.asc]. NOAA National Centers for Environmental 
    Information. https://doi.org/10.25921/rzxg-p717.
    Accessed {date.today()}."""
)
st.markdown(
    f"""*Global mean surface instrumental temperature (Graphs 1, 4 and 5)*  \nRohde, R. A. and Hausfather, Z.: 
    The Berkeley Earth Land/Ocean Temperature Record, Earth Syst. Sci. Data, 12, 3469-3479, 
    https://doi.org/10.5194/essd-12-3469-2020, 2020. 
    Accessed {date.today()}."""
)
st.markdown(
    """*Antarctic ice core data (Graphs 2,3 and 4)*  \nUnited States Environmental Protection Agency. (2010). 
    Climate Change Indicators: Atmospheric Concentrations of Greenhouse Gases (Updated June 2024) [Dataset]. 
    US EPA. https://www.epa.gov/climate-indicators/climate-change-indicators-atmospheric-concentrations-greenhouse-gases.  
    Accessed September 19, 2025."""
)
st.markdown(
    """*Latest Atmospheric Carbon Dioxide (CO<sub>2</sub>) concentration (Graphs 2,3 and 4)*  \nLan, X., Tans, P. and K.W. Thoning: 
    Trends in globally-averaged CO2 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09 https://doi.org/10.15138/9N0H-ZH07. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Latest Atmospheric Methane (CH<sub>4</sub>) and Nitrous Oxide (N<sub>2</sub>O) concentrations (Graph 2)*  \nLan, X., 
    K.W. Thoning, and E.J. Dlugokencky: 
    Trends in globally-averaged CH4, N2O, and SF6 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09, https://doi.org/10.15138/P8XG-AA10. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Antarctic temperature data (Graph 3)*  \nParrenin, Frédéric; Masson-Delmotte, Valerie; 
    Köhler, Peter; Raynaud, Dominique; Paillard, Didier; Schwander, Jakob; Barbante, Carlo; Landais, Amaëlle; Wegner, Anna; 
    Jouzel, Jean (2013): Antarctic Temperature Stack (ATS) from five different ice cores (EDC, Vostok, Dome Fuji, TALDICE, 
    and EDML) [dataset]. PANGAEA, https://doi.org/10.1594/PANGAEA.810188,  \nIn supplement to: Parrenin, F et al. (2013): 
    Synchronous change of atmospheric CO2 and Antarctic temperature during the last deglacial warming. Science, 
    339(6123), 1060-1063, https://doi.org/10.1126/science.1226368.  \nAccessed September 23, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Global surface temperatures since the last glacial maximum (Graph 4)*  \nMatthew B. Osman, Jessica E. Tierney, 
    Jiang Zhu, Robert Tardif, Gregory J. Hakim, Jonathan King, Christopher J. Poulsen. 2021. 
    Globally resolved surface temperatures since the Last Glacial Maximum. Nature, 599, 239-244. 
    doi: 10.1038/s41586-021-03984-4. 
    Accessed from https://doi.org/10.25921/njxd-hg08, September 19, 2025."""
)
st.markdown(
    """*CMIP6 model output data (Graph 5)*  \nCopernicus Climate Change Service, Climate Data Store, 
    (2021): CMIP6 climate projections. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). 
    DOI: 10.24381/cds.c866074c. Accessed from https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview
    (Accessed on 2025-09-24)."""
)
st.markdown(
    """*CMIP6 model output plot original work (Graph 5)*  \nCopernicus Climate Change Service (C3S) Data Tutorials: 
    Plot an Ensemble of CMIP6 Climate Projections. (2022). Copernicus Climate Change Service (C3S). 
    https://ecmwf-projects.github.io/copernicus-training-c3s/projections-cmip6.html
    (Accessed on 2025-09-24)."""
)




