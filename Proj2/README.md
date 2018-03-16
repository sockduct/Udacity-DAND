# DAND Project 2 - Explore US Bikeshare Data

## Project Purpose and Notes
This project uses Python to explore data related to bike share systems for three major cities in the United States--**Chicago**, **New York City**, and **Washington**. The program reads in the specified CSV data file and answers interesting questions about it by computing descriptive statistics. This program also supports user interaction by taking in input to allow the user to choose the city file and optionally specify a time period filter.

## Installation and Requirements
* Install [Python](https://www.python.org/downloads/)
    * Note 1: Due to the features used, Python v3.6 or later is required
    * Note 2: Due to the size of the data files, 64bit Python is required
* Download [the data files](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/March/5aa88600_bikeshare/bikeshare.zip)
* Clone [this repo](https://github.com/sockduct/Udacity-DAND)
* From the repo's Proj2 directory, run:  `bikeshare.py`

## Project Requirements
* For each csv file answer the following questions:
    * What is the most popular month for start time?
    * What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    * What is the most popular hour of day for start time?
    * What is the total trip duration and average trip duration?
    * What is the most popular start station and most popular end station?
    * What is the most popular trip?
    * What are the counts of each user type?
    * What are the counts of gender?
    * What are the earliest (i.e. oldest person), most recent (i.e. youngest person), and most popular birth years?
* Program (bikeshare.py) must support user selectable time period filters including month, weekday, and hour.
* Program must allow user to choose from one of the three data files.
* Program must allow user the option to re-start.
* README (this file) and well commented code

## Project Solution Layout
* bikeshare.py - main program, read in user specified data file, allow specification of time period filter, tabulate statistics and show results
* rndcsvsmpl.py - used to create random sample of 10,000 entries for each of the data files; allows for rapid testing as loading the actual data files can take minutes
* timeperiod.py - holds classes for time period filter (all possible ways user can filter data) and time period results (all possible months, weeks, weekdays, and hours to allow for occurrence counting)
* util.py - generic utility functions

## Example Project Output
```
C:\GHRepos\Udacity-DAND\Proj2> bikeshare.py

Hello! Let's explore some US bikeshare data!
Would you like to see data for Chicago, New York, or Washington?
chi
Loading chicago.csv... - Processed in 15.00 seconds.
Converting to native types... - Processed in 48.99 seconds.

The city data ranges from January 1, 2017 to June 30, 2017.

Would you like to filter the city data analysis by 1) Month(s), 2) Day(s) of
a month, 3) Week(s), 4) Weekday(s), 5) Hours, or 6) no filter (none)?
1

January, February, March, April, May, June, or a range (February - April)?
feb-apr

Time Period Filter:
        months:  February - April               days of month:  All
        weeks:  All             weekdays:  All          hours:  All

OK? (Yes or No):  n

The city data ranges from January 1, 2017 to June 30, 2017.

Would you like to filter the city data analysis by 1) Month(s), 2) Day(s) of
a month, 3) Week(s), 4) Weekday(s), 5) Hours, or 6) no filter (none)?
5

Please enter a hour or a range from 0 - 23 (0 = midnight, 13 = 1 pm):
0-12

Time Period Filter:
        months:  February - April               days of month:  All
        weeks:  All             weekdays:  All          hours:  Midnight - Noon

OK? (Yes or No):  y

Statistics for chicago.csv
Time Period Filter:
        months:  February - April               days of month:  All
        weeks:  All             weekdays:  All          hours:  Midnight - Noon

-->Calculating the first statistic... - Calculation took 1.46 seconds.
The most popular month is:  April
-->Calculating the next statistic... - Calculation took 1.05 seconds.
The most popular day is:  Wednesday
-->Calculating the next statistic... - Calculation took 1.03 seconds.
The most popular hour is:  Eight AM
-->Calculating the next statistic... - Calculation took 1.02 seconds.
The total trip duration is:  184,301,921.00 seconds
The average trip duration is:  795.42 seconds
-->Calculating the next statistic... - Calculation took 1.28 seconds.
The most popular start stations is:  Clinton St & Washington Blvd
The most popular end stations is:  Streeter Dr & Grand Ave
-->Calculating the next statistic... - Calculation took 1.26 seconds.
The most popular trip is:  Lake Shore Dr & Monroe St to Streeter Dr & Grand Ave
-->Calculating the next statistic... - Calculation took 1.08 seconds.
User types and counts:
        Customer:  28,962
        Dependent:  2
        Subscriber:  202,741
-->Calculating the next statistic... - Calculation took 1.10 seconds.
Gender types and counts:
        Female:  46,135
        Male:  156,618
        Unknown:  28,952
-->Calculating the next statistic... - Calculation took 1.08 seconds.
The earliest (i.e., oldest) users were born in:  1899
The most recent (i.e., youngest) users were born in:  2016
The most popular year users were born in:  1989

Note:  Assuming a screen width of 132 characters, monospaced.
Would you like to view individual trip data?  ('Yes' or 'No')
y

Start Time           End Time        Trip Dur.  Start Station              End Station                User Type   Gender  Birth Yr
01-01-2017 00:00:36  01-01 00:06:32      356.0  Canal St & Taylor St       Canal St & Monroe St (*)   Customer    None    None

01-01-2017 00:02:54  01-01 00:08:21      327.0  Larrabee St & Menomone...  Sheffield Ave & Kingsb...  Subscriber  Male    1984

01-01-2017 00:06:06  01-01 00:18:31      745.0  Orleans St & Chestnut ...  Ashland Ave & Blackhaw...  Subscriber  Male    1985

01-01-2017 00:07:28  01-01 00:12:51      323.0  Franklin St & Monroe St    Clinton St & Tilden St     Subscriber  Male    1990

01-01-2017 00:07:57  01-01 00:20:53      776.0  Broadway & Barry Ave       Sedgwick St & North Ave    Subscriber  Male    1990


View another 5 lines of trip data?  ('Yes' or 'No')
n

Would you like to restart (with statistics)?  Enter "Yes" or "No":
n
C:\apps\working\udacity\dand\proj2 [master +9 ~0 -0 !]>
```

## License
[MIT License](license.txt)

