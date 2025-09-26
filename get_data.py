import pandas as pd
import requests
import xarray as xr
import streamlit as st

BE_GLOBAL_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt'
BE_ANTARCT_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/antarctica-TAVG-Trend.txt'
CO2_LATEST_PATH = r'data\\co2_annmean_gl.csv'
CH4_LATEST_PATH = r'data\\ch4_annmean_gl.csv'
N2O_LATEST_PATH = r'data\\n2o_annmean_gl.csv'
OSMAN_PATH = r'data\\LGMR_GMST_climo.nc'
CO2_HIST_PATH = r'data\\ghg-concentrations_fig-1.csv'
CH4_HIST_PATH = r'data\\ghg-concentrations_fig-2.csv'
N2O_HIST_PATH = r'data\\ghg-concentrations_fig-3.csv'
PARRENIN_PATH = r'data\\ATS.tab'
CMIP6_PATH = r'data\\global_mean_temp_data.xlsx'

@st.cache_data()
def get_cmip6_data():
    df = pd.read_excel(CMIP6_PATH)
    return df

@st.cache_data()
def get_be_global_data():

    df = pd.read_csv(BE_GLOBAL_URL, sep=r'\s+', comment = '%', \
        names = ['Year', 'Annual Anomaly', 'Annual Unc.', 'Five-year Anomaly', 'Five-year Unc.', \
        'Annual Anomaly(W)', 'Annual Unc.(W)', 'Five-year Anomaly(W)', 'Five-year Unc.(W)'])
    df = df[~df['Year'].isna()]

    # Add the global average temp to the anomaly
    for anom_col in [c for c in df.columns if 'Anomaly' in c]:
        df[anom_col] += 14.102

    df = df.rename(columns = {'Annual Anomaly' : 'Value'})
    df['Name'] = 'Temp_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_be_antarct_data():
    df = pd.read_csv(BE_ANTARCT_URL, sep=r'\s+', comment = '%', \
        names = ['Year', 'Month', 'Monthly Anomaly', 'Monthly Unc.', 'Annual Anomaly', 'Annual Unc.', \
        'Five-year Anomaly', 'Five-year Unc.'])
    df = df[~df['Year'].isna()]

    # Calculate the annual average anomaly
    df['Value'] = df.groupby('Year')['Monthly Anomaly'].mean()

    df['Name'] = 'Temp_antarct_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_parrenin_data():
    df = pd.read_csv(PARRENIN_PATH, sep=r'\s+', skiprows = 12, names = ['Year', 'Value'])
    df['Year'] = 1950 - df['Year'] * 1000
    df = df[~df['Year'].isnull()]
    df['Name'] = 'Temp_parrenin'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_osman_data():

    ds = xr.open_dataset(OSMAN_PATH)
    df = ds.to_dataframe()
    df['Year'] = 1950 - df.index
    df = df.rename(columns = {'gmst' : 'Value'})
    df['Name'] = 'Temp_hist'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_co2_latest_data():

    df = pd.read_csv(CO2_LATEST_PATH, comment = '#')
    df = df.rename(columns={'year' : 'Year', 'mean' : 'Value'})
    df = df[~df['Year'].isnull()]
    df['Name'] = 'CO2_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_ch4_latest_data():

    df = pd.read_csv(CH4_LATEST_PATH, comment = '#')
    df = df.rename(columns={'year' : 'Year', 'mean' : 'Value'})
    df = df[~df['Year'].isnull()]
    df['Name'] = 'CH4_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_n2o_latest_data():

    df = pd.read_csv(N2O_LATEST_PATH, comment = '#')
    df = df.rename(columns={'year' : 'Year', 'mean' : 'Value'})
    df = df[~df['Year'].isnull()]
    df['Name'] = 'N2O_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_n2o_hist_data():

    df = pd.read_csv(N2O_HIST_PATH, skiprows = 6)
    df = df.rename(columns={'Year (negative values = BC)' : 'Year'})
    
    # average the icecore data
    df['Value'] = df[['EPICA Dome C, Antarctica','Antarctica (Battle et al.)']].mean(axis=1)

    # we will not use the direct measurements from this file so get rid of them
    df = df[~df['Value'].isnull()]

    df['Year'] = pd.to_numeric(df['Year'])
    df['Value'] = pd.to_numeric(df['Value'])

    # insert a NaN datapoint to break line in regions where there are sparse datapoints
    year_diff = df['Year'].diff()
    index = year_diff[year_diff > 5000].index
    for i in index:
        df.loc[len(df)] = [df.loc[i-1,'Year'] + 1000] + [float("NaN")] * (df.shape[1] - 1)
    df['Name'] = 'N2O_hist'
    return df[['Year', 'Name', 'Value']].sort_values(by='Year')

@st.cache_data()
def get_ch4_hist_data():

    df = pd.read_csv(CH4_HIST_PATH, skiprows = 6)
    df = df.rename(columns={'Year (negative values = BC)' : 'Year'})

    df['Law Dome'] = df['Law Dome'].str.replace(',','')
    df['Law Dome'] = pd.to_numeric(df['Law Dome'])
    
    # average the icecore data
    df['Value'] = df[['EPICA Dome C, Antarctica','Law Dome']].mean(axis=1)

    # we will not use the direct measurements from this file so get rid of them
    df = df[~df['Value'].isnull()]

    df['Year'] = pd.to_numeric(df['Year'])
    df['Value'] = pd.to_numeric(df['Value'])

    # insert a NaN datapoint to break line in regions where there are sparse datapoints
    year_diff = df['Year'].diff()
    index = year_diff[year_diff > 5000].index
    for i in index:
        df.loc[len(df)] = [df.loc[i-1,'Year'] + 1000] + [float("NaN")] * (df.shape[1] - 1)
    df['Name'] = 'CH4_hist'
    return df[['Year', 'Name', 'Value']].sort_values(by='Year')

@st.cache_data()
def get_co2_hist_data():

    df = pd.read_csv(CO2_HIST_PATH, skiprows = 6)
    
    # we will not use the direct measurements from this file so get rid of them
    df = df[~df['Antarctic Ice Cores'].isnull()]

    df = df.rename(columns = {'Antarctic Ice Cores' : 'Value'})
    df['Year'] = pd.to_numeric(df['Year'])
    df['Value'] = pd.to_numeric(df['Value'])

    # insert a NaN datapoint to break line in regions where there are sparse datapoints
    year_diff = df['Year'].diff()
    index = year_diff[year_diff > 5000].index
    for i in index:
        df.loc[len(df)] = [df.loc[i-1,'Year'] + 1000] + [float("NaN")] * (df.shape[1] - 1)
    df['Name'] = 'CO2_hist'
    return df[['Year', 'Name', 'Value']].sort_values(by='Year')
    

if __name__ == "__main__":
    #get_be_data()
    get_cmip6_data()
    #get_n2o_hist_data()