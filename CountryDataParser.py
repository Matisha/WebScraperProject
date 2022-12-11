# Mathias Schoen
# Parser

### - - - Import Statements - - - #
import json
from os.path import exists

### - - - Data Struct Class - - - #
# Contains all data parsed from
# countries formatted into synced
# and ordered lists
### - - - - - - - - - - - - - - - #
class parsedCountryInfo:
    def __init__(self, cl, dd, td, ddn, tdn):
        self.cl = cl
        self.dd = dd
        self.td = td
        self.ddn = ddn
        self.tdn = tdn

    def getCL (self):
        return self.cl

    def getDD (self):
        return self.dd

    def getTD (self):
        return self.td

    def getDDN (self):
        return self.ddn
    
    def getTDN (self):
        return self.tdn

### - - - Data Importing & Parsing - - -  ###
# Given a select date, data is gathered, 
# sorted, and parsed, and returned in the 
# above parsedCountryInfo class
### - - - - - - - - - - - - - - - - - - - ###
def getAndParseData (dateToParse):

    # Find what file to open
    fileToGet = "CovidData-" + str(dateToParse) + ".json"
    # Make sure file exists, exit if not
    if (not exists(fileToGet)) : return None
    
    # Open JSON file and parse info
    with open(fileToGet) as file:
        rawData = json.load(file)

    ##### Begin data parsing: ######
    countryList = list(rawData.keys())      # Get list of all countries
    dailyDeathsList = []                    # Blank List of Daily Deaths
    totalDeathsList = []                    # Blank List of Total Deaths
    dailyDeathsNormList = []                # Blank List of Normalized Daily Deaths
    totalDeathsNormList = []                # Blank List of Normalized Total Deaths
    for country in rawData:                 #  | Begin itterating through each country to
        statsList = rawData[country]        #  | append stats for each country
        dailyDeathsList.append(statsList['dailyDeaths'])
        totalDeathsList.append(statsList['totalDeaths'])
        dailyDeathsNormList.append(statsList['dailyDeathsNorm'])
        totalDeathsNormList.append(statsList['totalDeathsNorm'])


    ##### Compiling & returning data ######
    parsedInfo = parsedCountryInfo(countryList, dailyDeathsList, totalDeathsList, dailyDeathsNormList, totalDeathsNormList)
    return parsedInfo