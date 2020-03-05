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

import openmc

# test command
# pytest tests -v --cov=paramak --cov-report term --cov-report html:htmlcov --cov-report xml --junitxml=test-reports/junit.xml
# from head paramak directory

class test_mixed_material(unittest.TestCase):

        def density_from_mixed_material(self):
                pass

if __name__ == '__main__':
        unittest.main()

class test_object_properties(unittest.TestCase):


        def test_make_multimaterial_from_material_objects(self):
                # tests that a multimaterial can be created by passing Material objects into the MultiMaterial function

                test_material = MultiMaterial('test_material',
                                              materials = [
                                                  Material('Li4SiO4'),
                                                  Material('Be12Ti')
                                              ],
                                              fracs = [0.50, 0.50],
                                              percent_type = 'vo')

                assert isinstance(test_material, openmc.Material) == False
                assert isinstance(test_material.neutronics_material, openmc.Material) == True
                
        
        def test_make_multimaterial_from_neutronics_materials(self):
            # tests that a multimaterial can be created by passing neutronics materials into the MultiMaterial function

            test_material = MultiMaterial('test_material',
                                          materials = [
                                              Material('Li4SiO4').neutronics_material,
                                              Material('Be12Ti').neutronics_material
                                          ],
                                          fracs = [0.50, 0.50],
                                          percent_type = 'vo')

            assert isinstance(test_material, openmc.Material) == False
            assert isinstance(test_material.neutronics_material, openmc.Material) == True

        
        def test_multimaterial_attributes_from_material_objects_and_neutronics_materials(self):
            # tests that multimaterials made from material objects and neutronics materials have the same properties

            test_material_1 = MultiMaterial('test_material_1',
                                            materials = [
                                                Material('Li4SiO4'),
                                                Material('Be12Ti')
                                            ],
                                            fracs = [0.5, 0.5],
                                            percent_type = 'vo').neutronics_material

            test_material_2 = MultiMaterial('test_material_2',
                                            materials = [
                                                Material('Li4SiO4').neutronics_material,
                                                Material('Be12Ti').neutronics_material
                                            ],
                                            fracs = [0.5, 0.5],
                                            percent_type = 'vo').neutronics_material

            
            assert test_material_1.density == test_material_2.density
            assert test_material_1.nuclides == test_material_2.nuclides
            

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


        def test_density_of_mixed_two_packed_and_non_packed_crystals(self):

                test_material_1 = Material(material_name='Li4SiO4')
                test_material_1_packed = Material(material_name='Li4SiO4', packing_fraction=0.65)

                mixed_material = MultiMaterial(material_name = 'mixed_material',
                                               materials = [test_material_1, test_material_1_packed],
                                               fracs = [0.2, 0.8],
                                               percent_type = 'vo')

                assert mixed_material.neutronics_material.density == pytest.approx((test_material_1.neutronics_material.density * 0.2) + (test_material_1.neutronics_material.density * 0.65 * 0.8))


        def test_density_of_mixed_materials_from_density_equation(self):

                test_material = Material('H2O', temperature_in_C=25, pressure_in_Pa=100000)  
                test_mixed_material = MultiMaterial(material_name = 'test_mixed_material', materials= [test_material], fracs=[1])

                assert test_material.neutronics_material.density ==  test_mixed_material.neutronics_material.density


        def test_density_of_mixed_one_packed_crystal_and_one_non_crystal(self):

                test_material_1 = Material(material_name="H2O", temperature_in_C=25, pressure_in_Pa=100000)

                test_material_2 = Material(material_name="Li4SiO4")
                test_material_2_packed = Material(material_name="Li4SiO4", packing_fraction=0.65)

                mixed_packed_crystal_and_non_crystal = MultiMaterial(material_name = 'mixed_packed_crystal_and_non_crystal',
                                                                     materials = [test_material_1, test_material_2_packed],
                                                                     fracs = [0.5, 0.5],
                                                                     percent_type = 'vo')

                assert mixed_packed_crystal_and_non_crystal.neutronics_material.density == pytest.approx( (test_material_1.neutronics_material.density * 0.5) + (test_material_2.neutronics_material.density * 0.65 * 0.5) )


        def test_packing_fraction_for_single_materials(self):
            
            test_material_1 = Material('Li4SiO4').neutronics_material

            test_material_2 = Material('Li4SiO4', packing_fraction=1).neutronics_material

            assert test_material_1.density == test_material_2.density

            test_material_3 = Material('Li4SiO4', packing_fraction=0.5).neutronics_material

            assert test_material_3.density == pytest.approx(test_material_1.density * 0.5)

            test_material_4 = Material('Li4SiO4', packing_fraction=0.75).neutronics_material

            assert test_material_4.density == pytest.approx(test_material_1.density * 0.75)
            

        def test_packing_fraction_for_multimaterial_function(self):

            test_material_5 = MultiMaterial('test_material_5',
                                    materials = [
                                        Material('tungsten'),
                                        Material('eurofer'),
                                    ],
                                    fracs = [
                                        0.5, 
                                        0.5
                                    ]).neutronics_material

            test_material_6 = MultiMaterial('test_material_6',
                                    materials = [
                                        Material('tungsten', packing_fraction=1),
                                        Material('eurofer', packing_fraction=1)
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ]).neutronics_material

            assert test_material_5.density == test_material_6.density


            test_material_7 = MultiMaterial('test_material_7',
                                    materials = [
                                        Material('tungsten', packing_fraction=0.5),
                                        Material('eurofer', packing_fraction=0.5)
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ]).neutronics_material

            assert test_material_7.density == pytest.approx(test_material_5.density * 0.5)


        def test_packing_fraction_for_mix_materials_function(self):

            test_material_8 = openmc.Material.mix_materials(name='test_material_8',
                                    materials = [
                                        Material('tungsten').neutronics_material,
                                        Material('eurofer').neutronics_material
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ],
                                    percent_type = 'vo')

            test_material_9 = openmc.Material.mix_materials(name='test_material_9',
                                    materials = [
                                        Material('tungsten', packing_fraction=1).neutronics_material,
                                        Material('eurofer', packing_fraction=1).neutronics_material 
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ],
                                    percent_type = 'vo')

            assert test_material_8.density == test_material_9.density

            test_material_10 = openmc.Material.mix_materials(name='test_material_10',
                                    materials = [
                                        Material('tungsten', packing_fraction=0.5).neutronics_material,
                                        Material('eurofer', packing_fraction=0.5).neutronics_material 
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ],
                                    percent_type = 'vo')

            assert test_material_10.density == pytest.approx(test_material_8.density * 0.5)


        def test_multimaterial_vs_mix_materials(self):

            test_material_11 = MultiMaterial('test_material_11',
                                    materials = [
                                        Material('tungsten'),
                                        Material('eurofer')
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ]).neutronics_material

            test_material_12 = openmc.Material.mix_materials(name='test_material_12',
                                    materials = [
                                        Material('tungsten').neutronics_material,
                                        Material('eurofer').neutronics_material
                                    ],
                                    fracs = [
                                        0.5,
                                        0.5
                                    ],
                                    percent_type = 'vo')

            assert test_material_11.density == test_material_12.density

            test_material_13 = MultiMaterial('test_material_13',
                                    materials = [
                                        Material('tungsten', packing_fraction=0.6),
                                        Material('eurofer', packing_fraction=0.8)
                                    ],
                                    fracs = [
                                        0.3,
                                        0.7
                                    ]).neutronics_material

            test_material_14 = openmc.Material.mix_materials(name='test_material_14',
                                    materials = [
                                        Material('tungsten', packing_fraction=0.6).neutronics_material,
                                        Material('eurofer', packing_fraction=0.8).neutronics_material
                                    ],
                                    fracs = [
                                        0.3,
                                        0.7
                                    ],
                                    percent_type = 'vo')

            assert test_material_13.density == test_material_14.density



            
