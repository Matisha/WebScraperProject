################################
#  PYTHON WEB SCRAPER PROJECT  #
################################
# Authors:                     #
# - Arham Irshad               #
# - Kevin Nelson               #
# - Mathias Schoen             #
################################

#################################
#    JSON GENERATOR FUNCTION   #
# - - - - - - - - - - - - - - -#
#        COMMON FORMAT:        #
# "country" : {                #
#   "name" : "<name of country>"
#   "dailyDeathRaw"    : ""    #
#   "totDeathRateRaw"  : ""    #
#   "dailyDeathNorm"   : ""    #
#   "totDeathRateNorm" : ""    #
# }                            #
################################

###### Import Statements ######
from bs4 import BeautifulSoup
import requests
import re

##### Data Storage Class for space between JSON and Scraping ######
class StatsByCountry:
    def __init__(self, countryName, dailyDeaths, totalDeaths, dailyDeathsNorm, totalDeathsNorm):
            self.countryName = countryName
            self.dailyDeaths = dailyDeaths
            self.totalDeaths = totalDeaths
            self.dailyDeathsNorm = dailyDeathsNorm
            self.totalDeathsNorm = totalDeathsNorm

# Use main_table_countries_today, main_table_countries_yesterday, main_table_countries_yesterday2 for targetDay
def scrape_country(url, country, targetDay="main_table_countries_today") :
    # Request and soupify country
    htmlPage = requests.get(url).content
    soup = BeautifulSoup(htmlPage, 'html.parser')

    # Select the day...
    totalTable = soup.find('table', id=targetDay)
    #print(type(country))
    if type(country) == list:
        finalData = []
        for i in country:
            # Get the table row the country is in:
            countryRow = totalTable.find('a', text=i).parent.parent

            
            dailyDeathsElement     = countryRow.select_one(":nth-child(6)").text # Get the daily death rates (6th row)
            totalDeathsElement     = countryRow.select_one(":nth-child(5)").text # Get the total death rates (5th row)
            totalDeathsElementNORM = countryRow.select_one(":nth-child(12)").text

            # Check if they're blank
            # also remove commas

            # Deaily Deaths
            if (dailyDeathsElement == "") or (dailyDeathsElement == "N/A") or (dailyDeathsElement == None):
                dailyDeaths = 0
            else :
                dailyDeathsElement = re.sub(",", "", dailyDeathsElement)
                dailyDeaths = int(dailyDeathsElement)

            # Total Deaths
            if (totalDeathsElement == "") or (totalDeathsElement == "N/A") or (totalDeathsElement == None):
                totalDeaths = 0
            else :
                totalDeathsElement = re.sub(",", "", totalDeathsElement)
                totalDeaths = int(totalDeathsElement)


            # Normalized total deaths
            if (totalDeathsElementNORM == "") or (totalDeathsElementNORM == "N/A") or (totalDeathsElement == None):
                totalDeathsNorm = 0
            else :
                totalDeathsElementNORM = re.sub(",", "", totalDeathsElementNORM)
                totalDeathsNorm = int(totalDeathsElementNORM)

            # Normalized daily deaths (must be generated from given data)
            if totalDeaths == 0 or totalDeathsNorm == 0: # No divide by zero...
                dailyDeathsNorm = 0
            else:
                dailyDeathsNorm = dailyDeaths / (totalDeaths / totalDeathsNorm)
            finalData.append(StatsByCountry(i, dailyDeaths, totalDeaths, dailyDeathsNorm, totalDeathsNorm))

    else:
        # Get the table row the country is in:
        countryRow = totalTable.find('a', text=country).parent.parent

            
        dailyDeathsElement     = countryRow.select_one(":nth-child(6)").text # Get the daily death rates (6th row)
        totalDeathsElement     = countryRow.select_one(":nth-child(5)").text # Get the total death rates (5th row)
        totalDeathsElementNORM = countryRow.select_one(":nth-child(12)").text

        # Check if they're blank
        # also remove commas

        # Deaily Deaths
        if (dailyDeathsElement == "") or (dailyDeathsElement == "N/A") or (dailyDeathsElement == None):
            dailyDeaths = 0
        else :
            dailyDeathsElement = re.sub(",", "", dailyDeathsElement)
            dailyDeaths = int(dailyDeathsElement)

        # Total Deaths
        if (totalDeathsElement == "") or (totalDeathsElement == "N/A") or (totalDeathsElement == None):
            totalDeaths = 0
        else :
            totalDeathsElement = re.sub(",", "", totalDeathsElement)
            totalDeaths = int(totalDeathsElement)


        # Normalized total deaths
        if (totalDeathsElementNORM == "") or (totalDeathsElementNORM == "N/A") or (totalDeathsElement == None):
            totalDeathsNorm = 0
        else :
            totalDeathsElementNORM = re.sub(",", "", totalDeathsElementNORM)
            totalDeathsNorm = int(totalDeathsElementNORM)

        # Normalized daily deaths (must be generated from given data)
        if totalDeaths == 0 or totalDeathsNorm == 0: # No divide by zero...
            dailyDeathsNorm = 0
        else:
            dailyDeathsNorm = dailyDeaths / (totalDeaths / totalDeathsNorm)
        return StatsByCountry(country, dailyDeaths, totalDeaths, dailyDeathsNorm, totalDeathsNorm)
    return finalData


    # Gather all data
    # dataCollection = []
    # for link in soup.find_all('script'):
    #     if len(link.get_text()) > 20000:
    #         dataCollection.append(link.get_text())
    
    # # Separate out the data we need
    # totalDeathsData = []
    # dailyDeathsData = []
    # junkData = [] # Just in case...
    # for i in dataCollection:
    #     if "Total Deaths" in i:
    #         totalDeathsData.append(i)
    #     elif "graph-deaths-daily" in i:
    #         dailyDeathsData.append(i)
    #     else:
    #         junkData.append(i)

    # # Converts the data to a more usable format
    # totalDeathsData = totalDeathsData[0].split("\n")
    # dailyDeathsData = dailyDeathsData[0].split("\n")
    
    # datesForTotalDeaths = totalDeathsData[14].split(": ")[1].split("   }")[0].split('","')
    # totalDeathsData = totalDeathsData[38].split(",")

    # datesForDailyDeaths = dailyDeathsData[14].split(": ")[1].split("   }")[0].split('","')
    # dailyDeathsData = dailyDeathsData[59].split(",")

    # datesForDailyDeaths[-1] = datesForDailyDeaths[-1][0:12]
    # datesForDailyDeaths[0] = datesForDailyDeaths[0][2:-1] + "0"

    # totalDeathsData[0] = 0
    # dailyDeathsData[0] = 0

    # totalDeathsData.pop(-1)
    # totalDeathsData[-1] = re.sub(']        }]', '', totalDeathsData[-1])

    # dailyDeathsData.pop(-1)
    # dailyDeathsData[-1] = re.sub(']', '', dailyDeathsData[-1])
    
    # # Converts everything to numbers
    # for i in range(0, len(totalDeathsData)):
    #     if totalDeathsData[i] == "null":
    #         totalDeathsData[i] = 0
    #     else:
    #         totalDeathsData[i] = int(totalDeathsData[i])
    # for i in range(0, len(dailyDeathsData)):
    #     if dailyDeathsData[i] == "null":
    #         dailyDeathsData[i] = 0
    #     else:
    #         dailyDeathsData[i] = int(dailyDeathsData[i])

    #return StatsByCountry(country, [dailyDeathsData, datesForDailyDeaths], [totalDeathsData, datesForTotalDeaths])

    #### This will probably be useful for detecting availiable countries and looping through all... Later though. ####
    #print((dataCollection[3]))

def get_countries(url="https://www.worldometers.info/coronavirus/", targetDay="main_table_countries_today"):
    # Get soup
    htmlPage = requests.get(url).content
    soup = BeautifulSoup(htmlPage, 'html.parser')
    # Break it down to the country list
    results = soup.find('table', id=targetDay)
    table = results.find('tbody')
    HTMLedCountries = table.findAll('a')
    # Prep to extract country names
    countries = []
    counter = 1
    for link in HTMLedCountries:
        if counter % 2 == 1: # It was grabbing a number for each country, not sure which
            countries.append(link.get_text()) # Only gets country name
        counter += 1
        if counter >= 220: # Keeps from reaching dataless countries
            return countries

    #content = results.find_all('td')
    #print(content)
    #i = 1
    #for data in content:
    #    if i%10 == 1:
    #        print(data.text.strip())
    #        pass

# x = get_countries('https://www.worldometers.info/coronavirus/')
# x = scrape_country('https://www.worldometers.info/coronavirus/', 'USA')