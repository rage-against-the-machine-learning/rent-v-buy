# THIS SCRIPT PARES THE DATA SCOPE DOWN TO STRICTLY THE STATE OF CALIFORNIA

import pandas as pd
import numpy as np 

import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute().parent))

import config 

# Load the Data
county_ts = pd.read_csv('../data/raw/unzipped/County_time_series.csv/County_time_series.csv')
city_ts = pd.read_csv('../data/raw/unzipped/City_time_series.csv/City_time_series.csv')
zip_ts = pd.read_csv('../data/raw/unzipped/Zip_time_series.csv/Zip_time_series.csv')

fips_mapping = pd.read_pickle('../data/interim/fips_map.pickle')




