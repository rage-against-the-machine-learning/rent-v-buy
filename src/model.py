# This script takes the clean dataset and generates predictions

import pandas as pd

from matplotlib import pyplot as plt
from fbprophet import Prophet
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from dateutil import relativedelta
from scipy import stats

import json
import pickle

import pathlib
import sys
import os 
sys.path.append(str(pathlib.Path().absolute().parent))
    

# number of months between two dates
def find_pred_size (df:pd.DataFrame) -> int:
    '''
    purpose: calculate the number of months b/t the most recent time series data point
    and present day
    :df: pandas DataFrame holding teh time series for a specific zip code
    :output: months (integer)
    '''
    assert 'ds' in df.columns, "'ds' column needs to be in the input DataFrame"
    today = datetime.now()
    r = relativedelta.relativedelta(today, df['ds'].max())
    years = r.years
    months = r.months

    return int((years * 12) + months)


#do we want to rent or buy
def make_model_input_df (data:pd.DataFrame, rent_or_buy:str, rerun:bool=False) -> pd.DataFrame:
    '''
    :data: the entire dataframe generated by the california_only.py script
    :rent_or_buy: input string to specify which of the two prediciton values to forecast
    :rerun: a boolean value to indicate if this is the second time the model is being run (True--run a second time, False--run for the first time)
    :zip_code_of_interest: 5 digit integer
    :returns: a DataFrame ready to input into fbprophet for time series forecasting'''

    #based on the input which column do we want to look at
    # we will do both as long as data is present for each zip code
    if rent_or_buy == 'rent':   
        model_payload = data.rename(columns={ 'Zri_MultiFamilyResidenceRental': 'y'})
    else:
        model_payload = data.rename(columns={'ZHVI_SingleFamilyResidence': 'y'})

    #if this is a model rerun? if so removed the outliers
    if rerun:
        y=model_payload['y']
        acceptable_range = y.between(y.quantile(0.1), y.quantile(0.9)) 
        index_names = model_payload[~acceptable_range].index
        model_payload.drop(index_names, inplace=True) 

    return model_payload


#actual prediction model
def find_value_today(model_payload:pd.DataFrame, prediction_size:int) -> (float, pd.DataFrame):
    '''
    purpose: generate a predicted value based on the specified rent or buy input 
    :model_payload: DataFrame already filtered on a zipcode w/ either rent or buy specified 
    :prediction_size: the number of periods (in months) between the last actual data point time and today
    :output: returns a tuple (forecasted rent or buy value, DataFrame with underlying time series Trend)
    '''

    try:
        my_model = Prophet(interval_width=0.95, 
                           yearly_seasonality= 3, 
                           weekly_seasonality=False, 
                           daily_seasonality=False)
        
        my_model.fit(model_payload)

        future = my_model.make_future_dataframe(periods=prediction_size, freq='M')
        # make a predictions DataFrame
        forecast = my_model.predict(future)
        # my_forcast_data = forecast[['ds', 'yhat']] <-- this is unreachable code 

        # Collect the last projected value (today's value)
        value_today = forecast['yhat'].iloc[-1]
        appr_data = forecast["trend"]
        return value_today, appr_data

    except:
        value_today = 0
        return value_today, None


def calc_appr_rate(appr_data:pd.DataFrame):
    '''
    purpose: this function looks back to the most recent 3 year appreciation trends
    and calculates the Compound Annual Growth Rate
    :appr_data: trend data generated from Facebook Prophet when the predictions were generated
    '''
    # Use indices to get the most recent 3 years
    old_value = appr_data.iloc[-37]
    new_value = appr_data.iloc[-1]

    # Calculate CAGR
    cagr = (new_value / old_value)**(1/3) - 1
    return round(cagr * 100, 2)
    
