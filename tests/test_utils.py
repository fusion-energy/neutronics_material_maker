#!/usr/bin/env python3

__author__ = "neutronics material maker development team"


import json
import os
import unittest

import openmc

import neutronics_material_maker as nmm

if __name__ == "__main__":
    unittest.main()


class test_object_properties(unittest.TestCase):

    def test_additional_lines_multimaterial_mcnp(self):

        test_mat1 = nmm.Material.from_library(
            'Li4SiO4',
            additional_end_lines={'mcnp': ['mat1_additional']}
        )
        test_mat2 = nmm.Material.from_library(
            'Be12Ti',
            additional_end_lines={'mcnp': ['mat2_additional']}
        )

        test_mat3 = nmm.Material.from_mixture(
            name='mixed',
            materials=[test_mat1, test_mat2],
            temperature=500,
            fracs=[0.5, 0.5],
            material_id=3,
            volume_in_cm3=1,
            additional_end_lines={
                'mcnp': ['extra_mcnp_lin'],
                'serpent': ['extra_serpent_lin'],
                'fispact': ['extra_fispact_lin'],
                'shift': ['extra_shift_lin'],
            }
        )

        assert test_mat3.mcnp_material.split('\n')[-1] == 'extra_mcnp_lin'
        assert test_mat3.serpent_material.split(
            '\n')[-1] == 'extra_serpent_lin'
        assert test_mat3.fispact_material.split(
            '\n')[-1] == 'extra_fispact_lin'
        assert test_mat3.shift_material.split('\n')[-1] == 'extra_shift_lin'

    def test_additional_lines_mcnp(self):

        test_mat = nmm.Material.from_library(
            'H2O',
            pressure=1e6,
            temperature=393,
            material_id=1,
            additional_end_lines={'mcnp': ['        mt24 lwtr.01']}
        )
        assert test_mat.mcnp_material.split('\n')[-1] == '        mt24 lwtr.01'

    def test_additional_lines_shift(self):
        test_mat = nmm.Material.from_library(
            'H2O',
            pressure=1e6,
            temperature=393,
            material_id=1,
            additional_end_lines={'shift': ['coucou']}
        )
        assert test_mat.shift_material.split('\n')[-1] == 'coucou'

    def test_additional_lines_fispact(self):
        test_mat = nmm.Material.from_library(
            'H2O',
            pressure=1e6,
            temperature=393,
            material_id=1,
            volume_in_cm3=1,
            additional_end_lines={'fispact': ['coucou']}
        )
        assert test_mat.fispact_material.split('\n')[-1] == 'coucou'

    def test_additional_lines_serpent(self):
        test_mat = nmm.Material.from_library(
            'H2O',
            pressure=1e6,
            temperature=393,
            material_id=1,
            additional_end_lines={'serpent': ['coucou']}
        )
        assert test_mat.serpent_material.split('\n')[-1] == 'coucou'

    def test_additional_lines_from_json(self):
        """
        tests multiple additional lines are added to the mcnp material card
        """
        test_material_1 = {
            "mat_with_add_line": {
                "chemical_equation": "WC",
                "material_id": 2,
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
                "additional_end_lines": {'mcnp': ['coucou1', 'coucou2']}
            }
        }

        with open("extra_material_1.json", "w") as outfile:
            json.dump(test_material_1, outfile)

        nmm.AddMaterialFromFile("extra_material_1.json")

        test_mat = nmm.Material.from_library('mat_with_add_line')
        assert test_mat.mcnp_material.split('\n')[-2] == 'coucou1'
        assert test_mat.mcnp_material.split('\n')[-1] == 'coucou2'

    def test_incorrect_additional_lines_code_name(self):

        def incorrect_additional_lines_code_name():
            """Set additional_end_lines to not the name of a neutronics code
            which should raise an error"""

            nmm.Material.from_library(
                'Li4SiO4',
                additional_end_lines={'unknow code': ['coucou']}
            )

        self.assertRaises(
            ValueError,
            incorrect_additional_lines_code_name
        )

    def test_incorrect_additional_lines_code_value_type(self):

        def incorrect_additional_lines_code_value_type():
            """Set additional_end_lines value to a string
            which should raise an error"""

            nmm.Material.from_library(
                'Li4SiO4',
                additional_end_lines={'unknow code': 'serpent'}
            )

        self.assertRaises(
            ValueError,
            incorrect_additional_lines_code_value_type
        )

    def test_incorrect_additional_lines_code_value_list_type(self):

        def incorrect_additional_lines_code_value_list_type():
            """Set additional_end_lines value to a list of ints
            which should raise an error"""

            nmm.Material.from_library(
                'Li4SiO4',
                additional_end_lines={'unknow code': [1]}
            )

        self.assertRaises(
            ValueError,
            incorrect_additional_lines_code_value_list_type
        )

    def test_check_add_additional_end_lines_error_handeling(self):

        def incorrect_type_dict():
            """Set additional_end_lines value to a string which should raise an
            error"""

            nmm.utils.check_add_additional_end_lines('mcnp')

        self.assertRaises(
            ValueError,
            incorrect_type_dict
        )

        def incorrect_type_dict_value_empty():
            """Set additional_end_lines value to a string which should raise an
            error"""

            nmm.utils.check_add_additional_end_lines({'mcnp': 'random string'})

        self.assertRaises(
            ValueError,
            incorrect_type_dict_value_empty
        )

        def incorrect_type_dict_value():
            """Set additional_end_lines value to a list of ints which should
            raise an error"""

            nmm.utils.check_add_additional_end_lines({'mcnp': [1, 2, 3]})

        self.assertRaises(
            ValueError,
            incorrect_type_dict_value
        )

    def test_zaid_to_isotope(self):
        assert nmm.utils.zaid_to_isotope("3006") == "Li6"
        assert nmm.utils.zaid_to_isotope("03006") == "Li6"
        assert nmm.utils.zaid_to_isotope("003006") == "Li6"

        assert nmm.utils.zaid_to_isotope("8018") == "O18"
        assert nmm.utils.zaid_to_isotope("08018") == "O18"
        assert nmm.utils.zaid_to_isotope("008018") == "O18"

        assert nmm.utils.zaid_to_isotope("26056") == "Fe56"
        assert nmm.utils.zaid_to_isotope("026056") == "Fe56"
        assert nmm.utils.zaid_to_isotope("026056") == "Fe56"

        assert nmm.utils.zaid_to_isotope("092235") == "U235"
        assert nmm.utils.zaid_to_isotope("92235") == "U235"

    def test_isotope_to_zaid(self):
        assert nmm.utils.isotope_to_zaid("Li6") == "003006"

        assert nmm.utils.isotope_to_zaid("O18") == "008018"

        assert nmm.utils.isotope_to_zaid("Fe56") == "026056"

        assert nmm.utils.isotope_to_zaid("U235") == "092235"

    def test_entries_from_each_json_file_get_into_the_internal_dict(self):
        all_mats = nmm.AvailableMaterials().keys()

        assert "A-150 Tissue-Equivalent Plastic (A150TEP)" in all_mats
        assert "Zirconium Hydride (ZrH2)" in all_mats
        assert "Pb842Li158" in all_mats
        assert "FLiNaBe" in all_mats
        assert "WC" in all_mats
        assert "CuCrZr" in all_mats
        assert "DD_plasma" in all_mats
        assert "DT_plasma" in all_mats
        assert "Pb" in all_mats
        assert "Zr5Pb4" in all_mats
        assert "isotropic graphite HPG-59" in all_mats
        assert "Nb3Sn" in all_mats
        assert "ReBCO" in all_mats
        assert "He" in all_mats
        assert "xenon" in all_mats
        assert "Li4SiO4" in all_mats
        assert "Li2TiO3" in all_mats
        assert "Li" in all_mats
        assert "FLiNaK" in all_mats

    def test_number_of_materials_in_dict(self):
        import neutronics_material_maker as nmm_again

        assert len(nmm_again.AvailableMaterials().keys()) >= 418

    def test_dictionary_of_materials_makes_openmc_materials(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material.from_library(
                mat, temperature=300, pressure=5e6)

            assert isinstance(test_mat.openmc_material, openmc.Material)

    def test_dictionary_of_materials_makes_mcnp_materials(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material.from_library(
                mat, temperature=300, pressure=5e6, material_id=1
            )

            assert isinstance(test_mat.mcnp_material, str)

    def test_dictionary_of_materials_makes_shift_materials(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material.from_library(
                mat, temperature=300, pressure=5e6, material_id=1
            )

            assert isinstance(test_mat.shift_material, str)

    def test_dictionary_of_materials_makes_fispact_materials(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material.from_library(
                mat,
                temperature=300,
                pressure=5e6,
                volume_in_cm3=1.5)

            assert isinstance(test_mat.fispact_material, str)

    def test_dictionary_of_materials_makes_serpent_materials(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material.from_library(
                mat, temperature=300, pressure=5e6)

            assert isinstance(test_mat.serpent_material, str)

    def test_adding_one_material_AddMaterialFromFile(self):
        test_material_1 = {
            "WC2": {
                "chemical_equation": "WC",
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            }
        }

        with open("extra_material_1.json", "w") as outfile:
            json.dump(test_material_1, outfile)

        number_of_materials = len(nmm.AvailableMaterials())
        nmm.AddMaterialFromFile("extra_material_1.json")

        assert number_of_materials + 1 == len(nmm.AvailableMaterials())
        assert "WC2" in nmm.AvailableMaterials().keys()
        os.system("rm extra_material_1.json")

    def test_adding_two_material_AddMaterialFromFile(self):
        test_material_1 = {
            "WC3": {
                "chemical_equation": "WC",
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            },
            "WB2": {
                "chemical_equation": "WB",
                "density": 15.3,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            },
        }

        with open("extra_material_1.json", "w") as outfile:
            json.dump(test_material_1, outfile)

        number_of_materials = len(nmm.AvailableMaterials())
        nmm.AddMaterialFromFile("extra_material_1.json")

        assert number_of_materials + 2 == len(nmm.AvailableMaterials())
        assert "WC3" in nmm.AvailableMaterials().keys()
        assert "WB2" in nmm.AvailableMaterials().keys()
        os.system("rm extra_material_1.json")

    def test_replacing_material_using_AddMaterialFromFile(self):
        test_material_1 = {
            "Li4SiO4": {
                "chemical_equation": "WC",
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            }
        }

        with open("extra_material_1.json", "w") as outfile:
            json.dump(test_material_1, outfile)

        number_of_materials = len(nmm.AvailableMaterials())
        nmm.AddMaterialFromFile("extra_material_1.json")

        assert number_of_materials == len(nmm.AvailableMaterials())
        assert "Li4SiO4" in nmm.AvailableMaterials().keys()
        os.system("rm extra_material_1.json")

    def test_AddMaterialFromDir(self):
        os.system("mkdir new_materials")

        test_material_1 = {
            "Li4SiO42": {
                "chemical_equation": "WC",
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            }
        }

        with open(
            os.path.join("new_materials", "extra_material_1.json"), "w"
        ) as outfile:
            json.dump(test_material_1, outfile)

        test_material_2 = {
            "Li4SiO43": {
                "chemical_equation": "WC",
                "density": 18.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
            }
        }

        with open(
            os.path.join("new_materials", "extra_material_2.json"), "w"
        ) as outfile:
            json.dump(test_material_2, outfile)

        number_of_materials = len(nmm.AvailableMaterials())
        nmm.AddMaterialFromDir("new_materials")

        os.system("rm -rf new_materials")
        assert number_of_materials + 2 == len(nmm.AvailableMaterials())
        assert "Li4SiO42" in nmm.AvailableMaterials().keys()
        assert "Li4SiO43" in nmm.AvailableMaterials().keys()
