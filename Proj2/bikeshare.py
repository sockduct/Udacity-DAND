#!/usr/bin/env python3.6-64
################################################################################
# Need 64-bit Python 3.6+
# With 32-bit Python will run out of memory
# Note:  Using variable annotations - requires 3.6+
################################################################################

'''Program to read in various CSV data sets about bike sharing services and
   provide statistics on them.  Optionally allows statistics to be constrained
   by a user specified time period filter.'''

################################################################################
# To do:
#===============================================================================
# * Re-factor focusing on eliminating duplicate code/making useful generics
# ** e.g., timeperiod.py:  in the __init__, initialize the days_of_month using
#                          a loop instead of typing all 31 entries of the map
# ** e.g., think about how to make the interactive prompt more generic - the
#          logic is pretty similar and should not require repeating itself
# * Add better testing - perhaps unit tests or some pytest integration
# * Support dynamic field definition (e.g. if the dataset is slightly changed,
#   some column(s) are/is not available), the program can adapt to the new data
#   structure by updating a config file
################################################################################

################################################################################
# Notes:
# Q) Why didn't you use pandas?
# A) The original intent of this assignment was to show how much work it was
#    to use the csv stdlib as opposed to pandas (which is introduced later in
#    the program).  However, there is some value in limiting yourself to just
#    the Python stdlib.  Some programs include Python as an embedded automation
#    engine but only allow the stdlib - no 3rd party libraries are allowed.
#    Thus, I found this a useful exercise.
################################################################################

# System Imports:
from calendar import monthrange
from collections import OrderedDict
from csv import DictReader
from datetime import datetime, date, timedelta
import os
import sys
from time import time
from typing import Any, List, Tuple, Union

# My Imports:
from timeperiod import TimePeriodFilter, TimePeriodResult
from util import dict_filter, dict_keyfilter, one_or_mult, time_str


# Filenames - use ALL CAPS for global constants
CHI = 'chicago.csv'
NYC = 'new_york_city.csv'
WAS = 'washington.csv'


def get_city() -> str:
    '''Asks the user for a city and returns the filename for that city's bike share
       data.

       Args:  None
       Returns:  Filename for a city's bikeshare data
    '''

    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        if city == '1' or 'chicago'.startswith(city.lower()):
            return CHI
        elif city == '2' or 'new york'.startswith(city.lower()):
            return NYC
        elif city == '3' or 'washington'.startswith(city.lower()):
            return WAS
        # Surreptitious test data!
        elif city == '4' or 'sample'.startswith(city.lower()):
            return 'chicago-sample.csv'
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
            set_month(time_period)
        elif answer == '2' or 'days of month'.startswith(answer.lower()):
            set_days_of_month(time_period)
        # This one first since 'week' would always preempt it
        elif answer == '4' or 'weekdays'.startswith(answer.lower()):
            set_weekday(time_period)
        elif answer == '3' or 'weeks'.startswith(answer.lower()):
            set_week(time_period)
        elif answer == '5' or 'hours'.startswith(answer.lower()):
            set_hour(time_period)
        elif answer == '6' or ('none'.startswith(answer.lower()) or
                               'no filter'.startswith(answer.lower())):
            time_period.clear()
        else:
            print('\nPlease enter 1) Month, 2) Day, 3) Week, 4) Weekday, 5) Hour, '
                  'or 6) None.')

        print('\n{}'.format(time_period))
        answer = input('OK? (Yes or No):  ')
        if 'yes'.startswith(answer.lower()) or 'ok'.startswith(answer.lower()):
            break

    return time_period


def set_month(time_period: TimePeriodFilter) -> None:
    '''Asks the user for a month (range) and updates the passed time period
       filter.

       Args:  Time period filter
       Returns:  None
    '''

    def parse_month(month):
        '''Try to convert user input into month (Jan - Jun) or re-prompt if
           unable to do so.'''
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


