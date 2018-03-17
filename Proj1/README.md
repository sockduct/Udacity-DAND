# DAND Project 1 - Explore Weather Trends

## Project Purpose and Notes
In this project, you will analyze local and global temperature data and compare the temperature trends where you live to overall global temperature trends.

## Installation and Requirements
* [PDF Viewer](https://get.adobe.com/reader/)
* Spreadsheet Program (Optional) to view underlying data
    * [Microsoft Excel](https://products.office.com/en-us/excel)
    * [Microsoft Excel Viewer via OneDrive](https://support.office.com/en-us/article/work-with-worksheet-data-in-onedrive-c051a205-1c06-4feb-94d8-793b0126b53a)
    * [Google Sheets](https://www.google.com/sheets/about/)

## Project Requirements
* Create a visualization and prepare a write up describing the similarities and differences between global temperature trends and temperature trends in the closest big city to where you live (Detroit, Michigan, USA).
* Steps:
    * Extract the data from the database. Using the Udacity [project workspace]() that is connected to a database, export the temperature data for the world as well as for the closest big city to where you live. The list of cities and countries is in the city_list table on this page. Use SQL to interact with the database.
    * Write a SQL query to extract the city level data. Export to CSV.
    * Write a SQL query to extract the global data. Export to CSV.
    * Open up the CSV in whatever tool you feel most comfortable using. We suggest using Excel or Google sheets, but you are welcome to use another tool, such as Python or R.
    * Create a line chart that compares your city’s temperatures with the global temperatures. Make sure to plot the moving average rather than the yearly averages in order to smooth out the lines, making trends more observable.
    * Make observations about the similarities and differences between the world averages and your city’s averages, as well as overall trends.
    * For example:
        * Is your city hotter or cooler on average compared to the global average?
        * Has the difference been consistent over time?
        * How do the changes in your city’s temperatures over time compare to the changes in the global average?
        * What does the overall trend look like?
        * Is the world getting hotter or cooler?
        * Has the trend been consistent over the last few hundred years?
* Submission - a PDF which includes:
    * An outline of steps taken to prepare the data to be visualized in the chart, such as:
        * What tools did you use for each step? (Python, SQL, Excel, etc)
        * How did you calculate the moving average?
        * What were your key considerations when deciding how to visualize the trends?
        * Line chart with local and global temperature trends
        * At least four observations about the similarities and/or differences in the trends
* README (this file)

## Project Solution Layout
* Avg Temps.xlsx - Average temperature data for Detroit and Globally including charts and comparisons (created with Microsoft Excel 2013)
* City List.csv|xlsx - List of available cities
* Detroit Avg Temps.csv - Average temperatures extracted from database for Detroit
* Exploring Weather Trends - P1.docx - Report/Project Submission (created with Microsoft Word 2013)
* [Exploring Weather Trends - P1.pdf](https://github.com/sockduct/Udacity-DAND/blob/master/Proj1/Exploring%20Weather%20Trends%20-%20P1.pdf) - Report/Project Submission in PDF format
* Global Avg Temps.csv - Average temperatures extracted from database for the World
* Moving Average Example.xlsx - Example of calculating moving averages

## License
[MIT License](license.txt)

