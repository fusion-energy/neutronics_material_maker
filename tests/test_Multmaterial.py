"""
This file is part of PARAMAK which is a design tool capable 
of creating 3D CAD models compatible with automated neutronics 
analysis.

PARAMAK is released under GNU General Public License v3.0. 
Go to https://github.com/Shimwell/paramak/blob/master/LICENSE 
for full license details.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Copyright (C) 2019  UKAEA

THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
"""

import pytest
import unittest

from paramak import Shape

# test command
# pytest tests -v --cov=paramak --cov-report term --cov-report html:htmlcov --cov-report xml --junitxml=test-reports/junit.xml
# from head paramak directory

class test_object_properties(unittest.TestCase):

        def test_shape_default_properties(self):

                test_shape = Shape()

                assert test_shape.points == None

        def test_correct_points(self):

                test_shape = Shape()

                test_shape.points = [
                        (0, 0, 200),
                        (200, 0, 100),
                        (0, 0, 0),
                        (0, 0, 200)
                ]

                assert test_shape.points[0] == test_shape.points[-1]


        def test_incorrect_points(self):

                test_shape = Shape()

                def incorrect_points_function():

                        test_shape.points = [
                                (0, 0, 200),
                                (200, 0, 100),
                                (0, 0, 0),
                                (0, 0, 50)
                        ]

                self.assertRaises(ValueError, incorrect_points_function)


if __name__ == '__main__':
        unittest.main()

