# THIS SCRIPT PARES THE DATA SCOPE DOWN TO STRICTLY THE STATE OF CALIFORNIA

import pandas as pd
import numpy as np 
import zipcodes
from datetime import datetime
import pickle

import warnings
warnings.filterwarnings('ignore')

import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute().parent))


# LOAD DATA
city_ts = pd.read_csv('../../data/raw/zecon/City_time_series.csv')
zip_ts = pd.read_csv('../../data/raw/zecon/Zip_time_series.csv')

fips_mapping = pd.read_pickle('../../data/interim/fips_map.pickle')


# PARE DOWN CITY TABLE TO JUST CA
print('Begin paring down scope of data to just California...')
city_ts_merged = city_ts.merge(fips_mapping,
                              how='left',
                              left_on='RegionName',
                              right_on='Unique_City_ID')

ca_city_ts = city_ts_merged[city_ts_merged['State'] == 'CA']
ca_city_ts.rename(columns={'RegionName_x': 'RegionName'}, inplace=True)
ca_city_ts.drop('RegionName_y', axis=1, inplace=True)
ca_city_ts.reset_index(drop=True, inplace=True)

# Free up memory
del city_ts_merged
del city_ts


# PARE DOWN ZIP TABLE TO JUST CA 
## Note: All CA Zipcodes start with the number 9
zip_ts['ZipCode_str'] = zip_ts['RegionName'].astype(str)
maybe_ca_zips = [zipcode for zipcode in zip_ts['ZipCode_str'].unique().tolist() if zipcode[0] == '9']

# Use `zipcodes` to pare down the maybe_ca_zips to DEFINITE CA zips
print('Use the `zipcodes` package to gather California-only zip codes...')
confirmed_CA_zips = []

for zipcode in maybe_ca_zips:
    zip_info = zipcodes.matching(zipcode)[0]
    if zip_info['state'] == 'CA':
        confirmed_CA_zips.append(zipcode)
    else:
        pass

ca_zip_ts = zip_ts[zip_ts['ZipCode_str'].isin(confirmed_CA_zips)]
ca_zip_ts.reset_index(drop=True, inplace=True)

# Expand the ca_zip_ts table to include additional location metadata like lat/long/city/county etc.
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

