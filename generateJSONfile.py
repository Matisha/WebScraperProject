#################################
#  PYTHON WEB SCRAPER PROJECT   #
#################################
# Authors:                      #
# - Arham Irshad                #
# - Kevin Nelson                #
# - Mathias Schoen              #
#################################

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

# Imports
from bs4 import BeautifulSoup
import requests
import json
import DemoCountryGetter as dcg
from datetime import datetime

# Add any counties you want to this list!!
countryList = ["Australia", "UK", "Switzerland", "S. Korea", "Czechia"]
demoURL = "https://www.worldometers.info/coronavirus/"

def generateJSONfile (url) :

    masterDict = {"countries" : []}
    for country in countryList :    # Run through every country in the list
        
        # Get the country data using external function, then format data into a dictionary
        # CURRENT DICTIONARY IS TEMPORARY, SHOULD MIRROR COMMON FORMAT ABOVE, NOT CURRENT FORMAT BELOW (CURERNT FORMAT JUST FOR TESTING)
        rawData = dcg.scrape_country(demoURL, country)
        dictToAdd = {"name" : str(country), "dailyDeaths" : rawData.dailyDeaths, "totalDeaths" : rawData.totalDeaths, "dailyDeathsNorm" : rawData.dailyDeathsNorm, "totalDeathsNorm" : rawData.totalDeathsNorm}
        masterDict["countries"].append(dictToAdd)
    
    # Generate filename:
    date = datetime.now().strftime("%m-%d-%Y")
    fileName = "CovidData-" + date + ".json"

    # Finally, dump objects into JSON file:
    json_object = json.dumps(masterDict, indent = 4)
    with open(fileName, "w") as outfile :
        outfile.write(json_object)

generateJSONfile(demoURL)