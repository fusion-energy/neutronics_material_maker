#!/usr/bin/env python3

__author__ = "neutronics material maker development team"


import unittest

import openmc
import pytest

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
