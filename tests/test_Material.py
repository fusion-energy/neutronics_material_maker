#!/usr/bin/env python3

__author__ = "neutronics material maker development team"


import json
import os
import unittest

import pytest

import neutronics_material_maker as nmm


class test_object_properties(unittest.TestCase):
    def test_density_of_material_is_set_from_equation(self):
        test_mat = nmm.Material("FLiBe", temperature_in_K=80, pressure_in_Pa=1)
        assert test_mat.density is not None

    def test_density_of_material_is_set_from_crystal(self):
        test_mat = nmm.Material("Li4SiO4")
        assert test_mat.density is not None

    def test_density_of_material_is_set(self):
        test_mat = nmm.Material("eurofer")
        assert test_mat.density is not None

    def test_material_from_elements(self):
        test_mat = nmm.Material(
            material_name="test",
            elements={"Li": 0.4, "Zr": 0.6},
            percent_type="ao",
            density=1,
            density_unit="g/cm3",
        )
        test_mat.openmc_material
        assert "Li6" in test_mat.openmc_material.get_nuclides()
        assert "Li7" in test_mat.openmc_material.get_nuclides()

    def test_material_from_isotopes(self):
        test_mat = nmm.Material(
            material_name="test",
            isotopes={"Li6": 0.4, "Li7": 0.6},
            percent_type="ao",
            density=1,
            density_unit="g/cm3",
        )
        assert "Li6" in test_mat.openmc_material.get_nuclides()
        assert "Li7" in test_mat.openmc_material.get_nuclides()

    def test_material_from_zaid_int_isotopes(self):
        test_mat = nmm.Material(
            material_name="test",
            isotopes={3006: 0.4, 3007: 0.6},
            percent_type="ao",
            density=1,
            density_unit="g/cm3",
        )
        test_mat.openmc_material
        assert "Li6" in test_mat.openmc_material.get_nuclides()
        assert "Li7" in test_mat.openmc_material.get_nuclides()

    def test_material_from_zaid_str_isotopes(self):
        test_mat = nmm.Material(
            material_name="test",
            isotopes={"3006": 0.4, "3007": 0.6},
            percent_type="ao",
            density=1,
            density_unit="g/cm3",
        )
        test_mat.openmc_material
        assert "Li6" in test_mat.openmc_material.get_nuclides()
        assert "Li7" in test_mat.openmc_material.get_nuclides()

    def test_iron_density(self):
        a = nmm.Material("Iron")
        assert a.openmc_material.density == 7.874

        a = nmm.Material("Iron")
        serpent_density = a.serpent_material.split("\n")[0].split()[2]
        assert float(serpent_density) == pytest.approx(7.874)

        a = nmm.Material("Iron", material_id=45)
        mcnp_density = a.mcnp_material.split("\n")[0].split()[3]
        assert float(mcnp_density) == pytest.approx(7.874)

        a = nmm.Material("Iron", volume_in_cm3=100)
        fispact_density = a.fispact_material.split("\n")[0].split()[1]
        assert float(fispact_density) == pytest.approx(7.874)

    def test_fispact_material(self):
        a = nmm.Material("Li4SiO4", volume_in_cm3=1.0)
        line_by_line_material = a.fispact_material.split("\n")

        assert len(line_by_line_material) == 10
        assert a.fispact_material.split(
            "\n")[0].startswith("DENSITY 2.31899993235464")
        assert a.fispact_material.split("\n")[1] == "FUEL 8"
        assert "Li6 3.537400925715E+21" in line_by_line_material
        assert "Li7 4.307481314353E+22" in line_by_line_material
        assert "Si28 1.074757396925E+22" in line_by_line_material
        assert "Si29 5.457311411014E+20" in line_by_line_material
        assert "Si30 3.597484069651E+20" in line_by_line_material
        assert "O16 4.650130496709E+22" in line_by_line_material
        assert "O17 1.766602913225E+19" in line_by_line_material
        assert "O18 9.324307302413E+19" in line_by_line_material

    def test_fispact_material_with_volume(self):
        a = nmm.Material("Li4SiO4", volume_in_cm3=2.0)
        line_by_line_material = a.fispact_material.split("\n")

        assert len(line_by_line_material) == 10
        assert line_by_line_material[0].startswith("DENSITY 2.31899993235464")
        assert line_by_line_material[1] == "FUEL 8"
        assert "Li6 7.074801851431E+21" in line_by_line_material
        assert "Li7 8.614962628707E+22" in line_by_line_material
        assert "Si28 2.149514793849E+22" in line_by_line_material
        assert "Si29 1.091462282203E+21" in line_by_line_material
        assert "Si30 7.194968139301E+20" in line_by_line_material
        assert "O16 9.300260993419E+22" in line_by_line_material
        assert "O17 3.533205826449E+19" in line_by_line_material
        assert "O18 1.864861460483E+20" in line_by_line_material

    def test_mcnp_material_suffix(self):
        test_material1 = nmm.Material(
            "Nb3Sn", material_tag="Nb3Sn", zaid_suffix=".21c", material_id=27
        )
        mcnp_material1 = test_material1.mcnp_material
        test_material2 = nmm.Material(
            "Nb3Sn", material_tag="Nb3Sn", zaid_suffix=".30c", material_id=27
        )
        mcnp_material2 = test_material2.mcnp_material
        test_material3 = nmm.Material(
            "Nb3Sn", material_tag="Nb3Sn", material_id=27)
        mcnp_material3 = test_material3.mcnp_material

        assert len(mcnp_material3) < len(mcnp_material2)
        assert len(mcnp_material1) == len(mcnp_material2)
        assert mcnp_material1.count("21c") == mcnp_material2.count("30c")

    def test_mcnp_material_lines(self):
        test_material = nmm.Material(
            "Nb3Sn",
            material_tag="test",
            density=3,
            zaid_suffix=".30c",
            decimal_places=6,
            material_id=27,
        )
        line_by_line_material = test_material.mcnp_material.split("\n")

        assert len(line_by_line_material) == 12

        assert line_by_line_material[0].split()[0] == "c"
        assert line_by_line_material[0].split()[1] == "test"
        assert line_by_line_material[0].split()[2] == "density"
        assert float(line_by_line_material[0].split()[3]) == pytest.approx(3)
        assert line_by_line_material[0].split()[4] == "g/cm3"

        assert line_by_line_material[1] == "M27   041093.30c  7.500000e-01"

        assert "      050120.30c  8.145000e-02" in line_by_line_material
        assert "      050119.30c  2.147500e-02" in line_by_line_material
        assert "      050115.30c  8.500000e-04" in line_by_line_material
        assert "      050112.30c  2.425000e-03" in line_by_line_material
        assert "      050118.30c  6.055000e-02" in line_by_line_material
        assert "      050122.30c  1.157500e-02" in line_by_line_material
        assert "      050124.30c  1.447500e-02" in line_by_line_material
        assert "      050114.30c  1.650000e-03" in line_by_line_material
        assert "      050117.30c  1.920000e-02" in line_by_line_material
        assert "      050116.30c  3.635000e-02" in line_by_line_material

    def test_mcnp_material_lines_with_decimal_places(self):
        test_material = nmm.Material(
            "Nb3Sn",
            material_tag="test",
            density=3,
            zaid_suffix=".30c",
            material_id=27,
            decimal_places=3,
        )
        line_by_line_material = test_material.mcnp_material.split("\n")

        assert len(line_by_line_material) == 12

        assert line_by_line_material[0].split()[0] == "c"
        assert line_by_line_material[0].split()[1] == "test"
        assert line_by_line_material[0].split()[2] == "density"
        assert float(line_by_line_material[0].split()[3]) == pytest.approx(3)
        assert line_by_line_material[0].split()[4] == "g/cm3"

        assert line_by_line_material[1] == "M27   041093.30c  7.500e-01"

        assert "      050120.30c  8.145e-02" in line_by_line_material
        assert "      050119.30c  2.148e-02" in line_by_line_material  # rounded up
        assert "      050115.30c  8.500e-04" in line_by_line_material
        assert "      050112.30c  2.425e-03" in line_by_line_material
        assert "      050118.30c  6.055e-02" in line_by_line_material
        assert "      050122.30c  1.158e-02" in line_by_line_material  # rounded up
        assert "      050124.30c  1.448e-02" in line_by_line_material  # rounded up
        assert "      050114.30c  1.650e-03" in line_by_line_material
        assert "      050117.30c  1.920e-02" in line_by_line_material
        assert "      050116.30c  3.635e-02" in line_by_line_material

    def test_mcnp_material_lines_contain_underscore(self):
        test_material = nmm.Material(
            chemical_equation="Nb3Sn",
            material_tag="test2",
            density=3.2,
            density_unit="g/cm3",
            material_id=1,
            percent_type="wo",
        )
        line_by_line_material = test_material.mcnp_material.split("\n")

        assert len(line_by_line_material) == 12

        assert line_by_line_material[0].split()[0] == "c"
        assert line_by_line_material[0].split()[1] == "test2"
        assert line_by_line_material[0].split()[2] == "density"
        assert float(line_by_line_material[0].split()[3]) == pytest.approx(3.2)
        assert line_by_line_material[0].split()[4] == "g/cm3"

        assert "-" in line_by_line_material[1]
        assert "-" in line_by_line_material[2]
        assert "-" in line_by_line_material[3]
        assert "-" in line_by_line_material[4]
        assert "-" in line_by_line_material[5]
        assert "-" in line_by_line_material[6]
        assert "-" in line_by_line_material[7]
        assert "-" in line_by_line_material[8]
        assert "-" in line_by_line_material[9]
        assert "-" in line_by_line_material[10]
        assert "-" in line_by_line_material[11]

    def test_serpent_material_lines_contain_underscore(self):
        test_material = nmm.Material(
            chemical_equation="Nb3Sn",
            material_tag="test2",
            density=3.2,
            density_unit="g/cm3",
            material_id=1,
            percent_type="wo",
        )
        line_by_line_material = test_material.serpent_material.split("\n")

        assert len(line_by_line_material) == 12

        assert line_by_line_material[0].split()[0] == "mat"
        assert line_by_line_material[0].split()[1] == "test2"
        assert float(line_by_line_material[0].split()[2]) == pytest.approx(3.2)

        assert "-" in line_by_line_material[1]
        assert "-" in line_by_line_material[2]
        assert "-" in line_by_line_material[3]
        assert "-" in line_by_line_material[4]
        assert "-" in line_by_line_material[5]
        assert "-" in line_by_line_material[6]
        assert "-" in line_by_line_material[7]
        assert "-" in line_by_line_material[8]
        assert "-" in line_by_line_material[9]
        assert "-" in line_by_line_material[10]
        assert "-" in line_by_line_material[11]

    def test_serpent_material_suffix(self):
        test_material1 = nmm.Material(
            "Nb3Sn", material_tag="Nb3Sn", zaid_suffix=".21c")
        serpent_material1 = test_material1.serpent_material

        test_material2 = nmm.Material(
            "Nb3Sn", material_tag="Nb3Sn", zaid_suffix=".30c")
        serpent_material2 = test_material2.serpent_material

        test_material3 = nmm.Material("Nb3Sn", material_tag="Nb3Sn")
        serpent_material3 = test_material3.serpent_material

        assert len(serpent_material3) < len(serpent_material2)
        assert len(serpent_material1) == len(serpent_material2)
        assert serpent_material1.count("21c") == serpent_material2.count("30c")

    def test_serpent_material_lines(self):
        test_material = nmm.Material(
            "Nb3Sn", material_tag="test", density=3, zaid_suffix=".30c"
        )
        line_by_line_material = test_material.serpent_material.split("\n")

        assert len(line_by_line_material) == 12
        assert line_by_line_material[0].split()[0] == "mat"
        assert line_by_line_material[0].split()[1] == "test"
        assert float(line_by_line_material[0].split()[2]) == pytest.approx(3)
        assert "      041093.30c  7.50000000e-01" in line_by_line_material
        assert "      050120.30c  8.14500000e-02" in line_by_line_material
        assert "      050119.30c  2.14750000e-02" in line_by_line_material
        assert "      050115.30c  8.50000000e-04" in line_by_line_material
        assert "      050112.30c  2.42500000e-03" in line_by_line_material
        assert "      050118.30c  6.05500000e-02" in line_by_line_material
        assert "      050122.30c  1.15750000e-02" in line_by_line_material
        assert "      050124.30c  1.44750000e-02" in line_by_line_material
        assert "      050114.30c  1.65000000e-03" in line_by_line_material
        assert "      050117.30c  1.92000000e-02" in line_by_line_material
        assert "      050116.30c  3.63500000e-02" in line_by_line_material

    def test_serpent_material_lines_with_decimal_places(self):
        test_material = nmm.Material(
            "Nb3Sn",
            material_tag="test",
            density=3.3333,
            zaid_suffix=".30c",
            decimal_places=4,
        )
        line_by_line_material = test_material.serpent_material.split("\n")

        assert len(line_by_line_material) == 12
        assert line_by_line_material[0].split()[0] == "mat"
        assert line_by_line_material[0].split()[1] == "test"
        assert float(line_by_line_material[0].split()[
                     2]) == pytest.approx(3.3333)
        assert "      041093.30c  7.5000e-01" in line_by_line_material
        assert "      050120.30c  8.1450e-02" in line_by_line_material
        assert "      050119.30c  2.1475e-02" in line_by_line_material
        assert "      050115.30c  8.5000e-04" in line_by_line_material
        assert "      050112.30c  2.4250e-03" in line_by_line_material
        assert "      050118.30c  6.0550e-02" in line_by_line_material
        assert "      050122.30c  1.1575e-02" in line_by_line_material
        assert "      050124.30c  1.4475e-02" in line_by_line_material
        assert "      050114.30c  1.6500e-03" in line_by_line_material
        assert "      050117.30c  1.9200e-02" in line_by_line_material
        assert "      050116.30c  3.6350e-02" in line_by_line_material

    def test_material_creation_from_chemical_formula_with_enrichment(self):

        pb_fraction = 3
        li_fraction = 7
        enrichment = 20

        lithium_lead_elements = "Li" + \
            str(li_fraction) + "Pb" + str(pb_fraction)
        test_material = nmm.Material(
            "lithium-lead",
            enrichment=enrichment,
            enrichment_target="Li6",
            enrichment_type="ao",
            chemical_equation=lithium_lead_elements,
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
        assert pb_atom_count == pytest.approx(
            pb_fraction / (pb_fraction + li_fraction))
        assert li_atom_count == pytest.approx(
            li_fraction / (pb_fraction + li_fraction))
        assert li6_atom_count * 4.0 == pytest.approx(li7_atom_count)

        assert li6_atom_count == pytest.approx(
            (enrichment / 100.0) * (li_fraction / (pb_fraction + li_fraction)),
            rel=0.01,
        )
        assert li7_atom_count == pytest.approx(
            ((100.0 - enrichment) / 100) *
            (li_fraction / (pb_fraction + li_fraction)),
            rel=0.01,
        )

    def test_material_creation_from_chemical_formula_with_enrichment2(self):

        pb_fraction = 3
        li_fraction = 7
        enrichment = 20

        lithium_lead_elements = "Li" + \
            str(li_fraction) + "Pb" + str(pb_fraction)
        test_material = nmm.Material(
            "lithium-lead",
            enrichment=enrichment,
            enrichment_target="Li6",
            enrichment_type="ao",
            chemical_equation=lithium_lead_elements,
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
        assert pb_atom_count == pytest.approx(pb_fraction / 10)
        assert li_atom_count == pytest.approx(li_fraction / 10)
        # assert li6_atom_count*5. == li7_atom_count #todo use approximatly
        assert li6_atom_count == pytest.approx(
            enrichment * li_fraction / 1000, rel=0.01
        )
        assert li7_atom_count == pytest.approx(
            (100.0 - enrichment) * li_fraction / 1000, rel=0.01
        )

    def test_density_of_crystals(self):

        # these tests fail because the density value is too far away from calculated value
        # however, this could be becuase the density values are rounded to 2 dp

        test_mat = nmm.Material(material_name="Li4SiO4")
        assert test_mat.openmc_material.density == pytest.approx(
            2.32, rel=0.01)

        test_mat = nmm.Material(material_name="Li2SiO3")
        assert test_mat.openmc_material.density == pytest.approx(
            2.44, rel=0.01)

        test_mat = nmm.Material(material_name="Li2ZrO3")
        assert test_mat.openmc_material.density == pytest.approx(
            4.03, rel=0.01)

        test_mat = nmm.Material(material_name="Li2TiO3")
        assert test_mat.openmc_material.density == pytest.approx(
            3.34, rel=0.01)

        test_mat = nmm.Material(material_name="Li8PbO6")
        assert test_mat.openmc_material.density == pytest.approx(
            4.14, rel=0.01)

        test_mat = nmm.Material(material_name="Be")
        assert test_mat.openmc_material.density == pytest.approx(
            1.88, rel=0.01)

        test_mat = nmm.Material(material_name="Be12Ti")
        assert test_mat.openmc_material.density == pytest.approx(
            2.28, rel=0.01)

        test_mat = nmm.Material(material_name="Ba5Pb3")
        assert test_mat.openmc_material.density == pytest.approx(
            5.84, rel=0.01)

        test_mat = nmm.Material(material_name="Nd5Pb4")
        assert test_mat.openmc_material.density == pytest.approx(
            8.79, rel=0.01)

        test_mat = nmm.Material(material_name="Zr5Pb3")
        assert test_mat.openmc_material.density == pytest.approx(
            8.23, rel=0.01)

        #  TODO extra checks for all the crystals needed here

    def test_density_of_enriched_crystals(self):

        test_mat = nmm.Material(material_name="Li4SiO4")
        test_mat_enriched = nmm.Material(
            material_name="Li4SiO4",
            enrichment=50.0,
            enrichment_target="Li6",
            enrichment_type="ao",
        )
        assert (test_mat.openmc_material.density >
                test_mat_enriched.openmc_material.density)

    def test_density_of_packed_crystals(self):

        test_mat = nmm.Material(material_name="Li4SiO4")
        test_mat_packed = nmm.Material(
            material_name="Li4SiO4",
            packing_fraction=0.35)
        assert (
            test_mat.openmc_material.density * 0.35
            == test_mat_packed.openmc_material.density
        )

    def test_material_creation_from_chemical_formula(self):

        pb_fraction = 3
        li_fraction = 7

        lithium_lead_elements = "Li" + \
            str(li_fraction) + "Pb" + str(pb_fraction)
        test_material = nmm.Material(
            "lithium-lead",
            chemical_equation=lithium_lead_elements,
            temperature_in_C=450,
        )
        nucs = test_material.openmc_material.nuclides
        pb_atom_count = 0
        li_atom_count = 0
        for entry in nucs:
            if entry[0].startswith("Pb"):
                pb_atom_count = pb_atom_count + entry[1]
            if entry[0].startswith("Li"):
                li_atom_count = li_atom_count + entry[1]
        assert pb_atom_count == pytest.approx(
            pb_fraction / (pb_fraction + li_fraction))
        assert li_atom_count == pytest.approx(
            li_fraction / (pb_fraction + li_fraction))

    def test_incorrect_settings(self):

        def enrichment_too_high():
            """checks a ValueError is raised when enrichment is over 100"""

            nmm.Material("Li4SiO4", enrichment=200)

        self.assertRaises(ValueError, enrichment_too_high)

        def enrichment_too_low():
            """checks a ValueError is raised when enrichment is under 0"""

            nmm.Material("Li4SiO4", enrichment=-10)

        self.assertRaises(ValueError, enrichment_too_low)

        def incorrect_pressure_in_Pa():
            """checks a ValueError is raised when pressure_in_Pa is below 0"""

            nmm.Material("H2O", temperature_in_C=10, pressure_in_Pa=-1e6)

        self.assertRaises(ValueError, incorrect_pressure_in_Pa)

        def incorrect_temperature_in_K():
            """checks a ValueError is raised when temperature_in_K is below 0"""

            nmm.Material("H2O", temperature_in_K=-10, pressure_in_Pa=1e6)

        self.assertRaises(ValueError, incorrect_temperature_in_K)

        def incorrect_temperature_in_C():
            """checks a ValueError is raised when temperature_in_C is below absolute zero"""

            nmm.Material("H2O", temperature_in_C=-300, pressure_in_Pa=1e6)

        self.assertRaises(ValueError, incorrect_temperature_in_C)

        def incorrect_elements_chemical_equation_usage():
            """checks a ValueError is raised when the both chemical_equation and elements are used"""

            nmm.Material(
                material_name='my_mat',
                enrichment=50.0,
                chemical_equation="Li4SiO4",
                elements={'C': 0.3333, 'O': 0.666},
                enrichment_type="ao",
            )

        self.assertRaises(
            ValueError,
            incorrect_elements_chemical_equation_usage)

        def incorrect_enrichment_target():
            """checks a ValueError is raised when the enrichment target is not a natural isotope"""

            nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li9",
                enrichment_type="ao",
            )

        self.assertRaises(ValueError, incorrect_enrichment_target)

        def test_missing_temperature_He():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                material_name="He",
                pressure_in_Pa=1e6,
            )

        self.assertRaises(ValueError, test_missing_temperature_He)

        def test_missing_temperature_H2O():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                material_name="H2O",
                pressure_in_Pa=1e6,
            )

        self.assertRaises(ValueError, test_missing_temperature_H2O)

        def test_missing_temperature_CO2():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                material_name="CO2",
                pressure_in_Pa=1e6,
            )

        self.assertRaises(ValueError, test_missing_temperature_CO2)

        def test_incorrect_material_name_type():
            """checks a ValueError is raised when the temperature is not set"""

            test_material = nmm.Material("H2O",
                                         temperature_in_C=10,
                                         pressure_in_Pa=-1e6)
            test_material.material_name = 1

        self.assertRaises(ValueError, test_incorrect_material_name_type)

        def test_incorrect_density_unit_type():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                density=1.,
                density_unit='grams per cm3')

        self.assertRaises(ValueError, test_incorrect_density_unit_type)

        def test_incorrect_percent_type_type():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                density=1.,
                percent_type='weight percent')

        self.assertRaises(ValueError, test_incorrect_percent_type_type)

        def test_incorrect_enrichment_type_type():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                density=1.,
                enrichment_type='weight percent')

        self.assertRaises(ValueError, test_incorrect_enrichment_type_type)

        def test_incorrect_atoms_per_unit_cell():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                atoms_per_unit_cell=-1.)

        self.assertRaises(ValueError, test_incorrect_atoms_per_unit_cell)

        def test_incorrect_volume_of_unit_cell_cm3():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                volume_of_unit_cell_cm3=-1.)

        self.assertRaises(ValueError, test_incorrect_volume_of_unit_cell_cm3)

        def test_incorrect_temperature_in_c():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                temperature_in_C=-1000.)

        self.assertRaises(ValueError, test_incorrect_temperature_in_c)

        def test_incorrect_temperature_in_k():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                temperature_in_K=-1.)

        self.assertRaises(ValueError, test_incorrect_temperature_in_k)

        def test_incorrect_zaid_suffix_type():
            """checks a ValueError is raised when the temperature is not set"""

            nmm.Material(
                "eurofer",
                zaid_suffix=0.80)

        self.assertRaises(ValueError, test_incorrect_zaid_suffix_type)

        def test_incorrect_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            wrong type"""

            nmm.Material(
                "eurofer",
                packing_fraction="1"
            )

        self.assertRaises(ValueError, test_incorrect_packing_fraction)

        def test_too_large_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            too large"""

            nmm.Material(
                "eurofer",
                packing_fraction=1.1
            )

        self.assertRaises(ValueError, test_too_large_packing_fraction)

        def test_too_small_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            too large"""

            nmm.Material(
                "eurofer",
                packing_fraction=-0.1
            )

        self.assertRaises(ValueError, test_too_small_packing_fraction)

        def test_chemical_equation_wrong_type():
            """checks a ValueError is raised when the chemical_equation is the
            not a str"""

            nmm.Material(
                "eurofer",
                chemical_equation=-0.1
            )

        self.assertRaises(ValueError, test_chemical_equation_wrong_type)

        def test_enrichment_too_high():
            """checks a ValueError is raised when the enrichment is the
            too large"""

            nmm.Material(
                "Li4SiO4",
                enrichment=101,
                enrichment_target='Li6'
            )

        self.assertRaises(ValueError, test_enrichment_too_high)

        def test_enrichment_too_low():
            """checks a ValueError is raised when the enrichment is the
            too small"""

            nmm.Material(
                "Li4SiO4",
                enrichment=-1,
                enrichment_target='Li6'
            )

        self.assertRaises(ValueError, test_enrichment_too_low)

        def test_pressure_in_Pa_too_low():
            """checks a ValueError is raised when the pressure_in_Pa is the
            too small"""

            nmm.Material(
                "Li4SiO4",
                pressure_in_Pa=-1
            )

        self.assertRaises(ValueError, test_pressure_in_Pa_too_low)

        def test_reference_wrong_type():
            """checks a ValueError is raised when the reference is the
            not a string"""

            nmm.Material(
                "Li4SiO4",
                reference=-1
            )

        self.assertRaises(ValueError, test_reference_wrong_type)

        def test_material_id_wrong_type():
            """checks a ValueError is raised when the material_id is the
            not an int"""

            nmm.Material(
                "Li4SiO4",
                material_id='one'
            )

        self.assertRaises(ValueError, test_material_id_wrong_type)

        # TODO get this working
        # def no_enrichment_target():
        #     """checks a ValueError is raised when the enrichment target is set to none"""

        #     nmm.Material(
        #         material_name="my_mat",
        #         chemical_equation="Li4SiO",
        #         enrichment=50.0,
        #         enrichment_target=None,
        #         enrichment_type=None,
        #     )
        # self.assertRaises(ValueError, no_enrichment_target)

        def incorrect_reference_type():
            """checks a ValueError is raised when the reference is an int"""

            nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                reference=1,
            )

        self.assertRaises(ValueError, incorrect_reference_type)

        def incorrect_setting_for_id():
            """checks a ValueError is raised when the id is not set
            and an mcnp material card is need"""

            test_material = nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                material_id=1.0,
            )

            test_material.mcnp_material

        self.assertRaises(ValueError, incorrect_setting_for_id)

        def incorrect_setting_for_id2():
            """checks a ValueError is raised when the id is set as a str
            and an mcnp material card is need"""

            test_material = nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                material_id="1.0",
            )

            test_material.mcnp_material

        self.assertRaises(ValueError, incorrect_setting_for_id2)

        def incorrect_setting_for_volume_in_cm3_1():
            """checks a ValueError is raised when the volume_in_cm3 is set to a string"""

            test_material = nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                volume_in_cm3="1.0",
            )

            test_material.fispact_material

        self.assertRaises(ValueError, incorrect_setting_for_volume_in_cm3_1)

        def incorrect_setting_for_volume_in_cm3_2():
            """checks a ValueError is raised when the id is not set
            and an mcnp material card is need"""

            test_material = nmm.Material(
                material_name="Li4SiO4",
                enrichment=50.0,
                enrichment_target="Li6",
                enrichment_type="ao",
                material_id=None,
            )

            test_material.fispact_material

        self.assertRaises(ValueError, incorrect_setting_for_volume_in_cm3_2)

    def test_setting_for_volume_int(self):
        """checks the volume_in_cm3 is set to an int"""

        nmm.Material(
            material_name="Li4SiO4",
            enrichment=50.0,
            enrichment_target="Li6",
            enrichment_type="ao",
            volume_in_cm3=1,
        )

    def test_setting_for_volume_float(self):
        """checks the volume_in_cm3 is set to an float"""

        nmm.Material(
            material_name="Li4SiO4",
            enrichment=50.0,
            enrichment_target="Li6",
            enrichment_type="ao",
            volume_in_cm3=1.1,
        )

    def test_json_dump_works(self):
        test_material = nmm.Material(
            "H2O", temperature_in_C=100, pressure_in_Pa=1e6)
        assert isinstance(json.dumps(test_material), str)

    def test_json_dump_contains_correct_keys(self):
        test_material = nmm.Material(
            "H2O", temperature_in_C=100, pressure_in_Pa=1e6)
        test_material_in_json_form = test_material.to_json()

        assert "atoms_per_unit_cell" in test_material_in_json_form.keys()
        assert "density" in test_material_in_json_form.keys()
        assert "density_equation" in test_material_in_json_form.keys()
        assert "density_unit" in test_material_in_json_form.keys()
        assert "chemical_equation" in test_material_in_json_form.keys()
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
        test_material = nmm.Material(
            "H2O", temperature_in_C=100, pressure_in_Pa=1e6)
        test_material_in_json_form = test_material.to_json()

        assert test_material_in_json_form["pressure_in_Pa"] == 1e6
        assert test_material_in_json_form["temperature_in_C"] == 100
        assert test_material_in_json_form["material_name"] == "H2O"

    def test_temperature_from_C_in_materials(self):
        """checks that the temperature set in C ends up in the temperature
        attribute of the openmc materials"""

        test_material = nmm.Material(
            'H2O',
            temperature_in_C=10,
            pressure_in_Pa=15.5e6
        )

        assert test_material.temperature_in_K == 283.15
        assert test_material.temperature_in_C == 10
        assert test_material.openmc_material.temperature == 283.15

        line_by_line_material = test_material.serpent_material.split("\n")

        assert line_by_line_material[0].split()[-1] == "283.15"
        assert line_by_line_material[0].split()[-2] == "tmp"

    def test_temperature_from_K_in_materials(self):
        """checks that the temperature set in K ends up in the temperature
        attribute of the openmc materials"""

        test_material = nmm.Material(
            'H2O',
            temperature_in_K=300,
            pressure_in_Pa=15.5e6
        )

        assert test_material.temperature_in_K == 300
        assert test_material.temperature_in_C == pytest.approx(26.85)
        assert test_material.openmc_material.temperature == 300

        line_by_line_material = test_material.serpent_material.split("\n")

        assert line_by_line_material[0].split()[-1] == "300"
        assert line_by_line_material[0].split()[-2] == "tmp"

    def test_temperature_not_in_materials(self):
        """checks that the temperature set in K ends up in the temperature
        attribute of the openmc materials"""

        test_material = nmm.Material('WC')
        assert test_material.openmc_material.temperature is None

        line_by_line_material = test_material.serpent_material.split("\n")

        assert line_by_line_material[0].split()[-1] != "300"
        assert line_by_line_material[0].split()[-2] != "tmp"

    @staticmethod
    def test_restricted_eval():
        """Test that arbitrary commands cannot be injected."""
        with pytest.raises(NameError):
            nmm.Material(
                "BadMaterial",
                temperature_in_C=100,
                pressure_in_Pa=1e6,
                density_equation="os.system('ls')"
            )


if __name__ == "__main__":

    unittest.main()
