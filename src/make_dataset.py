'''
make_datset.py

This file serves to: 
1. Read in the downloaded data from zillow/zecon on Kaggle.com as pandas DataFrames
2. Create a Mapping table that gives the city-name to region to state, to FIPS links
This mapping table will be pickled and saved in the /data/interim folder as `fips_map.pikcle`
and subsequently used for purposes of data pre-processing.
'''

import pandas as pd 
import numpy as np  

import pathlib
import sys
import os 
sys.path.append(str(pathlib.Path().absolute().parent))

import warnings
warnings.filterwarnings('ignore')


# Unzip the files and read the csvs
csv_dfs = {}

zecon_dir = '../../data/raw/zecon/'

for filename in os.listdir(zecon_dir):
    print(f"Reading in {filename}...")        
    if '.csv' in filename:
        try:
            csv_dfs[filename[:-4]] = pd.read_csv(f'{zecon_dir}{filename}', 
                                                 error_bad_lines=False)
        except:
            csv_dfs[filename[-4:]] = pd.read_csv(f'{zecon_dir}{filename}', 
                                                 encoding='latin-1')

print("All csv's loaded.")


# CREATE FIPS MAP FROM THE COUNTY CROSS WALK, COUNTY TIME SERIES, CITIES CROSSWALK, CITY TIME SERIES
county_xwalk = csv_dfs['CountyCrossWalk_Zillow']
city_xwalk = csv_dfs['cities_crosswalk']

county_ts = csv_dfs['County_time_series']
city_ts = csv_dfs['City_time_series']

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
interim_dir = '../../data/interim/'
merged.to_pickle(f'{interim_dir}fips_map.pickle')
