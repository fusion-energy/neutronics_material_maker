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
import json

from neutronics_material_maker import Material


class test_object_properties(unittest.TestCase):
    def test_material_creation_from_chemical_formula(self):

        lead_fraction = 3
        lithium_fraction = 7

        lithium_lead_elements = "Li" + \
            str(lithium_fraction) + "Pb" + str(lead_fraction)
        test_material = Material(
            "lithium-lead",
            elements=lithium_lead_elements,
            temperature_in_C=450)
        nucs = test_material.openmc_material.nuclides
        pb_atom_count = 0
        li_atom_count = 0
        for entry in nucs:
            if entry[0].startswith("Pb"):
                pb_atom_count = pb_atom_count + entry[1]
            if entry[0].startswith("Li"):
                li_atom_count = li_atom_count + entry[1]
        assert pb_atom_count == lead_fraction
        assert li_atom_count == lithium_fraction

    def test_material_creation_from_chemical_formula_with_enrichment(self):

        lead_fraction = 3
        lithium_fraction = 7
        enrichment = 20

        lithium_lead_elements = "Li" + \
            str(lithium_fraction) + "Pb" + str(lead_fraction)
        test_material = Material(
            "lithium-lead",
            enrichment=enrichment,
            enrichment_target="Li6",
            enrichment_type="ao",
            elements=lithium_lead_elements,
            temperature_in_C=450,
        )
        nucs = test_material.openmc_material.nuclides
        pb_atom_count = 0
        li_atom_count = 0
        li6_atom_count = 0
        li7_atom_count = 0
        for entry in nucs:
            if entry[0].startswith("Pb"):
                pb_atom_count = pb_atom_count + entry[1]
            if entry[0].startswith("Li"):
                li_atom_count = li_atom_count + entry[1]
            if entry[0] == "Li6":
                li6_atom_count = li6_atom_count + entry[1]
            if entry[0] == "Li7":
                li7_atom_count = li7_atom_count + entry[1]
        print(nucs)
        assert pb_atom_count == lead_fraction
        assert li_atom_count == lithium_fraction
        # assert li6_atom_count*5. == li7_atom_count #todo use approximatly
        assert li6_atom_count == pytest.approx(
            enrichment * lithium_fraction / 100, rel=0.01
        )
        assert li7_atom_count == pytest.approx(
            (100.0 - enrichment) * lithium_fraction / 100, rel=0.01
        )

    def test_density_of_crystals(self):

        # these tests fail because the density value is too far away from calculated value
        # however, this could be becuase the density values are rounded to 2 dp

        test_material = Material(material_name="Li4SiO4")
        assert test_material.openmc_material.density == pytest.approx(
            2.32, rel=0.01)

        test_material = Material(material_name="Li2SiO3")
        assert test_material.openmc_material.density == pytest.approx(
            2.44, rel=0.01)

        test_material = Material(material_name="Li2ZrO3")
        assert test_material.openmc_material.density == pytest.approx(
            4.03, rel=0.01)

        test_material = Material(material_name="Li2TiO3")
        assert test_material.openmc_material.density == pytest.approx(
            3.34, rel=0.01)

        test_material = Material(material_name="Li8PbO6")
        assert test_material.openmc_material.density == pytest.approx(
            4.14, rel=0.01)

        test_material = Material(material_name="Be")
        assert test_material.openmc_material.density == pytest.approx(
            1.88, rel=0.01)

        test_material = Material(material_name="Be12Ti")
        assert test_material.openmc_material.density == pytest.approx(
            2.28, rel=0.01)

        test_material = Material(material_name="Ba5Pb3")
        assert test_material.openmc_material.density == pytest.approx(
            5.84, rel=0.01)

        test_material = Material(material_name="Nd5Pb4")
        assert test_material.openmc_material.density == pytest.approx(
            8.79, rel=0.01)

        test_material = Material(material_name="Zr5Pb3")
        assert test_material.openmc_material.density == pytest.approx(
            8.23, rel=0.01)

        # test_material = Material(material_name="Zr5Pb4")
        # assert test_material.openmc_material.density ==
        # pytest.approx(#insert)

        #  TODO extra checks for all the crystals needed here

    def test_density_of_enriched_crystals(self):

        test_material = Material(material_name="Li4SiO4")
        test_material_enriched = Material(
            material_name="Li4SiO4",
            enrichment=50.0,
            enrichment_target="Li6",
            enrichment_type="ao",
        )
        assert (
            test_material.openmc_material.density
            > test_material_enriched.openmc_material.density
        )

    def test_density_of_packed_crystals(self):

        test_material = Material(material_name="Li4SiO4")
        test_material_packed = Material(
            material_name="Li4SiO4", packing_fraction=0.35)
        assert (
            test_material.openmc_material.density * 0.35
            == test_material_packed.openmc_material.density
        )

    def test_material_creation_from_chemical_formula(self):

        lead_fraction = 3
        lithium_fraction = 7

        lithium_lead_elements = "Li" + \
            str(lithium_fraction) + "Pb" + str(lead_fraction)
        test_material = Material(
            "lithium-lead",
            elements=lithium_lead_elements,
            temperature_in_C=450)
        nucs = test_material.openmc_material.nuclides
        pb_atom_count = 0
        li_atom_count = 0
        for entry in nucs:
            if entry[0].startswith("Pb"):
                pb_atom_count = pb_atom_count + entry[1]
            if entry[0].startswith("Li"):
                li_atom_count = li_atom_count + entry[1]
        assert pb_atom_count == lead_fraction / \
            (lead_fraction + lithium_fraction)
        assert li_atom_count == lithium_fraction / \
            (lead_fraction + lithium_fraction)

    def test_material_creation_from_chemical_formula_with_enrichment(self):

        lead_fraction = 3
        lithium_fraction = 7
        enrichment = 20

        lithium_lead_elements = "Li" + \
            str(lithium_fraction) + "Pb" + str(lead_fraction)
        test_material = Material(
            "lithium-lead",
            enrichment=enrichment,
            enrichment_target="Li6",
            enrichment_type="ao",
            elements=lithium_lead_elements,
            temperature_in_C=450,
        )
        nucs = test_material.openmc_material.nuclides
        pb_atom_count = 0
        li_atom_count = 0
        li6_atom_count = 0
        li7_atom_count = 0
        for entry in nucs:
            if entry[0].startswith("Pb"):
                pb_atom_count = pb_atom_count + entry[1]
            if entry[0].startswith("Li"):
                li_atom_count = li_atom_count + entry[1]
            if entry[0] == "Li6":
                li6_atom_count = li6_atom_count + entry[1]
            if entry[0] == "Li7":
                li7_atom_count = li7_atom_count + entry[1]
        print(nucs)
        assert pb_atom_count == lead_fraction / \
            (lead_fraction + lithium_fraction)
        assert li_atom_count == lithium_fraction / \
            (lead_fraction + lithium_fraction)
        assert li6_atom_count * 4.0 == pytest.approx(li7_atom_count)

        assert li6_atom_count == pytest.approx(
            (enrichment / 100.0)
            * (lithium_fraction / (lead_fraction + lithium_fraction)),
            rel=0.01,
        )
        assert li7_atom_count == pytest.approx(
            ((100.0 - enrichment) / 100)
            * (lithium_fraction / (lead_fraction + lithium_fraction)),
            rel=0.01,
        )

    def test_incorrect_settings(self):
        def incorrect_temperature_in_K():
            """checks a ValueError is raised when the temperature_in_K is below 0"""

            Material("H2O", temperature_in_K=-10, pressure_in_Pa=1e6)

        self.assertRaises(ValueError, incorrect_temperature_in_K)

        def incorrect_temperature_in_C():
            """checks a ValueError is raised when the temperature_in_C is below absolute zero"""

            Material("H2O", temperature_in_C=-300, pressure_in_Pa=1e6)

        self.assertRaises(ValueError, incorrect_temperature_in_C)

        def incorrect_enrichment_target():
            """checks a ValueError is raised when the enrichment target is not a natural isotope"""

            Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li9",
                enrichment_type="ao",
            )

        self.assertRaises(ValueError, incorrect_enrichment_target)

        def incorrect_reference_type():
            """checks a ValueError is raised when the refernces is the wrong type"""

            Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                reference=1,
            )

        self.assertRaises(ValueError, incorrect_reference_type)

    def test_json_dump_works(self):
        test_material = Material(
            "H2O",
            temperature_in_C=100,
            pressure_in_Pa=1e6)
        assert isinstance(json.dumps(test_material), str)

    def test_json_dump_contains_correct_keys(self):
        test_material = Material(
            "H2O",
            temperature_in_C=100,
            pressure_in_Pa=1e6)
        test_material_in_json_form = test_material.to_json()

        assert "atoms_per_unit_cell" in test_material_in_json_form.keys()
        assert "density" in test_material_in_json_form.keys()
        assert "density_equation" in test_material_in_json_form.keys()
        assert "density_unit" in test_material_in_json_form.keys()
        assert "elements" in test_material_in_json_form.keys()
        assert "enrichment" in test_material_in_json_form.keys()
        assert "enrichment_target" in test_material_in_json_form.keys()
        assert "enrichment_type" in test_material_in_json_form.keys()
        assert "isotopes" in test_material_in_json_form.keys()
        assert "material_name" in test_material_in_json_form.keys()
        assert "material_tag" in test_material_in_json_form.keys()
        assert "packing_fraction" in test_material_in_json_form.keys()
        assert "percent_type" in test_material_in_json_form.keys()
        assert "pressure_in_Pa" in test_material_in_json_form.keys()
        assert "reference" in test_material_in_json_form.keys()
        assert "temperature_in_C" in test_material_in_json_form.keys()
        assert "temperature_in_K" in test_material_in_json_form.keys()
        assert "volume_of_unit_cell_cm3" in test_material_in_json_form.keys()

    def test_json_dump_contains_correct_values(self):
        test_material = Material(
            "H2O",
            temperature_in_C=100,
            pressure_in_Pa=1e6)
        test_material_in_json_form = test_material.to_json()

        assert test_material_in_json_form["pressure_in_Pa"] == 1e6
        assert test_material_in_json_form["temperature_in_C"] == 100
        assert test_material_in_json_form["material_name"] == "H2O"


if __name__ == "__main__":

    unittest.main()
