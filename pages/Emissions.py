import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_historic_ghg_data,
    get_per_capita_ghg_data,
    get_pathways_temp_data,
    get_ghg_sector_data,
    get_pathways_ghg_data,
)

st.set_page_config(
    page_title='Climate Change in Graphs: Emissions',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.sidebar.header("Emissions")

st.markdown("# Greenhouse gas emissions")
############################################# Historic GHG plot ###########################################################
df_historic_ghg = get_historic_ghg_data()
df_historic_ghg['total_emissions_co2eq'] = df_historic_ghg[['co2','ch4','n2o']].sum(axis=1)
df_per_capita = get_per_capita_ghg_data()

min_value = df_historic_ghg['Year'].min()
max_value = df_historic_ghg['Year'].max()

from_year, to_year = st.slider(
    "Select year range",
    min_value=min_value,
    max_value=max_value,
    format="%0.0f",
    value=(min_value, max_value),
    key="historic_ghg_slider"
)

col1, col2 = st.columns(2)

with col1:
    selected_graph = st.selectbox("Choose a graph:", ['World total GHG emissions by substance', 'GHG emissions by country', 
        'GHG emissions per capita by country'])

fig1 = make_subplots()

if selected_graph == 'World total GHG emissions by substance':

    df_world = df_historic_ghg[df_historic_ghg.Entity == 'World']
    # Add traces
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.co2, 
            name='CO<sub>2</sub>',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='blue'),
            stackgroup='one')
    )
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.ch4, 
            name='CH<sub>4</sub>',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='red'),
            stackgroup='one')
    )
    fig1.add_trace(
        go.Scatter(x=df_world.Year,
            y=df_world.n2o, 
            name='N<sub>2</sub>O',
            hovertemplate =
            'Value: %{y:.2e} ton'+
            '<br>Year: %{x:.0f}',
            line=dict(color='green'),
            stackgroup='one')
    )
elif selected_graph == 'GHG emissions by country':
    selected_countries = st.multiselect(
            'Select Countries',
            df_historic_ghg.Entity.unique(),
            default = ['United States','China','Russia','European Union (28)'],
            placeholder = "Choose at least one"
    )
    for country in selected_countries:
        fig1.add_trace(
            go.Scatter(x=df_historic_ghg.loc[df_historic_ghg.Entity == country, 'Year'],
                y=df_historic_ghg.loc[df_historic_ghg.Entity == country, 'total_emissions_co2eq'], 
                name=country,
                hovertemplate =
                'Value: %{y:.2e} ton'+
                '<br>Year: %{x:.0f}')
        )
else:
    selected_countries = st.multiselect(
            'Select Countries',
            df_per_capita.Entity.unique(),
            default = ['United States','China','Russia','European Union (27)','United Kingdom','Japan','World'],
            placeholder = "Choose at least one"
    )
    for country in selected_countries:
        fig1.add_trace(
            go.Scatter(x=df_per_capita.loc[df_per_capita.Entity == country, 'Year'],
                y=df_per_capita.loc[df_per_capita.Entity == country, 'ghg'], 
                name=country,
                hovertemplate =
                'Value: %{y:.2e} ton'+
                '<br>Year: %{x:.0f}')
        )

fig1.update_layout(
    title_text=f"Graph 1: {selected_graph} by year in CO<sub>2</sub> equivalent",
    xaxis=dict(range=[from_year, to_year])
)
# # Set x-axis title
fig1.update_xaxes(title_text="Year")

# # Set y-axes titles
fig1.update_yaxes(title_text="Emissions (tons of CO<sub>2</sub> equivalent)")
st.plotly_chart(fig1, use_container_width=True)
st.caption("""Graph 1: World greenhouse gas emissions by substance and total greenhouse gas emissions by country, by year in CO₂ 
    equivalent, emissions from all sources, including agriculture and land-use change. Total greenhouse gas emissions include 
    emissions of carbon dioxide (CO₂), nitrous oxide (N₂O) and methane (CH₄). Data 
    from [Our World in Data](https://ourworldindata.org/grapher/ghg-emissions-by-gas).""")

############################################# Country 2023 GHG plot ###########################################################

