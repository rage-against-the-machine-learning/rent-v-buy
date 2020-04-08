# this script takes the clean dataset gets the data for the current month
# Created by Skye
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime
from dateutil.parser import parse
from dateutil import relativedelta
from tqdm import tqdm
import json
    
# number of months between two dates
def find_pred_size (df:pd.DataFrame) -> int:
    assert 'ds' in df.columns, "'ds' column needs to be in the input DataFrame"
    today = datetime.now()
    r = relativedelta.relativedelta(today, df['ds'].max())
    years = r.years
    months = r.months
    return int((years * 12) + months)

#do we want to rent or buy
def interest_dataset(data, rent_or_buy, zip_code_of_interest):
    #based on the input which column do we want to look at
    # we will do both as long as data is present for each zip code
    if rent_or_buy == 'rent':   
        renamed_dataset = data.rename(columns={ 'Zri_MultiFamilyResidenceRental': 'y'})
    else:
        renamed_dataset = data.rename(columns={'ZHVI_SingleFamilyResidence': 'y'})
        
    return renamed_dataset

#actual prediction model
def find_value_today(data, prediction_size):
    try:
        my_model = Prophet(interval_width=0.95, 
                           yearly_seasonality= 3, 
                           weekly_seasonality=False, 
                           daily_seasonality=False)
        #my_model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        my_model.fit(data)
        future = my_model.make_future_dataframe(periods=prediction_size, freq='M')
        forecast = my_model.predict(future)
        my_forcast_data = forecast[['ds', 'yhat']]
        value_today = forecast['yhat'].iloc[-1]
        appr_data = forecast["trend"]
    except:
        value_today = 0
    return value_today, appr_data

def cal_appre_rate(df, appr_data):
    old_value = appr_data.iloc[-37]
    print(old_value)
    new_value = appr_data.iloc[-1]
    print(new_value)
    rate = np.exp(np.log(new_value/old_value)/3) - 1.0
    return round(rate*100, 2)

def make_main(my_data, zip_code_of_interest):
    #for each zipcode
    clean_data = my_data.loc[my_data['ZipCode'] == zip_code_of_interest]
    
    #change date column to the correct format
    prediction_size_rent = find_pred_size(clean_data)
    prediction_size_buy  = find_pred_size(clean_data)
    
    #zipcode we want data for
    # #need to check if region name is always the same...
    rent_dataset = interest_dataset(clean_data, 'rent', zip_code_of_interest)
    buy_dataset  = interest_dataset(clean_data, 'buy', zip_code_of_interest)
   
    #predict
    rent_value, appr_data_rent = find_value_today(rent_dataset, prediction_size_rent)
    #print(rent_value)
    buy_value, appr_data_buy  = find_value_today(buy_dataset, prediction_size_buy)
    #print(buy_value)
    
    #appreciation rate
    appr_rate_buy = cal_appre_rate(buy_dataset, appr_data_buy)
    
    #round values
    rent_value = int(rent_value)
    buy_value = round(buy_value/1000, 1)
    
    return {str(zip_code_of_interest): {"buy": f'${buy_value:,}k', "rent": f'${rent_value:,}/month', "appr_rate" : f'{appr_rate_buy}%'}}


#get the clean data
clean_data = pd.read_pickle('../data/interim/interpolated_fillnaTime_df.pickle')

#get the list of zipcodes so we can parse through them
cal_zip_list = clean_data['ZipCode'].unique().tolist()

#run Prophet on all the zipcodes
result_dict={}
for i in tqdm(cal_zip_list):
    result = make_main(clean_data, i)
    result_dict.update(result)

#make sure its in double quotes and not single quotes
my_dict = json.dumps(result_dict)
test_dict = json.loads(my_dict)

#put it into a csv file
df = pd.DataFrame(test_dict).T
df.to_csv('../data/interim/rent_buy_zip.csv')