ca_zip_ts['City'] = [zip_city_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['County'] = [zip_county_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Lat'] = [zip_latlong[row.ZipCode_str]['Lat'] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Long'] = [zip_latlong[row.ZipCode_str]['Long'] for row in ca_zip_ts.itertuples()]


# Intermediate Step: Pare down FIPS Mapping to only CA and then grab zipcodes using `zipcodes` package
fips_mapping_CA = fips_mapping.loc[fips_mapping['State'] == 'CA']
fips_mapping_CA.reset_index(drop=True, inplace=True)

zip_meta = dict()
for row in fips_mapping_CA.itertuples():
    city_to_check = row.City
    info = zipcodes.filter_by(city=city_to_check)
    for i in info:
        if row.County in i['county']:
            zip_meta[i['zip_code']] = {'Lat': float(i['lat']), 
                                          'Long': float(i['long']),
                                          'City' : i['city'],
                                          'County' : i['county'].replace(" County", "")}
# Convert the dict to DataFrame
zip_meta_df = pd.DataFrame(zip_meta).T
zip_meta_df.reset_index(inplace=True)

city_uniqueCityID = dict(zip(fips_mapping_CA['City'], fips_mapping_CA['Unique_City_ID']))
city_metroName = dict(zip(fips_mapping_CA['City'], fips_mapping_CA['MetroName']))
city_regionName = dict(zip(fips_mapping_CA['City'], fips_mapping_CA['RegionName']))
 
zip_meta_df['State'] = 'CA'
zip_meta_df['StateName'] = 'California'
zip_meta_df['CensusRegion'] = 'West'

metroname_column = list()
uniquecityID_column = list()
regionname_column = list()

for city in zip_meta_df['City']:
    if city in city_uniqueCityID and city in city_metroName:
        uniquecityID_column.append(city_uniqueCityID[city])
        metroname_column.append(city_metroName[city])
        regionname_column.append(city_regionName[city])
    else:
        uniquecityID_column.append(np.nan)
        metroname_column.append(np.nan)
        regionname_column.append(np.nan)
        
zip_meta_df['Unique_City_ID'] = uniquecityID_column
zip_meta_df['MetroName'] = metroname_column
zip_meta_df['RegionName'] = regionname_column

zip_meta_df.rename(columns={'index':'ZipCode'}, inplace=True)

fips_zip_mapping_CA = zip_meta_df.copy()

# Free up memory
del fips_mapping
del zip_meta_df

# Pare down the data to only hone in in the ZHVI and ZRI columns (which are the most complete of all avail info)
print('Gather the relevant columns for buy / rent predictions...')
ZHVI_ZRI_columns = ['ZHVI_1bedroom', 'ZHVI_2bedroom',
       'ZHVI_3bedroom', 'ZHVI_4bedroom', 'ZHVI_5BedroomOrMore',
       'ZHVI_AllHomes', 'ZHVI_BottomTier', 'ZHVI_CondoCoop', 'ZHVI_MiddleTier',
       'ZHVI_SingleFamilyResidence', 'ZHVI_TopTier', 'ZRI_AllHomes',
       'ZRI_AllHomesPlusMultifamily', 'ZriPerSqft_AllHomes',
       'Zri_MultiFamilyResidenceRental', 'Zri_SingleFamilyResidenceRental']

fips_loc_columns = ['ZipCode_str', 'City', 'County', 'Lat', 'Long']

city_ts_columns = ['Date', 'MetroName', 'StateName', 'CensusRegion', 'Unique_City_ID', 'City', 'County', 'State']
zip_ts_columns = ['Date', 'RegionName', 'ZipCode_str', 'City', 'County', 'Lat', 'Long']

ca_city_zill_ts = ca_city_ts[city_ts_columns + ZHVI_ZRI_columns]
ca_zip_zill_ts = ca_zip_ts[zip_ts_columns + ZHVI_ZRI_columns]

# EXPAND THE CITY DATA WITH ZIP INFORMATION 
# Use the updated fips_zip_mapping_df to expand the location metadata is in both the city and the zip tables
city_w_zips_ts = ca_city_zill_ts.merge(fips_zip_mapping_CA,
                                     on='Unique_City_ID',
                                     how='left',
                                     suffixes=('', '_y'))

# Remove duplicate columns as a result of the merge
for col in city_w_zips_ts.columns:
    if '_y' in col:
        city_w_zips_ts.drop(col, axis=1, inplace=True)
    else:
        pass

# Remove the rows with Zipcodes already in the Zip TS table
city_w_zips_ts = city_w_zips_ts[~city_w_zips_ts['ZipCode'].isin(list(set(ca_zip_zill_ts['ZipCode_str'])))]  
city_w_zips_ts.reset_index(drop=True, inplace=True)

# EXPAND THE ZIP DATA WITH CITY INFORMATION
ca_zip_zill_ts.rename(columns={'RegionName':'ZipCode_int'}, inplace=True)
ca_zip_zill_ts['County'] = [countyname.replace(" County", "") if " County" in countyname else countyname 
                            for countyname in ca_zip_zill_ts['County']]

ca_zip_w_fips = ca_zip_zill_ts.merge(fips_mapping_CA,
                                     how='left',
                                     on=['City', 'County'])


# Save the files (prior to imputing with city-data): 
ca_city_ts.to_pickle('../../data/interim/california-city-ts.pickle')
ca_zip_ts.to_pickle('../../data/interim/california-zip-ts.pickle')

# Save the files (after imputing missing zipcodes with city data)
city_w_zips_ts.to_pickle('../../data/interim/ca-city-w-zip-ts.pickle')
ca_zip_w_fips.to_pickle('../../data/interim/ca-zip-w-city-ts.pickle')


# Clean up the df for modeling:
ca_zip_ts = ca_zip_ts.copy()
del ca_zip_w_fips
del ca_zip_zill_ts
del city_w_zips_ts


ca_zip_ts.rename(columns={'RegionName':'FIPS',
                          'ZipCode_str' : 'ZipCode'}, inplace=True)

# Facebook Prophet needs to have a column called 'ds' with datetime types 
ca_zip_ts['ds'] = ca_zip_ts['Date'].apply(lambda _ : datetime.strptime(_, "%Y-%m-%d"))

all_zips = list(set(ca_zip_ts['ZipCode']))

# Go through the zipcodes and get the min and max dates for each of the zip codes
zip_minmax_dates = dict()

for zipcode in all_zips:
    sub_df = ca_zip_ts[ca_zip_ts['ZipCode'] == zipcode]
    zip_minmax_dates[zipcode] = {'min_date': sub_df.ds.min(),
                                 'max_date': sub_df.ds.max()}

min_max_dates_df = pd.DataFrame(zip_minmax_dates).T
min_max_dates_df.reset_index(inplace=True)
min_max_dates_df.rename(columns={'index':'zip_code'}, inplace=True)

excl_these = min_max_dates_df[(min_max_dates_df['max_date'] < '2017')]

# Create a list of Zipcodes we need to generate 0's for predictions for
zips_to_exclude = excl_these['zip_code'].tolist()
with open ('../../data/processed/exclude_these_zips.pickle', 'wb') as f:
    pickle.dump(zips_to_exclude, f)
    
del excl_these

# Create DataFrame that applies time interpolated values for zipcodes (time series) 
# that have missing values
print("Imputing null values by applying time interpolation...")
interpol = ca_zip_ts.copy()
interpol = interpol[['ds', 'ZipCode', 'ZHVI_SingleFamilyResidence', 'Zri_MultiFamilyResidenceRental']]

interpol_time = interpol.copy()
interpol_time.set_index('ds', inplace=True)

interpol_time = interpol_time.assign(ZHVI_ITime=interpol_time.ZHVI_SingleFamilyResidence.interpolate(method='time', limit_direction='both'))
interpol_time = interpol_time.assign(ZRI_ITime=interpol_time.Zri_MultiFamilyResidenceRental.interpolate(method='time', limit_direction='both'))

interpol_time.drop(['ZHVI_SingleFamilyResidence', 'Zri_MultiFamilyResidenceRental'], axis=1, inplace=True)
interpol_time.rename(columns={'ZHVI_ITime':'ZHVI_SingleFamilyResidence',
                              'ZRI_ITime': 'Zri_MultiFamilyResidenceRental'}, inplace=True) 
interpol_time = interpol_time.reset_index()
interpol_time['ZipCode'] = interpol_time['ZipCode'].astype('int32')

del interpol

# Save the dataframe for modeling into the data/interim folder:
print("Saving the DataFrame for modeling...")
interpol_time.to_pickle('../../data/processed/interpolated_fillnaTime_df.pickle')