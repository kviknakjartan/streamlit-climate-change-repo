import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_erf_historic_data,
    get_warming_historic_data
)

st.set_page_config(
    page_title='Climate Change in Graphs: Quantities',
    page_icon='sun.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

def hex_to_rgb(hex_color):
    """
    Converts a hexadecimal color string to an RGB tuple.

    Args:
        hex_color (str): The hexadecimal color string (e.g., "#RRGGBB" or "RRGGBB").

    Returns:
        tuple: An RGB tuple (red, green, blue) where each component is an integer
               between 0 and 255.
    """
    hex_color = hex_color.lstrip('#')  # Remove '#' if present
    
    # Ensure the hex string has 6 characters
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format. Expected 6 characters (e.g., 'RRGGBB').")

    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    return (red, green, blue)

def plot_quantity_with_uncertainty_by_year(fig, years, quantity, quantity_lower, quantity_upper, name, unit, color):
    # Add traces
    fig.add_trace(
        go.Scatter(x=years,
            y=quantity, 
            name=name,
            hovertemplate =
            'Value: %{y:.3f} ' + unit +
            '<br>Year: %{x:.0f}',
            line=dict(color=f'rgb({color[0]},{color[1]},{color[2]})'))
    )

    fig.add_trace(
        go.Scatter(x=pd.concat([years, years[::-1]]),
            y=pd.concat([quantity_upper, quantity_lower[::-1]]), 
            name=name + ' uncertainty',
            fill='toself',
            fillcolor=f'rgba({color[0]},{color[1]},{color[2]},0.2)',
            hoverinfo="skip",
            line=dict(color=f'rgba({color[0]},{color[1]},{color[2]},0.2)', width=0.1),
            showlegend=False)
    )
    return fig

st.sidebar.header("Quantities")

st.markdown("# Physical quantities")

#################### Evolution of ERF #############################

df, df_05, df_95 = get_erf_historic_data()

fig1 = make_subplots()

names = ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'volcanic', 'solar', 'aerosol','land_use']
labels = ['Carbon dioxide (CO<sub>2</sub>)','Methane (CH<sub>4</sub>)','Nitrous oxide (N<sub>2</sub>O)',
    'Other well-mixed GHG','Ozone (O<sub>3</sub>)', 'Volcanic','Solar','Aerosol','Land use (albedo)']
colors = [(52, 91, 235),(59, 156, 23),(209, 109, 197),(205, 209, 75),(55, 179, 204),(99, 90, 43),(217, 188, 28),
    (105, 90, 98),(145, 207, 207)]

for var_name, label, color in zip(names, labels, colors):
    fig1 = plot_quantity_with_uncertainty_by_year(fig1, df.year, df[var_name], df_05[var_name], df_95[var_name], 
        label, 'W m<sup>-2</sup>', color)

fig1.add_trace(
    go.Scatter(x=df.year,
        y=df['total'], 
        name='Total',
        hovertemplate =
        'Value: %{y:.3f} W m<sup>-2</sup>' + 
        '<br>Year: %{x:.0f}',
        line=dict(color='black', width=0.7))
)

fig1.update_layout(
    title_text=f"Graph 1: Evolution of effective radiative forcing (ERF) 1750-2019",
    
)
# Set x-axis title
fig1.update_xaxes(title_text="Year")

# Set y-axes titles
fig1.update_yaxes(title_text="Effective radiative forcing (W m<sup>-2</sup>)")
st.plotly_chart(fig1, use_container_width=True)

st.caption(f"""Graph 1: Evolution of effective radiative forcing (ERF) 1750-2019. Effective radiative forcing is the energy 
    gained or lost by the Earth that results from an event or activity, such as the addition of greenhouse gases or aerosols. 
    It is a fundamental driver of changes in the energy budget of the Earth at the top of the atmosphere (Forster et. al., 2021). 
    Shaded regions show the "very likely" (5-95%) ranges. 
    Data from [IPCC](https://ipcc-browser.ipcc-data.org/browser/dataset/7506/0).""")

#################### Change in ERF #############################

labels = ['Carbon dioxide (CO<sub>2</sub>)', 'Other well-mixed GHG','Ozone (O<sub>3</sub>)', 'Water vapour (Stratosphere)', 
    'Albedo', 'Contrails', 'Aerosols', 'Total anthropogenic', 'Solar']

