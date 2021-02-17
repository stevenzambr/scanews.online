import time
import requests
import csv
import os
import paramiko
import sys
from bs4 import BeautifulSoup as bs
from keybert import KeyBERT
from datetime import datetime
from PIL import Image
from io import BytesIO

# Array of the supported news sites
newsSites = ['nyTimes','yahoo','nbc','cbs','fox','cnbc']; 

# Function that takes a string and removes , " ; ' and :
def removeSpecialChars(title : str):
	return title.strip().replace(',','').replace('"','').replace(';','').replace("'",'').replace(':','').replace('.','')

# Function that returns the current date and time as a string
def getCurrentDateAndTime():
	t = datetime.now()
	return t.strftime("%d %b %Y at %H:%M:%S")

# Function that return current date and time as a string for footer
def getCurrentDateAndTimeFooter():
	t = datetime.now()
	return "Updated: " + t.strftime("%d %b %Y at %H:%M:%S")

# Function to search images based on keywords
def keyword_images():
	for data in updatedTitles:
		searchurl = SEARCH_ENGINE + data
		response = requests.get(searchurl)
		soup = bs(response.text,'html.parser')
		resultsTable = soup.find(id='results_table')
		resultsFirst = resultsTable.findAll('a',href=True)
		if len(resultsFirst) != 0:
			imagelinksSourceGlobal.append(resultsFirst[0]['href'])
			innerResponse = requests.get(resultsFirst[0]['href'])
			innerSoup = bs(innerResponse.text,'html.parser')
			innerResultsFirst = innerSoup.findAll('a',href=True)	
			imagelinksGlobal.append(innerResultsFirst[1]['href'])
		else :
			imagelinksSourceGlobal.append('https://placeholder.com/')
			imagelinksGlobal.append('https://via.placeholder.com/450x300')
	print('Done getting new keyword based images')

