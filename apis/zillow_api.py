import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import xmltodict
import pprint
from bs4 import BeautifulSoup
import ssl
import json

api_key = "X1-ZWz17ft1hv1urv_2avji"
service_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?' #zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

parms = dict()
parms['zws-id'] = api_key
parms['rentzestimate'] = "true"
parms['address'] = "5212 Duval St #B"
parms['citystatezip'] = "Austin, TX"

url = service_url + urllib.parse.urlencode(parms)
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')


soup = BeautifulSoup(data, "xml")
print("---First response-----")
print(soup.prettify())

zpid = soup.select("zpid")[0].find(text=True)

print("Latitude: ", soup.response.results.latitude.find(text=True))
print("Longitude: ", soup.response.results.longitude.find(text=True))
print("Size [sq ft]: ", soup.response.results.finishedSqFt.find(text=True))
print("Bedrooms: ", soup.response.results.bedrooms.find(text=True))
print("Bathrooms: ", soup.response.results.bathrooms.find(text=True))
print("Year built: ", soup.response.results.yearBuilt.find(text=True))
print("Property value estimate: [US$]", soup.response.results.zestimate.amount.find(text=True))
print("Rent estimate: [US$]", soup.response.results.rentzestimate.amount.find(text=True))

# Finding neighborhoods
service_url = 'http://www.zillow.com/webservice/GetRegionChildren.htm?' #zws-id=<ZWSID>&state=wa&city=seattle&childtype=neighborhood
parms = dict()
parms['zws-id'] = api_key
parms['state'] = "Texas"
parms['city'] = "Austin"
parms['childtype'] = "neighborhood"

url = service_url + urllib.parse.urlencode(parms)
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')


soup = BeautifulSoup(data, "xml")
print("---Second response-----")
print(soup.prettify())

neighborhoods = [tag.find(text=True) for tag in soup.find_all('name')]

for neighborhood in neighborhoods:
    print('Searching ', neighborhood)