data = [[2.16, 0.25, 0.26, 0, True, 'rgb(201, 14, 55)', 0, 'Carbon dioxide (CO<sub>2</sub>)', False],
        [0.54, 0.11, 0.11, 0, False, 'rgb(143, 14, 42)', 1, 'Methane (CH<sub>4</sub>)', True],
        [0.21, 0.03, 0.03, 0.54, False, 'rgb(232, 93, 23)', 1, 'Nitrous oxide (N<sub>2</sub>O)', True],
        [0.41, 0.08, 0.08, 0.75, False, 'rgb(232, 186, 35)', 1, 'Halogens', True],
        [0.47, 0.24, 0.23, 0, True, 'rgb(201, 14, 55)', 2, 'Ozone (O<sub>3</sub>)', False],
        [0.05, 0.05, 0.05, 0, True, 'rgb(201, 14, 55)', 3, 'Water vapour (Stratosphere)', False],
        [0.08, 0.1, 0.08, 0, True, 'rgb(219, 114, 132)', 4, 'Dark particles on ice', True],
        [-0.2, 0.1, 0.1, -0.2, False, 'rgb(8, 10, 102)', 4, 'Land use', True],
        [0.06, 0.04, 0.04, 0, True, 'rgb(201, 14, 55)', 5, 'Contrails', False],
        [-0.22, 0.26, 0.25, -0.22, False, 'rgb(33, 36, 184)', 6, 'Aerosol-radiation', True],
        [-0.84, 0.59, 0.61, -1.06, False, 'rgb(108, 110, 186)', 6, 'Aerosol-cloud', True],
        [2.72, 0.76, 0.76, 0, True, 'rgb(201, 14, 55)', 7, 'Total anthropogenic', False],
        [-0.02, 0.08, 0.06, -0.02, False, 'rgb(160, 70, 179)', 8, 'Solar', False]]  

fig2 = go.Figure()

for i,row in enumerate(data):

    bar_lenghts = [0] * len(labels)
    bar_lenghts[row[6]] = np.abs(row[0])
    pos_errors = [0] * len(labels)
    pos_errors[row[6]] = row[1]
    neg_errors = [0] * len(labels)
    neg_errors[row[6]] = row[2]
    bases = [99] * len(labels)
    bases[row[6]] = row[3]

    customdata = np.array([row[0:3]] * len(labels))
    customdata[:,1] = customdata[:,0] + customdata[:,1]
    customdata[:,2] = customdata[:,0] - customdata[:,2]

    fig2.add_trace(go.Bar(
        name=row[7],
        x=labels,
        y=bar_lenghts,
        hovertemplate =
            'Value: %{customdata[0]:.2f} W m<sup>-2</sup>'+
            '<br>Range: [%{customdata[2]:.2f} to %{customdata[1]:.2f}] W m<sup>-2</sup>',
        customdata = customdata,
        error_y=dict(
                type='data',  # Indicates error values are provided as data
                symmetric=False,  # Crucial for non-symmetric error bars
                array=pos_errors,  # Positive error values
                arrayminus=neg_errors,  # Negative error values
                visible=row[4]
            ),
        base=bases,
        showlegend=row[8],
        marker_color=row[5]
    ))

fig2.add_trace(go.Bar(
        name='Invisible bars',
        x=labels,
        y=[0] * len(labels),
        error_y=dict(
                type='data',  # Indicates error values are provided as data
                symmetric=False,  # Crucial for non-symmetric error bars
                array=[0, 0.22, 0, 0, 0.1, 0, 0.85, 0, 0.08],  # Positive error values
                arrayminus=[0, 0.22, 0, 0, 0.1, 0, 0.86, 0, 0.06],  # Negative error values
                visible=True
            ),
        base=[99, 1.16, 99, 99, -0.2, 99, -1.06, 99, -0.02],
        showlegend=False
))

fig2.update_layout(
    barmode='stack', 
    title='Graph 2: Change in effective radiative forcing (ERF) 1750-2019',
    yaxis=dict(range=[-2, 4]),
    )
fig2.update_yaxes(title_text="Effective radiative forcing (W m<sup>-2</sup>)")

st.plotly_chart(fig2, use_container_width=True)

st.caption("""Graph 2: Change in effective radiative forcing (ERF) 1750-2019 by forcing agents. Solid bars represent best 
    estimates, and "very likely" (5–95%) ranges are given by error bars. Plot adopted from Forster et. al. (2021)""")

#################### Evolution of warming #############################

df = get_warming_historic_data()

fig3 = make_subplots()

