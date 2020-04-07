'''
california_only.py 

This script serves to pare down the scope of the data collected from Zillow to only
* California
* Zip Code level granularity
'''

import pandas as pd 
import zipcodes

import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute().parent.parent))

import warnings
warnings.filterwarnings('ignore')


# 1. Load the Data
data_zecon_path = str(pathlib.Path().absolute().parent) + '/data/raw/zecon'
data_interim_path = str(pathlib.Path().absolute().parent) + '/data/interim'

county_ts = pd.read_csv(f'{data_zecon_path}/County_time_series.csv')
city_ts = pd.read_csv(f'{data_zecon_path}/City_time_series.csv')
zip_ts = pd.read_csv(f'{data_zecon_path}/Zip_time_series.csv')
fips_mapping = pd.read_pickle(f'{data_interim_path}/fips_map.pickle')

# 2. Scope the data down to CA

# 2A. Scope down to CA at the city-level
city_ts_merged = city_ts.merge(fips_mapping,
                              how='left',
                              left_on='RegionName',
                              right_on='Unique_City_ID')

ca_city_ts = city_ts_merged[city_ts_merged['State'] == 'CA']
ca_city_ts.rename(columns={'RegionName_x': 'RegionName'}, inplace=True)
ca_city_ts.drop('RegionName_y', axis=1, inplace=True)
ca_city_ts.reset_index(drop=True, inplace=True)

# 2B. Scope down to CA at the ZipCode level 
zip_ts['ZipCode_str'] = zip_ts['RegionName'].astype(str)
zip_ts['ZipCode_str'] = ['0' + zipcode if len(zipcode) == 4 else zipcode for zipcode in zip_ts['ZipCode_str']]

# All CA zipcodes begin with the number 9
potential_CA_zipcodes = [zipcode for zipcode in zip_ts['ZipCode_str'].unique().tolist() if zipcode[0] == '9']

print('Using zipcodes package to help scope down data to CA-only...')
confirmed_CA_zips = []
for zipcode in potential_CA_zipcodes:
    # Use the zipcodes package to only save those zipcodes that are in fact located in California
    zip_info = zipcodes.matching(zipcode)[0]
    if zip_info['state'] == 'CA':
        confirmed_CA_zips.append(zipcode)
    else:
        pass

# Filter down on these potential California zipcodes
ca_zip_ts = zip_ts[zip_ts['ZipCode_str'].isin(confirmed_CA_zips)]
ca_zip_ts.reset_index(drop=True, inplace=True)

# Use zipcodes package to retreive county information and lat/long coordinates
zip_city_map = dict()
zip_county_map = dict()
zip_latlong = dict()

for zipcode in ca_zip_ts['ZipCode_str'].unique():
    zipinfo = zipcodes.matching(zipcode)
    try: 
        for info in zipinfo:
            zip_city_map[zipcode] = info['city']
            zip_county_map[zipcode] = info['county']
            zip_latlong[zipcode] = {'Lat' : info['lat'], 'Long' : info['long']}
    except:
        pass

# Extend the dataframe with this metadata
ca_zip_ts['City'] = [zip_city_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['County'] = [zip_county_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Lat'] = [zip_latlong[row.ZipCode_str]['Lat'] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Long'] = [zip_latlong[row.ZipCode_str]['Long'] for row in ca_zip_ts.itertuples()]

print('Data scoped to CA only...')
print('Select relevant columns for prediction...')

# Grab relevant columns of interest for predicting rent & buy values
ZHVI_ZRI_columns = ['ZHVIPerSqft_AllHomes', 'PctOfHomesDecreasingInValues_AllHomes',
       'PctOfHomesIncreasingInValues_AllHomes',
       'PctOfListingsWithPriceReductionsSeasAdj_AllHomes',
       'PctOfListingsWithPriceReductionsSeasAdj_CondoCoop',
       'PctOfListingsWithPriceReductionsSeasAdj_SingleFamilyResidence',
       'PctOfListingsWithPriceReductions_AllHomes',
       'PctOfListingsWithPriceReductions_CondoCoop',
       'PctOfListingsWithPriceReductions_SingleFamilyResidence',
       'PriceToRentRatio_AllHomes', 'ZHVI_1bedroom', 'ZHVI_2bedroom',
       'ZHVI_3bedroom', 'ZHVI_4bedroom', 'ZHVI_5BedroomOrMore',
       'ZHVI_AllHomes', 'ZHVI_BottomTier', 'ZHVI_CondoCoop', 'ZHVI_MiddleTier',
       'ZHVI_SingleFamilyResidence', 'ZHVI_TopTier', 'ZRI_AllHomes',
       'ZRI_AllHomesPlusMultifamily', 'ZriPerSqft_AllHomes',
       'Zri_MultiFamilyResidenceRental', 'Zri_SingleFamilyResidenceRental']

fips_loc_columns = ['ZipCode_str', 'City', 'County', 'Lat', 'Long']

city_ts_columns = ['Date', 'MetroName', 'StateName', 'CensusRegion', 'Unique_City_ID', 'City', 'County', 'State']
zip_ts_columns = ['Date', 'RegionName', 'ZipCode_str', 'City', 'County', 'Lat', 'Long']

 
# 2B. Create a CA only FIPS mapping table
fips_mapping_CA = fips_mapping.loc[fips_mapping['State'] == 'CA']
fips_mapping_CA.reset_index(drop=True, inplace=True)

print('Create pandas DataFrame for model predictions...')
# Create the dataframe to use for predictions
ca_zip_zill_ts = ca_zip_ts[zip_ts_columns + ZHVI_ZRI_columns]
ca_zip_zill_ts.rename(columns={'RegionName':'ZipCode_int'}, inplace=True)
ca_zip_zill_ts['County'] = [countyname.replace(" County", "") if " County" in countyname else countyname 
                            for countyname in ca_zip_zill_ts['County']]

ca_zip_w_fips = ca_zip_zill_ts.merge(fips_mapping_CA,
                                     how='left',
                                     on=['City', 'County'])


# 3. Save the CA scoped zip code data into the interim data folder 
print('Saving the pickled CA-only zip code time series data to the interim folder...')
ca_zip_w_fips.to_pickle(f'{data_interim_path}/ca-zip-ts.pickle')




    





