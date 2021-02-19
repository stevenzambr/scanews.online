import requests
import json

# # NYTIMES

# # Read locally stored private NyTimes Api Key
# file = open("nyTimesApiKey.txt")
# nyTimesApiKey = file.read()
# file.close()

# # NyTimes API requests are capped 4000 requests per day and 10 requests per minute
# data = requests.get('https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+nyTimesApiKey).json()

# # Save data in json file
# with open('dataNyTimes.json', 'w') as outfile:
#     json.dump(data, outfile)

# # Read data and set variables for NyTimes
# topStory = data["results"][0]
# nyTimesTitle = topStory["title"]
# nyTimesLink = topStory["url"]
# nyTimesImage = topStory["multimedia"][0]["url"]
# nyTimesImageLink = nyTimesImage
# print("NyTimes Title: " + nyTimesTitle)
# print("NyTimes Article Link: " + nyTimesLink)
# print("NyTimes Image: " + nyTimesImage)


# # THE GUARDIAN  (Images not available with free API)

# # Read locally stored private The Guardian Api Key
# file = open("theGuardianApiKey.txt")
# theGuardianApiKey = file.read()
# file.close()

# # The Guardian Open Platform allows for up to 12 calls per second and up to 5,000 calls per day
# query = "https://content.guardianapis.com/search?section=world&format=json&order-by=newest&api-key="+ theGuardianApiKey
# data = requests.get(query).json()
# with open('dataTheGuardian.json', 'w') as outfile:
#     json.dump(data, outfile)

# theGuardianTitle = data["response"]["results"][0]["webTitle"]
# theGuardianLink = data["response"]["results"][0]["webUrl"]
# print("The Guardian Title: "+theGuardianTitle)
# print("The Guardian Article Link: " +theGuardianLink)


# Currents API 

# Read locally stored private Currents API Key
file = open("currentsApiKey.txt")
currentsApiKey = file.read()
file.close()

# Currents API supported languages, countries and categories
supportedLanguages = {"Arabic":"ar","Chinese":"zh","Dutch":"nl","English":"en","Finnish":"fi","French":"fr","German":"de","Hindi":"hi","Italian":"it","Japanese":"ja","Korean":"ko","Malay":"msa","Portuguese":"pt","Russian":"ru","Spanish":"es","Vietnamise":"vi"}
supportedCountries = {"United State":"US","Taiwan":"TW","German":"DE","United Kingdom":"GB","China":"CN","India":"IN","Spain":"ES","Italy":"IT","Poland":"PL","Australia":"AU","Malaysia":"MY","Singapore":"SG","Canada":"CA","South Korea":"KR","Denmark":"DK","France":"FR","Belgium":"BE","Japan":"JP","Austria":"AT","Portugal":"PT","Philippines":"PH","Hong Kong":"HK","Argentina":"AR","Venezuela":"VE","Brazil":"BR","Finland":"FI","Indonedia":"ID","Vietnam":"VN","Mexico":"MX","Greece":"GR","Netherlands":"NL","Norway":"NO","New Zealand":"NZ","Russia":"RU","Saudi-Arabia":"SA","Switzerland":"CH","Thailand":"TH","United Arab Emirates":"AE","Ireland":"IE","Iran":"IR","Iraq":"IQ","Romania":"RO","Afghanistan":"AF","Zimbabwe":"ZW","Myanmar":"MM","Sweden":"SE","Peru":"PE","Panama":"PA","Egypt":"EG","Turkey":"TR","Israel":"IL","Czech Republic":"CZ","Bangladesh":"BD","Nigeria":"NG","Kenya":"KE","Chile":"CL","Uruguay":"UY","Ecuador":"EC","Serbia":"RS","Hungary":"HU","Slovenia":"SI","Gahana":"GH","Bolivia":"BO","Pakistan":"PK","Colombia":"CO","North Korea":"NK","Paraguay":"PY","Palestine":"PS","Estonia":"EE","Lebanon":"LB","Qatar":"QA","Kuwait":"KW","Cambodia":"KH","Nepal":"NP","Luxembourg":"LU","Bosnia":"BA","Europe":"EU","Asia":"ASIA","International":"INT"}
supportedCategories = ["regional","technology","lifestyle","business","general","programming","science","entertainment","world","sports","finance","academia","politics","health","opinion","food","game","fashion","academic","crap","travel","culture","economy","environment","art","music","notsure","CS","education","redundant","television","commodity","movie","entrepreneur","review","auto","energy","celebrity","medical","gadgets","design","EE","security","mobile","estate","funny"]

# # Currents Latest News API

# # Configurable parameter for currents latest news API
# language = supportedLanguages["English"]

# # Currents API has 600 requests available per day (1 request every 2:24 minutes)
# url = (f'https://api.currentsapi.services/v1/latest-news?language={language}&apiKey='+currentsApiKey)
# dataLatestNews = requests.get(url).json()


# with open('dataCurrentsLatestNews.json', 'w') as outfile:
#     json.dump(dataLatestNews, outfile)

# TODO: More testing of the Currents Search API 

# Currents Search API

# Configurable parameters for currents search API
language = supportedLanguages["English"]
start_date = "2021-02-18" # +'&start_date='+start_date
end_date = "2021-02-19" # +'&end_date='+end_date
# typeParameter =
country = supportedCountries["International"] # +'&country='+country
category = "world" # +'&category='+category
# page_number =
domain = "cnbc.com,nytimes.com"
# domain_not =

# Currents API has 600 requests available per day (1 request every 2:24 minutes)
url = (f'https://api.currentsapi.services/v1/search?language={language}&domain={domain}&apiKey='+currentsApiKey)
dataSearch = requests.get(url).json()

# Save data search file locally
with open('dataSearch.json', 'w') as outfile:
    json.dump(dataSearch, outfile)


