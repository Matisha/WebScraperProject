# WebScraperProject
ME EN 6250 - **Programming of Engineers** - Web Scraping Project

## Introduction
Welcome to our Covid Dashboard project! Here in the main branch, you'll find working milestones for our project (currently web scraping and JSON generation). The master branch is for development and updates that the team works on, so if you'd like to use the JSON generator, please use the 'main' branch version.

## Instructions
To use the JSON generator, first download the 'main' branch as a .zip file to a computer with python installed. To adjust settings for the JSON generator, please open up the 'generateJSONfile.py' file. Near the top of the document, you'll find two settings you can change. The first is a list of countries to be scraped, where a user can add any country they would like to include in the JSON file. There is no limit to how many countries you can scrape, but country names can sometimes be very specific. The second option is a string which can be changed to view today's, yesterday's, or the day before yesterday's covid statistics.

To generate the JSON file, simply run the python program after adjusting you settings, and a file named 'CovidData-X-X-X' will be generated where the Xs represent the day the data was taken from.

## Project Description / Explanation
For our data scraping, we have broken it up into two main functions: generateJSONfile and scrape_country. scrape_country takes a url and scrapes that website to find a given country. It is currently optimized to run for worldometers. It grabs either today’s main data table, yesterday’s, or the table from two days ago. It then extracts the data for a target country. It pulls from that our target data points—daily death rate, cumulative deaths as of the target day, and cumulative deaths normalized by population and converts them from string to integer. We back out the population normalization factor from the cumulative death values, and apply it to the daily death rate to get the normalized daily death rate. This is all then added to a temporary storage class and returned for use by generateJSONfile. generateJSONfile writes the data into a master dictionary of “countries” and a list. That list contains a series of dictionaries which each contain a country and the associated data. This master dictionary is written to a JSON file labeled according to the day it was created.