def set_days_of_month(time_period: TimePeriodFilter) -> None:
    '''Asks the user for a day (range) and updates the passed time period
       filter.

       Args:  Time period filter
       Returns:  None
    '''
    # Determine year dynamically - but in this case, data is only from 2017...
    # year = date.today().year
    year = 2017

    while True:
        if time_period.month_start != time_period.month_end:
            print('\nIn order to select days of a month, you must first select a single'
                  ' month.')
            set_month(time_period)
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
            iday_start = int(day_start)
            if day_end:
                iday_end = int(day_end)
            else:
                iday_end = iday_start

            if (1 <= iday_start <= daymax) and (1 <= iday_end <= daymax):
                time_period.day_of_month_start = iday_start
                time_period.day_of_month_end = iday_end
                return
        except ValueError:
            pass

        print('\nPlease enter a day or a range (3 - 15) for {}, {} (1 - {}).'.format(
                    monthstr, year, daymax))


def set_weekday(time_period: TimePeriodFilter) -> None:
    '''Asks the user for a weekday (range) and updates the passed time period
       filter.

       Args:  Time period filter
       Returns:  None
    '''

    def parse_weekday(weekday):
        '''Try to convert user input into weekday or re-prompt if can't.'''
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
                        ' or a range \n(Tuesday - Thursday)?\n')

        if '-' in weekday:
            weekday_start, weekday_end = weekday.split('-')
            start_res = parse_weekday(weekday_start.strip())
            end_res = parse_weekday(weekday_end.strip())
            if start_res and end_res:
                time_period.weekday_start = start_res
                time_period.weekday_end = end_res
                break
        else:
            res = parse_weekday(weekday.strip())
            if res is not None:
                time_period.weekday_start = res
                time_period.weekday_end = res
                break


# Create function alias to match specifications
set_day = set_weekday


def set_week(time_period: TimePeriodFilter) -> None:
    '''Asks the user for a week (range) and updates the passed time period
       filter.

       Args:  Time period filter
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
            iweek_start = int(week_start)
            if week_end:
                iweek_end = int(week_end)
            else:
                iweek_end = iweek_start

            if (1 <= iweek_start <= 27) and (1 <= iweek_end <= 27):
                time_period.week_start = iweek_start
                time_period.week_end = iweek_end
                return
        except ValueError:
            pass

        print('\nPlease enter a week or a range from 1 - 27.')


def set_hour(time_period: TimePeriodFilter) -> None:
    '''Asks the user for a hour (range) and updates passed time period filter.

       Args:  Time period filter
       Returns:  None
    '''

    while True:
        hour = input('\nPlease enter a hour or a range from 0 - 23 (0 = midnight, '
                     '13 = 1 pm):\n')

        if '-' in hour:
            # In case a negative leading hour entered:
            try:
                hour_start, hour_end = hour.split('-')
            except ValueError:
                continue
        else:
            hour_start = hour
            hour_end = None

        try:
            ihour_start = int(hour_start)
            if hour_end:
                ihour_end = int(hour_end)
            else:
                ihour_end = ihour_start

            if (0 <= ihour_start <= 23) and (0 <= ihour_end <= 23):
                time_period.hour_start = ihour_start
                time_period.hour_end = ihour_end
                return
        except ValueError:
            pass

        print('\nPlease enter a hour or a range from 0 - 23.')


# Takes a significant amount of time to load the data - only do it once
def load_city_file(city_file: str, verbose: bool=False) -> List[OrderedDict]:
    '''Opens city_file, loads using csv stdlib DictReader, returns as list.

       Args:  city_file - assumed to be in current working directory
              verbose - optional toggle to enable debug-type output
       Returns:  list of results
    '''

    # Read in CSV using column headers as keys
    if verbose:
        load_start = time()
        print('Loading {}...'.format(city_file), end='', flush=True)
    with open(city_file) as infile:
        reader = DictReader(infile)
        data = list(reader)
    if verbose:
        print(' - Processed in {:.2f} seconds.'.format(time() - load_start))

    # Convert column types from str to native where appropriate
    # Takes roughly three times as long as loading the file into the data structure
    if verbose:
        conv_start = time()
        print('Converting to native types...', end='', flush=True)

    row: Any  # Allow changing types
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
            gender = row['Gender']
            if gender.strip() == '':
                row['Gender'] = None
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


def within_time(dtobj: datetime, time_period: TimePeriodFilter) -> bool:
    '''See if passed datetime object falls within passed time period filter -
       Yes?  Return True, otherwise return False.

       Args:  datetime object - the date and time in question
              Time period filter
       Returns:  boolean
    '''
            # Month
    return ((time_period.month_start <= dtobj.month <= time_period.month_end) and
            # Day of Month
            (time_period.day_of_month_start <= dtobj.day <= time_period.day_of_month_end)
            # Week
            and (time_period.week_start <= dtobj.isocalendar()[1] <= time_period.week_end)
            # Weekday
            and (time_period.weekday_start <= dtobj.weekday() <= time_period.weekday_end)
            # Hour
            and (time_period.hour_start <= dtobj.hour <= time_period.hour_end))


# Default to January (1) - June (6) as that's the range of data we have
def popular_month(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                  verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine month with highest number of start times within time period
       filter.
       Answer question:  What is the most popular month for start time?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  month name or tuple of month names in case of tie(s)
    '''
    period_results = TimePeriodResult()

    # Count up data and tally by month
    for row in city_data:
        # Check against time period filter:
        start = row['Start Time']

        if within_time(start, time_period):
            period_results.months[start.month] += 1

    # Max:
    month_val = max(period_results.months.values())
    filt_res = dict_filter(period_results.months)

    # Optionally see calculated month data:
    if verbose:
        print('popular_month/results:  {}, max:  {:,}'.format(filt_res, month_val))

    return one_or_mult(filt_res, month_val, time_period.months)


