from datetime import date
import streamlit as st
st.set_page_config(page_title="References", page_icon='sun.svg')

st.markdown("# References")
st.sidebar.header("References")

st.markdown(
    """*Antarctic Ice Cores: approximately 805,669 BCE to 2001 CE (Graphs 1,2 and 3)*  \nBereiter, B.; Eggleston, S.; Schmitt, J.; 
    Nehrbass-Ahles, C.; Stocker, T.F.; Fischer, H.; Kipfstuhl, S.; Chappellaz, J.A. (2015-02-04): 
    NOAA/WDS Paleoclimatology - Antarctic Ice Cores Revised 800KYr CO2 Data. 
    NOAA National Centers for Environmental Information. https://doi.org/10.25921/n8y4-bp27. 
    Accessed September 19, 2025."""
)
st.markdown(
    """*EPICA Dome C, Antarctica: approximately 797,446 BCE to 1937 CE (Graph 1)*  \nLoulergue, L., Schilt, A., Spahni, R., 
    Masson-Delmotte, V., Blunier, T., Lemieux, B., Barnola, J.-M., Raynaud, 
    D., Stocker, T. F., & Chappellaz, J. (2008). Orbital and millennial-scale features of atmospheric CH4 over the past 
    800,000 years. Nature, 453(7193), 383–386. https://doi.org/10.1038/nature06950. 
    Accessed September 19, 2025."""
)
st.markdown(
    """*Law Dome, Antarctica: approximately 1008 CE to 1980 CE (Graph 1)*  \nEtheridge, D. M., Steele, L. P., Francey, R. J., 
    & Langenfelds, R. L. (2002). Historic CH4 records from Antarctic and Greenland ice cores, Antarctic firn data, 
    and archived air samples from Cape Grim, Tasmania. In Trends: A compendium of data on global change. 
    U.S. Department of Energy. https://data.ess-dive.lbl.gov/portals/CDIAC. 
    Accessed September 19, 2025."""
)
st.markdown(
    """*EPICA Dome C, Antarctica: approximately 796,475 BCE to 1937 CE (Graph 1)*  \nSchilt, A., Baumgartner, M., Blunier, 
    T., Schwander, J., Spahni, R., Fischer, H., & Stocker, T. F. (2010). Glacial–interglacial and millennial-scale 
    variations in the atmospheric nitrous oxide concentration during the last 800,000 years. 
    Quaternary Science Reviews, 29(1–2), 182–192. https://doi.org/10.1016/j.quascirev.2009.03.011. 
    Accessed September 19, 2025."""
)
st.markdown(
    """*Antarctica: approximately 1903 CE to 1976 CE (Graph 1)*  \nBattle, M., Bender, M., Sowers, T., Tans, P. P., Butler, 
    J. H., Elkins, J. W., Ellis, J. T., Conway, T., Zhang, N., Lang, P., & Clarket, A. D. (1996). 
    Atmospheric gas concentrations over the past century measured in air from firn at the South Pole. 
    Nature, 383(6597), 231–235. https://doi.org/10.1038/383231a0. 
    Accessed September 19, 2025."""
)
st.markdown(
    """*Trends in Atmospheric Carbon Dioxide (CO<sub>2</sub>) (Graphs 1,2 and 3)*  \nLan, X., Tans, P. and K.W. Thoning: 
    Trends in globally-averaged CO2 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09 https://doi.org/10.15138/9N0H-ZH07. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Trends in Atmospheric Methane (CH<sub>4</sub>) (Graph 1)*  \nLan, X., K.W. Thoning, and E.J. Dlugokencky: 
    Trends in globally-averaged CH4, N2O, and SF6 determined from NOAA Global Monitoring Laboratory measurements. 
    Version 2025-09, https://doi.org/10.15138/P8XG-AA10. 
    Accessed September 21, 2025.""", unsafe_allow_html=True
)
st.markdown(
    """*Trends in Atmospheric Nitrous Oxide (N<sub>2</sub>O) (Graph 1)*  \nLan, X., K.W. Thoning, and E.J. Dlugokencky: 
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
    f"""*Sea ice extent and area data (Graph 5)*  \nFetterer, F., Knowles, K., Meier, W. N., Savoie, M., Windnagel, 
    A. K. & Stafford, T. (2025). 
    Sea Ice Index. (G02135, Version 4). [Data Set]. Boulder, Colorado USA. National Snow and Ice Data Center. 
    [https://doi.org/10.7265/a98x-0f50](https://doi.org/10.7265/a98x-0f50). Date Accessed {date.today()}."""
)
st.markdown(
    f"""*Cumulative Mass Balance of Greenland and Antarctica (Graph 6)*  \nUnited States Environmental Protection Agency. (2023). 
    Climate Change Indicators: Ice Sheets [Dataset]. US EPA. https://www.epa.gov/climate-indicators/climate-change-indicators-ice-sheets. 
    Date Accessed {date.today()}."""
)
st.markdown(
    """*Information on sea level rise (Graph 6 caption)*  \nIPCC (Intergovernmental Panel on Climate Change). (2013). 
    Climate change 2013—The physical science basis: Contribution of Working Group I to the Fifth Assessment Report of 
    the Intergovernmental Panel on Climate Change (T. F. Stocker, D. Qin, G.-K. Plattner, M. Tignor, S. K. Allen, 
    A. Boschung, A. Nauels, Y. Xia, V. Bex, & Midgley, Eds.). Cambridge University Press. www.ipcc.ch/report/ar5/wg1"""
)
