import requests
import json

# NYTIMES

# Read locally stored private NyTimes Api Key
file = open("nyTimesApiKey.txt")
nyTimesApiKey = file.read()
file.close()

# NyTimes API requests are capped 4000 requests per day and 10 requests per minute
data = requests.get('https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+nyTimesApiKey).json()

# Save data in json file
with open('dataNyTimes.json', 'w') as outfile:
    json.dump(data, outfile)

# Read data and set variables for NyTimes
topStory = data["results"][0]
nyTimesTitle = topStory["title"]
nyTimesLink = topStory["url"]
nyTimesImage = topStory["multimedia"][0]["url"]
nyTimesImageLink = nyTimesImage
print("NyTimes Title: " + nyTimesTitle)
print("NyTimes Article Link: " + nyTimesLink)
print("NyTimes Image: " + nyTimesImage)


# THE GUARDIAN  (Images not available with free API)

# Read locally stored private The Guardian Api Key
file = open("theGuardianApiKey.txt")
theGuardianApiKey = file.read()
file.close()

# The Guardian Open Platform allows for up to 12 calls per second and up to 5,000 calls per day
query = "https://content.guardianapis.com/search?section=world&format=json&order-by=newest&api-key="+ theGuardianApiKey
data = requests.get(query).json()
with open('dataTheGuardian.json', 'w') as outfile:
    json.dump(data, outfile)

theGuardianTitle = data["response"]["results"][0]["webTitle"]
theGuardianLink = data["response"]["results"][0]["webUrl"]
print("The Guardian Title: "+theGuardianTitle)
print("The Guardian Article Link: " +theGuardianLink)


# Currents API 

# Read locally stored private Currents API Key
file = open("currentsApiKey.txt")
currentsApiKey = file.read()
file.close()

# Configurable parameter for currents latest news API
supportedLanguages = {"Arabic":"ar","Chinese":"zh","Dutch":"nl","English":"en","Finnish":"fi","French":"fr","German":"de","Hindi":"hi","Italian":"it","Japanese":"ja","Korean":"ko","Malay":"msa","Portuguese":"pt","Russian":"ru","Spanish":"es","Vietnamise":"vi"}
language = supportedLanguages["English"]

# Currents API has 600 requests available per day (1 request every 2:24 minutes)
url = ('https://api.currentsapi.services/v1/latest-news?language='+language+'&apiKey='+currentsApiKey)
dataLatestNews = requests.get(url).json()


with open('dataCurrentsLatestNews.json', 'w') as outfile:
    json.dump(dataLatestNews, outfile)

# Configurable parameters for currents search API
supportedLanguages = {"Arabic":"ar","Chinese":"zh","Dutch":"nl","English":"en","Finnish":"fi","French":"fr","German":"de","Hindi":"hi","Italian":"it","Japanese":"ja","Korean":"ko","Malay":"msa","Portuguese":"pt","Russian":"ru","Spanish":"es","Vietnamise":"vi"}

language = supportedLanguages["English"]
# start_date = 
# end_date = 
# typeParameter =
# country = 
# category = 
# page_number =
# domain =

# Currents API has 600 requests available per day (1 request every 2:24 minutes)
url = ('https://api.currentsapi.services/v1/search?language='+language+'&start_date'+'&apiKey='+currentsApiKey)
dataLatestNews = requests.get(url).json()


with open('dataCurrentsLatestNews.json', 'w') as outfile:
    json.dump(dataLatestNews, outfile)


