from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh import transform
from bokeh import palettes
from bs4 import BeautifulSoup
import requests
import json
import ScrapeWebsite as SW
from datetime import date, timedelta
import numpy as np
import CountryDataParser as cdp   
from bokeh.embed import components
from bokeh.transform import dodge
############################  DAILY DEATH COUNTER #################################
day = str(date.today().day)
year = str(date.today().year)
month = str(date.today().month)

#Get data for past three days
date = ['','','']
Days = ['','','']
dailyDeathsList = [[],[],[]]
res = [[],[],[]]
for i in range(0,3):
    
    date[i] = str(int(day)-i) 
    if len(date[i]) == 1:
        date[i] = '0'+date[i]       
    countryInfoDemo = cdp.getAndParseData(year + '-' + month +'-'+ date[i]) # Get raw parsed data
    countryList = countryInfoDemo.getCL()               # Get list of countries
    dailyDeathsList[i] = countryInfoDemo.getDD()           # Get list of daily deaths
    Days[i] = year + '-' + month +'-'+ date[i]
    # initialize N
    N = 5
    
    # Indices of N largest elements in list
    # using sorted() + lambda + list slicing

    res[i] = sorted(range(len(dailyDeathsList[i])), key = lambda sub: dailyDeathsList[i][sub])[-N:]
countryList1 = ['']*5
d1 = ['']*5
d2 = ['']*5
d3 = ['']*5
for val in range(0,len(res[0])):
    countryList1[val] = countryList[res[0][val]]
    d1[val]=dailyDeathsList[0][res[0][val]]
    d2[val]=dailyDeathsList[1][res[1][val]]
    d3[val]=dailyDeathsList[2][res[2][val]]

counts = sum(zip(d1+d2+d3), ()) # like an hstack

x = [ (cl, Dates) for cl in countryList1 for Dates in Days  ]



source = ColumnDataSource(data=dict(x=x, counts=counts))
palette = ["Red","#718dbf","#e84d60"]
p = figure(x_range=FactorRange(*x), height=250, 
           title="Trend over past three days of current five highest Death Rate Countries",
           toolbar_location="right", tools="save")


# defining the Y-Axis Label
p.yaxis.axis_label = "Death Rate/Day"

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",fill_color= transform.factor_cmap('x', palette=["#c9d9d3","#718dbf","#e84d60"], factors= Days, start=1, end=2))

p.vbar(x=dodge('Death Rate', -0.25, range=p.x_range), top=Days[0], width=0.2, source=source,
       color="#c9d9d3", legend_label=str(Days[0]))

p.vbar(x=dodge('Death Rate',  0.0,  range=p.x_range), top=Days[1], width=0.2, source=source,
       color="#718dbf", legend_label=str(Days[1]))

p.vbar(x=dodge('Death Rate',  0.25, range=p.x_range), top=Days[2], width=0.2, source=source,
       color="#e84d60", legend_label=str(Days[2]))


p.xgrid.grid_line_color = None
p.legend.location = "top_left"



p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1


show(p)

# Get the script and div components to be inserted into HTML page
script_p, div_p = components(p)

# Write out these components to a generated file
with open('data/generatedScript3.txt', 'w') as file:
    file.write(script_p)
    file.write('\n')
    file.write('\n')
    file.write('\n')
    file.write(div_p)
    
"""
# pGrid make it consistent with theme
p.xgrid.grid_line_color = None
p.text_color = "#ffffff"
p.background_fill_color = "#2d2d2d"




# create a new plot with a title and axis labels
p = p = figure(x_range=x, title="Deaths by Country",toolbar_location=None, tools="")
p.vbar(x=x, top=y, legend_label="Daily Deaths", width=0.5, bottom=0, color="red")

# add a line renderer with legend and line thickness to the plot
#p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
"""