def get_rerun_list(my_dict:dict) -> (list, float, float):   
    '''
    Given a dictonary
    1. Find the std of the appr_rate and the mode and use this to determine the zipcodes that are outside of this range
    2. Find buy and rent values that are X10 the mean
    3. Find buy and rent values that are negative
    4. Output a list of zipcodes that need to be rerun
    
    :my_dict: a dictonary generated from make_UI_n_dec_calculator_outputs()
    '''
    df_og = pd.DataFrame(my_dict).T

    #get std and mode to determine which zipcodes to rerun
    appr_std = df_og.describe(include='all').loc['std']['appr_rate']
    appr_mode = stats.mode(df_og['appr_rate'])[0][0]

    appr_max = appr_mode + (appr_std *2)
    rerun_appr_max = df_og.index[df_og['appr_rate'] > appr_max].tolist()

    appr_min = appr_mode - (appr_std *2)
    rerun_appr_min = df_og.index[df_og['appr_rate'] < appr_min].tolist()

    #all the buy and rent values that are negative because that is not possible
    rerun_buy_min = df_og.index[df_og['buy'] < 0].tolist()
    rerun_rent_min = df_og.index[df_og['rent'] < 0].tolist()

    #max buy and rent values that are 10X the mean 
    buy_max = df_og.describe(include='all').loc['mean']['buy']*10
    rerun_buy_max = df_og.index[df_og['buy'] > buy_max].tolist()

    rent_max = (df_og.describe(include='all').loc['mean']['rent'])*10
    rerun_rent_max = df_og.index[df_og['rent'] > rent_max].tolist()

    #join these lists 
    rerun_list = list(set().union(rerun_buy_max, rerun_buy_min, rerun_rent_max, rerun_rent_min, rerun_appr_max, rerun_appr_min))
    rerun_list = [int(i) for i in rerun_list]
    print('Rerunning the following zipcodes...', rerun_list)
          
    return (rerun_list, appr_max, appr_min)
          
def get_delete_zipcodes(my_dict, appr_max, appr_min):
    '''
    Given a dictonary, max and min appreciation rate boundries
    1. Find buy and rent values that are negative
    2. Find appr_rates that are outside the boundries
    3. Output a list of zipcodes that need to be rerun
    
    my_dict: a dictonary generated from make_UI_n_dec_calculator_outputs() after certain zipcodes are rerun
    '''
    df = pd.DataFrame(my_dict).T

    #deleting values that are STILL negative. Its not possible so these need to be removed. 
    #this involves a close look into the model though
    delete_buy_min = df.index[df['buy'] < 0].tolist()
    delete_rent_min = df.index[df['rent'] < 0].tolist()

    delete_appr_max = df.index[df['appr_rate'] > appr_max].tolist()

    delete_appr_min = df.index[df['appr_rate'] < appr_min].tolist()

    delete_list = list(set().union(delete_buy_min, delete_rent_min, delete_appr_min))
    delete_list = [int(i) for i in delete_list]
    print('Removing all data for the following zipcodes:', delete_list)
    
    return delete_list
          
def make_UI_n_dec_calculator_outputs (my_data:pd.DataFrame, zip_code_of_interest:int, excl_zips:list, rerun:bool=False) -> (dict, dict):
    '''
    Given a zipcode, 
    1. Filter all time series data for that zip code
    2. Determine the prediction size
    3. Create sub dataframes each for rent and buy (as payloads for prediction)
    4. Generate predictions using FB Prophet for each rent & buy
    5. Use the respective trend data for rent & buy to calculate CAGR (appreciation rates)

    :my_data: preprocessed data generated by california_only.py script
    :zipcode_of_interest: 5 digit integer for the zipcode specified
    :rerun: a boolean value to determine if this is the second time the model is being run 
    :excl_zips: list of zip codes for which there is not sufficient information
    '''
    assert len(str(zip_code_of_interest)) == 5

    if zip_code_of_interest not in excl_zips:

        # For each zipcode
        clean_data = my_data.loc[my_data['ZipCode'] == zip_code_of_interest]
        clean_data.reset_index(drop=True, inplace=True)
        
        if rerun:
            # prepare the dataframe for payload to model
            rent_dataset = make_model_input_df(clean_data, 'rent', True)
            buy_dataset  = make_model_input_df(clean_data, 'buy', True)
        else:    
            rent_dataset = make_model_input_df(clean_data, 'rent')
            buy_dataset  = make_model_input_df(clean_data, 'buy')
        
        
        # Determine the number of months for which to forecast
        prediction_size_rent = find_pred_size(rent_dataset)
        prediction_size_buy  = find_pred_size(buy_dataset) 
        
        # Predict rent & buy values, keep trend data for home value trends
        rent_value, _ = find_value_today(rent_dataset, prediction_size_rent) # we don't need appr rates for rentals
        buy_value, appr_data_buy  = find_value_today(buy_dataset, prediction_size_buy)
        
        # Calculate the appreciation rate
        appr_rate_buy = calc_appr_rate(appr_data_buy)
        
        # Round values for UI output; exclude cents in rental values, express buy values in thousands
        rent_value = int(rent_value) 
        buy_value = round(buy_value/1000, 1) 

        UI_formatted = {str(zip_code_of_interest): {"buy": f'${buy_value:,}K', 
                                                    "rent": f'${rent_value:,}/month', 
                                                    "appr_rate" : f'{appr_rate_buy}%'}}

        rentVbuy_formatted = {str(zip_code_of_interest): {"buy": buy_value, 
                                                        "rent": rent_value, 
                                                        "appr_rate" : appr_rate_buy }}

    else:
        UI_formatted = {str(zip_code_of_interest): {"buy": '$0', 
                                                    "rent": '$0', 
                                                    "appr_rate" : '0%'}}

        rentVbuy_formatted = {str(zip_code_of_interest): {"buy": 0, 
                                                          "rent": 0, 
                                                          "appr_rate" : 0 }}

    return UI_formatted, rentVbuy_formatted

    
