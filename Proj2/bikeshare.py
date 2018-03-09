#!/usr/bin/env python3.6-64
################################################################################
# Need 64-bit Python 3.6+ (may work with 3.5)
# With 32-bit Python will run out of memory
################################################################################


################################################################################
# To do:
#===============================================================================
# * Update functions to leverage time_period class
# * Update function/class docstrings
# * Update function/class type hints and check with mypy
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
            # In case a negative leading hour entered:
            try:
                hour_start, hour_end = hour.split('-')
            except ValueError:
                continue
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


def within_time(dtobj, time_period):
    # Month
    if ((time_period.month_start <= dtobj.month <= time_period.month_end) and
    # Day of Month
        (time_period.day_of_month_start <= dtobj.day <= time_period.day_of_month_end)
    # Week
        and (time_period.week_start <= dtobj.isocalendar()[1] <= time_period.week_end)
    # Weekday
        and (time_period.weekday_start <= dtobj.weekday() <= time_period.weekday_end)
    # Hour
            and (time_period.hour_start <= dtobj.hour <= time_period.hour_end)):
        return True


def dict_filter(d, filtval=0):
    return {k: v for k, v in d.items() if v != filtval}


def dict_keyfilter(d, filtval='Unknown'):
    return {k: v for k, v in d.items() if k != filtval}


def one_or_mult(d, tgt_val, periods=None):
    # Duplicates?
    if len([v for v in d.values() if v == tgt_val]) > 1:
        mult_res = []
        for k, v in d.items():
            if v == tgt_val:
                if periods:
                    mult_res.append(periods[k])
                else:
                    mult_res.append(k)
        return tuple(mult_res)
    else:
        for k, v in d.items():
            if v == tgt_val:
                if periods:
                    return periods[k]
                else:
                    return k


# Default to January (1) - June (6) as that's the range of data we have
def popular_month(city_data: List[str], time_period: TimePeriodFilter,
                  verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine month with highest number of start times within time_period.
       Answer question:  What is the most popular month for start time?

       Args:  All data from the city file (city_data),
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
        print('popular_month/results:  {}, max:  {}'.format(filt_res, month_val))

    return one_or_mult(filt_res, month_val, time_period.months)


# Default to Monday (0) - Sunday (6)
def popular_day(city_data: List[str], time_period: TimePeriodFilter,
                verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine day with highest number of start times within time_period.
       Answer question:  What is the most popular day of week (Monday, Tuesday, etc.)
                         for start time?

       Args:  All data from the city file (city_data),
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
        print('popular_day/final results:  {}, max:  {}'.format(filt_res, day_val))

    return one_or_mult(filt_res, day_val, time_period.weekdays)


# Default to 0 - 23
def popular_hour(city_data: List[str], time_period: TimePeriodFilter,
                 verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine hour with highest number of start times within time_period.
       Answer question:  What is the most popular hour of the day (0, 1, ..., 23)
                         for start time?

       Args:  All data from the city file (city_data),
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
        print('popular_hour/final results:  {}, max:  {}'.format(filt_res, hour_val))

    return one_or_mult(filt_res, hour_val, time_period.hours)


# Default time_period?
def trip_duration(city_data: List[str], time_period: TimePeriodFilter,
                 verbose: bool=False) -> Union[Tuple[str, ...], str]:
    '''Determine total trip duration and average trip duration during time_period.
       Answer question:  What is the total trip duration and average trip duration?
                         (default/reasonable time_period???)

       Args:  All data from the city file (city_data),
       Returns:  total trip duration, average trip duration or tuple of tuples in
                 case of tie(s)
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

    return res_total, res_avg


def popular_stations(city_data, time_period, verbose=False):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular start station and most popular end station?
    '''
    start_stas = {}
    end_stas = {}
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
        print('popular_stations/results - Start Stations Found:  {}, End Stations '
              'Found:  {}, Station Records in time period:  {},\n\tMost Popular '
              'Station Results:  {}\n\tRecorded {} and {} times respectively'.format(
                  len(start_stas), len(end_stas), sta_count, res, pop_start, pop_end))

    return res


def popular_trip(city_data, time_period, verbose=False):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular trip?
    Note:  Defining a trip as the same start/end station pair
    '''
    trips = {}
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            trip = '{} to {}'.format(row['Start Station'], row ['End Station'])

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
        print('popular_trip/results - Trips Found:  {}, Records in time period:  '
              '{},\n\tMost Popular Trip Result:  {} - Taken {} times'.format(
                  len(trips), count, res, pop_trip))

    return res


def users(city_data, time_period, verbose=False):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of each user type?
    '''
    user_types = {}
    count = 0

    # Count up data and tally by station
    for row in city_data:
        start = row['Start Time']
        if within_time(start, time_period):
            user_type = row['User Type']

            if user_type in user_types:
                user_types[user_type] += 1
            else:
                user_types[user_type] = 1
            count += 1

    # Max
    pop_user = max(user_types.values())
    res = one_or_mult(user_types, pop_user)

    # Optionally see results:
    if verbose:
        print('user/results - Users Found:  {}, Records in time period:  {}, '
              'User Types Found:  {}'.format(len(user_types), count, user_types))

    return res


def gender(city_data, time_period, verbose=False):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of gender?
    '''
    genders = {}
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
    res = one_or_mult(genders, pop_gender)

    # Optionally see results:
    if verbose:
        print('gender/results - Genders Found:  {}, Records in time period:  {}, '
              'Gender Types Found:  {}'.format(len(genders), count, genders))

    return res


def birth_years(city_data, time_period, verbose=False):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    '''
    yobs = {}  # Year of Births
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
    # .keys is the default but using to make it clear/explicit that this is what's
    # desired
    new_birthyr = max(filt_yobs.keys())
    res['Youngest'] = new_birthyr
    old_birthyr = min(filt_yobs.keys())
    res['Oldest'] = old_birthyr

    # Optionally see results:
    if verbose:
        print('birth_years/results - Number of Birth Years Found:  {}, Records in '
              'time period:  {}, Birth Years Found:  {}'.format(len(yobs), count, yobs))

    return res


def display_data(city_data, lines=5):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    swap_none = lambda seq: [i if i else 'None' for i in seq]
    swap_long = lambda longstr: longstr if len(longstr) <= 25 else longstr[:22] + '...'

    def view_data(lines=5):
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
    # for city in [CHI, NYC, WAS]:
    for city in ['chicago-sample.csv']:
        data = load_city_file(city, verbose=True)

        # time_period = get_time_period()
        time_period = TimePeriodFilter(month_start=2, month_end=4)
        print(popular_month(data, time_period, verbose=True))
        time_period = TimePeriodFilter(weekday_start=2, weekday_end=4)
        print(popular_day(data, time_period, verbose=True))
        time_period = TimePeriodFilter(hour_start=1, hour_end=11)
        print(popular_hour(data, time_period, verbose=True))
        print(trip_duration(data, time_period, verbose=True))
        print(popular_stations(data, time_period, verbose=True))
        print(popular_trip(data, time_period, verbose=True))
        print(users(data, time_period, verbose=True))
        print(gender(data, time_period, verbose=True))
        print(birth_years(data, time_period, verbose=True))
        print()
        display_data(data)


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

