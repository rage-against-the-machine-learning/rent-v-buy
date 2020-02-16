import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import xmltodict
import pprint
from bs4 import BeautifulSoup
import ssl
import json
import pandas as pd
import requests

zillow_api_key = "X1-ZWz17ft1hv1urv_2avji"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Finding neighborhoods
service_url = "http://www.zillow.com/webservice/GetRegionChildren.htm?"
parms = dict()
parms['zws-id'] = zillow_api_key
parms['state'] = "Texas"
parms['city'] = "Austin"
parms['childtype'] = "neighborhood"

url = service_url + urllib.parse.urlencode(parms)
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')

# List all neighborhoods
zillow_response = BeautifulSoup(data, "xml").find('response').find('list')
#print(zillow_response)

df = pd.DataFrame(data = {'neighborhood': [tag.find(text=True) for tag in zillow_response.find_all('name')],
                        'longitude': [tag.find(text=True) for tag in zillow_response.find_all('longitude')],
                        'latitude': [tag.find(text=True) for tag in zillow_response.find_all('latitude')]}).set_index('neighborhood')
print(df)

# Get specific information about one neighborhood
# Get schools
test_neighborhood = 'North Austin'
realtor_headers = {
    'x-rapidapi-host': "realtor.p.rapidapi.com",
    'x-rapidapi-key': "70005b5ee2msh5ea18e4551424e5p168e01jsn6bc7cf8d8fba"
    }
realtor_url = "https://realtor.p.rapidapi.com/schools/list-nearby"

querystring = {"lon": str(df.loc['North Austin', 'longitude']),"lat": str(df.loc['North Austin', 'latitude'])}

response = requests.request("GET", realtor_url, headers=realtor_headers, params=querystring)
response = response.text

msg = json.loads(response)

for school in msg["schools"]:
    print(school["name"])


# Find rent and/or sale price for a house
service_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
parms = dict()
parms['zws-id'] = zillow_api_key
parms['rentzestimate'] = "true"
parms['address'] = "4709 Pecan Springs Rd"
parms['citystatezip'] = "Austin, TX"

url = service_url + urllib.parse.urlencode(parms)
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')

zillow_response = BeautifulSoup(data, "xml").find('response').find('results').find('result')

sale_estimate = int( zillow_response.find('zestimate').find('amount').find(text=True) )
rent_estimate = int( zillow_response.find('rentzestimate').find('amount').find(text=True) )

print(sale_estimate)
print(rent_estimate)

# Rent vs buy calculation
down_payment = 40000 # $
interest_rate = 0.06
amortization_horizon = 30 # years
property_tax_rate = 0.0125
hoa_dues = 2000 # $ annual
insurance = 1500 # $ anual
annual_appreciation = 0.03 # annual [to be replaced w/ ML model]
marginal_income_tax_rate = 0.30 # depends on tax bracket
inflation = 0.02

# monthly mortgage payment
initial_principal = sale_estimate-down_payment
mortgage_estimate = initial_principal*(1.0-1.0/(1.0+interest_rate/12))/( 1.0-1.0/(1.0+interest_rate/12)**(1.0+amortization_horizon*12) )

print(mortgage_estimate)

# Month 1
debt = initial_principal
interest = debt*interest_rate/12
paid_principal = mortgage_estimate-interest

print(paid_principal)