import requests
import json

# Zeit API (Images not available with API, usefull to do data analysis)

# Read locally stored private Zeit API Key
with open('../apiKeys.json') as f:
  zeitApiKey = json.load(f)["Zeit"]

# Parameters for Zeit API content
# q = # the main search query
# fields = # partially select output fields
# limit = # limit the amount of matches to return
# offset = # offset for the list of matches

url = 'http://api.zeit.de/content?q=texas&api_key='+zeitApiKey
dataZeit = requests.get(url).json()

# Save data Zeit file locally
with open('dataFiles/dataZeit.json', 'w') as outfile:
    json.dump(dataZeit, outfile)