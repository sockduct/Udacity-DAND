#!/usr/bin/env python3.6

## TODO: import all necessary packages and functions
from calendar import monthrange
##from collections import namedtuple
from csv import DictReader
from datetime import datetime, date
from time import time
from typing import List, Tuple, Union


# Filenames - use ALL CAPS for global constants
CHI = 'chicago.csv'
NYC = 'new_york_city.csv'
WAS = 'washington.csv'


##TimeRec = namedtuple('TimeRec', ['year', 'month', 'date', 'hour', 'minute', 'second'])


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


def get_day(month: Union[int, str]) -> int:
    '''Asks the user for a day and returns the specified day.

       Args:  month - targetted month, accepts int(1 - 12) or str
       Returns:  user selected day, validated by calendar.monthrange
    '''
    # Determine year dynamically - but in this case, data is only from 2017...
    # year = date.today().year
    year = 2017
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
              12: 'December'}

    if isinstance(month, int) and 1 <= month <= 12:
        daymax = monthrange(year, month)[1]
        monthstr = months[month]
    elif isinstance(month, str):
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
            dayint = int(day)
            if 1 <= dayint <= daymax:
                return dayint
        except ValueError:
            pass

        print('\nPlease enter a day for {}, {} from 1 - {}.'.format(monthstr, year, daymax))


# Takes a significant amount of time to load the data - only do it once
def load_city_file(city_file: str, verbose: bool=False) -> List[dict]:
    '''Opens city_file, loads using csv stdlib DictReader, returns as list.

       Args:  filename, assumed to be in current working directory
       Returns:  list of results
    '''

    # Read in CSV using column headers as keys
    if verbose:
        load_start = time()
        print('Loading {}...'.format(city_file))
    with open(city_file) as f:
        reader = DictReader(f)
        data = list(reader)
    if verbose:
        print('Processed in {} seconds.'.format(time() - load_start))

    # Convert column types from str to native where appropriate
    if verbose:
        conv_start = time()
        print('Converting to native types...')
    for row in data:
        # Parse out date into year, month, date, time - ('2017-01-01 00:00:36')
        # datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
        # Use %I for 12 hour time vs. %H for 24 hour time
        try:
            row['Start Time'] = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        except ValueError as err:
            print('Choked on start time:  {}'.format(row['Start Time']))
        try:
            row['End Time'] = datetime.strptime(row['End Time'], '%Y-%m-%d %H:%M:%S')
        except ValueError as err:
            print('Choked on end time:  {}'.format(row['End Time']))
        try:
            row['Trip Duration'] = int(row['Trip Duration'])
        except ValueError as err:
            print('Choked on trip duration:  {}'.format(row['Trip Duration']))
        # These are strings so leave as is:
        # row['Start Station']
        # row['End Station']
        # row['User Type']
        # row['Gender']
        try:
            birth_year = row['Birth Year']
            if birth_year:
                row['Birth Year'] = int(float(birth_year))
            else:
                row['Birth Year']  = None
        except ValueError as err:
            print('Choked on birth year:  {}'.format(row['Birth Year']))
    if verbose:
        print('Processed in {} seconds.'.format(time() - conv_start))

    return data


