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

countryList = ["canada", "mexico", "switzerland", "germany", "austria", "france", "spain", "italy"]
demoURL = "https://www.worldometers.info/coronavirus/country/"

def generateJSONfile (url) :

    masterDict = {"countries" : []}
    for country in countryList :    # Run through every country in the list
        
        # Get the country data using external function, then format data into a dictionary
        # CURRENT DICTIONARY IS TEMPORARY, SHOULD MIRROR COMMON FORMAT ABOVE, NOT CURRENT FORMAT BELOW (CURERNT FORMAT JUST FOR TESTING)
        rawDataArray = dcg.getCountryStats(url, country)
        dictToAdd = {"name" : str(country), "cases" : rawDataArray[0], "deaths" : rawDataArray[1]}
        masterDict["countries"].append(dictToAdd)
    
    # Finally, dump objects into JSON file:
    json_object = json.dumps(masterDict, indent = 4)
    with open("Data.json", "w") as outfile :
        outfile.write(json_object)

generateJSONfile(demoURL)