col1, col2 = st.columns(2)

with col1:
    selected_graph = st.selectbox("Choose a graph:", ['Cumulative GHG emissions by country 1850-2023',
        'GHG emissions by country 2023', 'Per capita GHG emissions by country 2023'])

if selected_graph == 'Cumulative GHG emissions by country 1850-2023':

    df_countries = df_historic_ghg[(~df_historic_ghg.Code.isnull()) & (df_historic_ghg.Entity != 'World')]
    df_cumulative = df_countries.groupby(by=['Entity','Code'], as_index=False).sum()
    df_cumulative = df_cumulative.rename(columns = {'total_emissions_co2eq' : 'Emissions (tons CO<sub>2</sub> eqv.)'})
    
    fig2 = px.choropleth(df_cumulative, locations="Code",
                    color="Emissions (tons CO<sub>2</sub> eqv.)", 
                    hover_name="Entity", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.turbid,
                    title=f'Graph 2: {selected_graph}')

elif selected_graph == 'GHG emissions by country 2023':

    df_countries = df_historic_ghg[(~df_historic_ghg.Code.isnull()) & (df_historic_ghg.Entity != 'World')]
    df_2023 = df_countries[df_countries.Year == 2023]
    df_2023 = df_2023.rename(columns = {'total_emissions_co2eq' : 'Emissions (tons CO<sub>2</sub> eqv.)'})

    fig2 = px.choropleth(df_2023, locations="Code",
                    color="Emissions (tons CO<sub>2</sub> eqv.)", 
                    hover_name="Entity", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.turbid,
                    title=f'Graph 2: {selected_graph}')

else:

    df_countries = df_per_capita[(~df_per_capita.Code.isnull()) & (df_per_capita.Entity != 'World')]
    df_2023 = df_countries[df_countries.Year == 2023]
    df_2023 = df_2023.rename(columns = {'ghg' : 'Emissions (tons CO<sub>2</sub> eqv.)'})

    fig2 = px.choropleth(df_2023, locations="Code",
                    color="Emissions (tons CO<sub>2</sub> eqv.)", 
                    hover_name="Entity", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.turbid,
                    title=f'Graph 2: {selected_graph}')

fig2.update_layout(
    coloraxis_colorbar=dict(
        orientation="h",  # Horizontal orientation
        yanchor="bottom", # Anchor the legend's bottom to the specified y-coordinate
        y=-0.3,           # Position below the plot area (adjust as needed)
        xanchor="left",   # Anchor the legend's left to the specified x-coordinate
        x=0.13               # Position at the left edge of the plot area
    )
)
st.plotly_chart(fig2, use_container_width=True)
st.caption("""Graph 2: Cumulative total greenhouse gas emissions by country 1850-2023 and total greenhouse gas emissions by 
    country 2023 in CO₂ equivalent, emissions from all sources, including agriculture and land-use change. Total greenhouse 
    gas emissions include emissions of carbon dioxide (CO₂), nitrous oxide (N₂O) and methane (CH₄). Data 
    from [Our World in Data](https://ourworldindata.org/grapher/ghg-emissions-by-gas).""")

############################################# Historic GHG by sector/region plot ###########################################################
df, df_total = get_ghg_sector_data()

df.Emissions *= 1000
df_total.Emissions *= 1000
df = df.rename(columns = {'Emissions' : "Emissions (tons of CO<sub>2</sub> equivalent)"})

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = st.slider(
    "Select year range",
    min_value=min_value,
    max_value=max_value,
    format="%0.0f",
    value=(min_value, max_value),
    key="sector_ghg_slider"
)

col1, col2 = st.columns(2)

with col1:
    selected_graph = st.selectbox("Choose a graph:", ['World total GHG emissions by sector 1970-2024',
        'Regional total GHG emissions by sector 1970-2024 (1)', 'Regional total GHG emissions by sector 1970-2024 (2)'])

if selected_graph == 'World total GHG emissions by sector 1970-2024':
    fig3 = px.area(df_total, x="Year", y="Emissions", color="Sector")
    
    fig3.update_yaxes(title_text="Emissions (tons of CO<sub>2</sub> equivalent)")
