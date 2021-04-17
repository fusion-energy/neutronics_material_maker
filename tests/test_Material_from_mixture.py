#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import json
import unittest
import warnings

import neutronics_material_maker as nmm
import openmc
import pytest


class test_object_properties(unittest.TestCase):
    def test_serpent_from_mixture_type(self):

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.50,
                0.50],
            percent_type="vo",
        )

        assert len(test_material.serpent_material) > 100
        assert isinstance(test_material.serpent_material, str)

    def test_mcnp_from_mixture_type(self):

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.50,
                0.50],
            percent_type="vo",
            material_id=2,
        )

        assert len(test_material.mcnp_material) > 100
        assert isinstance(test_material.mcnp_material, str)

    def test_shift_from_mixture_type(self):

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.50,
                0.50],
            percent_type="vo",
            temperature=300,
            material_id=2,
        )

        assert len(test_material.shift_material) > 100
        assert isinstance(test_material.shift_material, str)

    def test_fispact_from_mixture_type(self):

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.50,
                0.50],
            percent_type="vo",
            volume_in_cm3=20,
        )

        assert len(test_material.fispact_material) > 100
        assert isinstance(test_material.fispact_material, str)

    def test_make_from_mixture_from_material_objects(self):
        # tests that a from_mixture can be created by passing Material objects
        # into the from_mixture function

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.50,
                0.50],
            percent_type="vo",
        )

        assert isinstance(test_material, openmc.Material) is False
        assert isinstance(test_material.openmc_material, openmc.Material)

    def test_make_from_mixture_from_openmc_materials(self):
        # tests that a from_mixture can be created by passing neutronics
        # materials into the from_mixture function

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("Li4SiO4").openmc_material,
                nmm.Material.from_library("Be12Ti").openmc_material,
            ],
            fracs=[0.50, 0.50],
            percent_type="vo",
        )

        assert isinstance(test_material, openmc.Material) is False
        assert isinstance(test_material.openmc_material, openmc.Material)

    def test_mutliname_setting(self):

        test_material = nmm.Material.from_mixture(
            materials=[
                nmm.Material.from_library('Pb842Li158', temperature=500),
                nmm.Material.from_library('SiC')
            ],
            fracs=[0.5, 0.5])

        assert test_material.name is None
        test_material.name = 'tag_set_after_creation'
        assert test_material.name == 'tag_set_after_creation'

        test_material.openmc_material
        assert test_material.openmc_material.name == 'tag_set_after_creation'

        test_material = nmm.Material.from_mixture(
            materials=[
                nmm.Material.from_library('Pb842Li158', temperature=500),
                nmm.Material.from_library('SiC')
            ],
            fracs=[0.5, 0.5],
            name='tag_set_on_creation')

        assert test_material.name == 'tag_set_on_creation'

        test_material.openmc_material
        assert test_material.openmc_material.name == 'tag_set_on_creation'

    def test_from_mixture_attributes_from_material_objects_and_openmc_materials(
            self):
        # tests that from_mixtures made from material objects and neutronics
        # materials have the same properties

        test_material_1 = nmm.Material.from_mixture(
            name="test_material_1",
            materials=[
                nmm.Material.from_library("Li4SiO4"),
                nmm.Material.from_library("Be12Ti")],
            fracs=[
                0.5,
                0.5],
            percent_type="vo",
        ).openmc_material

        test_material_2 = nmm.Material.from_mixture(
            name="test_material_2",
            materials=[
                nmm.Material.from_library("Li4SiO4").openmc_material,
                nmm.Material.from_library("Be12Ti").openmc_material,
            ],
            fracs=[0.5, 0.5],
            percent_type="vo",
        ).openmc_material

        assert test_material_1.density == test_material_2.density
        assert test_material_1.nuclides == test_material_2.nuclides

    def test_density_of_mixed_two_packed_crystals(self):

        test_material_1 = nmm.Material.from_library(name="Li4SiO4")
        test_material_packed_1 = nmm.Material.from_library(
            name="Li4SiO4", packing_fraction=0.65
        )
        assert (
            test_material_1.openmc_material.density * 0.65
            == test_material_packed_1.openmc_material.density
        )

        test_material_2 = nmm.Material.from_library(name="Be12Ti")
        test_material_packed_2 = nmm.Material.from_library(
            name="Be12Ti", packing_fraction=0.35
        )
        assert (
            test_material_2.openmc_material.density * 0.35
            == test_material_packed_2.openmc_material.density
        )

        mixed_packed_crystals = nmm.Material.from_mixture(
            name="mixed_packed_crystals",
            materials=[test_material_packed_1, test_material_packed_2],
            fracs=[0.75, 0.25],
            percent_type="vo",
        )

        assert mixed_packed_crystals.openmc_material.density == pytest.approx(
            (test_material_1.openmc_material.density * 0.65 * 0.75)
            + (test_material_2.openmc_material.density * 0.35 * 0.25),
            rel=0.01,
        )

    def test_density_of_mixed_two_packed_and_non_packed_crystals(self):

        test_material_1 = nmm.Material.from_library(name="Li4SiO4")
        test_material_1_packed = nmm.Material.from_library(
            name="Li4SiO4", packing_fraction=0.65
        )

        mixed_material = nmm.Material.from_mixture(
            name="mixed_material",
            materials=[test_material_1, test_material_1_packed],
            fracs=[0.2, 0.8],
            percent_type="vo",
        )

        assert mixed_material.openmc_material.density == pytest.approx(
            (test_material_1.openmc_material.density * 0.2)
            + (test_material_1.openmc_material.density * 0.65 * 0.8)
        )

    def test_density_of_mixed_materials_from_density(self):

        test_material = nmm.Material.from_library(
            "H2O", temperature=300, pressure=100000)
        test_mixed_material = nmm.Material.from_mixture(
            name="test_mixed_material",
            materials=[test_material],
            fracs=[1])

        assert test_material.openmc_material.density == pytest.approx(
            test_mixed_material.openmc_material.density
        )

    def test_density_of_mixed_one_packed_crystal_and_one_non_crystal(self):

        test_material_1 = nmm.Material.from_library(
            name="H2O", temperature=300, pressure=100000
        )

        test_material_2 = nmm.Material.from_library(name="Li4SiO4")
        test_material_2_packed = nmm.Material.from_library(
            name="Li4SiO4", packing_fraction=0.65
        )

        mixed_packed_crystal_and_non_crystal = nmm.Material.from_mixture(
            name="mixed_packed_crystal_and_non_crystal",
            materials=[test_material_1, test_material_2_packed],
            fracs=[0.5, 0.5],
            percent_type="vo",
        )

        assert (
            mixed_packed_crystal_and_non_crystal.openmc_material.density
            == pytest.approx(
                (test_material_1.openmc_material.density * 0.5)
                + (test_material_2.openmc_material.density * 0.65 * 0.5)
            )
        )

    def test_packing_fraction_for_single_materials(self):

        test_material_1 = nmm.Material.from_library("Li4SiO4").openmc_material

        test_material_2 = nmm.Material.from_library(
            "Li4SiO4", packing_fraction=1).openmc_material

        assert test_material_1.density == test_material_2.density

        test_material_3 = nmm.Material.from_library(
            "Li4SiO4", packing_fraction=0.5).openmc_material

        assert test_material_3.density == pytest.approx(
            test_material_1.density * 0.5)

        test_material_4 = nmm.Material.from_library(
            "Li4SiO4", packing_fraction=0.75).openmc_material

        assert test_material_4.density == pytest.approx(
            test_material_1.density * 0.75)

    def test_packing_fraction_for_from_mixture_function(self):

        test_material_5 = nmm.Material.from_mixture(
            name="test_material_5",
            materials=[
                nmm.Material.from_library("tungsten"),
                nmm.Material.from_library("eurofer")],
            fracs=[
                0.5,
                0.5],
        ).openmc_material

        test_material_6 = nmm.Material.from_mixture(
            name="test_material_6",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=1),
                nmm.Material.from_library("eurofer", packing_fraction=1),
            ],
            fracs=[0.5, 0.5],
        ).openmc_material

        assert test_material_5.density == test_material_6.density

        test_material_7 = nmm.Material.from_mixture(
            name="test_material_7",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.5),
                nmm.Material.from_library("eurofer", packing_fraction=0.5),
            ],
            fracs=[0.5, 0.5],
        ).openmc_material

        assert test_material_7.density == pytest.approx(
            test_material_5.density * 0.5)

    def test_packing_fraction_of_a_from_mixture(self):

        test_material_6 = nmm.Material.from_mixture(
            name="test_material_6",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.34),
                nmm.Material.from_library("eurofer", packing_fraction=0.60),
            ],
            fracs=[0.5, 0.5],
        ).openmc_material

        test_material_7 = nmm.Material.from_mixture(
            name="test_material_7",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.34),
                nmm.Material.from_library("eurofer", packing_fraction=0.60),
            ],
            fracs=[0.5, 0.5],
            packing_fraction=0.25,
        ).openmc_material

        assert test_material_6.get_mass_density() * 0.25 == pytest.approx(
            test_material_7.get_mass_density()
        )

    def test_packing_fraction_for_mix_materials_function(self):

        test_material_8 = openmc.Material.mix_materials(
            name="test_material_8",
            materials=[
                nmm.Material.from_library("tungsten").openmc_material,
                nmm.Material.from_library("eurofer").openmc_material,
            ],
            fracs=[0.5, 0.5],
            percent_type="vo",
        )

        test_material_9 = openmc.Material.mix_materials(
            name="test_material_9", materials=[
                nmm.Material.from_library(
                    "tungsten", packing_fraction=1).openmc_material, nmm.Material.from_library(
                    "eurofer", packing_fraction=1).openmc_material, ], fracs=[
                0.5, 0.5], percent_type="vo", )

        assert test_material_8.density == test_material_9.density

        test_material_10 = openmc.Material.mix_materials(
            name="test_material_10", materials=[
                nmm.Material.from_library(
                    "tungsten", packing_fraction=0.5).openmc_material, nmm.Material.from_library(
                    "eurofer", packing_fraction=0.5).openmc_material, ], fracs=[
                0.5, 0.5], percent_type="vo", )

        assert test_material_10.density == pytest.approx(
            test_material_8.density * 0.5)

    def test_from_mixture_vs_mix_materials(self):

        test_material_11 = nmm.Material.from_mixture(
            name="test_material_11",
            materials=[
                nmm.Material.from_library("tungsten"),
                nmm.Material.from_library("eurofer")],
            fracs=[
                0.5,
                0.5],
        ).openmc_material

        test_material_12 = openmc.Material.mix_materials(
            name="test_material_12",
            materials=[
                nmm.Material.from_library("tungsten").openmc_material,
                nmm.Material.from_library("eurofer").openmc_material,
            ],
            fracs=[0.5, 0.5],
            percent_type="vo",
        )

        assert pytest.approx(
            test_material_11.density) == test_material_12.density

        test_material_13 = nmm.Material.from_mixture(
            name="test_material_13",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.6),
                nmm.Material.from_library("eurofer", packing_fraction=0.8),
            ],
            fracs=[0.3, 0.7],
        ).openmc_material

        test_material_14 = openmc.Material.mix_materials(
            name="test_material_14", materials=[
                nmm.Material.from_library(
                    "tungsten", packing_fraction=0.6).openmc_material, nmm.Material.from_library(
                    "eurofer", packing_fraction=0.8).openmc_material, ], fracs=[
                0.3, 0.7], percent_type="vo", )

        assert pytest.approx(
            test_material_13.density) == test_material_14.density

    def test_json_dump_works(self):
        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.6),
                nmm.Material.from_library("eurofer", packing_fraction=0.8),
            ],
            fracs=[0.3, 0.7],
        )
        assert isinstance(json.dumps(test_material), str)

    def test_json_dump_contains_correct_keys(self):
        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.6),
                nmm.Material.from_library("eurofer", packing_fraction=0.8),
            ],
            fracs=[0.3, 0.7],
        )
        test_material_in_json_form = test_material.to_json()

        assert "test_material" in list(test_material_in_json_form.keys())
        assert "percent_type" in test_material_in_json_form["test_material"].keys(
        )
        assert "packing_fraction" in test_material_in_json_form["test_material"].keys(
        )

    def test_json_dump_contains_correct_values(self):
        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("tungsten", packing_fraction=0.6),
                nmm.Material.from_library("eurofer", packing_fraction=0.8),
            ],
            fracs=[0.3, 0.7],
        )
        test_material_in_json_form = test_material.to_json()

        assert list(test_material_in_json_form.keys()) == ["test_material"]
        assert test_material_in_json_form["test_material"]["percent_type"] == "ao"
        assert test_material_in_json_form["test_material"]["packing_fraction"] == 1.0

    def test_incorrect_settings(self):
        def too_large_fracs():
            """checks a ValueError is raised when the fracs are above 1"""

            nmm.Material.from_mixture(
                name="test_material", materials=[
                    nmm.Material.from_library(
                        "tungsten", packing_fraction=0.6), nmm.Material.from_library(
                        "eurofer", packing_fraction=0.8), ], fracs=[
                    0.3, 0.75], )

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            too_large_fracs()
            # Verify some things
            assert len(w) >= 1
            assert issubclass(w[-1].category, UserWarning)
            # the second entry is needed as OpenMC material mixer also raises
            # and error
            assert "warning sum of MutliMaterials.fracs do not sum to 1." in str(
                w[-2].message)

        def too_small_fracs():
            """checks a ValueError is raised when the fracs are above 1"""

            nmm.Material.from_mixture(
                name="test_material", materials=[
                    nmm.Material.from_library(
                        "tungsten", packing_fraction=0.6), nmm.Material.from_library(
                        "eurofer", packing_fraction=0.8), ], fracs=[
                    0.3, 0.65], )

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            too_small_fracs()
            # Verify some things
            assert len(w) >= 1
            assert issubclass(w[-1].category, UserWarning)
            # the second entry is needed as OpenMC material mixer also raises
            # and error
            assert "warning sum of MutliMaterials.fracs do not sum to 1." in str(
                w[-2].message)

        def test_incorrect_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            wrong type"""

            nmm.Material.from_mixture(
                name="test_material", materials=[
                    nmm.Material.from_library(
                        "tungsten", packing_fraction=0.6), nmm.Material.from_library(
                        "eurofer", packing_fraction=0.8), ], fracs=[
                    0.3, 0.7], packing_fraction="1")

        self.assertRaises(ValueError, test_incorrect_packing_fraction)

        def test_too_large_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            too large"""

            nmm.Material.from_mixture(
                name="test_material", materials=[
                    nmm.Material.from_library(
                        "tungsten", packing_fraction=0.6), nmm.Material.from_library(
                        "eurofer", packing_fraction=0.8), ], fracs=[
                    0.3, 0.7], packing_fraction=1.1)

        self.assertRaises(ValueError, test_too_large_packing_fraction)

        def test_too_small_packing_fraction():
            """checks a ValueError is raised when the packing_fraction is the
            too large"""

            nmm.Material.from_mixture(
                name="test_material", materials=[
                    nmm.Material.from_library(
                        "tungsten", packing_fraction=0.6), nmm.Material.from_library(
                        "eurofer", packing_fraction=0.8), ], fracs=[
                    0.3, 0.7], packing_fraction=-0.1)

        self.assertRaises(ValueError, test_too_small_packing_fraction)

    def test_temperature_from_C_in_from_mixtures(self):
        """checks that the temperature set in C ends up in the temperature
        attribute of the openmc from_mixtures"""

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("tungsten"),
                nmm.Material.from_library("eurofer"),
            ],
            fracs=[0.3, 0.7],
            temperature=283.15
        )

        assert test_material.temperature == 283.15
        assert test_material.openmc_material.temperature == 283.15

        line_by_line_material = test_material.serpent_material.split("\n")

        assert line_by_line_material[0].split()[-1] == "283.15"
        assert line_by_line_material[0].split()[-2] == "tmp"

    def test_temperature_from_K_in_from_mixtures(self):
        """checks that the temperature set in K ends up in the temperature
        attribute of the openmc from_mixtures"""

        test_material = nmm.Material.from_mixture(
            name="test_material",
            materials=[
                nmm.Material.from_library("tungsten"),
                nmm.Material.from_library("eurofer"),
            ],
            fracs=[0.3, 0.7],
            temperature=300
        )

        assert test_material.temperature == 300
        assert test_material.openmc_material.temperature == 300

        line_by_line_material = test_material.serpent_material.split("\n")

        assert line_by_line_material[0].split()[-1] == "300"
        assert line_by_line_material[0].split()[-2] == "tmp"


if __name__ == "__main__":
    unittest.main()