names = ['CO2', 'CH4', 'N2O', 'otherGHG', 'O3', 'volcanic', 'solar', 'aerosol']
labels = ['Carbon dioxide (CO<sub>2</sub>)','Methane (CH<sub>4</sub>)','Nitrous oxide (N<sub>2</sub>O)',
    'Other well-mixed GHG','Ozone (O<sub>3</sub>)', 'Volcanic','Solar','Aerosol']
colors = [(52, 91, 235),(59, 156, 23),(209, 109, 197),(205, 209, 75),(55, 179, 204),(99, 90, 43),(217, 188, 28),
    (105, 90, 98)]

for var_name, label, color in zip(names, labels, colors):
    fig3 = plot_quantity_with_uncertainty_by_year(fig3, df.year, df[var_name + '_best'], df[var_name + '_p05'], 
        df[var_name + '_p95'], label, '°C', color)

fig3.add_trace(
    go.Scatter(x=df.year,
        y=df['total_best'], 
        name='Total',
        hovertemplate =
        'Value: %{y:.3f} °C' + 
        '<br>Year: %{x:.0f}',
        line=dict(color='black', width=0.7))
)

fig3.update_layout(
    title_text=f"Graph 3: Evolution of attributed warming due to ERF 1750-2019",
    
)
# Set x-axis title
fig3.update_xaxes(title_text="Year")

# Set y-axes titles
fig3.update_yaxes(title_text="Attributed warming (°C)")
st.plotly_chart(fig3, use_container_width=True)


st.caption(f"""Graph 3: Evolution of attributed warming due to ERF 1750-2019. The degree of warming resulting from ERF is 
    produced using emulation. The results shown are the medians from a 2237-member ensemble (Forster et. al, 2021). 
    Shaded regions show the "very likely" (5-95%) ranges. 
    Data and figure adoption from [IPCC](https://ipcc-browser.ipcc-data.org/browser/dataset/7512).""")

#################### Change in Temperature #############################

labels = ['Carbon dioxide (CO<sub>2</sub>)', 'Other well-mixed GHG','Ozone (O<sub>3</sub>)', 'Water vapour (Stratosphere)', 
    'Albedo', 'Contrails', 'Aerosols', 'Solar', 'Volcanic', 'Total']

data = [[1.01, 0.40, 0.27, 0, True, 'rgb(201, 14, 55)', 0, 'Carbon dioxide (CO<sub>2</sub>)', False],
        [0.28, 0.11, 0.09, 0, False, 'rgb(143, 14, 42)', 1, 'Methane (CH<sub>4</sub>)', True],
        [0.10, 0.04, 0.03, 0.28, False, 'rgb(232, 93, 23)', 1, 'Nitrous oxide (N<sub>2</sub>O)', True],
        [0.19, 0.08, 0.05, 0.38, False, 'rgb(232, 186, 35)', 1, 'Halogens', True],
        [0.23, 0.16, 0.12, 0, True, 'rgb(201, 14, 55)', 2, 'Ozone (O<sub>3</sub>)', False],
        [0.02, 0.04, 0.02, 0, True, 'rgb(201, 14, 55)', 3, 'Water vapour (Stratosphere)', False],
        [0.04, 0.06, 0.04, 0, True, 'rgb(219, 114, 132)', 4, 'Dark particles on ice', True],
        [-0.11, 0.06, 0.07, -0.11, False, 'rgb(8, 10, 102)', 4, 'Land use', True],
        [0.02, 0.03, 0.01, 0, True, 'rgb(201, 14, 55)', 5, 'Contrails', False],
        [-0.13, 0.12, 0.15, -0.13, False, 'rgb(33, 36, 184)', 6, 'Aerosol-radiation', True],
        [-0.38, 0.26, 0.39, -0.51, False, 'rgb(108, 110, 186)', 6, 'Aerosol-cloud', True],
        [-0.01, 0.05, 0.03, -0.01, False, 'rgb(160, 70, 179)', 7, 'Solar', False],
        [-0.02, 0.01, 0.01, -0.02, False, 'rgb(160, 70, 179)', 8, 'Volcanic', False],  
        [1.27, 0.37, 0.31, 0, True, 'rgb(201, 14, 55)', 9, 'Total', False]]

fig4 = go.Figure()

