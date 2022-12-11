# Mathias Schoen
# Detailed bokeh viewer

### - - - Import Statements - - - ###
import numpy as np                              # Numpy, becuase math
import json                                     # JSON, to read the data
from os.path import exists                      # To check if a file exists

from bokeh.io import show, curdoc, output_notebook # Used to display the actual graphs
from bokeh.plotting import figure               # Import figure, and models:
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, DatePicker
from bokeh.palettes import brewer               # Color palettle for bars
from bokeh.embed import components, json_item   # Allows users to embed Bokeh figures into HTML
from bokeh.layouts import row, column

import pandas as pd                             # Base pandas insall
import geopandas as gpd                         # Pandas geodata module

import ScrapeWebsite as sw                      # Our own scrape website code
import CountryDataParser as cdp                 # Our own JSON parser

### - - - Map Image Generator: - - - #
# This is the big one: generating a map
# based on data from JSON file
### - - - - - - - - - - - - - - - - - - - - -#



def generate_json_data(selectedDate):

    # Generate GeoDataFrame object:
    gdf = gpd.read_file('data/mapping/ne_110m_admin_0_countries.shp')[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf.head()

    # Drop antarctica because tutorial says it's huge and takes up a lot of map space
    gdf = gdf.drop(gdf.index[159])  # 159 is the code for antarctica, get that dude outta here

    # Now we import our main data. For this example we'll be using daily deaths on 2022-12-10
    countryInfoDemo = cdp.getAndParseData(selectedDate) # Get raw parsed data
    countryList = countryInfoDemo.getCL()               # Get list of countries
    dailyDeathsList = countryInfoDemo.getDD()           # Get list of daily deaths
    minDD = min(dailyDeathsList)                        # Find MIN daily deaths
    maxDD = max(dailyDeathsList)                        # Find MAX daily deaths
    dataFrameTemplate = []                              # Create template for pandas data frame
    for idx, country in enumerate(countryList):
        dataFrameTemplate.append([country, dailyDeathsList[idx]])

    # Construct pandas dataframe to merge with geodata datafarme to pass to Bokeh
    df = pd.DataFrame(dataFrameTemplate, columns=['country', 'dailydeaths'])
    df.head()

    # Merge pandas dataframe and geodata frame based on COUNTRY SYNCHRONIZATION:
    merged_df = gdf.merge(df, left_on='country', right_on= 'country', how='left')
    merged_df_json = json.loads(merged_df.to_json())    # Format dataframes to JSON
    json_geodata = json.dumps(merged_df_json)           # Dump JSON

    return [json_geodata, maxDD]

### - - - Bokeh Map Generator: - - - #
# This is the big one: generating a map
# based on data
### - - - - - - - - - - - - - - - - - - - - -#
generatedGeoData = generate_json_data('2022-12-08')
geosource = GeoJSONDataSource(geojson=generatedGeoData[0]) # Initialize frame
maxDD = generatedGeoData[1] # Get maximum daily deaths

# Create palette for geoframe to use & Convert palette to a linear color mapper
palette = brewer['YlGnBu'][8]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette=palette, low=0, high=maxDD)

# Generate labels for the horizontal data bar
tick_spacers = np.linspace(0, maxDD, 9)
tick_labels = {}
for idx, i in enumerate(tick_spacers):
    tick_labels[str(i)] = str(round(i))

# Add function for hovering over countries:
hover = HoverTool(tooltips = [ ('Country/region','@country'), ('Daily Death Rates', '@dailydeaths')])

# Generate colorbar for country map
color_bar = ColorBar(color_mapper=color_mapper,
label_standoff=8, width=500, height=20, border_line_color=None, location = (0,0),
orientation='horizontal')

# Now we finally start creating the figure objects:
figureTitle = 'Daily Death Rates'
p = figure(title=figureTitle, height=400, width=600, toolbar_location=None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Add patch renderer to figure:
p.patches('xs', 'ys', source=geosource, fill_color = {'field' : 'dailydeaths', 'transform' : color_mapper},
line_color='black', line_width=0.25, fill_alpha = 1)

p.add_layout(color_bar, 'below')

# Updater Function for Map:
def update_plot(attr, old, new):
    date = datePicker.value
    new_data = generate_json_data(date)
    geosource.geojson = new_data

datePicker = DatePicker(title='Select date to View: ', value="2022-12-08", min_date="2022-12-08", max_date="2022-12-11")
datePicker.on_change("value", update_plot)

layout = column(p, datePicker)

# Get the script and div components to be inserted into HTML page
script_p, div_p = components(layout)

# Write out these components to a generated file
with open('data/generatedScript.txt', 'w') as file:
    file.write(script_p)
    file.write('\n')
    file.write('\n')
    file.write('\n')
    file.write(div_p)