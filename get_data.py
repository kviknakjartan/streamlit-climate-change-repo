import pandas as pd
import requests
import xarray as xr
import streamlit as st
from pathlib import Path

ICE_SHEET_URL = r'https://www.epa.gov/system/files/other-files/2024-05/ice_sheets_fig-1.csv'
SEA_ICE_N_URL = r'https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/'
SEA_ICE_S_URL = r'https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/'
BE_GLOBAL_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt'
BE_ANTARCT_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/antarctica-TAVG-Trend.txt'
CO2_LATEST_PATH = Path("data/co2_annmean_gl.csv")
CH4_LATEST_PATH = Path("data/ch4_annmean_gl.csv")
N2O_LATEST_PATH = Path("data/n2o_annmean_gl.csv")
OSMAN_PATH = Path("data/LGMR_GMST_climo.nc")
CO2_HIST_PATH = Path("data/ghg-concentrations_fig-1.csv")
CH4_HIST_PATH = Path("data/ghg-concentrations_fig-2.csv")
N2O_HIST_PATH = Path("data/ghg-concentrations_fig-3.csv")
PARRENIN_PATH = Path("data/ATS.tab")
CMIP6_PATH = Path("data/global_mean_temp_data.xlsx")

def fractional_year_to_datetime(year_float):
    year = int(year_float)
    # Calculate days from the fractional part (approximate, considering leap years)
    days = int((year_float - year) * 365.25)
    base_date = pd.to_datetime(f'{year}-01-01')
    return base_date + pd.DateOffset(days=days)

@st.cache_data()
def get_ice_sheet_data():
    df = pd.read_csv(ICE_SHEET_URL, skiprows = 6)
    df['Date'] = df['Year'].apply(fractional_year_to_datetime)
    # Change into long format
    df_long = pd.melt(df,
                  id_vars=['Date', 'Year'],  # Columns to keep as identifiers
                  var_name='Source',       # Name for the new column holding the original column names
                  value_name='Value')
    # Drop all dates with empty Value
    df_long = df_long[~df_long.Value.isna()]
    # Add an empty value for Nasa 2018 where there is a gap in the record
    empty_df = pd.DataFrame({ 'Year' : [2018, 2018],
                              'Date' : [fractional_year_to_datetime(2018), fractional_year_to_datetime(2018)],
                              'Source' : ['NASA - Antarctica land ice mass', 'NASA - Greenland land ice mass'],
                              'Value' : [float("NaN"), float("NaN")]})
    df_long = pd.concat([df_long, empty_df]).sort_values(by=['Source', 'Date'])
    return df_long

@st.cache_data()
def get_sea_ice_data():
    all_months_n_df = pd.DataFrame()
    all_months_s_df = pd.DataFrame()
    for month in range(1,13):
        url_n = f"{SEA_ICE_N_URL}N_{month:02d}_extent_v4.0.csv"
        url_s = f"{SEA_ICE_S_URL}S_{month:02d}_extent_v4.0.csv"
        df_n = pd.read_csv(url_n, skipinitialspace=True)
        df_s = pd.read_csv(url_s, skipinitialspace=True)
        all_months_n_df = pd.concat([all_months_n_df, df_n])
        all_months_s_df = pd.concat([all_months_s_df, df_s])
    df = pd.concat([all_months_n_df, all_months_s_df])
    df = df.rename(columns={'mo' : 'month'})
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

    # For each hemisphere interpolate missing values, then do 12 month moving average
    df = df.replace(-9999, float("NaN"))
    df = df.sort_values(by=['region', 'date']).reset_index()
    for region in ['N','S']:
        df.loc[df['region'] == region, 'extent'] = df.loc[df['region'] == region, 'extent'].interpolate()
        df.loc[df['region'] == region, 'area'] = df.loc[df['region'] == region, 'area'].interpolate()
        df.loc[df['region'] == region,'ma_extent'] = df.loc[df['region'] == region,'extent'].rolling(window=12).mean()
        df.loc[df['region'] == region,'ma_area'] = df.loc[df['region'] == region,'area'].rolling(window=12).mean()
    return df

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
    get_ice_sheet_data()