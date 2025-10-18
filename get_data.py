import pandas as pd
import requests
from io import StringIO
import xarray as xr
import streamlit as st
from pathlib import Path
import numpy as np
from datetime import datetime
import json

CFB_PATH = Path("data/cmip56_feedbacks_AR6.json")
OHC_300_PATH = Path("data/global_ohc300m_2024.csv")
OHC_700_PATH = Path("data/global_ohc700m_2024.csv")
OHC_2000_PATH = Path("data/global_ohc2km_2024.csv")
OHC_700_2000_PATH = Path("data/global_ohc700-2km_2024.csv")
PH_ALOHA_URL = r'https://hahana.soest.hawaii.edu/hot/hotco2/HOT_surface_CO2.txt'
PH_ALOHA_BACKUP = Path("data/df_aloha.csv")
PH_HIST_PATH = Path("data/CSVExport.csv")
SEA_LEVEL_URL = r'https://climate.copernicus.eu/sites/default/files/custom-uploads/indicators-2024/sea-level/fig1/fig1_sea_level_indicators_climate_global_area_averaged_anomalies_DT24_updated_towards_2024_07_29_DATA.csv'
SEA_LEVEL_BACKUP = Path("data/fig1_sea_level_indicators_climate_global_area_averaged_anomalies_DT24_updated_towards_2024_07_29_DATA.csv")
SNOW_URL = r'https://climate.rutgers.edu/snowcover/files/moncov.nhland.txt'
SNOW_BACKUP = Path("data/moncov.nhland.txt")
GLACIERS_URL = r'https://www.epa.gov/system/files/other-files/2024-05/glaciers_fig-1.csv'
GLACIERS_BACKUP = Path("data/glaciers_fig-1.csv")
ICE_SHEET_URL = r'https://www.epa.gov/system/files/other-files/2024-05/ice_sheets_fig-1.csv'
ICE_SHEET_BACKUP = Path("data/ice_sheets_fig-1.csv")
SEA_ICE_N_URL = r'https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/'
SEA_ICE_S_URL = r'https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/'
BE_GLOBAL_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_summary.txt'
BE_ANTARCT_URL = r'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/antarctica-TAVG-Trend.txt'
CO2_LATEST_URL = r'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv'
CO2_LATEST_BACKUP = Path("data/co2_annmean_gl.csv")
CH4_LATEST_URL = r'https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv'
CH4_LATEST_BACKUP = Path("data/ch4_annmean_gl.csv")
N2O_LATEST_URL = r'https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_annmean_gl.csv'
N2O_LATEST_BACKUP = Path("data/n2o_annmean_gl.csv")
OSMAN_PATH = Path("data/LGMR_GMST_climo.nc")
CO2_HIST_PATH = Path("data/ghg-concentrations_fig-1.csv")
CH4_HIST_PATH = Path("data/ghg-concentrations_fig-2.csv")
N2O_HIST_PATH = Path("data/ghg-concentrations_fig-3.csv")
PARRENIN_PATH = Path("data/ATS.tab")
CMIP6_PATH = Path("data/global_mean_temp_data.xlsx")
SEA_LEVEL_HIST_PATH = Path("data/CSIRO_Recons_gmsl_yr_2015.txt")
SEA_LEVEL_PROJ_PATH = Path("data/ipcc_ar6_sea_level_projection_global.xlsx")
ERF_HISTORIC_PATH = Path("data/AR6_ERF_1750-2019.csv")
ERF_HISTORIC_PC05_PATH = Path("data/AR6_ERF_1750-2019_pc05.csv")
ERF_HISTORIC_PC95_PATH = Path("data/AR6_ERF_1750-2019_pc95.csv")
WARMING_HISTORIC_PATH = Path("data/fig7.8.csv")

def integer_to_datetime(int_date):
    year, remainder = divmod(int_date, 10000)
    month, day = divmod(remainder, 100)
    return datetime(year, month + 1, day)

def fractional_year_to_datetime(year_float):
    year = int(year_float)
    # Calculate days from the fractional part (approximate, considering leap years)
    days = int((year_float - year) * 365.25)
    base_date = pd.to_datetime(f'{year}-01-01')
    return base_date + pd.DateOffset(days=days)

def read_csv_from_url(csv_url, backup, timeout = 5, **kwargs):
    try:
        response = requests.get(csv_url, timeout = timeout)
        response.raise_for_status() # Raise an exception for bad status codes
        return pd.read_csv(StringIO(response.text), **kwargs)
    except:
        return pd.read_csv(backup, **kwargs)

def get_season(date):
    # returns string with the season and correct year
    year = date.year
    if date.month in [12,1,2]:
        season = 'Winter'
        if date.month in [1,2]:
            year -= 1
    elif date.month in [3,4,5]:
        season = 'Spring'
    elif date.month in [6,7,8]:
        season = 'Summer'
    elif date.month in [9,10,11]:
        season = 'Autumn'
    return f'{season} {year}'