elif selected_graph == 'Regional total GHG emissions by sector 1970-2024 (1)':
    
    df1 = df[df.Region.isin(['Europe','Eurasia','North America','Asia Pacific','Middle East'])]

    fig3 = px.area(df1, x="Year", y="Emissions (tons of CO<sub>2</sub> equivalent)", color="Sector", facet_col='Region')

    fig3.update_layout(
        yaxis=dict(range=[0, 10000000000])
    )
else:
    df1 = df[df.Region.isin(['South Asia','Southeast Asia','East Asia','Sub-Saharan Africa','Latin America'])]

    fig3 = px.area(df1, x="Year", y="Emissions (tons of CO<sub>2</sub> equivalent)", color="Sector", facet_col='Region')

    fig3.update_layout(
        yaxis=dict(range=[0, 20000000000])
    )

fig3.update_traces(hovertemplate =
                'Value: %{y:.2e} ton'+
                '<br>Year: %{x:.0f}')

fig3.update_layout(
    title_text=f"Graph 3: {selected_graph} by year in CO<sub>2</sub> equivalent",
    xaxis=dict(range=[from_year, to_year])
)
# # Set x-axis title
fig3.update_xaxes(title_text="Year")

# # Set y-axes titles
st.plotly_chart(fig3, use_container_width=True)
st.caption("""Graph 3: World and regional greenhouse gas emissions by year in CO₂ equivalent, emissions from all sources, 
    excluding land-use, land-use change and forestry (LULUCF). Regional data excludes international aviation and shipping. 
    Total greenhouse gas emissions include all anthropogenic 
    greenhouse gases. Data from [European Commission](https://edgar.jrc.ec.europa.eu/dataset_ghg2025).""")
############################################# Pathways GHG plot ###########################################################
df = get_pathways_ghg_data()

fig4 = make_subplots()

# Add traces
fig4.add_trace(
    go.Scatter(x=df.loc[df.Pathway == 'Historical', 'Year'],
        y=df.loc[df.Pathway == 'Historical', 'Emissions'] * 1000000, 
        name='Historical',
        hovertemplate =
        'Value: %{y:.1e} ton'+
        '<br>Year: %{x:.0f}',
        line=dict(color='black'))
)
# blue range
x = df.loc[df.Pathway == '2030 Targets only', 'Year']
y_lower = df.loc[(df.Pathway == 'Policies and action ') & (df.Limit == 'Low'), 'Emissions'] * 1000000000
y_upper = df.loc[(df.Pathway == 'Policies and action ') & (df.Limit == 'High'), 'Emissions'] * 1000000000
fig4.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Policies and action',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)
fig4.add_annotation(x=2100, y=y_upper.values[-1],
            text="+2.9°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(0,0,255,0.6)'),
            captureevents=True,
            hovertext="+2.9°C warming projected by 2100"
)
fig4.add_annotation(x=2100, y=y_lower.values[-1],
            text="+2.5°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(0,0,255,0.6)'),
            captureevents=True,
            hovertext="+2.5°C warming projected by 2100"
)

