# THIS SCRIPT PARES THE DATA SCOPE DOWN TO STRICTLY THE STATE OF CALIFORNIA

import pandas as pd
import numpy as np 
import zipcodes

import warnings
warnings.filterwarnings('ignore')

import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute().parent))


# Load the Data
county_ts = pd.read_csv('../data/raw/unzipped/County_time_series.csv/County_time_series.csv')
city_ts = pd.read_csv('../data/raw/unzipped/City_time_series.csv/City_time_series.csv')
zip_ts = pd.read_csv('../data/raw/unzipped/Zip_time_series.csv/Zip_time_series.csv')

fips_mapping = pd.read_pickle('../data/interim/fips_map.pickle')


# Pare each of down to only hold data points for the state of CA
ca_ts_merged = county_ts.merge(fips_mapping, 
                                how='left', 
                                on='RegionName')
ca_county_ts = ca_ts_merged[ca_ts_merged['State'] == 'CA']
ca_county_ts.reset_index(drop=True, inplace=True)

city_ts_merged = city_ts.merge(fips_mapping,
                              how='left',
                              left_on='RegionName',
                              right_on='Unique_City_ID')
ca_city_ts = city_ts_merged[city_ts_merged['State'] == 'CA']
ca_city_ts.reset_index(drop=True, inplace=True)

# Free up memory
del ca_ts_merged
del city_ts_merged
del county_ts
del city_ts

# Intermediate Step: Pare down FIPS Mapping to only CA and then grab zipcodes using `zipcodes` package
fips_mapping_CA = fips_mapping[fips_mapping['State'] == 'CA']

# Skye was right to put it in a dictionary instead of nested list objects
zip_meta = dict()

for row in fips_mapping_CA.itertuples():
    city_to_check = row.City 
    # There are repeat city names across the country
    info = zipcodes.filter_by(city=city_to_check)

    for i in info:
        # Grab only the relevant zip code metadata if the county matches (i.e. CA county, ignoring non-CA counties)
        if row.County in i['county']:
            zip_meta[i['zip_code']] = {'lat': float(i['lat']), 
                                          'long': float(i['long']),
                                          'city' : i['city'],
                                          'county' : i['county'].rstrip(" County")}

# Convert the zip_meta dict to a DatFrame
zip_meta_df = pd.DataFrame(zip_meta).T
zip_meta_df.reset_index(inplace=True)
 
# Now merge in the zip_meta_df with the fips_mapping_CA table to lengthen the table to hold all possible zip codes
# Each row with its own zip code
fips_zip_mapping_CA = zip_meta_df.merge(fips_mapping_CA,
                                        how='left',
                                        left_on=['county', 'city'],
                                        right_on=['County', 'City'])
fips_zip_mapping_CA.rename(columns={'index':'Zipcodes'}, inplace=True)
# Free up memory
del fips_mapping
del fips_mapping_CA


## Note: All CA Zipcodes start with the number 9
zip_ts['ZipCode_str'] = zip_ts['RegionName'].astype(str)
maybe_ca_zips = [zipcode for zipcode in zip_ts['ZipCode_str'].unique().tolist() if zipcode[0] == '9']

# Use `zipcodes` to pare down the maybe_ca_zips to DEFINITE CA zips
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
            zip_latlong[zipcode] = {'lat' : info['lat'], 'long' : info['long']}
            
    except:
        pass

ca_zip_ts['City'] = [zip_city_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['County'] = [zip_county_map[row.ZipCode_str] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Lat'] = [zip_latlong[row.ZipCode_str]['lat'] for row in ca_zip_ts.itertuples()]
ca_zip_ts['Long'] = [zip_latlong[row.ZipCode_str]['long'] for row in ca_zip_ts.itertuples()]

# Use the updated fips_zip_mapping_df to ensure the location metadata is in both the city and the zip tables



# Save the files: 
ca_city_ts.to_pickle('../data/interim/california-city-ts.pickle')
ca_zip_ts.to_pickle('../data/interim/california-zip-ts.pickle')