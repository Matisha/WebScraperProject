# Kevin Nelson
# Display of some over time data

# Imports:
import json
from os import listdir
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.embed import components
import CountryDataParser as CDP 

import pandas as pd

# Reading JSON data and storing by country for easy plotting
directoryList = listdir()
jsonList = []
for i in directoryList:
	if ".json" in i:
		splitNames = i.split('-')
		if splitNames[1] == '2022': # Only grab JSONs from after the restructure
			jsonList.append(splitNames)

dataByCountry = dict([]) # A dictionary of countries with a list of lists containing dates and that day's data
for idx, i in enumerate(jsonList):
	date = i[1] + "-" + i[2] + "-" + i[3].split('.')[0]
	daysData = CDP.getAndParseData(date)
	if idx == 0:
		for jdx, j in enumerate(daysData.getCL()):
			dataByCountry[j] = [[date, CDP.parsedCountryInfo(j, daysData.dd[jdx], daysData.td[jdx], daysData.ddn[jdx], daysData.tdn[jdx])]]
			
	else:
		for jdx, j in enumerate(daysData.getCL()):
			dataByCountry[j].append([date, CDP.parsedCountryInfo(j, daysData.dd[jdx], daysData.td[jdx], daysData.ddn[jdx], daysData.tdn[jdx])])
	

# Creating Plot
TOOLS = "pan,box_zoom,reset"
plot = figure(height=250, x_axis_label="Date (Dec 2022 day)", y_axis_label="Daily Deaths Normalized", tools=TOOLS)
plot.title.text = "Select a country to disble on graph"


for idx, key in enumerate(dataByCountry):
	if idx >= 6: # We have a lot of countries, this would get unusable quick...
		break
	times = []
	dailyDeathsNorm = []
	for i in dataByCountry[key]:
		times.append(int(i[0].split('-')[2]))
		dailyDeathsNorm.append(i[1].getDDN())
	plot.line(times, dailyDeathsNorm, legend_label=key, line_width=2, color=Spectral6[idx])

plot.legend.location = "top_left"
plot.legend.click_policy="hide"

script_plot, div_plot = components(plot)

with open('data/generatedScript2.txt', 'w') as file:
    file.write(script_plot)
    file.write('\n')
    file.write('\n')
    file.write('\n')
    file.write(div_plot)
