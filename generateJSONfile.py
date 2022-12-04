#################################
#  PYTHON WEB SCRAPER PROJECT   #
#################################
# Authors:                      #
# - Arham Irshad                #
# - Kevin Nelson                #
# - Mathias Schoen              #
#################################

###################################################################################
######### COUNTRY LIST ############################################################
## Please add any desired countries to scrape to this list. Capitalization matters!
countryList = ["Australia", "UK", "Switzerland", "S. Korea", "Czechia"]
###################################################################################
######### DATE TO PULL ############################################################
# Here, you can select what day you'd like to pull data from, incase you'd like to
# peak into the past!
# TODAY            -->  main_table_countries_today
# YESTERDAY        -->  main_table_countries_yesterday
# BEFORE YESTERDAY -->  main_table_countries_yesterday2
chooseDay = "main_table_countries_today"
###################################################################################
###################################################################################

# Imports
from bs4 import BeautifulSoup
import requests
import json
import ScrapeWebsite as SW
from datetime import datetime, timedelta

# URL Used for scraping
demoURL = "https://www.worldometers.info/coronavirus/"

# Use main_table_countries_today, main_table_countries_yesterday, main_table_countries_yesterday2 for targetDay
def generateJSONfile (url, targetDay=chooseDay) :

    # Initialize master dictionary that will eventually be converted to JSON file
    masterDict = {"countries" : []}

    ####################################################################
    # Loop thru every county in the list and scrape for statistics using scrape_country function:
    for country in countryList :
        # Get the country data using external function, then format data into a dictionary
        rawData = SW.scrape_country(url, country, targetDay)
        # Add to dictionary
        dictToAdd = {"name" : str(country), "dailyDeaths" : rawData.dailyDeaths, "totalDeaths" : rawData.totalDeaths, "dailyDeathsNorm" : rawData.dailyDeathsNorm, "totalDeathsNorm" : rawData.totalDeathsNorm}
        masterDict["countries"].append(dictToAdd)
    
    #############################################################
    # Generate filename with date:
    tday = datetime.now()   # Get today's date
    # Account for if the user is peaking into the past
    if (targetDay == "main_table_countries_yesterday")  : day = tday - timedelta(days=1)
    if (targetDay == "main_table_countries_yesterday2") : day = tday - timedelta(days=2)
    else : day = tday
    # Format date and convert to filename string
    date = datetime.strftime(day, "%m-%d-%Y")
    fileName = "CovidData-" + date + ".json"

    #############################################################
    # Finally, dump dictionary into JSON file:
    json_object = json.dumps(masterDict, indent = 4)
    with open(fileName, "w") as outfile :
        outfile.write(json_object)

generateJSONfile(demoURL)