for i,row in enumerate(data):

    bar_lenghts = [0] * len(labels)
    bar_lenghts[row[6]] = np.abs(row[0])
    pos_errors = [0] * len(labels)
    pos_errors[row[6]] = row[1]
    neg_errors = [0] * len(labels)
    neg_errors[row[6]] = row[2]
    bases = [99] * len(labels)
    bases[row[6]] = row[3]

    customdata = np.array([row[0:3]] * len(labels))
    customdata[:,1] = customdata[:,0] + customdata[:,1]
    customdata[:,2] = customdata[:,0] - customdata[:,2]

    fig4.add_trace(go.Bar(
        name=row[7],
        x=labels,
        y=bar_lenghts,
        hovertemplate =
            'Value: %{customdata[0]:.2f} °C'+
            '<br>Range: [%{customdata[2]:.2f} to %{customdata[1]:.2f}] °C',
        customdata = customdata,
        error_y=dict(
                type='data',  # Indicates error values are provided as data
                symmetric=False,  # Crucial for non-symmetric error bars
                array=pos_errors,  # Positive error values
                arrayminus=neg_errors,  # Negative error values
                visible=row[4]
            ),
        base=bases,
        showlegend=row[8],
        marker_color=row[5]
    ))

fig4.add_trace(go.Bar(
        name='Invisible bars',
        x=labels,
        y=[0] * len(labels),
        error_y=dict(
                type='data',  # Indicates error values are provided as data
                symmetric=False,  # Crucial for non-symmetric error bars
                array=[0, 0.23, 0, 0, 0.06, 0, 0.38, 0.05, 0.01, 0],  # Positive error values
                arrayminus=[0, 0.17, 0, 0, 0.07, 0, 0.54, 0.03, 0.01, 0],  # Negative error values
                visible=True
            ),
        base=[99, 0.57, 99, 99, -0.11, 99, -0.51, -0.01, -0.02, 99],
        showlegend=False
))

fig4.update_layout(
    barmode='stack', 
    title='Graph 4: Change in attributed warming due to ERF 1750-2019',
    yaxis=dict(range=[-1.5, 2]),
    )
fig4.update_yaxes(title_text="°C")

st.plotly_chart(fig4, use_container_width=True)

st.caption("""Graph 4: Change in attributed warming due to ERF 1750-2019 by forcing agents. The contribution of forcing 
    agents to 2019 temperature change relative to 1750 was produced using emulation (Forster et. al., 2021). The results 
    are from a 2237-member ensemble. Solid bars represent best estimates, and "very likely" (5–95%) ranges are given by error 
    bars. The error bars show the combined effects of forcing and climate response uncertainty using estimation 
    of [ECS](https://en.wikipedia.org/wiki/Climate_sensitivity) and [TCR](https://en.wikipedia.org/wiki/Climate_sensitivity), 
    and the distribution of calibrated model parameters from 44 CMIP6 models. Plot adopted from Forster et. al. (2021)""")

st.markdown("# References")

st.markdown(
    """*Effective radiative forcing and attributed warming (Graphs 1 through 4)*  \nForster, P., T. Storelvmo, K. Armour, W. 
    Collins, J.-L. Dufresne, 
    D. Frame, D.J. Lunt, T. Mauritsen, M.D. Palmer, M. Watanabe, M. Wild, and H. Zhang, 2021: The Earth’s Energy Budget, Climate 
    Feedbacks, and Climate Sensitivity. In Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to 
    the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S.L. 
    Connors, C. Péan, S. Berger, N. Caud, Y. Chen, L. Goldfarb, M.I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, 
    T.K. Maycock, T. Waterfield, O. Yelekçi, R. Yu, and B. Zhou (eds.)]. Cambridge University Press, Cambridge, United Kingdom 
    and New York, NY, USA, pp. 923–1054, doi: 10.1017/9781009157896.009."""
)
st.markdown(
    """*Evolution of effective radiative forcing (Graph 1)*  \nSmith, C. (2023): Chapter 7 of the Working Group I Contribution
     to the IPCC Sixth Assessment Report - data for Figure 7.6 (v20220721). NERC EDS Centre for Environmental Data Analysis, 
     06 July 2023. doi:10.5285/0dd364e74c254b64bb5fddb5dceed364. https://dx.doi.org/10.5285/0dd364e74c254b64bb5fddb5dceed364.
     Date Accessed 2025-10-10."""
)
st.markdown(
    """*Evolution of attributed warming due to ERF (Graph 3)*  \nSmith, C. (2023): Chapter 7 of the Working Group I Contribution 
    to the IPCC Sixth Assessment Report - data for Figure 7.8 (v20220721). NERC EDS Centre for Environmental Data Analysis, 
    06 July 2023. doi:10.5285/5ef11ad195844a59b83393870a5860e1. https://dx.doi.org/10.5285/5ef11ad195844a59b83393870a5860e1. 
    Date Accessed 2025-10-15."""
)