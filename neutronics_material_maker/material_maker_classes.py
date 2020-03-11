#!/usr/bin/env python3

"""
This file is part of Neutronics Material Maker which is a tool capable
of creating neutronics materials from a varity of input parameters.

Neutronics Material Maker is released under GNU General Public License v3.0.
Go to https://github.com/ukaea/neutronics_material_maker/blob/master/LICENSE
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

""" material_maker_classes.py: obtains the main classes as well as
material values such as density, chemical present etc ."""

__author__ = "Jonathan Shimwell"

import re
import json
import openmc
import math

from CoolProp.CoolProp import PropsSI

from .materials_fusion_breeders import material_dict


atomic_mass_unit_in_g = 1.660539040e-24

# percent_type = fraction type for the element as a whole
# enrichment_type = fraction type for the enrichment
# See To Do List for explanation on the current issues
# We may not want the functionality to override the percent_type specified in the dictionary because the material specifications are correct for that percent_type
# if we want to change the material significantly, we need to create a new material that is not populated from a dictionary and we have full control over percent_type etc.
# if this is the case, then this is basically done
# just need to take into account some flags such as explained below
# We need to also incorporate the 'enrichable' flag into our enrichment flow.
# This enrichable flag will be to do with the new method of enriching, i.e. will only be valid on two isotope elements, for now we will keep it just for Lithium

class Material:
    def __init__(
        self,
        material_name,
        packing_fraction=1.0,
        elements=None,
        isotopes=None,
        percent_type=None,
        density=None,
        density_equation=None,
        atoms_per_unit_cell=None,
        volume_of_unit_cell_cm3=None,
        density_unit=None,
        enrichment=None,
        enrichment_target=None,
        enrichment_type=None,
        temperature_in_C=None,
        temperature_in_K=None,
        pressure_in_Pa=None
    ):
        """Makes an OpenMC material object complete with isotopes and density 
        that vary with temperature, pressure and crystall stucture when appropiate. 
        Uses an internal database that contains fusion relevant materials

        Arguments:
            material_name {[type]} -- [description]

        Keyword Arguments:
            temperature_in_C {[type]} -- [description] (default: {None})
            temperature_in_K {[type]} -- [description] (default: {None})
            pressure_in_Pa {[type]} -- [description] (default: {None})
            enrichment_fraction {[type]} -- [description] (default: {None})
            packing_fraction {float} -- [description] (default: {1.0})
            elements {[type]} -- [description] (default: {None})
            isotopes {[type]} -- [description] (default: {None})
            density {[type]} -- [description] (default: {None})
            density_equation {[type]} -- [description] (default: {None})
            atoms_per_unit_cell {[type]} -- [description] (default: {None})
            volume_of_unit_cell_cm3 {[type]} -- [description] (default: {None})
            density_unit {str} -- [description] (default: {"g/cm3"})

        Raises:
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]

        Returns:
            [type] -- [description]
        """    

        self._material_name = material_name
        self._temperature_in_C = temperature_in_C
        self._temperature_in_K = temperature_in_K
        self._pressure_in_Pa = pressure_in_Pa
        self._packing_fraction = packing_fraction
        self._elements = elements
        self._isotopes = isotopes
        self._density = density
        self._density_equation = density_equation
        self._atoms_per_unit_cell = atoms_per_unit_cell
        self._volume_of_unit_cell_cm3 = volume_of_unit_cell_cm3
        self._density_unit = density_unit
        self._percent_type = percent_type
        self._enrichment = enrichment
        self._enrichment_target = enrichment_target
        self._enrichment_type = enrichment_type

        #derived values
        self.enrichment_element = None
        # self._enrichment_fraction = None
        self.density_packed = None

        self.neutronics_material = None
        self.list_of_fractions = None
        self.chemical_equation = None
        self.element_numbers = None
        self.element_symbols = None

        self.populate_from_dictionary()

 

        # checks that if we try to enrich a material by providing any of the arguments, that the other arguments are also provided
        if self.enrichment is not None:
            if self.enrichment_target == None or self.enrichment_type == None:
                raise ValueError('enrichment target and enrichment type are needed to enrich a material')

        if "temperature_dependant" in material_dict[self.material_name].keys():
            if temperature_in_K == None and temperature_in_C == None:
                if self.material_name == 'He':
                    raise ValueError("temperature_in_K or temperature_in_C is needed for", self.material_name, " Typical helium cooled blankets are 400C and 8e6Pa")
                elif self.material_name == 'H2O':
                    raise ValueError("temperature_in_K or temperature_in_C is needed for", self.material_name, " Typical water cooled blankets are 305C and 15.5e6Pa")
                raise ValueError("temperature_in_K or temperature_in_C is needed for", self.material_name)
            else:
                if temperature_in_K == None:
                    self.temperature_in_K = temperature_in_C + 273.15
                if temperature_in_C == None:
                    self.temperature_in_C = temperature_in_K + 273.15


        if "pressure_dependant" in material_dict[self.material_name].keys():
            if pressure_in_Pa == None:
                raise ValueError("pressure_in_Pa is needed for", self.material_name)


        self.make_material()


    @property
    def material_name(self):
        return self._material_name

    @material_name.setter
    def material_name(self, value):
        if type(value) is not str:
            raise ValueError("Material names must be a string")
        self._material_name = value


    @property
    def packing_fraction(self):
        return self._packing_fraction

    @packing_fraction.setter
    def packing_fraction(self, value):
        if type(value) is not float:
            raise ValueError("Material names must be a float")
        self._packing_fraction = value



    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = value




    @property
    def isotopes(self):
        return self._isotopes

    @isotopes.setter
    def isotopes(self, value):
        self._isotopes = value



    @property
    def density_equation(self):
        return self._density_equation

    @density_equation.setter
    def density_equation(self, value):
        self._density_equation = value


    @property
    def density_unit(self):
        return self._density_unit

    @density_unit.setter
    def density_unit(self, value):
        if value in ['g/cm3', 'g/cc', 'kg/m3', 'atom/b-cm', 'atom/cm3', None]:
            self._density_unit = value
        else:
            raise ValueError("only 'g/cm3', 'g/cc', 'kg/m3', 'atom/b-cm', 'atom/cm3' are supported for the density_units")

    @property
    def percent_type(self):
        return self._percent_type

    @percent_type.setter
    def percent_type(self, value):
        if value in ['ao', 'wo', None]:
            self._percent_type = value
        else:
            raise ValueError("only 'ao' and 'wo' are supported for the percent_type")

    @property
    def enrichment_type(self):
        return self._enrichment_type

    @enrichment_type.setter
    def enrichment_type(self, value):
        if value in ['ao', 'wo']:
            self._enrichment_type = value
        else:
            raise ValueError("only 'ao' and 'wo' are supported for the enrichment_type")



    @property
    def atoms_per_unit_cell(self):
        return self._atoms_per_unit_cell

    @atoms_per_unit_cell.setter
    def atoms_per_unit_cell(self, value):
        self._atoms_per_unit_cell = value



    @property
    def volume_of_unit_cell_cm3(self):
        return self._volume_of_unit_cell_cm3

    @volume_of_unit_cell_cm3.setter
    def volume_of_unit_cell_cm3(self, value):
        self._volume_of_unit_cell_cm3 = value




    @property
    def temperature_in_K(self):
        return self._temperature_in_K

    @temperature_in_K.setter
    def temperature_in_K(self, value):
        self._temperature_in_K = value



    @property
    def temperature_in_C(self):
        return self._temperature_in_C

    @temperature_in_C.setter
    def temperature_in_C(self, value):
        self._temperature_in_C = value



    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if value > 0:
            self._density = value
        else:
            raise ValueError("Density have been incorrectly set, density should be above 0")


    @property
    def enrichment(self):
        return self._enrichment

    @enrichment.setter
    def enrichment(self, value):
        if value is None:
            self._enrichment = value
        elif value < 0 or value > 100:
            raise ValueError("Enrichment must be between 0 and 100")
        else:
            self._enrichment = value


    @property
    def enrichment_target(self):
        return self._enrichment_target

    @enrichment_target.setter
    def enrichment_target(self, value):
        self._enrichment_target = value


    @property
    def pressure_in_Pa(self):
        return self._pressure_in_Pa

    @pressure_in_Pa.setter
    def pressure_in_Pa(self, value):
        self._pressure_in_Pa = value



    def populate_from_dictionary(self):

        if self.temperature_in_C is None and "temperature_in_C" in material_dict[self.material_name].keys():
            self.temperature_in_C = material_dict[self.material_name]["temperature_in_C"]

        if self.temperature_in_K is None and "temperature_in_K" in material_dict[self.material_name].keys():
            self.temperature_in_K = material_dict[self.material_name]["temperature_in_K"]

        if self.pressure_in_Pa is None and "pressure_in_Pa" in material_dict[self.material_name].keys():
            self.pressure_in_Pa = material_dict[self.material_name]["pressure_in_Pa"]

        if self.packing_fraction is None and "packing_fraction" in material_dict[self.material_name].keys():
            self.packing_fraction = material_dict[self.material_name]["packing_fraction"]

        if self.elements is None and "elements" in material_dict[self.material_name].keys():
            self.elements = material_dict[self.material_name]["elements"]

        if self.isotopes is None and "isotopes" in material_dict[self.material_name].keys():
            self.isotopes = material_dict[self.material_name]["isotopes"]

        if self.density is None and "density" in material_dict[self.material_name].keys():
            self.density = material_dict[self.material_name]["density"]

        if self.density_equation is None and "density_equation" in material_dict[self.material_name].keys():
            self.density_equation = material_dict[self.material_name]["density_equation"]

        if self.atoms_per_unit_cell is None and "atoms_per_unit_cell" in material_dict[self.material_name].keys():
            self.atoms_per_unit_cell = material_dict[self.material_name]["atoms_per_unit_cell"]

        if self.volume_of_unit_cell_cm3 is None and "volume_of_unit_cell_cm3" in material_dict[self.material_name].keys():
            self.volume_of_unit_cell_cm3 = material_dict[self.material_name]["volume_of_unit_cell_cm3"]

        if self.density_unit is None and "density_unit" in material_dict[self.material_name].keys():
            self.density_unit = material_dict[self.material_name]["density_unit"]

        if self.percent_type is None and "percent_type" in material_dict[self.material_name].keys():
            self.percent_type = material_dict[self.material_name]["percent_type"]

        if self.enrichment is None and "enrichment" in material_dict[self.material_name].keys():
            self.enrichment = material_dict[self.material_name]["enrichment"]

        if self.enrichment_target is None and "enrichment_target" in material_dict[self.material_name].keys():
            self.enrichment_target = material_dict[self.material_name]["enrichment_target"]

        if self.enrichment_type is None and "enrichment_type" in material_dict[self.material_name].keys():
            self.enrichment_type = material_dict[self.material_name]["enrichment_type"]

    def add_elements(self):

        if type(self.elements) == dict:
            self.element_numbers = self.elements.values()
            self.element_symbols = self.elements.keys()

        elif type(self.elements) == str:

            self.chemical_equation = self.elements

            self.element_numbers = self.get_element_numbers_normalized()
            self.element_symbols = self.get_elements_from_equation()

        if self.enrichment_target != None:
            enrichment_element = re.split('(\d+)',self.enrichment_target)[0]
        else:
            enrichment_element = None
        for element_symbol, element_number in zip(self.element_symbols, self.element_numbers):

            if element_symbol == enrichment_element:
                self.neutronics_material.add_element(element_symbol,
                                                        element_number,
                                                        percent_type=self.percent_type,
                                                        enrichment=self.enrichment,
                                                        enrichment_target=self.enrichment_target,
                                                        enrichment_type=self.enrichment_type)
            else:
                self.neutronics_material.add_element(
                    element_symbol, element_number, self.percent_type
                )

        # return element_symbols, element_numbers

    def add_isotopes(self):

        if "isotopes" in material_dict[self.material_name].keys():

            self.isotopes = material_dict[self.material_name]["isotopes"]

            self.isotope_numbers = self.isotopes.values()
            self.isotope_symbols = self.isotopes.keys()

            for isotope_symbol, isotope_number in zip(self.isotope_symbols, self.isotope_numbers):

                self.neutronics_material.add_nuclide(isotope_symbol, isotope_number, self.percent_type)


    def add_density(self):

        if type(self.density) == float:
            pass

        elif self.density == None and self.density_equation != None:


            temperature_in_K = self.temperature_in_K
            temperature_in_C = self.temperature_in_C
            pressure_in_Pa = self.pressure_in_Pa

            density = eval(self.density_equation)
            if density == None:
                raise ValueError("Density value of ", self.material_name, " can not be found")
            else:
                self.density = density

        elif self.atoms_per_unit_cell != None and self.volume_of_unit_cell_cm3 != None:

            self.atoms_per_unit_cell = material_dict[self.material_name]["atoms_per_unit_cell"]
            self.volume_of_unit_cell_cm3 = material_dict[self.material_name]["volume_of_unit_cell_cm3"]

            self.density = (self.get_crystal_molar_mass()
                            * atomic_mass_unit_in_g
                            * self.atoms_per_unit_cell
                            ) / self.volume_of_unit_cell_cm3
        else:

            raise ValueError(
                "density can't be set for " + str(self.material_name) +
                " provide either a density value, equation as a string, or atoms_per_unit_cell and volume_of_unit_cell_cm3",
            )

        self.neutronics_material.set_density(self.density_unit, self.density * self.packing_fraction)

        return self.neutronics_material

    def make_material(self):

        self.neutronics_material = openmc.Material(name=self.material_name)

        if self.isotopes is not None:

            self.add_isotopes()

        elif self.elements is not None:

            self.add_elements()

        self.add_density()

        # return self.neutronics_material

    def read_chemical_equation(self):
        return [a for a in re.split(r"([A-Z][a-z]*)", self.chemical_equation) if a]

    def get_elements_from_equation(self):
        chemical_equation_chopped_up = self.read_chemical_equation()
        list_elements = []

        for counter in range(0, len(chemical_equation_chopped_up)):
            if chemical_equation_chopped_up[counter].isalpha():
                element_symbol = chemical_equation_chopped_up[counter]
                list_elements.append(element_symbol)
        return list_elements

    def get_element_numbers_normalized(self):
        if self.list_of_fractions == None:
            self.get_element_numbers()
        norm_list_of_fractions = [
            float(i) / sum(self.list_of_fractions) for i in self.list_of_fractions
        ]
        return norm_list_of_fractions

    def get_element_numbers(self):
        chemical_equation_chopped_up = self.read_chemical_equation()
        list_of_fractions = []

        for counter in range(0, len(chemical_equation_chopped_up)):
            if chemical_equation_chopped_up[counter].isalpha():
                if counter == len(chemical_equation_chopped_up) - 1:
                    list_of_fractions.append(1.0)
                elif not (chemical_equation_chopped_up[counter + 1]).isalpha():
                    list_of_fractions.append(
                        float(chemical_equation_chopped_up[counter + 1])
                    )
                else:
                    list_of_fractions.append(1.0)
        self.list_of_fractions = list_of_fractions

    def get_atoms_in_crystal(self):
        self.get_element_numbers()
        atoms_in_crystal = sum(self.list_of_fractions)
        return atoms_in_crystal

    def get_crystal_molar_mass(self):
        molar_mass = (
            self.neutronics_material.average_molar_mass * self.get_atoms_in_crystal()
        )

        self.molar_mass = molar_mass
        return molar_mass

    def calculate_crystal_structure_density(self):
        density_g_per_cm3 = (
            self.get_crystal_molar_mass()
            * atomic_mass_unit_in_g
            * self.atoms_per_unit_cell
        ) / self.volume_of_unit_cell_cm3

        self.density = density_g_per_cm3


class MultiMaterial(list):
    def __init__(self, material_name, materials=[], fracs=[], percent_type='vo'):
        self.material_name = material_name
        self.materials = materials
        self.fracs = fracs
        self.percent_type = percent_type
        self.neutronics_material = None

        self.make_material()


    def make_material(self):

        if len(self.fracs) != len(self.materials):
            raise ValueError("There must be equal numbers of fracs and materials")

        openmc_material_objects = []
        for material in self.materials:
            if isinstance(material, openmc.Material) == True:
                openmc_material_objects.append(material)
            else:
                openmc_material_objects.append(material.neutronics_material)

        print(openmc_material_objects)

        self.neutronics_material = openmc.Material.mix_materials(name = self.material_name,
                                                                 materials = openmc_material_objects,
                                                                 fracs = self.fracs,
                                                                 percent_type = self.percent_type)

