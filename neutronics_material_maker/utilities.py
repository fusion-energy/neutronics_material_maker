# -*- coding: utf-8 -*-
"""
Created on Thu May  3 20:38:10 2018

@author: matti
"""

import numpy as np
from scipy.interpolate import interp1d

# =============================================================================
# A collection of utility scripts
# =============================================================================


def is_number(s):
    '''
    Determines if object type is a number
    '''
    try:
        float(s)
        return True
    except (ValueError, TypeError) as e:
        return False


def arevaluesthesame(value1, value2, relative_tolerance):
    '''
    Use math.isclose algorithm, it is better than numpy.isclose method.
    See https://github.com/numpy/numpy/issues/10161 for more on the discussion
    Since some python version don't come with math.isclose we implement it here
    directly
    '''
    # TODO: allow absolute_tolerance as input
    # TODO: can we call this `isclose`?
    absolute_tolerance = 0.0
    return (abs(value1-value2) <= max(relative_tolerance*max(abs(value1),
                                                             abs(value2)),
                                      absolute_tolerance))


def list_array(list_):
    '''
    Always returns a numpy array
    Can handle int, float, list, np.ndarray
    '''
    if isinstance(list_, list):
        return np.array(list_)
    elif is_number(list_):
        return np.array([list_])
    elif isinstance(list_, np.ndarray):
        return list_


def value_array(value):
    if is_number(value):
        return value
    else:
        return list_array(value)


def CtoK(T):
    return list_array(T)+273.15


def KtoC(T):
    return list_array(T)-273.15


def interp_1D(t, prop, T):
    if is_number(T):
        return interp1d(t, prop)(T)[0]
    else:
        return interp1d(t, prop)(T)


def color_manager(color):
        if type(color) not in (tuple, list, np.ndarray) or len(color) != 3:
            raise ValueError("3-length RGB color tuple please. "
                             "Not: ".format(color))
        return ' rgb ' + ' '.join([str(i) for i in np.array(color).clip(0,
                                   255)])


if __name__ is '__main__':
    pass