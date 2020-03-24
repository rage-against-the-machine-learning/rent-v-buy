## SCRIPT TO PREPARE DATA FOR MODEL PAYLOAD

import pandas as pd 
import numpy as np 

from datetime import datetime

import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute().parent))

# Load Data from data/interim directory:
zip_w_city = pd.read_pickle('../data/interim/ca-zip-w-city-ts.pickle')
city_w_zip = pd.read_pickle('../data/interim/ca-city-w-zip-ts.pickle')

ts_data = pd.concat([zip_w_city, city_w_zip])

# Transformations necessary for FB Prophet
# the date column must be a datetime type and labeled 'ds'
# the column we wish teo forecast must be labeled 'y'

class Prep_For_Modeling():

    def __init__(self, ts_df):     
        '''
        When initializing, pass in the time series DataFrame
        '''
        self.ts = ts_df
        self.zip = pd.DataFrame
        self.br = pd.DataFrame
        

    def convert_str_date_to_datetime (self, df:pd.DataFrame=ts_data) -> pd.DataFrame:
        '''
        converts the string values in "Date" column to datetime objects
        renames the "Date" column to "ds
        '''
        assert 'Date' in df.columns, 'df columns must contain a column "Date".'
        df['ds'] = df['Date'].apply(lambda _ : datetime.strptime(_, "%Y-%m-%d"))
        return df.drop('Date', axis=1)


    def user_specified_zipCode (self, zipcode, df:pd.DataFrame=self.ts) -> pd.DataFrame:
        '''
        pare down training data to only relevant zipcode
        '''
        if type(zipcode) == str: 
            pass
        elif type(zipcode) == float or type(zipcode) == int:
            zipcode = str(zipcode)

        zip_ts = df[df['ZipCode'] == zipcode]
        zip_ts.reset_index(drop=True, inplace=True)
        self.zip = zip_ts
        

    def user_specified_BR (self, num_of_br, df:pd.DataFrame=self.zip) -> pd.DataFrame:
        '''
        pare down training data to only relevant columns
        '''
        if type(num_of_br) == str:
            pass
        elif type(num_of_br) == float or type(num_of_br) == int:
            num_of_br = str(num_of_br)

        cols_to_get = [col for col in df.columns if num_of_br in col]
        self.br = df[cols_to_get]



