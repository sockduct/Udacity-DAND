#!/usr/bin/env python3.6-64
################################################################################
# Need 64-bit Python 3.6+ (may work with 3.5)
# With 32-bit Python will run out of memory
################################################################################


################################################################################
# To do:
#===============================================================================
# * Create a time_period class with supports one or a range of months, weeks,
#   days, and/or hours
# * time_period should also help with converting between string and numberical
#   form of all the above - see function defintions
# * Update functions to leverage this time_period class
#
################################################################################

# Imports:
from calendar import monthrange
from csv import DictReader
from datetime import datetime, date
from time import time
from timeperiod import TimePeriodFilter, TimePeriodResult
from typing import List, Tuple, Union


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


def get_time_period() -> TimePeriodFilter:
    '''Asks the user for a time period and returns the specified filter.

       Args:  None
       Returns:  Time period filter
    '''
    time_period = TimePeriodFilter()

    while True:
        print('\nThe city data ranges from January 1, 2017 to June 30, 2017.')
        answer = input('\nWould you like to filter the city data analysis by '
                            '1) Month(s), 2) Day(s) of \na month, 3) Week(s), 4) '
                            'Weekday(s), 5) Hours, or 6) no filter (none)?\n')
        if answer == '1' or 'months'.startswith(answer.lower()):
            get_month(time_period)
        elif answer == '2' or 'days of month'.startswith(answer.lower()):
            get_days_of_month(time_period)
        # This one first since 'week' would always preempt it
        elif answer == '4' or 'weekdays'.startswith(answer.lower()):
            get_weekday(time_period)
        elif answer == '3' or 'weeks'.startswith(answer.lower()):
            get_week(time_period)
        elif answer == '5' or 'hours'.startswith(answer.lower()):
            get_hour(time_period)
        elif answer == '6' or ('none'.startswith(answer.lower()) or
                               'no filter'.startswitch(answer.lower())):
            time_period.clear()
        else:
            print('\nPlease enter 1) Month, 2) Day, 3) Week, 4) Weekday, 5) Hour, '
                  'or 6) None.')

        print(time_period)
        answer = input('\nOK? (Yes or No):  ')
        if 'yes'.startswith(answer.lower()):
            break

    return time_period


def get_month(time_period) -> TimePeriodFilter:
    '''Asks the user for a month and returns the specified month.

       Args:  None
       Returns:  Month range
    '''

    def parse_month(month):
        if month == '1' or 'january'.startswith(month.lower()):
            return 1
        elif month == '2' or 'february'.startswith(month.lower()):
            return 2
        elif month == '3' or 'march'.startswith(month.lower()):
            return 3
        elif month == '4' or 'april'.startswith(month.lower()):
            return 4
        elif month == '5' or 'may'.startswith(month.lower()):
            return 5
        elif month == '6' or 'june'.startswith(month.lower()):
            return 6
        else:
            print('\nPlease enter 1) January, 2) February, 3) March, 4) April, 5) May, '
                  '6) June, or a range\n(February - April).')

    while True:
        month = input('\nJanuary, February, March, April, May, June, or a range '
                      '(February - April)?\n')

        if '-' in month:
            month_start, month_end = month.split('-')
            start_res = parse_month(month_start.strip())
            end_res = parse_month(month_end.strip())
            if start_res and end_res:
                time_period.month_start = start_res
                time_period.month_end = end_res
                break
        else:
            res = parse_month(month.strip())
            if res:
                time_period.month_start = res
                time_period.month_end = res
                break


def get_days_of_month(time_period) -> TimePeriodFilter:
    '''Asks the user for a day and returns the specified day.

       Args:  month - targetted month, accepts int(1 - 12) or str
       Returns:  user selected day, validated by calendar.monthrange
    '''
    # Determine year dynamically - but in this case, data is only from 2017...
    # year = date.today().year
    year = 2017

    while True:
        if time_period.month_start != time_period.month_end:
            print('\nIn order to select days of a month, you must first select a single'
                  ' month.')
            month = get_month(time_period)
        else:
            break

    _, daymax = monthrange(year, time_period.month_start)
    monthstr = time_period.months[time_period.month_start]

    while True:
        day = input('\nFor {}, {} (1 - {}), please enter a day or a range (3 - 15):'
                    '\n'.format(monthstr, year, daymax))

        if '-' in day:
            day_start, day_end = day.split('-')
        else:
            day_start = day
            day_end = None

        try:
            day_start = int(day_start)
            if day_end:
                day_end = int(day_end)
            else:
                day_end = day_start

            if (1 <= day_start <= daymax) and (1 <= day_end <= daymax):
                time_period.day_of_month_start = day_start
                time_period.day_of_month_end = day_end
                return
        except ValueError:
            pass

        print('\nPlease enter a day or a range (3 - 15) for {}, {} (1 - {}).'.format(
                    monthstr, year, daymax))


