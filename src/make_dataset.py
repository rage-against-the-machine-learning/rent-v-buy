import pandas as pd 
import numpy as np  
from zipfile import ZipFile

import pathlib
import sys
import os 
sys.path.append(str(pathlib.Path().absolute().parent))

import warnings
warnings.filterwarnings("ignore")


# Unzip the files and read the csvs
csv_dfs = {}

for filename in sorted(os.listdir('../data/raw/')):
    if '.csv.zip' in filename: 
        with ZipFile(f'../data/raw/{filename}', 'r') as a_zip:
            a_zip.extractall(f'../data/raw/unzipped/{filename[:-4]}')
            
    elif '.csv' in filename:
        csv_dfs[filename] = pd.read_csv(f'../data/raw/{filename}')
        
# Read in the extracted zip files       
for filename in sorted(os.listdir('../data/raw/unzipped/')):
    csv_dfs[filename[:-4]] = (pd.read_csv(f'../data/raw/unzipped/{filename}/{filename}', engine='python'))


# CREATE FIPS MAP FROM THE COUNTY CROSS WALK, COUNTY TIME SERIES, CITIES CROSSWALK, CITY TIME SERIES
county_xwalk = pd.read_csv('../data/raw/CountyCrosswalk_Zillow.csv')
city_xwalk = pd.read_csv('../data/raw/unzipped/cities_crosswalk.csv/cities_crosswalk.csv')

county_ts = pd.read_csv('../data/raw/unzipped/County_time_series.csv/County_time_series.csv')
city_ts = pd.read_csv('../data/raw/unzipped/City_time_series.csv/City_time_series.csv')

state_region_d = {
    'West' : ['Arizona', 'California', 'Colorado', 'Idaho', 'Montana', 'Nevada',  'New Mexico', 'Oregon', 'Utah',  'Washington'],
    'Midwest' : ['Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota',  'Ohio', 'South Dakota', 'Wisconsin'],
    'Northeast' : ['Connecticut', 'Maine', 'Massachusetts',  'New Hampshire', 'New Jersey', 'New York', 'Pennsylvania', 'Rhode Island', 'Vermont','Wyoming'],
    'South': ['Alabama', 'Arkansas', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Kentucky', 'Louisiana', 'Maryland', 'Mississippi',  'North Carolina', 'Oklahoma',  'South Carolina', 'Tennessee', 'Texas', 'Virginia', 'West Virginia'],
    'Pacific' : ['Hawaii', 'Alaska']
}

# Create dictionaries with the FIPS as key and county, state, or metro name as value to append to county_ts
countyname_by_FIPS = dict(zip(county_xwalk['FIPS'], county_xwalk['CountyName']))
statename_by_FIPS = dict(zip(county_xwalk['FIPS'], county_xwalk['StateName']))
metroname_by_FIPS = dict(zip(county_xwalk['FIPS'], county_xwalk['MetroName_Zillow']))

# Use the `countyname_by_FIPS` dictionary to impute a new column in the `county_ts` DataFrame
countyName_column = []
stateName_column = []
metroName_column = []

for row in county_ts.itertuples():
    # row.RegionName == crosswalk table's FIPS
    if row.RegionName in countyname_by_FIPS:
        countyName_column.append(countyname_by_FIPS[row.RegionName])
        stateName_column.append(statename_by_FIPS[row.RegionName])
        metroName_column.append(metroname_by_FIPS[row.RegionName])
    else:
        countyName_column.append(np.nan)
        stateName_column.append(np.nan)
        metroName_column.append(np.nan)
        
assert len(countyName_column) == len(county_ts) == len(stateName_column) == len(metroName_column)

county_ts['CountyName'] = countyName_column
county_ts['StateName'] = stateName_column
county_ts['MetroName'] = metroName_column

# Attach the region name to the respective counties
census_region_column = []
for row in county_ts.itertuples():
    for region, states in state_region_d.items():
        if row.StateName in states:
            census_region_column.append(region)
        else:
            pass
    
assert len(census_region_column) == len(county_ts), 'rework the for-loop'
county_ts['CensusRegion'] = census_region_column        

# Create the FIPS Map DataFrame
fips_map = county_ts[['RegionName', 'CountyName', 'MetroName', 'StateName', 'CensusRegion']]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

fips_map['StateAbbrev'] = [us_state_abbrev[row.StateName] for row in fips_map.itertuples()]

# Merge the city data into the fips_map table
merged = fips_map.merge(city_xwalk, 
                        left_on=['CountyName', 'StateAbbrev'], 
                        right_on=['County', 'State'],
                        how='left')

merged.drop(['CountyName', 'StateAbbrev'], axis=1, inplace=True)
merged = merged.drop_duplicates()
merged.reset_index(drop=True, inplace=True)

# Save the file in data/interim/ directory
merged.to_pickle('../data/interim/fips_map.pickle')
