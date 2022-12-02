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
import re

##### Data Storage Class for space between JSON and Scraping ######

class StatsByCountry:
    def __init__(self, countryName, dailyDeathsByYear, dailyCumulativeDeaths):
        self.countryName = countryName
        self.dailyDeathsByYear = dailyDeathsByYear
        self.dailyCumulativeDeaths = dailyCumulativeDeaths
        
##### URLS for statistic servers ######

def getCountryStats (url, country) :
    url1 = url + country #  Worldometer Coronavirus Tracker

    # HTML Parser:
    htmlPage = requests.get(url1).content
    parsedHTML = BeautifulSoup(htmlPage, 'html.parser')

    # Get stack of content in specific page and break it down into parent section
    tag_mainContent  = parsedHTML.find('div', attrs={'class' : 'content-inner'})
    data_Cases_P      = tag_mainContent.findChild('h1', text='Coronavirus Cases:').parent
    data_Deaths_P     = tag_mainContent.findChild('h1', text='Deaths:').parent

    # Extract data from child elements:
    data_Cases     = data_Cases_P.findChild('div', attrs={'class' : 'maincounter-number'}).findChild('span').text
    data_Deaths    = data_Cases_P.findChild('div', attrs={'class' : 'maincounter-number'}).findChild('span').text

    data_Cases  = re.sub(",", "", data_Cases)
    data_Cases  = re.sub(" ", "", data_Cases)
    data_Deaths = re.sub(",", "", data_Deaths)
    data_Deaths = re.sub(" ", "", data_Deaths)

    return [int(data_Cases), int(data_Deaths)]
