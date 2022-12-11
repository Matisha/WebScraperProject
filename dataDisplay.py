from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral3
from bs4 import BeautifulSoup
import requests
import json
import ScrapeWebsite as SW
from datetime import datetime, timedelta
import numpy as np

countryList = SW.get_countries() # ["Australia", "UK", "Switzerland", "S. Korea", "Czechia"]

############################  DAILY DEATH COUNTER #################################
with open('CovidData-12-09-2022.json') as json_file9:
    data9 = json.load(json_file9)
with open('CovidData-12-08-2022.json') as json_file8:
    data8 = json.load(json_file8)
with open('CovidData-12-07-2022.json') as json_file7:
    data7 = json.load(json_file7)

Days = ['12-09-2022','12-08-2022','12-07-2022']

y9= np.zeros(len(countryList))
y8= np.zeros(len(countryList))
y7= np.zeros(len(countryList))
for i in range(0,len(countryList)):
    
    #x[i] = data['countries'][i]["name"]
    y9[i] = data9['countries'][i]["dailyDeaths"]
    y8[i] = data8['countries'][i]["dailyDeaths"]
    y7[i] = data7['countries'][i]["dailyDeaths"]
    
    
    
x = [ (cl, Dates) for Dates in Days for cl in countryList ]
counts = sum(zip(y9, y8, y7), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))
palette = ["Red","#718dbf","#e84d60"]
p = figure(x_range=FactorRange(*x), height=250, title="Daily Death Counter",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",fill_color=factor_cmap('x', palette=Spectral3, factors=countryList))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1

# pGrid make it consistent with theme
p.xgrid.grid_line_color = None
p.text_color = "#ffffff"
p.background_fill_color = "#2d2d2d"

show(p)

"""
# create a new plot with a title and axis labels
p = p = figure(x_range=x, title="Deaths by Country",toolbar_location=None, tools="")
p.vbar(x=x, top=y, legend_label="Daily Deaths", width=0.5, bottom=0, color="red")

# add a line renderer with legend and line thickness to the plot
#p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
"""