# 1. BRING IN THE PREPROCESSED DATA & skip-zip codes
processed = pd.read_pickle('../data/interim/interpolated_fillnaTime_df.pickle')

my_file = open ('../../data/processed/exclude_these_zips.pickle', 'rb')
excl_zips = pickle.load(my_file)
excl_zips = [int(zip) for zip in excl_zips]


#2. Get all unique zip codes & iterate over them to create outputs:
all_ca_zips = processed['ZipCode'].unique().tolist()

UI_output = dict()
calculator_output = dict()

for zipcode in all_ca_zips:
    if zipcode not in excl_zips:
        UI, calculator = make_UI_n_dec_calculator_outputs (processed, zipcode, excl_zips)
        UI_output.update(UI)
        calculator_output.update(calculator)

with open('../../data/predictions/UI_output.json', 'w') as f1:
    json.dump(UI_output, f1)

with open('../../data/predictions/calculator_output.json', 'w') as f2:
    json.dump(calculator_output, f2)


## 3. Now we are going to rerun the predictions for certain models
rerun_list, appr_max, appr_min = get_rerun_list(calculator_output)

#rerun Prophet for the zipcodes that were identified
UI_output_rerun = dict()
calculator_output_rerun = dict()
excl_zips=[]
for zipcode in rerun_list :
    UI, calculator = make_UI_n_dec_calculator_outputs (processed, zipcode, excl_zips, True)
    UI_output_rerun.update(UI)
    calculator_output_rerun.update(calculator)
    calculator_output[str(zipcode)]=calculator_output_rerun[str(zipcode)]
    UI_output[str(zipcode)]=(UI_output_rerun[str(zipcode)])
delete_list = get_delete_zipcodes(calculator_output_rerun, appr_max, appr_min)

#deleting the old data on these zipcodes and replacing it 
for zipcode in delete_list:
    del calculator_output[str(zipcode)]
    del UI_output[str(zipcode)]
    #if they are in the delete_list then we just replace the values 
    # with 0 as we do not have enough information on these zipcodes
    no_info_cal = {str(zipcode): {"buy": 0, 
                                     "rent": 0, 
                                     "appr_rate" : 0 }}
    no_info_ui = {str(zipcode): {"buy": '$0', 
                                      "rent": '$0', 
                                       "appr_rate" : '0%'}}
    calculator_output.update(no_info_cal)
    UI_output.update(no_info_ui)
    #replace new data with outliers removed to the rest of the zipcode data
    else:
        calculator_output[str(zipcode)]=calculator_output_rerun[str(zipcode)]
        UI_output[str(zipcode)]=(UI_output_rerun[str(zipcode)])

with open('../data/predictions/UI_output_final.json', 'w') as f5:
    json.dump(UI_output, f5)

with open('../data/predictions/calculator_output_final.json', 'w') as f6:
    json.dump(calculator_output, f6)
