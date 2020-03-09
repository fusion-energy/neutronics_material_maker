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

material_dict = {
    "He": {
        "elements": {"He": 1.0},
        #"density_equation": 'Chemical("He", T=temperature_in_K, P=pressure_in_Pa).rho',
        "density_equation": "PropsSI('D', 'T', temperature_in_K, 'P', pressure_in_Pa, 'Helium')",
        "density_unit": "kg/m3",
        "reference": "CoolProp python package for density equation",
        "temperature_dependant": True,
        "pressure_dependant": True,
        # "percent_type": "ao"
    },
    "DT_plasma": {
        "isotopes": {"H2": 0.5, "H3": 0.5,},
        "density": 0.000001,
        "density_unit": "g/cm3",  # is this a case to support other units?
        # "percent_type": "ao"
    },
    "WC": {"elements": "WC",
           "density": 18.0,
           "density_unit": "g/cm3",
        #    "percent_type": "ao"
          },
    "H2O": {"elements": "H2O",
            # "density_equation": 'Chemical("H2O", T=temperature_in_K, P=pressure_in_Pa).rho',
            "density_equation": "PropsSI('D', 'T', temperature_in_K, 'P', pressure_in_Pa, 'Water')",
            "density_unit": "kg/m3",
            "reference": "CoolProp python package",
            "temperature_dependant": True,
            "pressure_dependant": True,
            # "percent_type": "ao"
           },
    "D2O": {
        "isotopes": {"H2": 2.0,
                     "O16": 0.99757+0.00205,
                     "O17": 0.00038,
                    #  "O18": 0.00205, #removed till mixed crosssections.xml files are avaialbe in openmc
                    },
        "density": 1.1,  # could be calculated using presure and temp
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "Nb3Sn": {"elements": "Nb3Sn",
              "density": 8.69,
              "density_unit": "g/cm3",
            #   "percent_type": "ao"
             },
    "Pb84.2Li15.8": {
        "elements": "Pb84.2Li15.8",
        "density_equation": "99.90*(0.1-16.8e-6*temperature_in_C)",
        "density_unit": "g/cm3",
        "reference": "density equation valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html",
        "temperature_dependant": True,
        "enrichable": True,
        # "percent_type": "ao"
    },
    "lithium-lead": {  # check whether this works because doesn't seem to be any elements
        "density_equation": "99.90*(0.1-16.8e-6*temperature_in_C)",
        "density_unit": "g/cm3",
        "reference": "density equation valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html",
        "temperature_dependant": True,
        # "percent_type": "ao"
    },
    "Li": {
        "elements": "Li",
        "density_equation": "0.515 - 1.01e-4 * (temperature_in_C - 200)",
        "density_unit": "g/cm3",
        "reference": "http://aries.ucsd.edu/LIB/PROPS/PANOS/li.html",
        "temperature_dependant": True,
        # "percent_type": "ao"
    },
    "F2Li2BeF2": {
        "elements": "F2Li2BeF2",
        "density_equation": "2.214 - 4.2e-4 * temperature_in_C",
        "density_unit": "g/cm3",
        "reference": "source http://aries.ucsd.edu/LIB/MEETINGS/0103-TRANSMUT/gohar/Gohar-present.pdf",
        "temperature_dependant": True,
        # "percent_type": "ao"
    },
    "Li4SiO4": {
        "elements": "Li4SiO4",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.17162883501e-21,  # could be replaced by a space group
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1188336 https://materialsproject.org/materials/mp-11737/",
        # "percent_type": "ao"
    },
    "Li2SiO3": {
        "elements": "Li2SiO3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.12255616623e-21,
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1208560 https://materialsproject.org/materials/mp-5012/",
        # "percent_type": "ao"
    },
    "Li2ZrO3": {
        "elements": "Li2ZrO3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.12610426777e-21,
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1207897 https://materialsproject.org/materials/mp-4156/",
        # "percent_type": "ao"
    },
    "Li2TiO3": {
        "elements": "Li2TiO3",
        "atoms_per_unit_cell": 4,
        "volume_of_unit_cell_cm3": 0.21849596020e-21,
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1203676 https://materialsproject.org/materials/mp-2931/",
        # "percent_type": "ao"
    },
    "Li8PbO6": {
        "elements": "Li8PbO6",
        "atoms_per_unit_cell": 1,
        "volume_of_unit_cell_cm3": 0.14400485967e-21,
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1198772 https://materialsproject.org/materials/mp-22538/",
        # "percent_type": "ao"
    },
    "Pb": {
        "elements": "Pb",
        "density": "10.678 - 13.174e-4 * (temperature_in_K-600.6)",
        "density_unit": "g/cm3",
        "reference": "https://www.sciencedirect.com/science/article/abs/pii/0022190261802261",
        # "percent_type": "ao"
    },
    "Be": {
        "elements": "Be",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.01587959994e-21,
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1312591 https://materialsproject.org/materials/mp-87/",
        # "percent_type": "ao"
    },
    "Be12Ti": {
        "elements": "Be12Ti",
        "atoms_per_unit_cell": 1,
        "volume_of_unit_cell_cm3": 0.11350517285e-21,
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1187703 https://materialsproject.org/materials/mp-11280/",
        # "percent_type": "ao"
    },
    "Ba5Pb3": {
        "elements": "Ba5Pb3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.74343377212e-21,
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1278091 https://materialsproject.org/materials/mp-622106/",
        # "percent_type": "ao"
    },
    "Nd5Pb4": {
        "elements": "Nd5Pb4",
        "atoms_per_unit_cell": 4,
        "volume_of_unit_cell_cm3": 1.17174024048e-21,
        "enrichable": False,
        "packable": True,
        "reference": "https://materialsproject.org/materials/mp-1204902/",
        # "percent_type": "ao"
    },
    "Zr5Pb3": {
        "elements": "Zr5Pb3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.43511266920e-21,
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1283750 https://materialsproject.org/materials/mp-681992/",
        # "percent_type": "ao"
    },
    "Zr5Pb4": {   # Not updated, no entry in materials project
        "elements": "Zr5Pb4",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.40435e-21,
        # "percent_type": "ao"
    },
    "SiC": {
        "elements": "SiC",
        "density": 3.,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "eurofer": {
        "elements": {
            "Fe": 0.88821,
            "B": 1e-05,
            "C": 0.00105,
            "N": 0.0004,
            "O": 1e-05,
            "Al": 4e-05,
            "Si": 0.00026,
            "P": 2e-05,
            "S": 3e-05,
            "Ti": 1e-05,
            "V": 0.002,
            "Cr": 0.09,
            "Mn": 0.0055,
            "Co": 5e-05,
            "Ni": 0.0001,
            "Cu": 3e-05,
            "Nb": 5e-05,
            "Mo": 3e-05,
            "Ta": 0.0012,
            "W": 0.011,
        },
        "element units": "atom fraction",
        "density": 7.78,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        # "percent_type": "ao"
    },
    "SS_316L_N_IG": {
        "elements": {
            "Fe": 62.973,
            "C": 0.030,
            "Mn": 2.00,
            "Si": 0.50,
            "P": 0.03,
            "S": 0.015,
            "Cr": 18.00,
            "Ni": 12.50,
            "Mo": 2.70,
            "N": 0.080,
            "B": 0.002,
            "Cu": 1.0,
            "Co": 0.05,
            "Nb": 0.01,
            "Ti": 0.10,
            "Ta": 0.01,
        },
        "element units": "atom fraction",
        "density": 7.93,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        # "percent_type": "ao"
    },
    "tungsten": {
        "elements": {
            "W": 0.999595,
            "Ag": 1e-05,
            "Al": 1.5e-05,
            "As": 5e-06,
            "Ba": 5e-06,
            "Ca": 5e-06,
            "Cd": 5e-06,
            "Co": 1e-05,
            "Cr": 2e-05,
            "Cu": 1e-05,
            "Fe": 3e-05,
            "K": 1e-05,
            "Mg": 5e-06,
            "Mn": 5e-06,
            "Na": 1e-05,
            "Nb": 1e-05,
            "Ni": 5e-06,
            "Pb": 5e-06,
            "Ta": 2e-05,
            "Ti": 5e-06,
            "Zn": 5e-06,
            "Zr": 5e-06,
            "Mo": 1e-04,
            "C": 3e-05,
            "H": 5e-06,
            "N": 5e-06,
            "O": 2e-05,
            "P": 2e-05,
            "S": 5e-06,
            "Si": 2e-05,
        },
        "element units": "atom fraction",
        "density": 19.0,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        # "percent_type": "ao"
    },
    "CuCrZr": {
        "elements": {
            "Cu": 0.9871,
            "Cr": 0.0075,
            "Zr": 0.0011,
            "Co": 0.0005,
            "Ta": 0.0001,
            "Nb": 0.001,
            "B": 1e-05,
            "O": 0.00032,
            "Mg": 0.0004,
            "Al": 3e-05,
            "Si": 0.0004,
            "P": 0.00014,
            "S": 4e-05,
            "Mn": 2e-05,
            "Fe": 0.0002,
            "Ni": 0.0006,
            "Zn": 0.0001,
            "As": 0.0001,
            "Sn": 0.0001,
            "Sb": 0.00011,
            "Pb": 0.0001,
            "Bi": 3e-05,
        },
        "element units": "atom fraction",
        "density": 8.9,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        # "percent_type": "ao"
    },
    "copper": {
        "elements": {"Cu": 1.0},
        "element units": "atom fraction",
        "density": 8.5,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SS347": {
        "elements": {
            "Fe": 67.42,
            "Cr": 18,
            "Ni": 10.5,
            "Nb": 1,
            "Mn": 2,
            "Si": 1,
            "C": 0.08,
        },
        "element units": "atom fraction",
        "density": 7.92,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SS321": {
        "elements": {
            "Fe": 67.72,
            "Cr": 18,
            "Ni": 10.5,
            "Ti": 0.7,
            "Mn": 2,
            "Si": 1,
            "C": 0.08,
        },
        "element units": "atom fraction",
        "density": 7.92,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SS316": {
        "elements": {
            "Fe": 67, 
            "Cr": 17, 
            "Ni": 14, 
            "Mo": 2
        },
        "element units": "atom fraction",
        "density": 7.97,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SS304": {
        "elements": {
            "Fe": 68.82,
            "Cr": 19,
            "Ni": 9.25,
            "Mn": 2,
            "Si": 0.75,
            "N": 0.1,
            "C": 0.08,
        },
        "element units": "atom fraction",
        "density": 7.96,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "P91": {
        "elements": {
            "Fe": 89, 
            "Cr": 9.1, 
            "Mo": 1, 
            "Mn": 0.5, 
            "Si": 0.4
        },
        "element units": "atom fraction",
        "density": 7.96,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SS316L": {
        "elements": {
            "C": 0.001384,
            "Si": 0.019722,
            "P": 0.000805,
            "S": 0.000518,
            "Cr": 0.181098,
            "Mn": 0.020165,
            "Fe": 0.648628,
            "Ni": 0.113247,
            "Mo": 0.014434
        },
        "element units": "atom fraction",
        "density": 8.00,
        "density_unit": "g/cm3",
        # "percent_type": "wo"
    },
    "ReBCO": {
        "elements": {
            "Y": 1.00,
            "Ba": 2.00,
            "Cu": 3.00,
            "O": 7.00
        },
        "element units": "atom fraction",
        "density": 6.3,
        "density_unit": "g/cm3",
        # "percent_type": "ao"
    },
    "SST91": {
        "elements": {
            "C": 0.10,
            "Mn": 0.45,
            "P": 0.02,
            "S": 0.01,
            "Si": 0.35,
            "Cr": 8.75,
            "Mo": 0.95,
            "V": 0.215,
            "N": 0.05,
            "Ni": 0.4,
            "Al": 0.04,
            "Nb": 0.08,
            "Fe": 88.585
        },
        "density": 7.77,
        "density_unit": "g/cm3",
        # "percent_type": "wo"
    }
}


class Material:
    def __init__(
        self,
        material_name,
        temperature_in_C=None,
        temperature_in_K=None,
        pressure_in_Pa=None,
        # enrichment_fraction=None,
        packing_fraction=1.0,
        volume_fraction=1.0,
        elements=None,
        isotopes=None,
        density=None,
        density_equation=None,
        atoms_per_unit_cell=None,
        volume_of_unit_cell_cm3=None,
        density_list=None,
        density_unit="g/cm3",
        percent_type=None,
        enrichment=None,
        enrichment_target=None,
        enrichment_type=None
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
            volume_fraction {float} -- [description] (default: {1.0})
            elements {[type]} -- [description] (default: {None})
            isotopes {[type]} -- [description] (default: {None})
            density {[type]} -- [description] (default: {None})
            density_equation {[type]} -- [description] (default: {None})
            atoms_per_unit_cell {[type]} -- [description] (default: {None})
            volume_of_unit_cell_cm3 {[type]} -- [description] (default: {None})
            density_list {[type]} -- [description] (default: {None})
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
        self.material_name = material_name
        self.temperature_in_C = temperature_in_C
        self.temperature_in_K = temperature_in_K
        self.pressure_in_Pa = pressure_in_Pa
        # self.enrichment_fraction = enrichment_fraction
        # self.enriched_isotope = "Li6"
        self.packing_fraction = packing_fraction
        self.volume_fraction = volume_fraction
        self.elements = elements
        self.isotopes = isotopes
        self.density = density
        self.density_value = None
        self.density_equation = density_equation
        self.atoms_per_unit_cell = atoms_per_unit_cell
        self.volume_of_unit_cell_cm3 = volume_of_unit_cell_cm3
        self.density_unit = density_unit
        self.density_list = density_list
        self.neutronics_material = None
        self.percent_type = percent_type
        self.enrichment = enrichment
        self._enrichment_target = enrichment_target
        self.enrichment_type = enrichment_type
        self.enrichment_element = None


        self.list_of_fractions = None
        self.chemical_equation = None

        self.populate_from_dictionary()

        # at the moment, we can only enrich lithium

        # we need to find a way to change the percent_type from the 'default' provided in the dictionary

        # ensures percent_type has been provided
        # at the moment, can be provided by the dictionary or by input, but dictionary value cannot be changed by input
        if self.percent_type == None:
            raise ValueError("percent type not provided")

        # checks that if we try to enrich a material by providing any of the arguments, that the other arguments are also provided
        if self.enrichment != None or self.enrichment_target != None or self.enrichment_type != None:
            if self.enrichment == None or self.enrichment_target == None or self.enrichment_type == None:
                raise ValueError('enrichment, enrichment target and enrichment type are needed to enrich material')

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
    def enrichment_target(self):
        return self._enrichment_target

    @enrichment_target.setter
    def enrichment_target(self, value):
        if value is None:
            self._enrichment_target = value
        else:
            self.enrichment_element = re.split('(\d+)',value)[0]
            self._enrichment_target = value
            self.make_material()


    def populate_from_dictionary(self):

        if "temperature_in_C" in material_dict[self.material_name].keys():
            self.temperature_in_C = material_dict[self.material_name]["temperature_in_C"]

        if "temperature_in_K" in material_dict[self.material_name].keys():
            self.temperature_in_K = material_dict[self.material_name]["temperature_in_K"]

        if "pressure_in_Pa" in material_dict[self.material_name].keys():
            self.pressure_in_Pa = material_dict[self.material_name]["pressure_in_Pa"]

        if "packing_fraction" in material_dict[self.material_name].keys():
            self.packing_fraction = material_dict[self.material_name]["packing_fraction"]

        if "volume_fraction" in material_dict[self.material_name].keys():
            self.volume_fraction = material_dict[self.material_name]["volume_fraction"]

        if "elements" in material_dict[self.material_name].keys():
            self.elements = material_dict[self.material_name]["elements"]

        if "isotopes" in material_dict[self.material_name].keys():
            self.isotopes = material_dict[self.material_name]["isotopes"]

        if "density" in material_dict[self.material_name].keys():
            self.density = material_dict[self.material_name]["density"]

        if "density_equation" in material_dict[self.material_name].keys():
            self.density_equation = material_dict[self.material_name]["density_equation"]

        if "atoms_per_unit_cell" in material_dict[self.material_name].keys():
            self.atoms_per_unit_cell = material_dict[self.material_name]["atoms_per_unit_cell"]

        if "volume_of_unit_cell_cm3" in material_dict[self.material_name].keys():
            self.volume_of_unit_cell_cm3 = material_dict[self.material_name]["volume_of_unit_cell_cm3"]

        if "density_unit" in material_dict[self.material_name].keys():
            self.density_unit = material_dict[self.material_name]["density_unit"]

        if "percent_type" in material_dict[self.material_name].keys():
            self.percent_type = material_dict[self.material_name]["percent_type"]

        if "enrichment" in material_dict[self.material_name].keys():
            self.enrichment = material_dict[self.material_name]["enrichment"]

        if "enrichment_target" in material_dict[self.material_name].keys():
            self.enrichment_target = material_dict[self.material_name]["enrichment_target"]

        if "enrichment_type" in material_dict[self.material_name].keys():
            self.enrichment_type = material_dict[self.material_name]["enrichment_type"]

    def add_elements(self):

        if self.elements is None:
            self.elements = material_dict[self.material_name]["elements"]
        else:
            material_dict[self.material_name]["elements"] = self.elements

        # percent_type for each element is provided by the self.percent_type value

        if type(self.elements) == dict and self.enrichment is None:
            element_numbers = self.elements.values()
            element_symbols = self.elements.keys()

        elif type(self.elements) == str and self.enrichment == None:

            self.chemical_equation = self.elements

            element_numbers = self.get_element_numbers_normalized()
            element_symbols = self.get_elements_from_equation()

        # enriching the material using the new enriching flow from openmc
        # at the moment, we are only enriching Li
        # check what the enrichment_target actually is
        # element is enriched according to enrichment_type
        # element is incorporated into material according to percent_type
        elif type(self.elements) == str and self.enrichment != None:

            self.chemical_equation = self.elements

            element_numbers = self.get_element_numbers_normalized()
            element_symbols = self.get_elements_from_equation()

        elif type(self.elements) == dict and self.enrichment != None:

            element_numbers = self.elements.values()
            element_symbols = self.elements.keys()

        for element_symbol, element_number in zip(element_symbols, element_numbers):
            if element_symbol == self.enrichment_element:
                self.neutronics_material.add_element(self.enrichment_element,
                                                        element_number,
                                                        percent_type=self.percent_type,
                                                        enrichment=self.enrichment,
                                                        enrichment_target=self.enrichment_target,
                                                        enrichment_type=self.enrichment_type)
            else:
                self.neutronics_material.add_element(
                    element_symbol, element_number, self.percent_type
                )

        return element_symbols, element_numbers

    def add_isotopes(self):

        if "isotopes" in material_dict[self.material_name].keys():

            self.isotopes = material_dict[self.material_name]["isotopes"]

            for isotopes_symbol in material_dict[self.material_name]["isotopes"].keys():

                isotopes_number = material_dict[self.material_name]["isotopes"][isotopes_symbol]
                self.neutronics_material.add_nuclide(isotopes_symbol, isotopes_number, self.percent_type)

    def add_density(self):
        print(self)
        if type(self.density) == float or type(self.density) == int:

            self.density_value = self.density
            self.neutronics_material.set_density(self.density_unit, self.density_value * self.packing_fraction)

        elif self.density == None and self.density_equation != None:

            temperature_in_C = self.temperature_in_C
            temperature_in_K = self.temperature_in_K
            pressure_in_Pa = self.pressure_in_Pa

            print('temperature_in_C =', temperature_in_C)
            print('temperature_in_K =', temperature_in_K)
            print('pressure_in_Pa =', pressure_in_Pa)
            print('density_equation =', self.density_equation)
            # print(eval(self.density_equation))
            calculated_density = eval(self.density_equation)
            if calculated_density == None:
                raise ValueError("Density value of ", self.material_name, " can not be found for a temperature of ",self.temperature_in_K, "K and pressure of ", self.pressure_in_Pa,'Pa')

            if self.density_unit == 'kg/m3':
                self.density_value = calculated_density / 1000.
            if self.density_unit == 'g/cm3':
                self.density_value = calculated_density
            if self.density_unit not in ['kg/m3','g/cm3']:
                raise ValueError("Density units of kg/m3 and g/cm3 are supported for density_equations")


            print('self.density_value ',self.density_value )

            self.neutronics_material.set_density(
                'g/cm3', self.density_value * self.packing_fraction
            )

        elif self.density_list != None:

            raise ValueError("Density values intopolated from a list is not yet implemented")

        elif self.atoms_per_unit_cell != None and self.volume_of_unit_cell_cm3 != None:

            self.atoms_per_unit_cell = material_dict[self.material_name][
                "atoms_per_unit_cell"
            ]
            self.volume_of_unit_cell_cm3 = material_dict[self.material_name][
                "volume_of_unit_cell_cm3"
            ]

            self.density_value = (
                self.get_crystal_molar_mass()
                * atomic_mass_unit_in_g
                * self.atoms_per_unit_cell
            ) / self.volume_of_unit_cell_cm3
            self.neutronics_material.set_density(self.density_unit, self.density_value * self.packing_fraction)

        else:

            raise ValueError(
                "density can't be set for " + str(self.material_name) +
                " provide either a density value, equation as a string, or atoms_per_unit_cell and volume_of_unit_cell_cm3",
            )


        return self.neutronics_material

    def make_material(self):

        self.neutronics_material = openmc.Material(name=self.material_name)

        if self.isotopes is not None:

            self.add_isotopes()

        if self.elements is not None:

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

