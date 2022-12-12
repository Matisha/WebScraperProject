# Mathias Schoen
# Detailed bokeh viewer

### - - - Import Statements - - - ###
from bokeh.io import show                       # Used to display the actual graphs
from bokeh.models import CustomJS, DatePicker   # Import JS interface & date picker interface

from bokeh.embed import components              # Allows users to embed Bokeh figures into HTML

# - - - - - Date Widget & Event Handler - - - - - #
def change_date_handler(attr, old, new):
    newFileToOpen = "CovidData-" + str(new) + ".json"
    CustomJS("console.log('New File Name: ' + )")

date_picker = DatePicker(title='Select date: ', value="2022-12-10", min_date="2022-12-01")
date_picker.on_change("value", change_date_handler)



### - - - Return Statements - - - ###
# Returns objects to be copy and pasted into the webpage

script_dp, div_dp = components(date_picker)

print(script_dp)
print(div_dp)