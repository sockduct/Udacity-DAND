#!/usr/bin/env python3

# System Imports:
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

