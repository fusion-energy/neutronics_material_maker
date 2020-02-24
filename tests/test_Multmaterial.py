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

from neutronics_material_maker import Material, MultiMaterial

# test command
# pytest tests -v --cov=paramak --cov-report term --cov-report html:htmlcov --cov-report xml --junitxml=test-reports/junit.xml
# from head paramak directory

class test_mixed_material(unittest.TestCase):

        def density_from_mixed_material(self):
                pass

if __name__ == '__main__':
        unittest.main()

class test_object_properties(unittest.TestCase):

        def test_density_of_mixed_two_packed_crystals(self): 

                test_material_1 = Material(material_name="Li4SiO4")
                test_material_packed_1 = Material(material_name="Li4SiO4", packing_fraction=0.65)
                assert test_material_1.neutronics_material.density * 0.65 == test_material_packed_1.neutronics_material.density

                test_material_2 = Material(material_name="Be12Ti")
                test_material_packed_2 = Material(material_name="Be12Ti", packing_fraction=0.35)
                assert test_material_2.neutronics_material.density * 0.35 == test_material_packed_2.neutronics_material.density

                mixed_packed_crystals = MultiMaterial(material_name = 'mixed_packed_crystals',
                                                      materials = [test_material_packed_1, test_material_packed_2],
                                                      fracs = [0.75,0.25],
                                                      percent_type = 'vo')

                assert mixed_packed_crystals.neutronics_material.density == pytest.approx( (test_material_1.neutronics_material.density * 0.65 * 0.75) + (test_material_2.neutronics_material.density * 0.35 * 0.25), rel=0.01)

        def test_density_of_mixed_materials_from_density_equation(self):

                test_material = Material('H2O', temperature_in_C=25, pressure_in_Pa=100000)  
                test_mixed_material = MultiMaterial(material_name = 'test_mixed_material', materials= [test_material], fracs=[1])

                assert test_material.neutronics_material.density ==  test_mixed_material.neutronics_material.density

