import requests
import json

# Read locally stored private NyTimes Api Key
file = open("nyTimesApiKey.txt")
nyTimesApiKey = file.read()
file.close()

# # Uncomment to use Archive Api to download and save data
# # Set year and month
# year = '2020'
# month = '11'

# # Get all NyTimes articles for the specified month
# data = requests.get("https://api.nytimes.com/svc/archive/v1/"+year+"/"+month+".json?api-key="+nyTimesApiKey).json()

# # Save data in json file (saved locally to avoid multiple requests for same archived data)
# with open('nyTimesData_'+year+'_'+month+'.json', 'w') as outfile:
#     json.dump(data, outfile)


# Read stored data
with open('nyTimesData_2021_1.json') as f:
  data_2021_1 = json.load(f)

# TODO: Data Analysis of NyTimes articles
print(data_2021_1["response"]["docs"][0]["headline"]["main"])