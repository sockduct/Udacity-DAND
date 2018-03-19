#!/usr/bin/env python3

'''Various utility functions leveraged by bikeshare.  Should be useful
   elsewhere too.'''

# System Imports:
from datetime import timedelta
import sys
from typing import Any, Union

# Couldn't figure out how to make this work:
# Type representation for my TimePeriodFilter class (see timeperiod.py)
# TPF = TypeVar('TPF')

def dict_filter(d: dict, filtval: int=0) -> dict:
    '''Return new dict without keys that have value of `filtval`.'''
    return {k: v for k, v in d.items() if v != filtval}


def dict_keyfilter(d: dict, filtval: str='Unknown') -> dict:
    '''Return new dict without keys that are equal to `filtval`.'''
    return {k: v for k, v in d.items() if k != filtval}


# Generic[TPF] would result in not indexable error (Union[Generic[TPF], None])
def one_or_mult(d: dict, tgt_val: int, periods: Any=None) -> Union[str, tuple]:
    '''Check dict of int results for one or multiple keys with result `tgt_val`.
       For a single result, return the matching key.  For multiple (tying)
       results, return a tuple of the matching keys.'''
    # Duplicates?
    if len([v for v in d.values() if v == tgt_val]) > 1:
        mult_res = []
        for k, v in d.items():
            if v == tgt_val:
                if periods:
                    # I'm indexed here!
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

    sys.exit('Error: {} not found in any of the keys!'.format(tgt_val))


def time_str(timeobj: Union[timedelta, float, int]) -> str:
    '''Take a datetime.timedelta object or a float and convert it to a string
       of the form w days, x hours, y minutes, z seconds where variables with
       a value of 0 are omitted.'''
    timestr = ''

    if not isinstance(timeobj, timedelta):
        newtime = timedelta(seconds=timeobj)
    else:
        newtime = timeobj

    days = newtime.days
    # Integer seconds
    isecs = newtime.seconds
    msecs = newtime.microseconds / 1_000_000
    mins, isecs = divmod(isecs, 60)
    hours, mins = divmod(mins, 60)
    secs = isecs + msecs

    if days:
        if days == 1:
            timestr += '1 day, '
        else:
            timestr += '{:,} days, '.format(days)
    if hours:
        if hours == 1:
            timestr += '1 hour, '
        else:
            timestr += '{} hours, '.format(hours)
    if mins:
        if mins == 1:
            timestr += '1 minutes, '
        else:
            timestr += '{} minutes, '.format(mins)
    if timestr and not secs:
        # Removing trailing ', '
        timestr = timestr[:-2]
    else:
        if .996 <= secs <= 1.005:
            timestr += '1 second'
        else:
            timestr += '{:.2f} seconds'.format(secs)

    return timestr

