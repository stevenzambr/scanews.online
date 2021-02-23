import requests
import json

# NYTIMES

# Read locally stored private NyTimes Api Key
with open('../apiKeys.json') as f:
  nyTimesApiKey = json.load(f)["NyTimes"]


# NyTimes API requests are capped at 4000 requests per day and 10 requests per minute
data = requests.get('https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+nyTimesApiKey).json()

# Save data in json file
with open('dataFiles/dataNyTimes.json', 'w') as outfile:
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