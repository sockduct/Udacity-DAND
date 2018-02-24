#!/usr/bin/env python3.6

## TODO: import all necessary packages and functions
from calendar import monthrange
import datetime


# Filenames - use ALL CAPS for global constants
CHI = 'chicago.csv'
NYC = 'new_york_city.csv'
WAS = 'washington.csv'


def get_city() -> str:
    '''Asks the user for a city and returns the filename for that city's bike share
       data.

       Args:  None
       Returns:  Filename for a city's bikeshare data.
    '''

    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        # TODO: handle raw input and complete function
        if city == '1' or 'chicago'.startswith(city.lower()):
            return CHI
        elif city == '2' or 'new york'.startswith(city.lower()):
            return NYC
        elif city == '3' or 'washington'.startswith(city.lower()):
            return WAS
        else:
            print('\nPlease enter 1) Chicago, 2) New York, or 3) Washington.')


def get_time_period() -> str:
    '''Asks the user for a time period and returns the specified filter.

       Args:  None
       Returns:  Time period filter
    '''

    while True:
        time_period = input('\nWould you like to filter the data by "month", "day", or not at'
                            ' all ("none")?\n')
        # TODO: handle raw input and complete function
        if time_period == '1' or 'month'.startswith(time_period.lower()):
            return 'month'
        elif time_period == '2' or 'day'.startswith(time_period.lower()):
            return 'day'
        elif (time_period == '3' or 'not at all'.startswith(time_period.lower())
                or 'none'.startswith(time_period.lower())):
            return 'none'
        else:
            print('\nPlease enter 1) Month, 2) Day, or 3) None.')


def get_month() -> str:
    '''Asks the user for a month and returns the specified month.

       Args:  None
       Returns:  Month
    '''

    while True:
        month = input('\nWhich month? January, February, March, April, May, or June?\n')
        # TODO: handle raw input and complete function
        if month == '1' or 'january'.startswith(month.lower()):
            return 'january'
        elif month == '2' or 'february'.startswith(month.lower()):
            return 'february'
        elif month == '3' or 'march'.startswith(month.lower()):
            return 'march'
        elif month == '4' or 'april'.startswith(month.lower()):
            return 'april'
        elif month == '5' or 'may'.startswith(month.lower()):
            return 'may'
        elif month == '6' or 'june'.startswith(month.lower()):
            return 'june'
        else:
            print('\nPlease enter 1) January, 2) February, 3) March, 4) April, 5) May, '
                  'or 6) June.')


def get_day(month) -> int:
    '''Asks the user for a day and returns the specified day.

       Args:  month - targetted month, accepts int(1 - 12) or str
       Returns:  user selected day, validated by calendar.monthrange
    '''
    # Determine year dynamically - but in this case, data is only from 2017...
    # year = datetime.date.today().year
    year = 2017
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
              12: 'December'}

    if type(month) is int and 1 <= month <= 12:
        daymax = monthrange(year, month)[1]
        monthstr = months[month]
    elif type(month) is str:
        if 'january'.startswith(month.lower()):
            daymax = monthrange(year, 1)[1]
            monthstr = months[1]
        elif 'february'.startswith(month.lower()):
            daymax = monthrange(year, 2)[1]
            monthstr = months[2]
        elif 'march'.startswith(month.lower()):
            daymax = monthrange(year, 3)[1]
            monthstr = months[3]
        elif 'april'.startswith(month.lower()):
            daymax = monthrange(year, 4)[1]
            monthstr = months[4]
        elif 'may'.startswith(month.lower()):
            daymax = monthrange(year, 5)[1]
            monthstr = months[5]
        elif 'june'.startswith(month.lower()):
            daymax = monthrange(year, 6)[1]
            monthstr = months[6]
        elif 'july'.startswith(month.lower()):
            daymax = monthrange(year, 7)[1]
            monthstr = months[7]
        elif 'august'.startswith(month.lower()):
            daymax = monthrange(year, 8)[1]
            monthstr = months[8]
        elif 'september'.startswith(month.lower()):
            daymax = monthrange(year, 9)[1]
            monthstr = months[9]
        elif 'october'.startswith(month.lower()):
            daymax = monthrange(year, 10)[1]
            monthstr = months[10]
        elif 'november'.startswith(month.lower()):
            daymax = monthrange(year, 11)[1]
            monthstr = months[11]
        elif 'december'.startswith(month.lower()):
            daymax = monthrange(year, 12)[1]
            monthstr = months[12]
        else:
            raise ValueError('Invalid month "{}" - expected 1-12 or "January".."December".'
                             ''.format(month))
    else:
        raise ValueError('Invalid month "{}" - expected 1-12 or "January".."December".'
                         ''.format(month))

    while True:
        day = input('\nPlease enter a day for {}, {} from 1 - {}:\n'.format(monthstr,
                    year, daymax))
        # TODO: handle raw input and complete function
        try:
            day = int(day)
            if 1 <= day <= daymax:
                return day
        except ValueError:
            pass

        print('\nPlease enter a day for {}, {} from 1 - {}.'.format(monthstr, year, daymax))


# Takes a significant amount of time to load the data - only do it once
def load_city_file(city_file: str) -> list
    '''Opens city_file, loads all lines into a list and returns it.

       Args:  filename, assumed to be in current working directory
       Returns:  all lines from filename
    '''
    data = []

    with open(city_file) as f:
        for line in f:
            data.append(line)

    return data


# Default to January (1) - June (6) as that's the range of data we have
def popular_month(city_data: list, time_period=(1, 6): tuple -> str:
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular month for start time?
    '''
    '''Determine month with highest number of start times within time_period.

       Args:  All data from the city file (city_data),
       Returns:  ...
    '''
    # TODO: complete function


def popular_day(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    '''
    # TODO: complete function


def popular_hour(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular hour of day for start time?
    '''
    # TODO: complete function


def trip_duration(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the total trip duration and average trip duration?
    '''
    # TODO: complete function


def popular_stations(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular start station and most popular end station?
    '''
    # TODO: complete function


def popular_trip(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular trip?
    '''
    # TODO: complete function


def users(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of each user type?
    '''
    # TODO: complete function


def gender(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of gender?
    '''
    # TODO: complete function


def birth_years(city_data, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    '''
    # TODO: complete function


def display_data():
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')
    # TODO: handle raw input and complete function


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    print('Calculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        
        #TODO: call popular_month function and print the results
        
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        
        # TODO: call popular_day function and print the results
        
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")    

    start_time = time.time()

    # What is the most popular hour of day for start time?
    # TODO: call popular_hour function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    # TODO: call trip_duration function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    # TODO: call popular_stations function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    # TODO: call popular_trip function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    # TODO: call users function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    # TODO: call gender function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    # TODO: call birth_years function and print the results

    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data()


def main():
    '''Entry point for direct script invocation.'''
    statistics()

    # Restart?
    while True:
        restart = input('\nWould you like to restart?  Enter "Yes" or "No":\n')
        if 'yes'.startswith(restart.lower()):
            statistics()
        elif 'no'.startswith(restart.lower()):
            return
        else:
            print('\nPlease enter "Yes" or "No".')


if __name__ == '__main__':
    main()

