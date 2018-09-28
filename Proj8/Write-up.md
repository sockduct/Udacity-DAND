# [Project 8 - Create a Tableau Story](https://github.com/sockduct/Udacity-DAND/tree/master/Proj8) Write-up

## [Tableau Public Workbook - US Flight Stats, Story](https://public.tableau.com/profile/james.small#!/vizhome/USFlightStatsRevised/USFlightsStory)

## Summary
This public Tableau story showcases US flights in a nutshell for 2008.  Beginning with flight destinations, then flight volumes, followed by flight cancellations and diversions, and ending with flight delays.  Each section allows filtering, and highlighting is used where it makes sense.  For each view, a brief description is provided.

## Design
* Initial:
  * The story begins with a map.  This clearly shows where people travel to within the US.  The map is interactive allowing the user to highlight various airports while revealing the airport code.  The viewer may also cycle through the months of the year to see how travel patterns change.  Continuing with each view (dashboard), filtering and highlighting are incorporated to allow and encourage exploration of the presented information.  Color is used sparingly, only added to the cancellation and delay views to highlight the different types of cancellation/delay causes.

* Revisions:
  * Based on feedback the following changes were made:
    * Added airports.csv and carriers.csv as data sources from the site supplemental data (see README)
    * Merged in fields from airports and carriers files to add carrier names (in addition to carrier code) and airport names and addresses (in addition to airport origin and destination codes)
    * For all worksheets - change default title to more descriptive one, add tooltips for carriers to show carrier name and for airports to show airport name and address, update axes labels, remove irrelevant axes/labels
    * Destinations worksheet - added legend explaining size of airport dot relates to traffic volume, added map layer - coastline for improved map visibility/readability
    * Volume-Month/Weekday worksheets - added callout for busiest and slowest months/days
    * Cancel-Cause worksheet - added number for Security column so it doesn't seem like it's 0
    * Diversions Worksheets - Had True/False, filtered out False, only want to show actual diversions, for Destination and Carrier diverions pointed out worst ones
    * US Flights Story - volume dashboard shows best/worst, cancellations/diversions/delays dashboards point out worst airport/carrier

## Feedback
* Comments from Syed S., Fellow DAND Student
  * 1st slide - on first glance it seems like not sure what its try to tell audience so add little heading and some legend explaining what dot size means and add detail to dot so if I hover I can see more details
  * 2nd slide - believe heading should be volume by time of the month and days and subheading volume by month or vol/month, also good to mention exactly which month day are highest/lowest.
  * 3rd slide - all look good except cancellation cause rather than cancel-cause sub heading
  * 4th slide - under Diversions slide False and true don't make sense so best to add some lines on heading that what false true means and add detail/label in mark to see if it add more value, also mention that WN make most diversions and ATL is where most get diverted
  * Last slide - worth mentioning that you found ORD caused most in delay, If you can use full name instead of abbreviations that would make it much easier for reader to make sense

## Resource Attribution
* The following resources were used in coming up with the solution for this project:
    * Tableau documentation and community forums
    * Some use of Python/pandas to explore data

## Previous Versions of the Tableau Workbook - US Flight Stats, Story
* [Original](https://public.tableau.com/profile/james.small#!/vizhome/USFlightStats/USFlightsStory)

