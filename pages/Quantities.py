import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from datetime import date

from get_data import (
    get_erf_historic_data
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
st.write("")

selected_graph = st.selectbox("Select graph:", ['Evolution of effective radiative forcing (ERF) 1750-2019'])

if selected_graph == 'Evolution of effective radiative forcing (ERF) 1750-2019':

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
    It is a fundamental driver of changes in the energy budget of the Earth at the top of the atmosphere (Forster et. al, 2021). 
    Shaded regions show the "very likely" (5-95%) ranges. 
    Data from [IPCC](https://ipcc-browser.ipcc-data.org/browser/dataset/7506/0).""")



st.markdown("# References")

st.markdown(
    """*Evolution of effective radiative forcing (Graph 1)*  \nForster, P., T. Storelvmo, K. Armour, W. Collins, J.-L. Dufresne, 
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