#!/usr/bin/env python3


class TimePeriodFilter:
    '''Time period filter allowing restriction of starting and ending periods for
       months, days_of_month, weeks, weekdays, and hours of the data set.'''
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    rev_months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}

    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
            5: 'Saturday', 6: 'Sunday'}
    rev_weekdays = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4,
                'saturday': 5, 'sunday': 6}

    hours = {0: 'Midnight', 1: 'One AM', 2: 'Two AM', 3: 'Three AM', 4: 'Four AM',
             5: 'Five AM', 6: 'Six AM', 7: 'Seven AM', 8: 'Eight AM', 9: 'Nine AM',
             10: 'Ten AM', 11: 'Eleven AM', 12: 'Noon', 13: 'One PM', 14: 'Two PM',
             15: 'Three PM', 16: 'Four PM', 17: 'Five PM', 18: 'Six PM',
             19: 'Seven PM', 20: 'Eight PM', 21: 'Nine PM', 22: 'Ten PM',
             23: 'Eleven PM'}

    def __init__(self, month_start=1, month_end=6, day_of_month_start=1,
                 day_of_month_end=31, week_start=1, week_end=27, weekday_start=0,
                 weekday_end=6, hour_start=0, hour_end=23):
        self.month_start = month_start
        self.month_end = month_end
        self.day_of_month_start = day_of_month_start
        self.day_of_month_end = day_of_month_end
        self.week_start = week_start
        self.week_end = week_end
        self.weekday_start = weekday_start
        self.weekday_end = weekday_end
        self.hour_start = hour_start
        self.hour_end = hour_end

    def __repr__(self):
        return ('<TimePeriodFilter(month_start={}, month_end={}, day_of_month_start={},'
                ' day_of_month_end={}, week_start={}, week_end={}, weekday_start={}, '
                ' weekday_end={}, hour_start={}, hour_end={}'
                ')>'.format(self.month_start, self.month_end, self.day_of_month_start,
                            self.day_of_month_end, self.week_start, self.week_end,
                            self.weekday_start, self.weekday_end, self.hour_start,
                            self.hour_end))

    def __str__(self):
        month_str = TimePeriodFilter._strgen(self.month_start, self.month_end, 1, 6,
                                             TimePeriodFilter.months)
        day_of_month_str = TimePeriodFilter._strgen(self.day_of_month_start,
                                                    self.day_of_month_end, 1, 31)
        week_str = TimePeriodFilter._strgen(self.week_start, self.week_end, 1, 27)
        weekday_str = TimePeriodFilter._strgen(self.weekday_start, self.weekday_end,
                                               0, 6, TimePeriodFilter.weekdays)
        hour_str = TimePeriodFilter._strgen(self.hour_start, self.hour_end, 0, 23,
                                            TimePeriodFilter.hours)

        return ('Time Period Filter:\n\tmonths:  {}\t\tdays of month:  {}'
                '\n\tweeks:  {}\t\tweekdays:  {}\t\thours:  {}\n'.format(month_str,
                    day_of_month_str, week_str, weekday_str, hour_str))

    def _strgen(startval, endval, startmin, endmax, transtr=None):
        if startval == startmin and endval == endmax:
            valstr = 'All'
        elif startval == endval:
            if transtr:
                valstr = transtr[startval]
            else:
                valstr = str(startval)
        else:
            if transtr:
                valstr = '{} - {}'.format(transtr[startval], transtr[endval])
            else:
                valstr = '{} - {}'.format(startval, endval)

        return valstr

    def clear(self):
        '''Reset to defaults.'''
        self.__init__()


class TimePeriodResult:
    '''Collect results for various time periods - months, days_of_month, weeks,
       weekdays, hours.'''
    def __init__(self, months=None, days_of_month=None, weeks=None, weekdays=None,
                 hours=None):
        self.months = months if months else {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.days_of_month = days_of_month if days_of_month else {1: 0, 2: 0, 3: 0,
                                          4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                                          11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                                          17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0,
                                          23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0,
                                          29: 0, 30: 0, 31: 0}
        self.weeks = weeks if weeks else {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                                          8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                                          14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0,
                                          20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0,
                                          26: 0, 27: 0}
        self.weekdays = weekdays if weekdays else {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
                                                   5: 0, 6: 0}
        self.hours = hours if hours else {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                                          7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                                          13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
                                          19: 0, 20: 0, 21: 0, 22: 0, 23: 0}

    def __repr__(self):
        return ('<TimePeriodResult(\n\tmonths={},\n\tdays of month={}\n\tweeks={},'
                '\n\tweekdays={}\n\thours={})>'.format(self.months, self.days_of_month,
                                                self.weeks, self.weekdays, self.hours))