def get_weekday(time_period) -> TimePeriodFilter:
    '''Asks the user for a weekday/range and returns the specified one.

       Args:  time_period
       Returns:  None
    '''

    def parse_weekday(weekday):
        if weekday == '1' or 'monday'.startswith(weekday.lower()):
            return 0
        elif weekday == '2' or 'tuesday'.startswith(weekday.lower()):
            return 1
        elif weekday == '3' or 'wednesday'.startswith(weekday.lower()):
            return 2
        elif weekday == '4' or 'thursday'.startswith(weekday.lower()):
            return 3
        elif weekday == '5' or 'friday'.startswith(weekday.lower()):
            return 4
        elif weekday == '6' or 'saturday'.startswith(weekday.lower()):
            return 5
        elif weekday == '7' or 'sunday'.startswith(weekday.lower()):
            return 6
        else:
            print('\nPlease enter 1) Monday, 2) Tuesday, 3) Wednesday, 4) Thursday, '
                  '5) Friday,\n6) Saturday, 7) Sunday, or a range (Tuesday - Thursday).')

    while True:
        weekday = input('\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday,'
                      ' or a range \n(February - April)?\n')

        if '-' in weekday:
            weekday_start, weekday_end = month.split('-')
            start_res = parse_weekdaymonth(weekday_start.strip())
            end_res = parse_weekdaymonth(weekday_end.strip())
            if start_res and end_res:
                time_period.weekday_start = start_res
                time_period.weekday_end = end_res
                break
        else:
            res = parse_weekday(weekday.strip())
            if res:
                time_period.weekday_start = res
                time_period.weekday_end = res
                break


# Create function alias to match specifications
get_day = get_weekday


def get_week(time_period) -> None:
    '''Asks the user for a week/week range and returns it.

       Args:  time_period
       Returns:  None
    '''

    while True:
        week = input('\nPlease enter a week or a range from 1 - 27:\n')

        if '-' in week:
            week_start, week_end = week.split('-')
        else:
            week_start = week
            week_end = None

        try:
            week_start = int(week_start)
            if week_end:
                week_end = int(week_end)
            else:
                week_end = week_start

            if (1 <= week_start <= 27) and (1 <= week_end <= 27):
                time_period.week_start = week_start
                time_period.week_end = week_end
                return
        except ValueError:
            pass

        print('\nPlease enter a week or a range from 1 - 27.')


def get_hour(time_period) -> None:
    '''Asks the user for a hour/hour range and returns it.

       Args:  time_period
       Returns:  None
    '''

    while True:
        hour = input('\nPlease enter a hour or a range from 0 - 23 (0 = midnight, '
                     '13 = 1 pm):\n')

        if '-' in hour:
            hour_start, hour_end = hour.split('-')
        else:
            hour_start = hour
            hour_end = None

        try:
            hour_start = int(hour_start)
            if hour_end:
                hour_end = int(hour_end)
            else:
                hour_end = hour_start

            if (0 <= hour_start <= 23) and (0 <= hour_end <= 23):
                time_period.hour_start = hour_start
                time_period.hour_end = hour_end
                return
        except ValueError:
            pass

        print('\nPlease enter a hour or a range from 0 - 23.')


