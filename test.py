import CountryDataParser as cdp  
import json
from os.path import exists 
Days = '2022-12-10'
fileToGet = "CovidData-" + str(Days) + ".json"
if ( exists(fileToGet)) : print(0)