@st.cache_data()
def get_snow_data():
    df = read_csv_from_url(SNOW_URL, SNOW_BACKUP, sep=r'\s+', names=['year','month','value'])
    df.month = pd.to_numeric(df.month)
    df['day'] = 1
    df['date'] = pd.to_datetime(df[['year','month','day']])
    df = df.set_index('date')
    # find all missing months and insert nan values
    min_date = df.index.min()
    max_date = df.index.max()
    full_date_range = pd.date_range(start=min_date.to_period('M').start_time,
                                    end=max_date.to_period('M').end_time,
                                    freq='MS') # 'MS' for month start
    df = df.reindex(full_date_range)
    df = df.reset_index()

    # get season and corresponding year
    df['season_year'] = df['index'].apply(get_season)
    df[['season','s_year']] = df['season_year'].str.split(' ', expand=True)
    df.s_year = pd.to_numeric(df.s_year)
    df_seasons = df.groupby(['s_year','season'])['value'].mean()

    # do not want values for seasons where there are months missing
    df_seasons_count = df[~df.value.isna()].groupby(['s_year','season']).size()
    missing_season_idx = df_seasons_count[df_seasons_count != 3].index
    df_seasons.loc[missing_season_idx] = float("NaN")
    df_seasons = df_seasons.reset_index()

    # get yearly average
    df_years = df.groupby(['year'])['value'].mean()

    # do not want values for years with missing months
    df_month_count = df[~df.value.isna()].groupby(['year']).size()
    missing_month_idx = df_month_count[df_month_count != 12].index
    df_years.loc[missing_month_idx] = float("NaN")
    return df_seasons, df_years

@st.cache_data()
def get_glaciers_data():
    df = read_csv_from_url(GLACIERS_URL, GLACIERS_BACKUP, skiprows = 6)
    return df

@st.cache_data()
def get_ice_sheet_data():
    df = read_csv_from_url(ICE_SHEET_URL, ICE_SHEET_BACKUP, skiprows = 6)
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
        backup_n = f"N_{month:02d}_extent_v4.0.csv"
        backup_s = f"S_{month:02d}_extent_v4.0.csv"
        url_n = f"{SEA_ICE_N_URL}{backup_n}"
        url_s = f"{SEA_ICE_S_URL}{backup_s}"
        df_n = read_csv_from_url(url_n, Path(f"data/{backup_n}"), timeout = 2, skipinitialspace=True)
        df_s = read_csv_from_url(url_s, Path(f"data/{backup_s}"), timeout = 2, skipinitialspace=True)
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

    df = read_csv_from_url(CO2_LATEST_URL, CO2_LATEST_BACKUP, comment = '#')
    df = df.rename(columns={'year' : 'Year', 'mean' : 'Value'})
    df = df[~df['Year'].isnull()]
    df['Name'] = 'CO2_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_ch4_latest_data():

    df = read_csv_from_url(CH4_LATEST_URL, CH4_LATEST_BACKUP, comment = '#')
    df = df.rename(columns={'year' : 'Year', 'mean' : 'Value'})
    df = df[~df['Year'].isnull()]
    df['Name'] = 'CH4_latest'
    return df[['Year', 'Name', 'Value']]

@st.cache_data()
def get_n2o_latest_data():

    df = read_csv_from_url(N2O_LATEST_URL, N2O_LATEST_BACKUP, comment = '#')
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

@st.cache_data()
def get_sea_level_hist_data():

    df = pd.read_csv(SEA_LEVEL_HIST_PATH, sep=r'\s+', names = ['Year', 'Value', 'Unc'])
    df.Year = df.Year - 0.5
    df.Year = df.Year.astype(int)
    return df

@st.cache_data()
def get_sea_level_proj_data():

    df = pd.read_excel(SEA_LEVEL_PROJ_PATH, sheet_name = "Total")
    df = df[df.confidence == 'medium']
    df = df[df.scenario.isin(['ssp126','ssp245','ssp585'])]
    df = pd.melt(df,
                  id_vars=['scenario', 'quantile'],
                  value_vars=range(2020, 2160, 10),
                  var_name='year',
                  value_name='level')
    #print(df.head())
    return df

@st.cache_data()
def get_sea_level_latest_data():
    df = read_csv_from_url(SEA_LEVEL_URL, SEA_LEVEL_BACKUP)
    df['Date'] = df['Time (years)'].apply(fractional_year_to_datetime)
    df = df.replace("nan", float("NaN"))
    df["Trendslope"] = np.gradient(df["OLS fit"].to_numpy() * 10, df['Time (years)'].to_numpy())
    return df

@st.cache_data()
def get_ph_data():

    df_global = pd.read_csv(PH_HIST_PATH, header=0, names=['date','value','uncertainty'])
    df_global.date = pd.to_datetime(df_global.date)
    df_aloha = read_csv_from_url(PH_ALOHA_URL, PH_ALOHA_BACKUP, sep=r'\s+', skiprows = 8)
    df_aloha = df_aloha.replace(-999, float("NaN"))
    df_aloha.date = pd.to_datetime(df_aloha.date)
    return df_global, df_aloha