# Default to Monday (0) - Sunday (6)
def popular_day(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine day with highest number of start times within time period
       filter.
       Answer question:  What is the most popular day of week (Monday, Tuesday,
                         etc.) for start time?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  day name or tuple of day names in case of tie(s)
    '''
    period_results = TimePeriodResult()

    # Count up data and tally by day
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            period_results.weekdays[start.weekday()] += 1

    # Max
    day_val = max(period_results.weekdays.values())
    filt_res = dict_filter(period_results.weekdays)

    # Optionally see calculated weekday data
    if verbose:
        print('popular_day/final results:  {}, max:  {:,}'.format(filt_res, day_val))

    return one_or_mult(filt_res, day_val, time_period.weekdays)


# Default to 0 - 23
def popular_hour(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                 verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine hour with highest number of start times within time period
       filter.
       Answer question:  What is the most popular hour of the day (0, 1, ...,
                         23) for start time?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  hour name or tuple of hour names in case of tie(s)
    '''
    period_results = TimePeriodResult()

    # Count up data and tally by hour
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            period_results.hours[start.hour] += 1

    # Max
    hour_val = max(period_results.hours.values())
    filt_res = dict_filter(period_results.hours)

    # Optionally see final hour data:
    if verbose:
        print('popular_hour/final results:  {}, max:  {:,}'.format(filt_res, hour_val))

    return one_or_mult(filt_res, hour_val, time_period.hours)


# Default time_period?
def trip_duration(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                  verbose: bool=False) -> Tuple[timedelta, float]:
    '''Determine total trip duration and average trip duration during time period
       filter.
       Answer question:  What is the total trip duration and average trip duration?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  total trip duration, average trip duration
    '''
    res_total = 0
    res_count = 0

    # Count up data and tally by trip duration
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            res_total += row['Trip Duration']
            res_count += 1

    res_avg = res_total/res_count

    # Optionally see results:
    if verbose:
        print('trip_duration/results - total:  {:,.2f}, average:  {:,.2f}, records '
              'in time period:  {:,}'.format(res_total, res_avg, res_count))

    # Total number of seconds is large, store it in a datetime object that
    # determines the number of days and seconds
    return timedelta(seconds=res_total), res_avg


def popular_stations(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                     verbose: bool=False) -> Tuple[Union[str, Tuple[str, ...]], ...]:
    '''Determine start and end stations with highest usage count during time
       period filter.
       Answer question:  What is the most popular start station and most popular
                         end station?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  Most popular start station and most popular end station
    '''
    start_stas: dict = {}
    end_stas: dict = {}
    sta_count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            start_sta = row['Start Station']
            end_sta = row['End Station']

            for elmt, ctnr in [(start_sta, start_stas), (end_sta, end_stas)]:
                if elmt in ctnr:
                    ctnr[elmt] += 1
                else:
                    ctnr[elmt] = 1
            sta_count += 1

    # Max
    pop_start = max(start_stas.values())
    pop_end = max(end_stas.values())

    res = {}
    res['Start Station'] = one_or_mult(start_stas, pop_start)
    res['End Station'] = one_or_mult(end_stas, pop_end)

    # Optionally see results:
    if verbose:
        print('popular_stations/results - Start Stations Found:  {:,}, End Stations '
              'Found:  {:,}, Station Records in time period:  {:,},\n\tMost Popular '
              'Station Results:  {}\n\tRecorded {:,} and {:,} times respectively'.format(
                  len(start_stas), len(end_stas), sta_count, res, pop_start, pop_end))

    return tuple((res['Start Station'], res['End Station']))


def popular_trip(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                 verbose: bool=False) -> Union[str, Tuple[str, ...]]:
    '''Count all start station --> end station sets and return one with highest
       frequency within the passed time period filter.
       Answer question:  What is the most popular trip?
       Note:  Defining a trip as the same start/end station pair

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  Most popular trip as defined above
    '''
    trips: dict = {}
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            trip = '{} to {}'.format(row['Start Station'], row['End Station'])

            if trip in trips:
                trips[trip] += 1
            else:
                trips[trip] = 1
            count += 1

    # Max
    pop_trip = max(trips.values())
    res = one_or_mult(trips, pop_trip)

    # Optionally see results:
    if verbose:
        print('popular_trip/results - Trips Found:  {:,}, Records in time period:  '
              '{:,},\n\tMost Popular Trip Result:  {} - Taken {:,} times'.format(
                  len(trips), count, res, pop_trip))

    return res


def users(city_data: List[OrderedDict], time_period: TimePeriodFilter,
          verbose: bool=False) -> dict:
    '''Count all user types including `Unknown`.
       Answer question:  What are the counts of each user type?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  dict of user types with count of each
    '''
    user_types: dict = {}
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            user_type = row['User Type']

            if user_type is None or user_type.strip() == '':
                user_type = 'Unknown'

            if user_type in user_types:
                user_types[user_type] += 1
            else:
                user_types[user_type] = 1
            count += 1

    # Max
    pop_user = max(user_types.values())
    maxres = one_or_mult(user_types, pop_user)

    # Optionally see results:
    if verbose:
        print('user/results - Users Found:  {:,}, Records in time period:  {:,}, '
              'User Types Found:  {}'.format(len(user_types), count, user_types))

    return user_types


def gender(city_data: List[OrderedDict], time_period: TimePeriodFilter,
           verbose: bool=False) -> dict:
    '''Count all gender types including `Unknown`.
       Answer question:  What are the counts of gender?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  dict of gender types with count of each
    '''
    genders: dict = {}
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            gender_type = row['Gender']

            if gender_type is None or gender_type.strip() == '':
                gender_type = 'Unknown'

            if gender_type in genders:
                genders[gender_type] += 1
            else:
                genders[gender_type] = 1
            count += 1

    # Max
    pop_gender = max(genders.values())
    maxres = one_or_mult(genders, pop_gender)

    # Optionally see results:
    if verbose:
        print('gender/results - Genders Found:  {:,}, Records in time period:  {:,}, '
              'Gender Types Found:  {}'.format(len(genders), count, genders))

    return genders


def birth_years(city_data: List[OrderedDict], time_period: TimePeriodFilter,
                verbose: bool=False) -> Tuple[int, int, int]:
    '''Tabulate all birth years including `Unknown`.  If possible (i.e., birth
       years present), determine youngest and oldest birth years.
       Answer question:  What are the earliest (i.e., oldest user), most recent
                         (i.e., youngest user), and most popular birth years?

       Args:  city_data - All data from the city file
              time_period - Time period filter
              verbose - optional toggle to enable debug-type output
       Returns:  tuple of youngest and oldest birth years
    '''
    yobs: dict = {}  # Year of Births
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            birth_year = row['Birth Year']

            if birth_year is None or birth_year == 0:
                birth_year = 'Unknown'

            if birth_year in yobs:
                yobs[birth_year] += 1
            else:
                yobs[birth_year] = 1
            count += 1

    # Max
    res = {'Unknown': yobs['Unknown']}
    filt_yobs = dict_keyfilter(yobs)
    # Sanity check
    if filt_yobs:
        # .keys is the default but using to make it clear/explicit that this is
        # what's desired
        new_birthyr = max(filt_yobs.keys())
        res['Youngest'] = new_birthyr
        old_birthyr = min(filt_yobs.keys())
        res['Oldest'] = old_birthyr
        max_cnt_birthyr = max(filt_yobs.values())
        res['Most Popular'] = one_or_mult(filt_yobs, max_cnt_birthyr)
    else:
        res = {k: 'Unknown' for k in ['Youngest', 'Oldest', 'Most Popular']}

    # Optionally see results:
    if verbose:
        print('birth_years/results - Number of Birth Years Found:  {:,}, Records in '
              'time period:  {:,}, Birth Years Found:  {}'.format(len(yobs), count, yobs))

    return (res['Oldest'], res['Youngest'], res['Most Popular'])


def display_data(city_data: List[OrderedDict], lines: int=5) -> None:
    '''Displays five lines of data at a time if the user specifies that he would
       like to view it.  After displaying, ask the user if he would like to see
       five more.  Continuing asking until user specifies no.

       Args:  city_data - All data from the city file
              lines - How many lines of data to view
       Returns:  None
    '''
    swap_none = lambda seq: [i if i else 'None' for i in seq]
    swap_long = lambda longstr: longstr if len(longstr) <= 25 else longstr[:22] + '...'

    def view_data(lines=5):
        '''Generator function to remember place in the data and print `lines`
           at a time.'''
        for i, line in enumerate(city_data):
            # Print the header row initially and every <lines> lines
            if i % lines == 0:
                (start_time, end_time, trip_dur, start_sta, end_sta, user, gender,
                    birthyr) = line.keys()
                # Abridge 'Trip Duration' and 'Birth Year' to save space
                print('\n{:19}  {:14}  {:9}  {:25}  {:25}  {:10}  {:6}  {:8}'.format(
                        start_time, end_time, 'Trip Dur.', start_sta, end_sta, user,
                        gender, 'Birth Yr'))

            (start_time, end_time, trip_dur, start_sta, end_sta, user, gender,
                birthyr) = swap_none(line.values())
            start_sta = swap_long(start_sta)
            end_sta = swap_long(end_sta)
            print('{:%m-%d-%Y %H:%M:%S}  {:%m-%d %H:%M:%S}  {:9,}  {:25}  {:25}'
                  '  {:10}  {:6}  {:<8}'.format(start_time, end_time, trip_dur,
                      start_sta, end_sta, user, gender, birthyr))

            # Yield every <lines> lines, but not on first run (i == 0)
            if (i + 1) % lines == 0 and i > 0:
                print()
                yield

    print('\nNote:  Assuming a screen width of 132 characters, monospaced.')
    display = input('Would you like to view individual trip data?'
                    '  (\'Yes\' or \'No\')\n')
    paged_data = view_data()
    while True:
        # If user just hits "Enter" (display == ''), don't count it as a yes
        if display and 'yes'.startswith(display.lower()):
            next(paged_data)
        else:
            break

        display = input('View another {} lines of trip data?  (\'Yes\' or \'No\')'
                        '\n'.format(lines))


def statistics(start_city: str=None, start_data:
               List[OrderedDict]=None) -> Tuple[str, List[OrderedDict]]:
    '''Calculates and prints out the descriptive statistics about a city and
       time period specified by the user via raw input.  Optionally takes a
       city data file and the loaded data to allow the user to re-run this
       function with different time period filters.  This avoids the time
       consuming process of having to re-load and re-parse the data for the
       same data set.

       Args:  start_city - City file if previously specified
              start_data - All data from the city file if previously loaded
       Returns:  city file and city data to allow re-running this function
    '''
    res: Any  # Allow multiple type assignment
    start_time = 0.0
    first_stat = True

    def next_stat(initial=False):
        '''Convenience function for printing beginning of stats info.'''
        nonlocal start_time
        nonlocal first_stat
        start_time = time()
        first_stat = False

        if initial:
            print('Statistics for {}\n{}'.format(city, time_period))
            print('-->Calculating the first statistic...', end='')
        else:
            print('-->Calculating the next statistic...', end='')

    stat_time = lambda start_time: print(' - Calculation took {:.2f} seconds.'
                                         ''.format(time() - start_time))

    # Filter by city (Chicago, New York, Washington)
    choose_city = True
    if start_city:
        answer = input('\nCurrent selected city data file is {}.  Choose another'
                       ' city?  (Yes/No)\n'.format(start_city))
        if answer.strip() == '' or not 'yes'.startswith(answer.lower()):
            choose_city = False

    if choose_city:
        city = get_city()
    else:
        city = start_city

    load_data = True
    if not choose_city and start_data:
        answer = input('{} data already loaded into memory.  Reload?  (Yes/No)\n'
                       ''.format(city))
        if answer.strip() == '' or not 'yes'.startswith(answer.lower()):
            load_data = False

    if load_data:
        data = load_city_file(city, verbose=True)
    else:
        data = start_data

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    print()

    # If starting month == ending month then skip
    if time_period.month_start != time_period.month_end:
        next_stat(initial=True) if first_stat else next_stat()
        # What is the most popular month for start time?
        res = popular_month(data, time_period, verbose=False)
        stat_time(start_time)
        print('The most popular month is:  {}'.format(res))

    # If starting weekday == ending weekday then skip
    if time_period.weekday_start != time_period.weekday_end:
        next_stat(initial=True) if first_stat else next_stat()
        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        res = popular_day(data, time_period, verbose=False)
        stat_time(start_time)
        print('The most popular day is:  {}'.format(res))

    # If starting hour == ending hour then skip
    if time_period.hour_start != time_period.hour_end:
        next_stat(initial=True) if first_stat else next_stat()
        # What is the most popular hour of day for start time?
        res = popular_hour(data, time_period, verbose=False)
        stat_time(start_time)
        print('The most popular hour is:  {}'.format(res))

    next_stat(initial=True) if first_stat else next_stat()
    # What is the total trip duration and average trip duration?
    res = trip_duration(data, time_period, verbose=False)
    stat_time(start_time)
    total_dur = time_str(res[0])
    avg_dur = time_str(res[1])
    print('The total trip duration is:  {}'.format(total_dur))
    print('The average trip duration is:  {}'.format(avg_dur))

    next_stat()
    # What is the most popular start station and most popular end station?
    res = popular_stations(data, time_period, verbose=False)
    stat_time(start_time)
    print('The most popular start stations is:  {}'.format(res[0]))
    print('The most popular end stations is:  {}'.format(res[1]))

    next_stat()
    # What is the most popular trip?
    res = popular_trip(data, time_period, verbose=False)
    stat_time(start_time)
    print('The most popular trip is:  {}'.format(res))

    next_stat()
    # What are the counts of each user type?
    res = users(data, time_period, verbose=False)
    stat_time(start_time)
    print('User types and counts:')
    for k, v in sorted(res.items()):
        print('\t{}:  {:,}'.format(k, v))

    next_stat()
    # What are the counts of gender?
    res = gender(data, time_period, verbose=False)
    stat_time(start_time)
    print('Gender types and counts:')
    for k, v in sorted(res.items()):
        print('\t{}:  {:,}'.format(k, v))

    next_stat()
    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    res = birth_years(data, time_period, verbose=False)
    stat_time(start_time)
    print('The earliest (i.e., oldest) users were born in:  {}'.format(res[0]))
    print('The most recent (i.e., youngest) users were born in:  {}'.format(res[1]))
    print('The most popular year users were born in:  {}'.format(res[2]))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(data)

    return city, data


# Alternate time_period settings for testing:
# ----------------------------------------------------------------------------
# time_period=TimePeriodFilter(month_start=2, month_end=4)
# time_period = TimePeriodFilter(weekday_start=2, weekday_end=4)
# time_period = TimePeriodFilter(hour_start=1, hour_end=11)
# time_period = TimePeriodFilter(month_start=2, month_end=4, weekday_start=2,
#                                weekday_end=4, hour_start=1, hour_end=11)
# Default is no time_period filtering
def test(dataset: str='sample', time_period: TimePeriodFilter=TimePeriodFilter()) -> None:
    '''Basic test function to validate program.  Allows using sample data
       (generated from actual data using rndcsvsmpl.py) which loads and
       processes quickly or real data.

       Args:  dataset - use sample data or actual (prod) data
              time_period - Time period filter
       Returns:  None
    '''
    res: Any  # Allow multiple type assignment

    if dataset == 'sample':
        test_data = ['chicago-sample.csv', 'new_york_city-sample.csv',
                     'washington-sample.csv']
    elif dataset == 'prod':
        test_data = [CHI, NYC, WAS]
    else:
        sys.exit('Error:  Unexpected dataset "{}" - expecting "sample" or "prod".'.format(
                 dataset))

    for city in test_data:
        print('\nStatistics for {}\n{}'.format(city, time_period))
        data = load_city_file(city, verbose=True)

        res = popular_month(data, time_period, verbose=True)
        print('-->The most popular month is:  {}'.format(res))
        res = popular_day(data, time_period, verbose=True)
        print('-->The most popular day is:  {}'.format(res))
        res = popular_hour(data, time_period, verbose=True)
        print('-->The most popular hour is:  {}'.format(res))
        res = trip_duration(data, time_period, verbose=True)
        total_dur = time_str(res[0])
        avg_dur = time_str(res[1])
        print('-->The total trip duration is:  {}'.format(total_dur))
        print('-->The average trip duration is:  {}'.format(avg_dur))
        res = popular_stations(data, time_period, verbose=True)
        print('-->The most popular start stations is:  {}'.format(res[0]))
        print('-->The most popular end stations is:  {}'.format(res[1]))
        res = popular_trip(data, time_period, verbose=True)
        print('-->The most popular trip is:  {}'.format(res))
        res = users(data, time_period, verbose=True)
        print('-->User types and counts:')
        for k, v in sorted(res.items()):
            print('--->\t{}:  {:,}'.format(k, v))
        res = gender(data, time_period, verbose=True)
        print('-->Gender types and counts:')
        for k, v in sorted(res.items()):
            print('--->\t{}:  {:,}'.format(k, v))
        res = birth_years(data, time_period, verbose=True)
        print('-->The earliest (i.e., oldest) users were born in:  {}'.format(res[0]))
        print('-->The most recent (i.e., youngest) users were born in:  {}'.format(
                res[1]))
        print('-->The most popular year users were born in:  {}'.format(res[2]))

        print()
        display_data(data)


def main(args: List[str]) -> None:
    '''Entry point for direct script invocation.  Allows calling main statistics
       function or test function.

       Args:  arguments from command line invocation as collected by sys
       Returns:  None
    '''
    city = None
    data = None

    if len(args) == 1 or (len(args) == 2 and 'statistics'.startswith(args[1].lower())):
        city, data = statistics()
    elif 2 <= len(args) <= 4 and 'test'.startswith(args[1].lower()):
        if len(args) == 4:
            # This (eval) is horrible from a security point of view...  :-(
            time_period = eval(args[3])
            test(args[2], time_period)
        elif len(args) == 3:
            test(args[2])
        else:
            test()
    else:
        callname = os.path.basename(args[0])
        sys.exit('Usage:  {} [test | statistics]'.format(callname))

    # Restart?
    while True:
        restart = input('\nWould you like to restart (with statistics)?  Enter "Yes"'
                        ' or "No":\n')
        if 'yes'.startswith(restart.lower()):
            statistics(city, data)
        elif 'no'.startswith(restart.lower()):
            return
        else:
            print('\nPlease enter "Yes" or "No".')


if __name__ == '__main__':
    main(sys.argv)

