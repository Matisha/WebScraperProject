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

def scrape_country(url, country) :
    # Request and soupify country
    url1 = url + 'country/' + country + '/' #  Worldometer Coronavirus Tracker
    htmlPage = requests.get(url1).content
    soup = BeautifulSoup(htmlPage, 'html.parser')

    # Gather all data
    dataCollection = []
    for link in soup.find_all('script'):
        if len(link.get_text()) > 20000:
            dataCollection.append(link.get_text())
    
    # Separate out the data we need
    totalDeathsData = []
    dailyDeathsData = []
    junkData = [] # Just in case...
    for i in dataCollection:
        if "Total Deaths" in i:
            totalDeathsData.append(i)
        elif "graph-deaths-daily" in i:
            dailyDeathsData.append(i)
        else:
            junkData.append(i)

    # Converts the data to a more usable format
    totalDeathsData = totalDeathsData[0].split("\n")
    dailyDeathsData = dailyDeathsData[0].split("\n")
    
    datesForTotalDeaths = totalDeathsData[14].split(": ")[1].split("   }")[0].split('","')
    totalDeathsData = totalDeathsData[38].split(",")

    datesForDailyDeaths = dailyDeathsData[14].split(": ")[1].split("   }")[0].split('","')
    dailyDeathsData = dailyDeathsData[59].split(",")

    datesForDailyDeaths[-1] = datesForDailyDeaths[-1][0:12]
    datesForDailyDeaths[0] = datesForDailyDeaths[0][2:-1] + "0"

    totalDeathsData[0] = 0
    dailyDeathsData[0] = 0

    totalDeathsData.pop(-1)
    totalDeathsData[-1] = re.sub(']        }]', '', totalDeathsData[-1])

    dailyDeathsData.pop(-1)
    dailyDeathsData[-1] = re.sub(']', '', dailyDeathsData[-1])
    
    # Converts everything to numbers
    for i in range(0, len(totalDeathsData)):
        if totalDeathsData[i] == "null":
            totalDeathsData[i] = 0
        else:
            totalDeathsData[i] = int(totalDeathsData[i])
    for i in range(0, len(dailyDeathsData)):
        if dailyDeathsData[i] == "null":
            dailyDeathsData[i] = 0
        else:
            dailyDeathsData[i] = int(dailyDeathsData[i])

    return StatsByCountry(country, [dailyDeathsData, datesForDailyDeaths], [totalDeathsData, datesForTotalDeaths])
    
    #### This will probably be useful for detecting availiable countries and looping through all... Later though. ####
    #print((dataCollection[3]))
    #results = soup.find(id='main_table_countries_today')
    #print(results)
    #content = results.find_all('td')
    #print(content)
    #i = 1
    #for data in content:
    #    if i%10 == 1:
    #        #print(data.text.strip())
    #        pass

x = scrape_country('https://www.worldometers.info/coronavirus/', 'us')
#print(x.dailyDeathsByYear)
