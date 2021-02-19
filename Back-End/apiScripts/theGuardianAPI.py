import requests
import json

# THE GUARDIAN  (Images not available with free API)

# Read locally stored private The Guardian Api Key
with open('../apiKeys.json') as f:
  theGuardianApiKey = json.load(f)["TheGuardian"]

# The Guardian Open Platform allows for up to 12 calls per second and up to 5,000 calls per day
query = "https://content.guardianapis.com/search?section=world&format=json&order-by=newest&api-key="+ theGuardianApiKey
data = requests.get(query).json()
with open('dataFiles/dataTheGuardian.json', 'w') as outfile:
    json.dump(data, outfile)

theGuardianTitle = data["response"]["results"][0]["webTitle"]
theGuardianLink = data["response"]["results"][0]["webUrl"]
print("The Guardian Title: "+theGuardianTitle)
print("The Guardian Article Link: " +theGuardianLink)