# Default to January (1) - June (6) as that's the range of data we have
def popular_month(city_data: List[str], time_period: Tuple[int, int]=(1, 6),
                  verbose: bool=False) -> Union[tuple, str]:
    '''Determine month with highest number of start times within time_period.
       Answer question:  What is the most popular month for start time?

       Args:  All data from the city file (city_data),
       Returns:  month name or tuple of month names in case of tie(s)
    '''
    res = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    rev_months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}

    # If time_period passed as strings, convert to ints:
    tpstr = False
    if isinstance(time_period[0], str):
        tpstr = True
        start = None
        for month in ['january', 'february', 'march', 'april', 'may', 'june']:
            if month.startswith(time_period[0].lower()):
                start = rev_months[month]
    if isinstance(time_period[1], str):
        tpstr = True
        end = None
        for month in ['january', 'february', 'march', 'april', 'may', 'june']:
            if month.startswith(time_period[0].lower()):
                end = rev_months[month]

    if not tpstr:
        tpvalid = True if 1 <= time_period[0] <= 6 else False

    if tpstr and start and stop:
        time_period = start, stop
    elif tpvalid:
        pass  # So only raise ValueError in one place
    else:
        raise ValueError('time_period must be in the range of 1-6 or January..June, '
                         'got {} - {}'.format(time_period[0], time_period[1]))

    for line in city_data:
        # Count
        res[line['Start Time'].month] += 1

    # Month with highest number of start times:
    if verbose:
        print('popular_month/results:  {}'.format(res))

    # Filter?
    if time_period == (1, 6):
        month_val = max(res.values())
        filt_res = res
    else:
        filt_res = {}
        for k in res:
            if time_period[0] <= k <= time_period[1]:
                filt_res[k] = res[k]
        month_val = max(res.values())

    # Duplicates?
    if len([v for v in filt_res.values() if v == month_val]) > 1:
        mult_res = []
        for k in res:
            if res[k] == month_val:
                mult_res.append(months[k])
        return tuple(mult_res)
    else:
        for k in res:
            if res[k] == month_val:
                return months[k]


# Default to Monday (0) - Sunday (6)
def popular_day(city_data: List[str], time_period: Tuple[int, int]=(0, 6),
                verbose: bool=False) -> Union[tuple, str]:
    '''Determine day with highest number of start times within time_period.
       Answer question:  What is the most popular day of week (Monday, Tuesday, etc.)
                         for start time?

       Args:  All data from the city file (city_data),
       Returns:  day name or tuple of day names in case of tie(s)
    '''
    # TODO: complete function
    res = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
            5: 'Saturday', 6: 'Sunday'}

    for line in city_data:
        # Count
        res[line['Start Time'].weekday()] += 1

    # Month with highest number of start times:
    if verbose:
        print('popular_day/results:  {}'.format(res))

    # Filter?
    if time_period == (0, 6):
        day_val = max(res.values())
        filt_res = res
    else:
        filt_res = {}
        for k in res:
            if time_period[0] <= k <= time_period[1]:
                filt_res[k] = res[k]
        day_val = max(res.values())

    # Duplicates?
    if len([v for v in filt_res.values() if v == day_val]) > 1:
        mult_res = []
        for k in res:
            if res[k] == day_val:
                mult_res.append(days[k])
        return tuple(mult_res)
    else:
        for k in res:
            if res[k] == day_val:
                return days[k]


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
        start_time = time()
        
        #TODO: call popular_month function and print the results
        
        print("That took %s seconds." % (time() - start_time))
        print("Calculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time()
        
        # TODO: call popular_day function and print the results
        
        print("That took %s seconds." % (time() - start_time))
        print("Calculating the next statistic...")    

    start_time = time()

    # What is the most popular hour of day for start time?
    # TODO: call popular_hour function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What is the total trip duration and average trip duration?
    # TODO: call trip_duration function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What is the most popular start station and most popular end station?
    # TODO: call popular_stations function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What is the most popular trip?
    # TODO: call popular_trip function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What are the counts of each user type?
    # TODO: call users function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What are the counts of gender?
    # TODO: call gender function and print the results

    print("That took %s seconds." % (time() - start_time))
    print("Calculating the next statistic...")
    start_time = time()

    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    # TODO: call birth_years function and print the results

    print("That took %s seconds." % (time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data()


def test():
    data = load_city_file(CHI, verbose=True)
    print(popular_month(data, verbose=True))
    print(popular_day(data, verbose=True))

    data = load_city_file(WAS, verbose=True)
    print(popular_month(data, verbose=True))


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
    # main()
    test()

