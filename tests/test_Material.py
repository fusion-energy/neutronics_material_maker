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

from neutronics_material_maker import Material


class test_object_properties(unittest.TestCase):

        def test_material_creation_from_chemical_formula(self):

                lead_fraction = 0.3
                lithium_fraction = 0.7

                lithium_lead_elements = 'Li'+str(lithium_fraction) +'Pb'+str(lead_fraction)
                test_material = Material('lithium-lead',
                                         elements=lithium_lead_elements,
                                         temperature_in_C=450)
                nucs = test_material.neutronics_material.nuclides
                pb_atom_count = 0
                li_atom_count = 0
                for entry in nucs:
                        if entry[0].startswith('Pb'):
                                pb_atom_count = pb_atom_count+ entry[1]
                        if entry[0].startswith('Li'):
                                li_atom_count = li_atom_count+ entry[1]
                assert pb_atom_count == lead_fraction
                assert li_atom_count == lithium_fraction

        def test_material_creation_from_chemical_formula_with_enrichment(self):

                lead_fraction = 0.3
                lithium_fraction = 0.7
                enrichment_fraction = 0.2

                lithium_lead_elements = 'Li'+str(lithium_fraction) +'Pb'+str(lead_fraction)
                test_material = Material('lithium-lead',
                                         enrichment_fraction=enrichment_fraction,
                                         elements=lithium_lead_elements,
                                         temperature_in_C=450)
                nucs = test_material.neutronics_material.nuclides
                pb_atom_count = 0
                li_atom_count = 0
                li6_atom_count = 0
                li7_atom_count = 0
                for entry in nucs:
                        if entry[0].startswith('Pb'):
                                pb_atom_count = pb_atom_count+ entry[1]
                        if entry[0].startswith('Li'):
                                li_atom_count = li_atom_count+ entry[1]
                        if entry[0] == 'Li6':
                                li6_atom_count = li6_atom_count+ entry[1]
                        if entry[0] == 'Li7':
                                li7_atom_count = li7_atom_count+ entry[1]
                print(nucs)
                assert pb_atom_count == lead_fraction
                assert li_atom_count == lithium_fraction
                # assert li6_atom_count*5. == li7_atom_count #todo use approximatly
                assert li6_atom_count == enrichment_fraction * lithium_fraction
                assert li7_atom_count == (1.-enrichment_fraction) * lithium_fraction

        def test_density_of_crystals(self):

                # these tests fail because the density value is too far away from calculated value
                # however, this could be becuase the density values are rounded to 2 dp

                test_material = Material(material_name="Li4SiO4")
                assert test_material.neutronics_material.density == pytest.approx(2.32)

                test_material = Material(material_name="Li2SiO3")
                assert test_material.neutronics_material.density == pytest.approx(2.44)

                test_material = Material(material_name="Li2ZrO3")
                assert test_material.neutronics_material.density == pytest.approx(4.03)

                test_material = Material(material_name="Li2TiO3")
                assert test_material.neutronics_material.density == pytest.approx(3.34)

                test_material = Material(material_name="Li8PbO6")
                assert test_material.neutronics_material.density == pytest.approx(4.14)

                test_material = Material(material_name="Be")
                assert test_material.neutronics_material.density == pytest.approx(1.88)

                test_material = Material(material_name="Be12Ti")
                assert test_material.neutronics_material.density == pytest.approx(2.28)

                test_material = Material(material_name="Ba5Pb3")
                assert test_material.neutronics_material.density == pytest.approx(5.84)

                test_material = Material(material_name="Nd5Pb4")
                assert test_material.neutronics_material.density == pytest.approx(8.79)

                test_material = Material(material_name="Zr5Pb3")
                assert test_material.neutronics_material.density == pytest.approx(8.23)

                # test_material = Material(material_name="Zr5Pb4")
                # assert test_material.neutronics_material.density == pytest.approx(#insert)

                #  TODO extra checks for all the crystals needed here

        def test_density_of_enriched_crystals(self): 

                test_material = Material(material_name="Li4SiO4")
                test_material_enriched = Material(material_name="Li4SiO4", enrichment_fraction=0.5)
                assert test_material.neutronics_material.density > test_material_enriched.neutronics_material.density



        def test_density_of_packed_crystals(self): 

                test_material = Material(material_name="Li4SiO4")
                test_material_packed = Material(material_name="Li4SiO4", packing_fraction=0.35)
                assert test_material.neutronics_material.density * 0.35 == test_material_packed.neutronics_material.density



if __name__ == '__main__':

        unittest.main()