y_lower = df.loc[(df.Pathway == 'Pledges and Targets') & (df.Limit == 'Low '), 'Emissions'] * 1000000000
y_upper = df.loc[(df.Pathway == 'Pledges and Targets') & (df.Limit == 'High'), 'Emissions'] * 1000000000
# blue-green range
fig4.add_trace(
    go.Scatter(x=x,
        y=y_upper, 
        name="Pledges and targets",
        hoverinfo = 'skip',
        line=dict(color='rgba(29, 140, 173,0.2)', width=0.1),
        showlegend=False)
)
fig4.add_trace(
    go.Scatter(x=x,
        y=y_lower, 
        name='Pledges and targets',
        fill='tonexty',
        fillcolor='rgba(29, 140, 173,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(29, 140, 173,0.2)', width=0.1))
)
fig4.add_annotation(x=2100, y=y_upper.values[-1],
            text="+2.1°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(29, 140, 173,0.6)'),
            captureevents=True,
            hovertext="+2.1°C warming projected by 2100"
)
# blue-green line
y = df.loc[df.Pathway == 'Optimistic scenario (net-zero pledges)', 'Emissions'] * 1000000000
fig4.add_trace(
    go.Scatter(x=df.loc[df.Pathway == 'Optimistic scenario (net-zero pledges)', 'Year'],
        y=y, 
        name='Optimistic scenario',
        hovertemplate =
        'Value: %{y:.1e} ton'+
        '<br>Year: %{x:.0f}',
        line=dict(color='rgb(29, 140, 173)'))
)
fig4.add_annotation(x=2100, y=y.values[-1],
            text="+1.9°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgb(29, 140, 173)'),
            captureevents=True,
            hovertext="+1.9°C warming projected by 2100"
)
# blue line
y = df.loc[df.Pathway == '2030 Targets only', 'Emissions'] * 1000000000
fig4.add_trace(
    go.Scatter(x=df.loc[df.Pathway == '2030 Targets only', 'Year'],
        y=y, 
        name='2030 targets only',
        hovertemplate =
        'Value: %{y:.1e} ton'+
        '<br>Year: %{x:.0f}',
        line=dict(color='blue'))
)
fig4.add_annotation(x=2100, y=y.values[-1],
            text="+2.6°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(0,0,255,1)'),
            captureevents=True,
            hovertext="+2.6°C warming projected by 2100"
)
y_lower = df.loc[(df.Pathway == '1.5C compatible') & (df.Limit == 'Low'), 'Emissions'] * 1000000000
y_upper = df.loc[(df.Pathway == '1.5C compatible') & (df.Limit == 'High'), 'Emissions'] * 1000000000
y_median = df.loc[(df.Pathway == '1.5C compatible') & (df.Limit == 'Median '), 'Emissions'] * 1000000000
# green
fig4.add_trace(
    go.Scatter(x=x,
        y=y_median, 
        name='1.5°C compatible',
        hovertemplate =
        'Value: %{y:.1e} ton'+
        '<br>Year: %{x:.0f}',
        line=dict(color='rgb(188, 189, 34)', dash='dash'))
)
fig4.add_annotation(x=2100, y=y_median.values[-1],
            text="+1.5°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgb(188, 189, 34)'),
            captureevents=True,
            hovertext="+1.5°C warming projected by 2100"
)
# green range
fig4.add_trace(
    go.Scatter(x=x,
        y=y_upper, 
        name="1.5°C compatible",
        hoverinfo = 'skip',
        line=dict(color='rgba(188, 189, 34,0.2)', width=0.1),
        showlegend=False)
)
fig4.add_trace(
    go.Scatter(x=x,
        y=y_lower, 
        name='1.5°C compatible (range)',
        fill='tonexty',
        fillcolor='rgba(188, 189, 34,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(188, 189, 34,0.2)', width=0.1))
)
fig4.update_layout(
    title_text=f"Graph 4: GHG emission pathways up to year 2100 in CO<sub>2</sub> equivalent",
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
fig4.update_yaxes(title_text="Emissions (tons of CO<sub>2</sub> equivalent)")
st.plotly_chart(fig4, use_container_width=True)
st.caption("""Graph 4: Past and future GHG emission pathways up to year 2100 in CO₂ equivalent. Corresponding 
    warming (relative to pre-industrial) by the year 2100 shown to the right of lines/ranges. Each pathway or range of pathways 
    is based on future scenario of implementation of policies or climate action (Climate Action Tracker, 2024). "Policies and 
    action" (blue range) corresponds 
    to a scenario where future emissions are governed by current policies. "2030 targets only" (blue line) correspongs to a 
    scenario where only Nationally Determined Contributions (NDCs) for the target year 2030 are implemented in the future. 
    "Pledges and targets" (blue-green range) pathways are based on 2030 NDC targets as well as the implementation of submitted 
    and binding long-term targets. "Optimistic scenario" describes a scenario of full implementation of all announced targets, 
    including net-zero targets. The light-green dashed line corresponds to implementation of policies that would meet the Paris agreement goal 
    of limiting warming to 1.5°C. All pathways are based on 2022 emissions. Historical emissions data 
    from [European Commission](https://edgar.jrc.ec.europa.eu/report_2025). Other data and graph exemplar from [Climate Action Tracker](https://climateactiontracker.org/global/emissions-pathways/).""")
############################################# Pathways temp plot ###########################################################
df = get_pathways_temp_data()

fig5 = make_subplots()

# Add traces
# blue range
x = df.loc[df.Pathway == '2030 Targets only', 'Year']
y_lower = df.loc[(df.Pathway == 'Policies and action ') & (df.Limit == 'Low'), 'gmt']
y_upper = df.loc[(df.Pathway == 'Policies and action ') & (df.Limit == 'High'), 'gmt']

fig5.add_trace(
    go.Scatter(x=pd.concat([x, x[::-1]]),
        y=pd.concat([y_upper, y_lower[::-1]]), 
        name='Policies and action',
        mode='lines',
        fill='toself',
        fillcolor='rgba(0,0,255,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(0,0,255,0.2)', width=0.1))
)
fig5.add_annotation(x=2100, y=y_upper.values[-1],
            text="+2.9°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(0,0,255,0.6)'),
            captureevents=True,
            hovertext="+2.9°C warming projected by 2100"
)
fig5.add_annotation(x=2100, y=y_lower.values[-1],
            text="+2.5°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(0,0,255,0.6)'),
            captureevents=True,
            hovertext="+2.5°C warming projected by 2100"
)
y_lower = df.loc[(df.Pathway == 'Pledges and Targets') & (df.Limit == 'Low'), 'gmt']
y_upper = df.loc[(df.Pathway == 'Pledges and Targets') & (df.Limit == 'High'), 'gmt']
# blue-green range
fig5.add_trace(
    go.Scatter(x=x,
        y=y_upper, 
        name="Pledges and targets",
        mode='lines',
        hoverinfo = 'skip',
        line=dict(color='rgba(29, 140, 173,0.2)', width=0.1),
        showlegend=False)
)
fig5.add_trace(
    go.Scatter(x=x,
        y=y_lower, 
        name='Pledges and targets',
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(29, 140, 173,0.2)',
        hoverinfo="skip",
        line=dict(color='rgba(29, 140, 173,0.2)', width=0.1))
)
fig5.add_annotation(x=2100, y=y_upper.values[-1],
            text="+2.1°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgba(29, 140, 173,0.6)'),
            captureevents=True,
            hovertext="+2.1°C warming projected by 2100"
)
# blue-green line
y = df.loc[df.Pathway == 'Optimistic scenario (net-zero pledges)', 'gmt']
fig5.add_trace(
    go.Scatter(x=df.loc[df.Pathway == 'Optimistic scenario (net-zero pledges)', 'Year'],
        y=y, 
        name='Optimistic scenario',
        mode='lines',
        hovertemplate =
        'Value: %{y:.1f} °C'+
        '<br>Year: %{x:.0f}',
        line=dict(color='rgb(29, 140, 173)'))
)
fig5.add_annotation(x=2100, y=y.values[-1],
            text="+1.9°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgb(29, 140, 173)'),
            captureevents=True,
            hovertext="+1.9°C warming projected by 2100"
)
# blue line
y = df.loc[df.Pathway == '2030 Targets only', 'gmt']
fig5.add_trace(
    go.Scatter(x=df.loc[df.Pathway == '2030 Targets only', 'Year'],
        y=y, 
        name='2030 targets only',
        mode='lines',
        hovertemplate =
        'Value: %{y:.1f} °C'+
        '<br>Year: %{x:.0f}',
        line=dict(color='blue'))
)
fig5.add_annotation(x=2100, y=y.values[-1],
            text="+2.6°C",
            showarrow=False,
            xshift=18,
            yshift=4,
            font = dict(color='rgba(0,0,255,1)'),
            captureevents=True,
            hovertext="+2.6°C warming projected by 2100"
)
y = df.loc[(df.Pathway == 'Paris agreement'), 'gmt']
# green line
fig5.add_trace(
    go.Scatter(x=x,
        y=y, 
        name='1.5°C compatible',
        mode='lines',
        hovertemplate =
        'Value: %{y:.1f} °C'+
        '<br>Year: %{x:.0f}',
        line=dict(color='rgb(188, 189, 34)'))
)
fig5.add_annotation(x=2100, y=y.values[-1],
            text="+1.5°C",
            showarrow=False,
            xshift=18,
            font = dict(color='rgb(188, 189, 34)'),
            captureevents=True,
            hovertext="+1.5°C warming projected by 2100"
)
fig5.add_trace(
    go.Scatter(x=df.loc[df.Pathway == 'Historical', 'Year'],
        y=df.loc[df.Pathway == 'Historical', 'gmt'], 
        name='Historical',
        mode="lines+markers+text",
        text=["+0.6°C", "+0.8°C", "+1.0°C", "", "+1.3°C"],
        textposition="top center",
        hovertemplate =
        'Value: %{y:.1f} °C'+
        '<br>Year: %{x:.0f}',
        line=dict(color='black'))
)
fig5.update_layout(
    title_text=f"Graph 5: Projected warming corresponding to emission pathways",
    legend=dict(
            x=0.1,  # x-position (0.1 is near left)
            y=0.7,  # y-position (0.9 is near top)
            xref="container",
            yref="container",
            orientation = 'h'
        )
)
# # Set x-axis title
fig5.update_xaxes(title_text="Year")