while True:
	try:
		# Webscraping various news page headlines using BeautifulSoup
		print('Getting titles...')

		originalImages = []

		# NYTIMES FRONT PAGE HEADLINE
		url = requests.get("https://www.nytimes.com")
		nyTimesTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		# Ranked from most to least prominent nyTimes css classes 
		nyTimesClasses = ["css-bmo67g e1lsht870","e-big-banner-headline e-smaller e-rule e-hasDek","css-cok7h5 e1sjycav0","css-m2iw8b e1sjycav0","css-1lb1c0f e1sjycav0","css-1bxzzgs e1sjycav0","css-xxaj7r e1sjycav0","css-xxaj7r e1lsht870","css-1bxzzgs e1lsht870","css-1ayculb e1voiwgp0"]
		# Goes through the css classes and uses the most prominent
		for className in nyTimesClasses:
			nyTimesTitle = soup.find(class_=className)
			if nyTimesTitle != None: # and nyTimesTitle.parent != None and nyTimesTitle.parent.find('a',href=True) != None:
				if nyTimesTitle.text != '':
					parentOfNyTimesTitle = nyTimesTitle.parent
					while(parentOfNyTimesTitle.get('href') == None):
						parentOfNyTimesTitle = parentOfNyTimesTitle.parent
					nyTimesTitleLink = parentOfNyTimesTitle.get('href')
					if(nyTimesTitleLink[0]!= 'h'):
						nyTimesTitleLink = 'https://www.nytimes.com' + nyTimesTitleLink
					break
		print("NYTimes : " + nyTimesTitle.text.strip().replace(',',''))
		if len(soup.findAll('img')) < 4:
			originalImages.append("https://via.placeholder.com/450x300")
		else :
			originalImages.append(soup.findAll('img')[3].get('src'))

		# YAHOO FRONT PAGE HEADLINE
		url = requests.get("https://www.yahoo.com/")
		yahooTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		yahooTitle = soup.find(id="ntk-title")
		parentOfYahooTitle = yahooTitle.parent
		while(parentOfYahooTitle.get('href') == None):
			parentOfYahooTitle = parentOfYahooTitle.parent
		yahooTitleLink = parentOfYahooTitle.get('href')
		if(yahooTitleLink[0]!= 'h'):
			yahooTitleLink = 'https://www.yahoo.com' + yahooTitleLink
		print("Yahoo : " + yahooTitle.text.strip().replace(',',''))
		originalImages.append(soup.findAll('img')[2].get('src'))


		# NBC FRONT PAGE HEADLINE
		url = requests.get("https://www.nbcnews.com/")
		nbcTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		soup2 = bs(url.text, 'html.parser')
		# Ranked from most to least prominent nbc css classes 
		nbcClasses = ["cover-spread__headline","tease-card__headline"]
		nbcTitle = ""
		# Goes through the css classes and uses the most prominent
		for className in nbcClasses:
			nbcTitle = soup.find(class_=className)
			if nbcTitle != None:
				if nbcTitle.text != '':
					nbcTitleLink = nbcTitle.find_all('a',href=True)[0]['href']
					break
		print("NBC : " + nbcTitle.text.strip().replace(',',''))
		originalImages.append("https://via.placeholder.com/450x300")

		# CBS FRONT PAGE HEADLINE
		url = requests.get("https://www.cbsnews.com/")
		cbsTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		cbsTitle = soup.find_all(class_="item__hed")
		cbsTitleLink = cbsTitle[1].parent.parent.get('href')
		print("CBS : " + cbsTitle[1].text.strip().replace(',',''))
		imgSearch = str(soup.find_all(class_="img")[0])
		start = imgSearch.find('src="https')
		end = imgSearch.find('"',start + 8)
		originalImages.append(imgSearch[start+5:end])

		# FOX FRONT PAGE HEADLINE
		url = requests.get("https://www.foxnews.com/")
		foxTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		foxTitle = soup.find_all(class_="title title-color-default")
		foxTitleLink = foxTitle[10].find_all('a',href=True)[0]['href']
		print("Fox : " + foxTitle[10].text.strip().replace(',',''))
		tempImageLink = str(soup.find_all('img')[11].get('src'))
		# Check if link starts with h, needed for gif images in frontpage of fox
		if(tempImageLink[0] != 'h'):
			originalImages.append('https://www.foxnews.com' + tempImageLink)
		else:
			originalImages.append(tempImageLink)

		# CNBC FRONT PAGE HEADLINE
		url = requests.get("https://www.cnbc.com/")
		cnbcTime = getCurrentDateAndTime()
		soup = bs(url.content,features="lxml")
		# Ranked from most to least prominent nbc css classes 
		cnbcClasses = ["FeaturedCard-packagedCardTitle","FeaturedCard-title"]
		cnbcTitle = ""
		# Goes through the css classes and uses the most prominent
		for className in cnbcClasses:
			cnbcTitle = soup.find(class_=className)
			if cnbcTitle != None:
				if cnbcTitle.text != '':
					# Title link for FeaturedCard-title
					cnbcTitleLink = cnbcTitle.find_all('a',href=True)[0]['href']
					break				
		if(cnbcTitle == None):
			cnbcTitle = foxTitle
			cnbcTitle.text = "Scanews was not able to scan this headline"
		print("CNBC : " + cnbcTitle.text.strip().replace(',',''))
		originalImages.append("https://via.placeholder.com/450x300")
		print('Done Getting Titles')

		# List of headlines with special characters removed
		titles = [removeSpecialChars(nyTimesTitle.text),removeSpecialChars(yahooTitle.text),removeSpecialChars(nbcTitle.text),removeSpecialChars(cbsTitle[1].text),removeSpecialChars(foxTitle[10].text),removeSpecialChars(cnbcTitle.text)]
		print('Processing keywords for titles...')
		# List to store the updated titles
		updatedTitles = []
		# Natural language processing using KeyBERT to extract the top 3 keywords of the headlines, this is done to improve image searching results
		for t in titles:
			model = KeyBERT('distilbert-base-nli-mean-tokens')
			keywords = model.extract_keywords(t,keyphrase_ngram_range=(1, 3),stop_words='english')
			updatedTitles.append(keywords[0])
		print('Done processing keywords:')
		print(updatedTitles)

		# Picsearch link used to scrape images
		SEARCH_ENGINE = 'https://www.picsearch.com/index.cgi?q='

		# Save folder name for images
		SAVE_FOLDER = 'images'

		# Array containing the nlp images
		imagelinksGlobal = []

		# Array containing the nlp images source
		imagelinksSourceGlobal = []

		# Creates images folder if it does not exist yet and calls download_images function
		if not os.path.exists(SAVE_FOLDER):
			os.mkdir(SAVE_FOLDER)
		print('Using keywords to find fitting images...')
		keyword_images()

		# Commands to update csv file on website server through ssh
		sedNyTimesTitle = " sed -i " + "'/^NYTimes,/s/[^,]*/" + nyTimesTitle.text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedNyTimesTime = " sed -i " + "'/^NYTimes,/s/[^,]*/" + nyTimesTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedNyTimesTitleLink = " sed -i " + "'/^NYTimes,/s/[^,]*/" + nyTimesTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedNyTimesOgImage = " sed -i " + "'/^NYTimes,/s/[^,]*/" + originalImages[0].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedNyTimesNlpImage = " sed -i " + "'/^NYTimes,/s/[^,]*/" + imagelinksGlobal[0].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedNyTimesOgImageSource = " sed -i " + "'/^NYTimes,/s/[^,]*/" + "https://www.nytimes.com".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedNyTimesNlpImageSource = " sed -i " + "'/^NYTimes,/s/[^,]*/" + imagelinksSourceGlobal[0].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateNyTimesRow = sedNyTimesTitle + sedNyTimesTime + sedNyTimesTitleLink + sedNyTimesOgImage + sedNyTimesNlpImage + sedNyTimesOgImageSource + sedNyTimesNlpImageSource

		sedYahooTitle = " sed -i " + "'/^Yahoo,/s/[^,]*/" + yahooTitle.text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedYahooTime = " sed -i " + "'/^Yahoo,/s/[^,]*/" + yahooTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedYahooTitleLink = " sed -i " + "'/^Yahoo,/s/[^,]*/" + yahooTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedYahooOgImage = " sed -i " + "'/^Yahoo,/s/[^,]*/" + originalImages[1].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedYahooNlpImage = " sed -i " + "'/^Yahoo,/s/[^,]*/" + imagelinksGlobal[1].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedYahooOgImageSource = " sed -i " + "'/^Yahoo,/s/[^,]*/" + "https://www.yahoo.com/".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedYahooNlpImageSource = " sed -i " + "'/^Yahoo,/s/[^,]*/" + imagelinksSourceGlobal[1].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateYahooRow = sedYahooTitle + sedYahooTime + sedYahooTitleLink + sedYahooOgImage + sedYahooNlpImage + sedYahooOgImageSource + sedYahooNlpImageSource

		sedNbcTitle = " sed -i " + "'/^NBC,/s/[^,]*/" + nbcTitle.text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedNbcTime = " sed -i " + "'/^NBC,/s/[^,]*/" + nbcTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedNbcTitleLink = " sed -i " + "'/^NBC,/s/[^,]*/" + nbcTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedNbcOgImage = " sed -i " + "'/^NBC,/s/[^,]*/" + originalImages[2].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedNbcNlpImage = " sed -i " + "'/^NBC,/s/[^,]*/" + imagelinksGlobal[2].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedNbcOgImageSource = " sed -i " + "'/^NBC,/s/[^,]*/" + "https://www.nbcnews.com/".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedNbcNlpImageSource = " sed -i " + "'/^NBC,/s/[^,]*/" + imagelinksSourceGlobal[2].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateNbcRow = sedNbcTitle + sedNbcTime + sedNbcTitleLink + sedNbcOgImage + sedNbcNlpImage + sedNbcOgImageSource + sedNbcNlpImageSource

		sedCbsTitle = " sed -i " + "'/^CBS,/s/[^,]*/" + cbsTitle[1].text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedCbsTime = " sed -i " + "'/^CBS,/s/[^,]*/" + cbsTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedCbsTitleLink = " sed -i " + "'/^CBS,/s/[^,]*/" + cbsTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedCbsOgImage = " sed -i " + "'/^CBS,/s/[^,]*/" + originalImages[3].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedCbsNlpImage = " sed -i " + "'/^CBS,/s/[^,]*/" + imagelinksGlobal[3].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedCbsOgImageSource = " sed -i " + "'/^CBS,/s/[^,]*/" + "https://www.cbsnews.com/".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedCbsNlpImageSource = " sed -i " + "'/^CBS,/s/[^,]*/" + imagelinksSourceGlobal[3].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateCbsRow = sedCbsTitle + sedCbsTime + sedCbsTitleLink + sedCbsOgImage + sedCbsNlpImage + sedCbsOgImageSource + sedCbsNlpImageSource

		sedFoxTitle = " sed -i " + "'/^Fox,/s/[^,]*/" + foxTitle[10].text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedFoxTime = " sed -i " + "'/^Fox,/s/[^,]*/" + foxTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedFoxTitleLink = " sed -i " + "'/^Fox,/s/[^,]*/" + foxTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedFoxOgImage = " sed -i " + "'/^Fox,/s/[^,]*/" + originalImages[4].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedFoxNlpImage = " sed -i " + "'/^Fox,/s/[^,]*/" + imagelinksGlobal[4].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedFoxOgImageSource = " sed -i " + "'/^Fox,/s/[^,]*/" + "https://www.foxnews.com/".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedFoxNlpImageSource = " sed -i " + "'/^Fox,/s/[^,]*/" + imagelinksSourceGlobal[4].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateFoxRow = sedFoxTitle + sedFoxTime + sedFoxTitleLink + sedFoxOgImage + sedFoxNlpImage + sedFoxOgImageSource + sedFoxNlpImageSource

		sedCnbcTitle = " sed -i " + "'/^CNBC,/s/[^,]*/" + cnbcTitle.text.strip().replace(',','').replace('/','\/').replace('&','\&').replace("'","") + "/2'" + " newsData.csv \n"
		sedCnbcTime = " sed -i " + "'/^CNBC,/s/[^,]*/" + cnbcTime.replace('/','\/') + "/3'" + " newsData.csv \n"
		sedCnbcTitleLink = " sed -i " + "'/^CNBC,/s/[^,]*/" + cnbcTitleLink.replace('/','\/').replace('&','\&') + "/4'" + " newsData.csv \n"
		sedCnbcOgImage = " sed -i " + "'/^CNBC,/s/[^,]*/" + originalImages[5].replace('/','\/').replace('&','\&') + "/5'" + " newsData.csv \n"
		sedCnbcNlpImage = " sed -i " + "'/^CNBC,/s/[^,]*/" + imagelinksGlobal[5].replace('/','\/').replace('&','\&') + "/6'" + " newsData.csv \n"
		sedCnbcOgImageSource = " sed -i " + "'/^CNBC,/s/[^,]*/" + "https://www.cnbc.com/".replace('/','\/') + "/7'" + " newsData.csv \n"
		sedCnbcNlpImageSource = " sed -i " + "'/^CNBC,/s/[^,]*/" + imagelinksSourceGlobal[5].replace('/','\/').replace('&','\&') + "/8'" + " newsData.csv \n"
		updateCnbcRow = sedCnbcTitle + sedCnbcTime + sedCnbcTitleLink + sedCnbcOgImage + sedCnbcNlpImage + sedCnbcOgImageSource + sedCnbcNlpImageSource

		footerDateAndTime = getCurrentDateAndTimeFooter()
		updateFooter = " sed -i " + "'/^Footer,/s/[^,]*/" + footerDateAndTime + "/2'" + " newsData.csv"

		# Connects to website server through shh using paramiko ssh client and executes the previously created commands on the server (only works with locally stored private shh keys)
		def ssh_conn():
		    client = paramiko.SSHClient()
		    client.load_system_host_keys()
		    print("Connecting to server through ssh...")
		    client.connect('scanews.online',username= 'stevenzv7')
		    print("Connection established")
		    print("Updating newsData.csv...")    
		    client.exec_command("cd scanews.online \n" + updateNyTimesRow + updateYahooRow + updateNbcRow + updateCbsRow + updateFoxRow + updateCnbcRow + updateFooter)
		    print("Website updated") 

		# Downloads, resizes, and uploads images to the website server using the webscraped image links
		def downloadAndUploadImages():
			print("Downloadind and uploading images...")
			# Width used to resize images
			basewidth = 600
			#i = 0
			# Array used to save the paths of the saved images
			imagesArray = []
			# Original images 
			for i , originalImageLink in enumerate(originalImages):
				try:
					response = requests.get(originalImageLink)
					# Resize image to get smaller file size
					img = Image.open(BytesIO(response.content)).convert('RGB')
					wpercent = (basewidth/float(img.size[0]))
					hsize = int((float(img.size[1])*float(wpercent)))
					img = img.resize((basewidth,hsize), Image.ANTIALIAS)
					# Save image locally
					img.save('images/' + newsSites[i] +'Original.jpg','JPEG',optimize=True,quality=90)
					# Add path of saved image to images array
					imagesArray.append('images/' + newsSites[i] +'Original.jpg')
					#i = i + 1
				except Exception as e:
					print('Exception: ')
					print(e)
					img = Image.open('images/notAvailable.jpg').convert('RGB')
					img.save('images/' + newsSites[i] +'Original.jpg','JPEG')
					imagesArray.append('images/' + newsSites[i] +'Original.jpg')
					#i = i + 1
			# Build scp command to upload images to server from the saved images paths
			commandToRun = 'scp ' + imagesArray[0] + ' ' + imagesArray[1] + ' ' + imagesArray[2] + ' ' + imagesArray[3] + ' ' + imagesArray[4] + ' ' + imagesArray[5] + ' ' + 'stevenzv7@scanews.online:"~/scanews.online/images"'
			while True:
				try:
					# Command will only run with correct locally stored private ssh keys
					os.system(commandToRun)
					break
				except:
					print("Could not connect to server, retrying in 5sec...")
					time.sleep(5)
					pass		
			#i = 0
			# Image array is emptied to now download and upload keyword images
			imagesArray = []
			# Keyword images (See Original images above for documentation)
			for i,keywordImageLink in enumerate(imagelinksGlobal):
				try:
					response = requests.get(keywordImageLink)
					img = Image.open(BytesIO(response.content)).convert('RGB')
					wpercent = (basewidth/float(img.size[0]))
					hsize = int((float(img.size[1])*float(wpercent)))
					img = img.resize((basewidth,hsize), Image.ANTIALIAS)
					img.save('images/' + newsSites[i] +'Keyword.jpg','JPEG',optimize=True,quality=90)
					imagesArray.append('images/' + newsSites[i] +'Keyword.jpg')	
					#i = i + 1				
				except Exception as e:
					print('Exception: ')
					print(e)
					img = Image.open('images/notAvailable.jpg').convert('RGB')
					img.save('images/' + newsSites[i] +'Keyword.jpg','JPEG')
					imagesArray.append('images/' + newsSites[i] +'Keyword.jpg')
					#i = i + 1
			commandToRun = 'scp ' + imagesArray[0] + ' ' + imagesArray[1] + ' ' + imagesArray[2] + ' ' + imagesArray[3] + ' ' + imagesArray[4] + ' ' + imagesArray[5] + ' ' + 'stevenzv7@scanews.online:"~/scanews.online/images"'
			while True:
				try:
					os.system(commandToRun)
					break
				except:
					print("Could not connect to server, retrying in 5sec...")
					time.sleep(5)
					pass
			print("Uploaded images") 		

		downloadAndUploadImages()
		ssh_conn()	

		# # Uncomment to update the local newsData.csv file
		# print('Updating csv...')
		# # Creates a csv file with first column name of the website and second column the front page headline
		# with open('newsData.csv','w') as f:
		# 	thewriter = csv.writer(f)
		# 	thewriter.writerow(['Website Name', 'Headline', 'Date and time of scan', 'Link to headline article','Link to original headline image','Link to nlp searched image','Original image source','Nlp searched image source'])
		# 	thewriter.writerow(['NYTimes', nyTimesTitle.text.strip().replace(',',''), nyTimesTime, nyTimesTitleLink,originalImages[0],imagelinksGlobal[0],'https://www.nytimes.com',imagelinksSourceGlobal[0]])
		# 	thewriter.writerow(['Yahoo', yahooTitle.text.strip().replace(',',''), yahooTime,yahooTitleLink,originalImages[1],imagelinksGlobal[1],"https://www.yahoo.com/",imagelinksSourceGlobal[1]])
		# 	thewriter.writerow(['NBC', nbcTitle.text.strip().replace(',',''),nbcTime,nbcTitleLink,originalImages[2],imagelinksGlobal[2],"https://www.nbcnews.com/",imagelinksSourceGlobal[2]])
		# 	thewriter.writerow(['CBS', cbsTitle[1].text.strip().replace(',',''),cbsTime,cbsTitleLink,originalImages[3],imagelinksGlobal[3],"https://www.cbsnews.com/",imagelinksSourceGlobal[3]])
		# 	thewriter.writerow(['Fox', foxTitle[10].text.strip().replace(',',''),foxTime,foxTitleLink,originalImages[4],imagelinksGlobal[4],"https://www.foxnews.com/",imagelinksSourceGlobal[4]])
		# 	thewriter.writerow(['CNBC', cnbcTitle.text.strip().replace(',',''),cnbcTime,cnbcTitleLink,originalImages[5],imagelinksGlobal[5],"https://www.cnbc.com/",imagelinksSourceGlobal[5]])
		# 	thewriter.writerow(['Footer', footerDateAndTime,footerDateAndTime,footerDateAndTime,footerDateAndTime,footerDateAndTime,footerDateAndTime,footerDateAndTime])

		# print('Done Updating csv')

		print("Waiting 1 minute to update page again")
		time.sleep(60)
		print("Running script again")
	except:
		print("Unexpected error: ", sys.exc_info()[0])
		print("Waiting 30 seconds to update page again")
		time.sleep(30)
		print("Running script again")
		continue