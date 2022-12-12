################################
#  PYTHON WEB SCRAPER PROJECT  #
################################
# Authors:                     #
# - Arham Irshad               #
# - Kevin Nelson               #
# - Mathias Schoen             #
################################

##### TO DO LIST: ######
# - This is only a demo, these need to be broken up into function(s) that return proper data
# - Nothing handles errors yet, this needs to be implemented
# - This file should be able to be imported into the main file. Right now it just does the bare minimum

###### Import Statements ######
from bs4 import BeautifulSoup
import requests

#####   Input Variables    ######
country = str(input("Enter a country to view: ")).lower()

##### URLS for statistic servers ######
url1 = "https://www.worldometers.info/coronavirus/country/" + country #  Worldometer Coronavirus Tracker

# HTML Parser:
# TDOD --> Error handler if the url is invalid / requests can't find the specified country
htmlPage = requests.get(url1).content
parsedHTML = BeautifulSoup(htmlPage, 'html.parser')

# Get stack of content in specific page and break it down into parent section
tag_mainContent  = parsedHTML.find('div', attrs={'class' : 'content-inner'})
data_Cases_P     = tag_mainContent.findChild('h1', text='Coronavirus Cases:').parent

# Extract data from child elements:
data_Cases     = data_Cases_P.findChild('div', attrs={'class' : 'maincounter-number'}).findChild('span')

print("Cases:     " + data_Cases.text + "\n")

def getCountryStats (url, country) :
    url1 = "url" + country #  Worldometer Coronavirus Tracker