# # Set y-axes titles
fig5.update_yaxes(title_text="Warming since pre-industrial (°C)")
st.plotly_chart(fig5, use_container_width=True)
st.caption("""Graph 5: Projected warming (relative to pre-industrial) corresponding to emission pathways. Each pathway or range of pathways 
    is based on future scenario of implementation of policies or climate action (Climate Action Tracker, 2024). "Policies and 
    action" (blue range) corresponds 
    to a scenario where future emissions are governed by current policies. "2030 targets only" (blue line) correspongs to a 
    scenario where only Nationally Determined Contributions (NDCs) for the target year 2030 are implemented in the future. 
    "Pledges and targets" (blue-green range) pathways are based on 2030 NDC targets as well as the implementation of submitted 
    and binding long-term targets. "Optimistic scenario" describes a scenario of full implementation of all announced targets, 
    including net-zero targets. The light-green corresponds to implementation of policies that would meet the Paris agreement goal 
    of limiting warming to 1.5°C. All pathways are based on 2022 emissions. Data and graph exemplar from [Climate Action Tracker](https://climateactiontracker.org/global/emissions-pathways/).""")
###########################################################################################################################
st.markdown("### References")

st.markdown(
    """*Greenhouse gas emissions, world total and by country (Graphs 1 and 2)*  \nJones, M. W., Peters, G. P., Gasser, T., Andrew, 
    R. M., Schwingshackl, C., Gütschow, J., Houghton, R. A., Friedlingstein, P., Pongratz, J., & Le Quéré, C. (2024) – with major 
    processing by Our World in Data. “Annual carbon dioxide, methane and nitrous oxide emissions including land use” [dataset]. 
    Jones et al., “National contributions to climate change 2024.2” [original data].
    Accessed 2025-10-21."""
)
st.markdown(
    """*Greenhouse gas emissions, world and regional total by sector (Graph 3)*  \nEDGAR (Emissions Database for Global 
    Atmospheric Research) Community GHG Database, a collaboration between the European Commission, Joint Research Centre (JRC), 
    the International Energy Agency (IEA), and comprising IEA-EDGAR CO2, EDGAR CH4, EDGAR N2O, EDGAR F-GASES version 
    EDGAR_2025_GHG (2025) European Commission, JRC (Datasets). The complete citation of the EDGAR Community GHG Database is 
    available in the 'Sources and References' section.
    Accessed 2025-10-23."""
)
st.markdown(
    """*Emission pathways up to year 2100 (Graphs 4 and 5)*  \nClimate Action Tracker (2024). 2100 Warming Projections: Emissions and 
    expected warming based on pledges and current policies. November 2024. Available 
    at: https://climateactiontracker.org/global/temperatures/. Copyright ©2024 by Climate Analytics and NewClimate Institute. 
    All rights reserved.
    Accessed 2025-10-22."""
)
