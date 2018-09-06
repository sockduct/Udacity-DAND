# [DAND](https://www.udacity.com/course/data-analyst-nanodegree--nd002) Project 7 - Wrangle and Analyze Data

## Project Purpose and Notes
Using Python and its libraries for data wrangling.  This will consist of gathering data from a variety of sources and in a variety of formats, assessing its quality and tidiness, and then cleaning it.  Document wrangling efforts in a Jupyter Notebook provided by Udacity, plus showcase them through analyses and visualizations using Python (and its libraries) and/or SQL. Use a tweet archive provided to and curated by Udacity from WeRateDogs (@dog_rates).

This project was created and tested on Windows 10 64bit using Python 3.6.5 32 bit with the following libraries:

**Package** | **Version**
----------|----------
fractions | (3.6.5 stdlib)
io | (3.6.5 stdlib)
json | (3.6.5 stdlib)
jupyter | 1.0.0
jupyter-client | 5.2.3
jupyter-console | 5.2.0
jupyter-core | 4.4.0
(Jupyter) notebook | 5.6.0
jupyterlab | 0.34.4
jupyterlab-launcher | 0.13.1
matplotlib | 2.2.3
numpy | 1.15.1
os | (3.6.5 stdlib)
pandas | 0.23.4
pycountry | 18.5.26
re | (3.6.5 stdlib)
requests | 2.19.1
sys | (3.6.5 stdlib)
tweepy | (Must get latest version from GitHub, v3.6.0 from PyPI not new enough!)

## Installation and Requirements
* Install [Python 3.6](https://www.python.org/downloads/)
    * Note: Python v3.6 or later recommended
* Install jupyter, matplotlib, numpy, pandas, requests, seaborn, and tweepy via pip, conda, or your preferred Python package manager
* Clone [this repo](https://github.com/sockduct/Udacity-DAND)
* Optionally open the notebook in Jupyter (either with the notebook or lab subcommand)

## Project Requirements
* Wrangle the dataset to create an interesting and trustworthy analyses and visualizations
  * Use the wrangle_act.ipynb Jupyter Notebook template
  * Must address all key points below
* Starting from the initial dataset, for good results the following will be necessary:
  * additional gathering (see data sources below)
  * assessing
    * Visually
    * Programmatically
    * Quality Issues - document and fix at least 8
    * Tidiness Issues - document and fix at least 2
  * cleaning
* Store, analyze, and visualize the wrangled data
  * Store the clean dataframe as twitter_archive_master.csv
    * Can also use a SQLite database
  * At least 3 insights and 1 visualization must be produced
* Reporting on
  1. data wrangling efforts
    1) Create a 300-600 word written report named wrangle_report.pdf or wrangle_report.html which briefly describes wrangling efforts
    2) Framed as internal document
  2. data analyses and visualizations
    1) Create a 250-word minimum written report named act_report.pdf or act_report.html which communicates the insights and displays the visualization(s) produced from the wrangled data
    2) Framed as external document, e.g., as a blog post or magazine article
    3) Can create these from separate Jupyter Notebook using Markdown functionality or using a word processor/desktop publisher

## Resource Attribution
* The following resources were used in coming up with the solution for this project:
    * StackOverflow
    * Extensive use of pandas, Twitter API and tweepy docs
    * Use of matplotlib and requests docs
    * Some use of Python for Data Analysis, 2e

## Project Solution Documents
* [get_tweets](get_tweets.py) - Python module for retrieving Tweets
* [Project 7 - Jupyter Notebook](wrangle_act.ipynb) - Jupyter Notebook for Project
* [README (What you're reading!)](README.md)
* [secrets](secrets.exmpl) - Secrets initialization file, rename extension to .cfg and populate with your Twitter API secrets
* [store_ex](store_ex.py) - Quick run through of Python stdlib persistant storage options
* [tweepy_ex](tweepy_ex.py) - Some examples of using the tweepy library
* [twitter-archive-enhanced.csv](twitter-archive-enhanced.csv) - Original dataset of Tweets in CSV format
* [twitter-archive-enhanced.xlsx](twitter-archive-enhanced.xlsx) - Excel Spreadsheet with original dataset of tweets (tab1), the image prediction info (tab2), and Twitter API/tweepy model info (tab3)

## License
[MIT License](LICENSE)

