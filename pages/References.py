from datetime import date
import streamlit as st
st.set_page_config(page_title="Climate Change in Graphs: References", page_icon='sun.svg')

st.markdown("# References")
st.sidebar.header("References")

st.markdown(
    """*Antarctic ice core data (Graphs 1,2 and 3)*  \nUnited States Environmental Protection Agency. (2010). 
    Climate Change Indicators: Atmospheric Concentrations of Greenhouse Gases (Updated June 2024) [Dataset]. 
    US EPA. https://www.epa.gov/climate-indicators/climate-change-indicators-atmospheric-concentrations-greenhouse-gases.  
    Accessed September 19, 2025."""
)
st.markdown(
    """*Latest Atmospheric Carbon Dioxide (CO<sub>2</sub>) concentration (Graphs 1,2 and 3)*  \nLan, X., Tans, P. and K.W. Thoning: 
    Trends in globally-averaged CO2 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09 https://doi.org/10.15138/9N0H-ZH07. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Latest Atmospheric Methane (CH<sub>4</sub>) and Nitrous Oxide (N<sub>2</sub>O) concentrations (Graph 1)*  \nLan, X., 
    K.W. Thoning, and E.J. Dlugokencky: 
    Trends in globally-averaged CH4, N2O, and SF6 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09, https://doi.org/10.15138/P8XG-AA10. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Antarctic temperature data (Graph 2)*  \nParrenin, Frédéric; Masson-Delmotte, Valerie; 
    Köhler, Peter; Raynaud, Dominique; Paillard, Didier; Schwander, Jakob; Barbante, Carlo; Landais, Amaëlle; Wegner, Anna; 
    Jouzel, Jean (2013): Antarctic Temperature Stack (ATS) from five different ice cores (EDC, Vostok, Dome Fuji, TALDICE, 
    and EDML) [dataset]. PANGAEA, https://doi.org/10.1594/PANGAEA.810188,  \nIn supplement to: Parrenin, F et al. (2013): 
    Synchronous change of atmospheric CO2 and Antarctic temperature during the last deglacial warming. Science, 
    339(6123), 1060-1063, https://doi.org/10.1126/science.1226368.  \nAccessed September 23, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Global surface temperatures since the last glacial maximum (Graph 3)*  \nMatthew B. Osman, Jessica E. Tierney, 
    Jiang Zhu, Robert Tardif, Gregory J. Hakim, Jonathan King, Christopher J. Poulsen. 2021. 
    Globally resolved surface temperatures since the Last Glacial Maximum. Nature, 599, 239-244. 
    doi: 10.1038/s41586-021-03984-4. 
    Accessed from https://doi.org/10.25921/njxd-hg08, September 19, 2025."""
)
st.markdown(
    f"""*Estimated global average surface temperature (Graphs 3 and 4)*  \nRohde, R. A. and Hausfather, Z.: 
    The Berkeley Earth Land/Ocean Temperature Record, Earth Syst. Sci. Data, 12, 3469-3479, 
    https://doi.org/10.5194/essd-12-3469-2020, 2020. 
    Accessed {date.today()}."""
)
st.markdown(
    """*CMIP6 model output data (Graph 4)*  \nCopernicus Climate Change Service, Climate Data Store, 
    (2021): CMIP6 climate projections. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). 
    DOI: 10.24381/cds.c866074c. Accessed from https://cds.climate.copernicus.eu/datasets/projections-cmip6?tab=overview
    (Accessed on 24-09-2025)."""
)
st.markdown(
    """*CMIP6 model output plot original work (Graph 4)*  \nCopernicus Climate Change Service (C3S) Data Tutorials: 
    Plot an Ensemble of CMIP6 Climate Projections. (2022). Copernicus Climate Change Service (C3S). 
    https://ecmwf-projects.github.io/copernicus-training-c3s/projections-cmip6.html
    (Accessed on 24-09-2025)."""
)
st.markdown(
    f"""*Sea ice extent and area data (Graph 5)*  \nFetterer, F., Knowles, K., Meier, W. N., Savoie, M., Windnagel, 
    A. K. & Stafford, T. (2025). 
    Sea Ice Index. (G02135, Version 4). [Data Set]. Boulder, Colorado USA. National Snow and Ice Data Center. 
    [https://doi.org/10.7265/a98x-0f50](https://doi.org/10.7265/a98x-0f50). Date Accessed {date.today()}."""
)
st.markdown(
    f"""*Cumulative Mass Balance of Greenland and Antarctica (Graph 6)*  \nUnited States Environmental Protection Agency. (2021). 
    Climate Change Indicators: Ice Sheets [Dataset]. US EPA. https://www.epa.gov/climate-indicators/climate-change-indicators-ice-sheets. 
    Date Accessed {date.today()}."""
)
st.markdown(
    f"""*Cumulative mass balance for a set of observed glaciers (Graph 7)*  \nUnited States Environmental Protection Agency. (2010). 
    Climate Change Indicators: Ice Sheets [Dataset]. US EPA. https://www.epa.gov/climate-indicators/climate-change-indicators-glaciers. 
    Date Accessed {date.today()}."""
)
st.markdown(
    f"""*Northern hemisphere snow cover extent (Graph 8)*  \nRobinson, David A., Estilow, Thomas W., and NOAA CDR Program (2012): 
    NOAA Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover Extent (SCE), Version 1. [dataset]. 
    NOAA National Centers for Environmental Information. doi: 10.7289/V5N014G9.
    Date Accessed {date.today()}."""
)
st.markdown(
    """*Global mean sea level reconstruction (Graph 9)*  \nChurch, J.A. and N.J. White (2011), Sea-level rise from the late 19th 
    to the early 21st century. Surveys in Geophysics, 32, 585-602, doi:10.1007/s10712-011-9119-1."""
)