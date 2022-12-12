# WebScraperProject
ME EN 6250 - **Programming of Engineers** - Web Scraping Project

## Introduction
Welcome to our Covid Dashboard project! Here in the main branch, you'll find working milestones for our project (currently web scraping and JSON generation). The master branch is for development and updates that the team works on, so if you'd like to use the JSON generator, please use the 'main' branch version.

## Instructions
To use our dashboard, first download the 'main' branch as a .zip file to a computer with python installed. To update the data, please run the included 'generateJSONfile.py' file in order to refresh the statistics. To view these statistics, please open the HTML file in the repository. This will open your default browser to our webpage where data can be viewed and interacted with. 

## Project Description / Explanation
For our data scraping, we have broken it up into two main functions: generateJSONfile and scrape_country. scrape_country takes a url and scrapes that website to find a given country. It is currently optimized to run for worldometers. It grabs either today’s main data table, yesterday’s, or the table from two days ago. It then extracts the data for a target country. It pulls from that our target data points—daily death rate, cumulative deaths, and cumulative deaths normalized by population and parese them into usable integers. We back out the population normalization factor from the cumulative death values, and apply it to the daily death rate to get the normalized daily death rate. The country's data is compiled into a storage class and returned to be used by generateJSONfile. generateJSONfile writes the data into a master list of countries which contains a series of dictionaries which each contain a country and the associated data. Finally, this master dictionary is written to a JSON file labeled according to the day it was created.

For our data display, we have decided to work with an HTML document as our primary display method, generating code to be added to the HTML file for display. This allows us to customize the website and create an intuitive user interface. The downside of this method is that **Python Callback functions are disabled for local machines**, meaning the webpage cannot interact with data directly. If this page were on a server and NOT a local machine, however, python callbacks would be enabled - allowing direct refreshing of the data from the webpage's UI. For now, manual regeneration of the JSON file(s) is required - being handled by the generateJSONfile script included in the repository.
