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
    def test_serpent_multimaterial_type(self):

        for mat in nmm.AvailableMaterials().keys():
            print(mat)
            test_mat = nmm.Material(
                mat, temperature_in_K=300, pressure_in_Pa=5e6)

            assert isinstance(test_mat.openmc_material, openmc.Material)

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
