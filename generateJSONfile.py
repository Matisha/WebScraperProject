#################################
#  PYTHON WEB SCRAPER PROJECT   #
#################################
# Authors:                      #
# - Arham Irshad                #
# - Kevin Nelson                #
# - Mathias Schoen              #
#################################

# Imports
from bs4 import BeautifulSoup
import requests
import json
import ScrapeWebsite as SW
from datetime import datetime, timedelta

###################################################################################
######### DATE TO PULL ############################################################
# Here, you can select what day you'd like to pull data from, incase you'd like to
# peak into the past!
# TODAY            -->  main_table_countries_today
# YESTERDAY        -->  main_table_countries_yesterday
# BEFORE YESTERDAY -->  main_table_countries_yesterday2
chooseDay = "main_table_countries_today"
###################################################################################
######### COUNTRY LIST ############################################################
## Please add any desired countries to scrape to this list. Capitalization matters!
countryList = SW.get_countries(targetDay=chooseDay) # ["Australia", "UK", "Switzerland", "S. Korea", "Czechia"]
###################################################################################

# URL Used for scraping
demoURL = "https://www.worldometers.info/coronavirus/"

# Use main_table_countries_today, main_table_countries_yesterday, main_table_countries_yesterday2 for targetDay
def generateJSONfile (url=demoURL, targetDay=chooseDay,countryList=countryList):

    # Initialize master dictionary that will eventually be converted to JSON file
    masterDict = {}

    ####################################################################
    # Loop thru every county in the list and scrape for statistics using scrape_country function:
    rawData = SW.scrape_country(url, countryList, targetDay)
    for country in rawData:
        subDict = {"dailyDeaths" : country.dailyDeaths, "totalDeaths" : country.totalDeaths, "dailyDeathsNorm" : country.dailyDeathsNorm, "totalDeathsNorm" : country.totalDeathsNorm}
        masterDict[str(country.countryName)] = subDict
    
    #############################################################
    # Generate filename with date:
    tday = datetime.now()   # Get today's date
    # Account for if the user is peaking into the past
    if (targetDay == "main_table_countries_yesterday")  : day = tday - timedelta(days=1)
    elif (targetDay == "main_table_countries_yesterday2") : day = tday - timedelta(days=2)
    else : day = tday
    
    # Format date and convert to filename string
    date = datetime.strftime(day, "%Y-%m-%d")
    fileName = "CovidData-" + date + ".json"

    #############################################################
    # Finally, dump dictionary into JSON file:
    json_object = json.dumps(masterDict, indent = 4)
    with open(fileName, "w") as outfile :
        outfile.write(json_object)

#generateJSONfile()

for i in ["main_table_countries_today", "main_table_countries_yesterday","main_table_countries_yesterday2"]:
    generateJSONfile(targetDay=i)