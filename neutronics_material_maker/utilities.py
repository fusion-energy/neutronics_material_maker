# -*- coding: utf-8 -*-
"""
Created on Thu May  3 20:38:10 2018

@author: matti
"""

import numpy as np
import unittest
# =============================================================================
# A collection of utility scripts
# =============================================================================

ABS_ZEROC = -273.15  # In Celsius
ABS_ZEROK = 0  # in Kelvin


def is_number(s):
    '''
    Determines if object type is a number
    Now catches True/False which return 1./0. when floated
    '''
    if s is True or s is False:
        return False
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
    elif isinstance(list_, np.ndarray):
        try:  # This catches the odd np.array(8) instead of np.array([8])
            len(list_)
            return(list_)
        except TypeError:
            return np.array([list_])
    elif is_number(list_):
        return np.array([list_])
    else:
        raise TypeError('Could not convert input type to list_array to a '
                        'np.array.')


def CtoK(T):
    if T is not None:
        T = list_array(T)
        if np.all(T >= ABS_ZEROC):
            return list_array(T)-ABS_ZEROC
        else:
            raise ValueError('Negative temperature in K specified.')


def KtoC(T):
    if T is not None:
        T = list_array(T)
        if np.all(T >= ABS_ZEROK):
            return T+ABS_ZEROC
        else:
            raise ValueError('Negative temperature in K specified.')


def kgm3togcm3(density):
    if density:
        return density/1000


def gcm3tokgm3(density):
    if density:
        return density*1000


def color_manager(color):
        if type(color) not in (tuple, list, np.ndarray) or len(color) != 3:
            raise ValueError("3-length RGB color tuple please. "
                             "Not: ".format(color))
        return ' rgb ' + ' '.join([str(i) for i in np.array(color).clip(0,
                                   255)])


class test_utilities(unittest.TestCase):

    def test_isnum(self):
        tests = [(0, True),
                 (10, True),
                 (10., True),
                 ('s', False),
                 ('1', True),
                 ('1234', True),
                 ('1234uy', False),
                 (False, False),
                 (True, False),
                 (np.pi, True),
                 (np.array([0]), True),
                 (np.array([0, 1, 2]), False)]
        for t in tests:
            self.assertIs(is_number(t[0]), t[1], msg=t)

    def test_listarray(self):
        passes = [0, [1], np.array([0]), np.array([1, 2, 3]), .3, 34, np.pi,
                  [1, 2], [1, 't'], np.array(['f'])]
        for p in passes:
            self.assertTrue(isinstance(list_array(p), np.ndarray))
            len(list_array(p))  # Implicit no raise error
        fails = ['t', True, False, None]
        for f in fails:
            with self.assertRaises(TypeError):
                list_array(f)

    def test_CtoK(self):
        self.assertEqual(CtoK(ABS_ZEROC), ABS_ZEROK)
        self.assertEqual(CtoK(300), 300-ABS_ZEROC)
        fails = [-1000, ABS_ZEROC-1]
        for f in fails:
            with self.assertRaises(ValueError):
                CtoK(f)
        self.assertEqual(CtoK(None), None)

    def test_KtoC(self):
        self.assertEqual(KtoC(ABS_ZEROK), ABS_ZEROC)
        self.assertEqual(KtoC(300), 300+ABS_ZEROC)
        fails = [-1000, ABS_ZEROK-1]
        for f in fails:
            with self.assertRaises(ValueError):
                KtoC(f)
        self.assertEqual(KtoC(None), None)

    def test_kgcm(self):
        self.assertEqual(kgm3togcm3(None), None)
        self.assertEqual(gcm3tokgm3(None), None)


if __name__ is '__main__':
    unittest.main()