@st.cache_data()
def get_ohc_data():

    df_300 = pd.read_csv(OHC_300_PATH)
    df_700 = pd.read_csv(OHC_700_PATH)
    df_2000 = pd.read_csv(OHC_2000_PATH)
    df_700_2000 = pd.read_csv(OHC_700_2000_PATH)

    df_300.time = df_300.time.apply(integer_to_datetime)
    df_700.time = df_700.time.apply(integer_to_datetime)
    df_2000.time = df_2000.time.apply(integer_to_datetime)
    df_700_2000.time = df_700_2000.time.apply(integer_to_datetime)

    return df_300, df_700, df_2000, df_700_2000

@st.cache_data()
def get_erf_historic_data():

    df = pd.read_csv(ERF_HISTORIC_PATH)
    df_05 = pd.read_csv(ERF_HISTORIC_PC05_PATH)
    df_95 = pd.read_csv(ERF_HISTORIC_PC95_PATH)

    return df, df_05, df_95

@st.cache_data()
def get_warming_historic_data():

    df = pd.read_csv(WARMING_HISTORIC_PATH)

    return df

@st.cache_data()
def get_climate_feedback_data():

    with open(CFB_PATH, 'r') as file:
        data = json.load(file)

    df_cmip5 = pd.DataFrame(data['cmip5'])
    df_cmip5 = df_cmip5.drop(columns = ['models', 'resid_fbk'])
    df_cmip5['generation'] = 'cmip5'
    df_cmip5 = df_cmip5.rename(columns = {'ALB_fbk' : 'Surface Albedo', 'NET_fbk' : 'Net', 'CLD_fbk' : 'Cloud',
        'WVLR_fbk' : 'Water Vapour + Lapse Rate', 'PL_fbk' : 'Planck'})
    df_cmip5 = pd.melt(df_cmip5,
                  id_vars=['generation'],
                  value_vars=[c for c in df_cmip5.columns if c != 'generation'],
                  var_name='feedback',
                  value_name='value')

    df_cmip6 = pd.DataFrame(data['cmip6'])
    df_cmip6 = df_cmip6.drop(columns = ['models', 'resid_fbk'])
    df_cmip6['generation'] = 'cmip6'
    df_cmip6 = df_cmip6.rename(columns = {'ALB_fbk' : 'Surface Albedo', 'NET_fbk' : 'Net', 'CLD_fbk' : 'Cloud',
        'WVLR_fbk' : 'Water Vapour + Lapse Rate', 'PL_fbk' : 'Planck'})
    df_cmip6 = pd.melt(df_cmip6,
                  id_vars=['generation'],
                  value_vars=[c for c in df_cmip6.columns if c != 'generation'],
                  var_name='feedback',
                  value_name='value')

    ########################## code adopted from https://github.com/mzelinka/AR6_figure/blob/v1.0.0/AR6_fbk_violin_plot.py ###########

    # AR6 expert-assessed values provided by Masa on 1/27/21:
    Masa_names =      ['Net',       'Planck',   'WV+LR','Albedo','Cloud','Other']
    AR6 =    np.array([-1.16081,    -3.22,      1.30,    0.35,    0.42,  -0.01081]) 
    AR6p5 =  np.array([-1.81313204, -3.39,      1.13,    0.18,   -0.10,  -0.27159185]) 
    AR6p95 = np.array([-0.50848796, -3.05,      1.47,    0.52,    0.94,   0.24997185])  
    AR6p17 = np.array([-1.539513677,-3.32,      1.20,    0.25,    0.12,  -0.16411])  
    AR6p83 = np.array([-0.782106323,-3.12,      1.40,    0.45,    0.72,   0.14248]) 

    X=np.ma.zeros((10000,6))
    for i,name in enumerate(Masa_names):
        mean = AR6[i]
        p5,p17,p83,p95 = AR6p5[i],AR6p17[i],AR6p83[i],AR6p95[i]
        CI90 = p95-p5
        # 90% confidence interval corresponds to +/- 1.64485 times the standard deviation 
        std = CI90/2/1.64485
        print('Inferred AR6 '+name+' standard deviation = '+str(np.round(std,2)))
        this = sorted(np.random.normal(mean, std, 10000))
        # Clip the tails
        p2p5,p97p5 = np.percentile(this,[2.5,97.5])
        X[:,i] = np.ma.masked_outside(this, p2p5,p97p5)
    ############################################################################################################################
    df_ar6 = pd.DataFrame(X, columns=['Net','Planck','Water Vapour + Lapse Rate','Surface Albedo','Cloud','resid_fbk'])
    df_ar6 = df_ar6.drop(columns = ['resid_fbk'])
    df_ar6['generation'] = 'ar6'
    df_ar6 = pd.melt(df_ar6,
                  id_vars=['generation'],
                  value_vars=[c for c in df_ar6.columns if c != 'generation'],
                  var_name='feedback',
                  value_name='value')
    return df_cmip5, df_cmip6, df_ar6
    
if __name__ == "__main__":
    get_climate_feedback_data()