# Takes a significant amount of time to load the data - only do it once
def load_city_file(city_file: str, verbose: bool=False) -> List[dict]:
    '''Opens city_file, loads using csv stdlib DictReader, returns as list.

       Args:  filename, assumed to be in current working directory
       Returns:  list of results
    '''

    # Read in CSV using column headers as keys
    if verbose:
        load_start = time()
        print('Loading {}...'.format(city_file), end='', flush=True)
    with open(city_file) as f:
        reader = DictReader(f)
        data = list(reader)
    if verbose:
        print(' - Processed in {:.2f} seconds.'.format(time() - load_start))

    # Convert column types from str to native where appropriate
    # Takes roughly three times as long as loading the file into the data structure
    if verbose:
        conv_start = time()
        print('Converting to native types...', end='', flush=True)
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
            row['Trip Duration'] = float(row['Trip Duration'])
        except ValueError as err:
            print('Choked on trip duration:  {}'.format(row['Trip Duration']))
        # These are strings so leave as is:
        # row['Start Station']
        # row['End Station']
        # row['User Type']
        # Gender doesn't exist in Washington file so add None
        try:
            _ = row['Gender']
        except KeyError as err:
            row['Gender'] = None
        try:
            birth_year = row['Birth Year']
            if birth_year:
                row['Birth Year'] = int(float(birth_year))
            else:
                row['Birth Year'] = None
        except ValueError as err:
            print('Choked on birth year:  {}'.format(row['Birth Year']))
        except KeyError as err:
            row['Birth Year'] = None
    if verbose:
        print(' - Processed in {:.2f} seconds.'.format(time() - conv_start))

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

    for row in city_data:
        # Count
        res[row['Start Time'].month] += 1

    # Optionally see calculated month data:
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
    res = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
            5: 'Saturday', 6: 'Sunday'}

    for row in city_data:
        # Count
        res[row['Start Time'].weekday()] += 1

    # Optionally see calculated day data:
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


# Default to 0 - 23
def popular_hour(city_data: List[str], time_period: Tuple[int, int]=(0, 23),
                 verbose: bool=False) -> Union[tuple, int]:
    '''Determine hour with highest number of start times within time_period.
       Answer question:  What is the most popular hour of the day (0, 1, ..., 23)
                         for start time?

       Args:  All data from the city file (city_data),
       Returns:  hour name or tuple of hour names in case of tie(s)
    '''
    res = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
           11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
           21: 0, 22: 0, 23: 0}
    hours = {0: 'Midnight', 1: 'One AM', 2: 'Two AM', 3: 'Three AM', 4: 'Four AM',
             5: 'Five AM', 6: 'Six AM', 7: 'Seven AM', 8: 'Eight AM', 9: 'Nine AM',
             10: 'Ten AM', 11: 'Eleven AM', 12: 'Noon', 13: 'One PM', 14: 'Two PM',
             15: 'Three PM', 16: 'Four PM', 17: 'Five PM', 18: 'Six PM',
             19: 'Seven PM', 20: 'Eight PM', 21: 'Nine PM', 22: 'Ten PM',
             23: 'Eleven PM'}

    for row in city_data:
        # Count
        res[row['Start Time'].hour] += 1

    # Optionally see calculated hour data:
    if verbose:
        print('popular_hour/results:  {}'.format(res))

    # Filter?
    if time_period == (0, 23):
        hour_val = max(res.values())
        filt_res = res
    else:
        filt_res = {}
        for k in res:
            if time_period[0] <= k <= time_period[1]:
                filt_res[k] = res[k]
        hour_val = max(res.values())

    # Duplicates?
    if len([v for v in filt_res.values() if v == hour_val]) > 1:
        mult_res = []
        for k in res:
            if res[k] == hour_val:
                mult_res.append(hours[k])
        return tuple(mult_res)
    else:
        for k in res:
            if res[k] == hour_val:
                return hours[k]


# Default time_period?
def trip_duration(city_data: List[str], time_period: Tuple[int, int],
                 verbose: bool=False) -> Union[tuple, int]:
    '''Determine total trip duration and average trip duration during time_period.
       Answer question:  What is the total trip duration and average trip duration?
                         (default/reasonable time_period???)

       Args:  All data from the city file (city_data),
       Returns:  total trip duration, average trip duration or tuple of tuples in
                 case of tie(s)
    '''
    res_total = sum(row['Trip Duration'] for row in city_data)
    res_avg = res_total/len(city_data)

    # Optionally see calculated hour data:
    if verbose:
        print('popular_hour/results:  {}'.format(res))

    # Filter?
    if time_period == (0, 23):
        hour_val = max(res.values())
        filt_res = res
    else:
        filt_res = {}
        for k in res:
            if time_period[0] <= k <= time_period[1]:
                filt_res[k] = res[k]
        hour_val = max(res.values())

    # Duplicates?
    if len([v for v in filt_res.values() if v == hour_val]) > 1:
        mult_res = []
        for k in res:
            if res[k] == hour_val:
                mult_res.append(hours[k])
        return tuple(mult_res)
    else:
        for k in res:
            if res[k] == hour_val:
                return hours[k]


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
    for city in [CHI, NYC, WAS]:
        data = load_city_file(city, verbose=True)
        print(popular_month(data, verbose=True))
        print(popular_day(data, verbose=True))
        print(popular_hour(data, verbose=True))
        print()


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

