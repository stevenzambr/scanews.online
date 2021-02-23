import requests
import json
import os
import time
from datetime import datetime, date, timedelta

# Currents API 

# Read locally stored private Currents API Key
with open('../apiKeys.json') as f:
  currentsApiKey = json.load(f)["Currents"]

# Currents API supported languages, countries and categories
supportedLanguages = {"Arabic":"ar","Chinese":"zh","Dutch":"nl","English":"en","Finnish":"fi","French":"fr","German":"de","Hindi":"hi","Italian":"it","Japanese":"ja","Korean":"ko","Malay":"msa","Portuguese":"pt","Russian":"ru","Spanish":"es","Vietnamise":"vi"}
supportedCountries = {"United State":"US","Taiwan":"TW","German":"DE","United Kingdom":"GB","China":"CN","India":"IN","Spain":"ES","Italy":"IT","Poland":"PL","Australia":"AU","Malaysia":"MY","Singapore":"SG","Canada":"CA","South Korea":"KR","Denmark":"DK","France":"FR","Belgium":"BE","Japan":"JP","Austria":"AT","Portugal":"PT","Philippines":"PH","Hong Kong":"HK","Argentina":"AR","Venezuela":"VE","Brazil":"BR","Finland":"FI","Indonedia":"ID","Vietnam":"VN","Mexico":"MX","Greece":"GR","Netherlands":"NL","Norway":"NO","New Zealand":"NZ","Russia":"RU","Saudi-Arabia":"SA","Switzerland":"CH","Thailand":"TH","United Arab Emirates":"AE","Ireland":"IE","Iran":"IR","Iraq":"IQ","Romania":"RO","Afghanistan":"AF","Zimbabwe":"ZW","Myanmar":"MM","Sweden":"SE","Peru":"PE","Panama":"PA","Egypt":"EG","Turkey":"TR","Israel":"IL","Czech Republic":"CZ","Bangladesh":"BD","Nigeria":"NG","Kenya":"KE","Chile":"CL","Uruguay":"UY","Ecuador":"EC","Serbia":"RS","Hungary":"HU","Slovenia":"SI","Gahana":"GH","Bolivia":"BO","Pakistan":"PK","Colombia":"CO","North Korea":"NK","Paraguay":"PY","Palestine":"PS","Estonia":"EE","Lebanon":"LB","Qatar":"QA","Kuwait":"KW","Cambodia":"KH","Nepal":"NP","Luxembourg":"LU","Bosnia":"BA","Europe":"EU","Asia":"ASIA","International":"INT"}
supportedCategories = ["regional","technology","lifestyle","business","general","programming","science","entertainment","world","sports","finance","academia","politics","health","opinion","food","game","fashion","academic","crap","travel","culture","economy","environment","art","music","notsure","CS","education","redundant","television","commodity","movie","entrepreneur","review","auto","energy","celebrity","medical","gadgets","design","EE","security","mobile","estate","funny"]

# # Currents Latest News API https://currentsapi.services/en/docs/latest_news

# # Configurable parameter for currents latest news API
# language = supportedLanguages["English"]

# # Currents API has 600 requests available per day (1 request every 2:24 minutes)
# url = (f'https://api.currentsapi.services/v1/latest-news?language={language}&apiKey='+currentsApiKey)
# dataLatestNews = requests.get(url).json()


# # Save currents latest news file locally
# with open('dataFiles/dataCurrentsLatestNews.json', 'w') as outfile:
#     json.dump(dataLatestNews, outfile)


# # Upload/Update Currents latest news data file on website server
# commandToRun = 'scp dataFiles/dataCurrentsLatestNews.json stevenzv7@scanews.online:"~/scanews.online/dataFiles"'
# while True:
# 	try:
# 		# Command will only run with correct locally stored private ssh keys
# 		os.system(commandToRun)
# 		break
# 	except:
# 		print("Could not connect to server, retrying in 5sec...")
# 		time.sleep(5)
# 		pass	

# Currents Search API https://currentsapi.services/en/docs/search

# Configurable parameters for currents search API
language = supportedLanguages["English"]
start_date = (date.today()-timedelta(days=1)).strftime("%Y-%m-%d") # &start_date={start_date}
end_date =date.today().strftime("%Y-%m-%d") # &end_date={end_date}
typeParameter = "1" # &type={typeParameter}
country = supportedCountries["International"] # &country={country}
category = "world, general" # &category={category}
page_number = "1" # &page_number={page_number}
# domain = "bbc.com,cnn.com,nytimes.com,theguardian.com,foxnews.com,washingtonpost.com,cnbc.com" # &domain={domain}
domain = "bbc.com,cnn.com,nytimes.com,dailymail.co.uk,theguardian.com,foxnews.com,washingtonpost.com,cnbc.com,express.co.uk,usatoday.com,buzzfeed.com,nbcnews.com,thesun.co.uk,nypost.com,businessinsider.com,forbes.com" # &domain={domain}
keywords = "" # &keywords={keywords}
# domain_not = # &domain_not={domain_not}

# Currents API has 600 requests available per day (1 request every 2:24 minutes for continuous 24h)
url = (f'https://api.currentsapi.services/v1/search?language={language}&start_date={start_date}&end_date={end_date}&type={typeParameter}&category={category}&page_number={page_number}&domain={domain}&apiKey=')+currentsApiKey
dataCurrentsSearch = requests.get(url).json()

# Save data search file locally
with open('dataFiles/dataCurrentsSearch.json', 'w') as outfile:
    json.dump(dataCurrentsSearch, outfile)

# Upload/Update Currents search data file on website server
commandToRun = 'scp dataFiles/dataCurrentsSearch.json stevenzv7@scanews.online:"~/scanews.online/dataFiles"'
while True:
	try:
		# Command will only run with correct locally stored private ssh keys
		os.system(commandToRun)
		break
	except:
		print("Could not connect to server, retrying in 5sec...")
		time.sleep(5)
		pass	

