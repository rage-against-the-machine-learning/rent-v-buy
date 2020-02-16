import requests

url = "https://realtor.p.rapidapi.com/properties/list-for-sale"

querystring = {"sort":"relevance","radius":"10","city":"Austin","offset":"0","limit":"20","state_code":"TX"}

headers = {
    'x-rapidapi-host': "realtor.p.rapidapi.com",
    'x-rapidapi-key': "70005b5ee2msh5ea18e4551424e5p168e01jsn6bc7cf8d8fba"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)