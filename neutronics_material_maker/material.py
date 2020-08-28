#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import json
import re
from json import JSONEncoder
import os
import json
from pathlib import Path

import openmc
from CoolProp.CoolProp import PropsSI

atomic_mass_unit_in_g = 1.660539040e-24


def _default(self, obj):
    """ monkey-patches json module so that the custom to_json
    method is used which allows Materials to be json dumped
    """
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder.default
JSONEncoder.default = _default


def AddMaterialFromDir(directory=None):
    """Add materials to the internal library from a directory of json files"""
    for filename in Path(directory).glob("*.json"):
        with open(filename, "r") as f:
            new_data = json.load(f)
            material_dict.update(new_data)

    print("Added materials to library", sorted(list(material_dict.keys())))


def AddMaterialFromFile(filename=None):
    """Add materials to the internal library from a json file"""
    with open(filename, "r") as f:
        new_data = json.load(f)
        material_dict.update(new_data)
    print("Added materials to library", sorted(list(material_dict.keys())))


def AvailableMaterials():
    """Returns a dictionary of avaialbe materials"""
    print(material_dict)
    return material_dict


# loads the internal material library of materials
material_dict = {}
AddMaterialFromDir(Path(__file__).parent / "data")


class Material():
    def __init__(
        self,
        material_name,
        packing_fraction=1.0,
        material_tag=None,
        enrichment=None,
        temperature_in_C=None,
        temperature_in_K=None,
        pressure_in_Pa=None,
        elements=None,
        isotopes=None,
        percent_type=None,
        density=None,
        density_equation=None,
        atoms_per_unit_cell=None,
        volume_of_unit_cell_cm3=None,
        density_unit=None,
        enrichment_target=None,
        enrichment_type=None,
        reference=None,
    ):
        """Produces a material by looking up the material_name in a
        collection of prepared materials. Modifiers to the material
        isotopes are applied according to arguments such
        as enrichment. Modifiers to the material density are applied
        according to arguments like temperature_in_C and pressure_in_Pa
        where appropiate (gases, liquids). The collection of materials
        includes presure density, temperature relationships so can
        adjust the density accordingly. The intended use is a tool to
        facilitate the use common materials library from a collection,
        however it is also possible to make complete Materials without
        using the reference collection but more inputs are needed from
        the user.

       :param material_name: this is the reference name used to look up
        the material from the internal collection. Currently avaialbe
        options are ['DT_plasma', 'Pb', 'Be', 'Be12Ti', 'Ba5Pb3', 'Nd5Pb4',
        'Zr5Pb3', 'Zr5Pb4', 'Li', 'Li4SiO4', 'Li2SiO3', 'Li2ZrO3',
        'Li2TiO3', 'Nb3Sn', 'CuCrZr', 'copper', 'ReBCO', 'Pb842Li158',
        'lithium-lead', 'Li8PbO6', 'WC', 'WB', 'SiC', 'borated_polythylene',
        'eurofer', 'SS_316L_N_IG', 'tungsten', 'SS347', 'SS321', 'SS316',
        'SS304', 'P91', 'SS316L', 'SST91', 'concrete_ordinary',
        'concrete_heavy', 'concrete_boronated_heavy', 'B4C', 'He', 'H2O',
        'D2O', 'CO2', 'nitrogen', 'argon', 'xenon']
       :type material_name: string
       :param packing_fraction: this value is mutliplier by the density
        which allows packing_fraction to be taken into account for materials
        involving an amount of void. Recall that packing_fraction is equal
        to 1/void fraction
       :type packing_fraction: float
       :param material_tag: this is a string that is assigned to the
        multimaterial as an identifier. This is used by neutronics
        codes that need to access materials via a unique identifier
       :type material_tag: string
       :param enrichment: this is the percentage of isotope enrichement
       required for the material. This works for materials that have
       an enrichment_target specified. The internal material collection
       have Li6 specified as an enrichment_target for Li, Li4SiO4, Li2SiO3,
       Li2ZrO3, Li2TiO3, lithium-lead and Li8PbO6. Enrichment of the Li6
       and depention of Li7 impacts the density of a material and the
       materials within the collection take this into account. It is also
       possible to use this when making materials not included in the
       reference collection but an enrichment_target must also be provided.
       :type enrichment: float
       :param temperature_in_C: the temperature of the material in degrees
        Celsius. Temperature impacts the density of some materials in the
        collection. Materials in the collection that are impacted by
        temperature have density equaltions that depend on temperature.
        These tend to be liquids and gases used for coolants and even
        liquids such as lithium-lead and FLiBe that are used as a breeder
        materials.
       :type temperature_in_C: float
       :param temperature_in_K: the temperature of the material in degrees
        Kelvin. Temperature impacts the density of some materials in the
        collection. Materials in the collection that are impacted by
        temperature have density equaltions that depend on temperature.
        These tend to be liquids and gases used for coolants and even
        liquids such as lithium-lead and FLiBe that are used as a breeder
        materials.
       :type temperature_in_K: float
       :param pressure_in_Pa: the temperature of the material in degrees
        C. Temperature impacts the density of some materials in the collection.
        Materials in the collection that are impacted by temperature have
        density equaltions that depend on temperature. These tend to be
        liquids and gases used for coolants and even liquids such as
        lithium-lead and FLiBe that are used as a breeder materials.
       :type pressure_in_Pa:


        :return: a neutronics_material_maker.Material object that has
        isotopes and density based on the input material name and modifiers.
        The Material has can return a openmc_material using the
        Material.openmc_material property
        :rtype: neutronics_material_maker.Material
    """

        self.material_name = material_name
        self.material_tag = material_tag
        self.temperature_in_C = temperature_in_C
        self.temperature_in_K = temperature_in_K
        self.pressure_in_Pa = pressure_in_Pa
        self.packing_fraction = packing_fraction
        self.elements = elements
        self.isotopes = isotopes
        self.density = density
        self.density_equation = density_equation
        self.atoms_per_unit_cell = atoms_per_unit_cell
        self.volume_of_unit_cell_cm3 = volume_of_unit_cell_cm3
        self.density_unit = density_unit
        self.percent_type = percent_type
        self.enrichment = enrichment
        self.enrichment_target = enrichment_target
        self.enrichment_type = enrichment_type
        self.reference = reference

        # derived values
        self.enrichment_element = None
        self.density_packed = None

        self.openmc_material = None
        self.list_of_fractions = None
        self.chemical_equation = None
        self.element_numbers = None
        self.element_symbols = None

        self._populate_from_inbuilt_dictionary()

        # checks that if we try to enrich a material by providing any of the
        # arguments, that the other arguments are also provided
        if self.enrichment is not None:
            if self.enrichment_target is None or self.enrichment_type is None:
                raise ValueError(
                    "enrichment target and enrichment type are needed to enrich a material"
                )

        if "temperature_dependant" in material_dict[self.material_name].keys():
            if temperature_in_K is None and temperature_in_C is None:
                if self.material_name == "He":
                    raise ValueError(
                        "temperature_in_K or temperature_in_C is needed for",
                        self.material_name,
                        " Typical helium cooled blankets are 400C and 8e6Pa",
                    )
                elif self.material_name == "H2O":
                    raise ValueError(
                        "temperature_in_K or temperature_in_C is needed for",
                        self.material_name,
                        " Typical water cooled blankets are 305C and 15.5e6Pa",
                    )
                raise ValueError(
                    "temperature_in_K or temperature_in_C is needed for",
                    self.material_name,
                )
            else:
                if temperature_in_K is None:
                    self.temperature_in_K = temperature_in_C + 273.15
                if temperature_in_C is None:
                    self.temperature_in_C = temperature_in_K + 273.15

        if "pressure_dependant" in material_dict[self.material_name].keys():
            if pressure_in_Pa is None:
                raise ValueError(
                    "pressure_in_Pa is needed for",
                    self.material_name)

        self.make_material()

    @property
    def material_name(self):
        return self._material_name

    @material_name.setter
    def material_name(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("material_name must be a string", value)
        self._material_name = value

    @property
    def material_tag(self):
        return self._material_tag

    @material_tag.setter
    def material_tag(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("material_tag must be a string", value)
        self._material_tag = value

    @property
    def packing_fraction(self):
        return self._packing_fraction

    @packing_fraction.setter
    def packing_fraction(self, value):
        value = float(value)
        if not isinstance(value, float):
            raise ValueError("packing_fraction must be a float")
        if value < 0.0:
            raise ValueError("packing_fraction must be greater than 0")
        if value > 1.0:
            raise ValueError("packing_fraction must be less than 1.")
        self._packing_fraction = value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        if isinstance(value, dict) or isinstance(value, str) or value is None:
            self._elements = value
        else:
            raise ValueError(
                "Elements must be dictionaries e.g. {'Li':0.07, 'Si': 0.93}"
            )

    @property
    def isotopes(self):
        return self._isotopes

    @isotopes.setter
    def isotopes(self, value):
        if isinstance(value, dict) or value is None:
            self._isotopes = value
        else:
            raise ValueError(
                "Isotopes must be dictionaries e.g. {'Li6':0.07, 'Li7': 0.93}"
            )

    @property
    def density_equation(self):
        return self._density_equation

    @density_equation.setter
    def density_equation(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("density_equation should be a string")
        self._density_equation = value

    @property
    def density_unit(self):
        return self._density_unit

    @density_unit.setter
    def density_unit(self, value):
        if value in ["g/cm3", "g/cc", "kg/m3", "atom/b-cm", "atom/cm3", None]:
            self._density_unit = value
        else:
            raise ValueError(
                "only 'g/cm3', 'g/cc', 'kg/m3', 'atom/b-cm', 'atom/cm3' are supported for the density_units"
            )

    @property
    def percent_type(self):
        return self._percent_type

    @percent_type.setter
    def percent_type(self, value):
        if value in ["ao", "wo", None]:
            self._percent_type = value
        else:
            raise ValueError(
                "only 'ao' and 'wo' are supported for the percent_type")

    @property
    def enrichment_type(self):
        return self._enrichment_type

    @enrichment_type.setter
    def enrichment_type(self, value):
        if value is not None:
            if value not in ["ao", "wo"]:
                raise ValueError(
                    "only 'ao' and 'wo' are supported for the enrichment_type"
                )
        self._enrichment_type = value

    @property
    def atoms_per_unit_cell(self):
        return self._atoms_per_unit_cell

    @atoms_per_unit_cell.setter
    def atoms_per_unit_cell(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError("atoms_per_unit_cell must be greater than 0")
        self._atoms_per_unit_cell = value

    @property
    def volume_of_unit_cell_cm3(self):
        return self._volume_of_unit_cell_cm3

    @volume_of_unit_cell_cm3.setter
    def volume_of_unit_cell_cm3(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "volume_of_unit_cell_cm3 must be greater than 0")
        self._volume_of_unit_cell_cm3 = value

    @property
    def temperature_in_K(self):
        return self._temperature_in_K

    @temperature_in_K.setter
    def temperature_in_K(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError("temperature_in_K must be greater than 0")
        self._temperature_in_K = value

    @property
    def temperature_in_C(self):
        return self._temperature_in_C

    @temperature_in_C.setter
    def temperature_in_C(self, value):
        if value is not None:
            if value < -273.15:
                raise ValueError(
                    "temperature_in_C must be greater than -273.15")
        self._temperature_in_C = value

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if value is not None:
            if value < 0:
                raise ValueError(
                    "Density have been incorrectly set, density should be above 0"
                )
        self._density = value

    @property
    def enrichment(self):
        return self._enrichment

    @enrichment.setter
    def enrichment(self, value):
        if value is not None:
            if value < 0 or value > 100:
                raise ValueError("Enrichment must be between 0 and 100")
        self._enrichment = value

    @property
    def enrichment_target(self):
        return self._enrichment_target

    @enrichment_target.setter
    def enrichment_target(self, value):
        if value is not None:
            if value not in openmc.data.NATURAL_ABUNDANCE.keys():
                raise ValueError(
                    "enrichment_target must be a naturally occuring isotope from this list",
                    openmc.data.NATURAL_ABUNDANCE.keys(),
                )
        self._enrichment_target = value

    @property
    def pressure_in_Pa(self):
        return self._pressure_in_Pa

    @pressure_in_Pa.setter
    def pressure_in_Pa(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError("pressure_in_Pa must be greater than 0")
        self._pressure_in_Pa = value

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("reference must be a string")
        self._reference = value

    def isotope_to_zaid(isotope):
        z,a,m = openmc.data.zam(isotope)    
        zaid = str(z).zfill(3) + str(a).zfill(3)
        return zaid

    def fispact_material(self, volume):
        mat_card = ['DENSITY ' + str(self.openmc_material.get_mass_density()),
                    'FUEL ' + str(len(self.openmc_material.nuclides))]
        for isotope in self.openmc_material.nuclides:
            number_of_atoms = 1 # Todo molar mass openmc_material.get_mass_density()
            mat_card.append(isotope[1][0] + ' ' + '{:.12e}'.format(number_of_atoms))
        # https: // github.com / ukaea / neutronics_material_maker / blob / d35d6c17f255480954aa37b904d514a54ddee7a5 / neutronics_material_maker / nmm.py  # L122

    def serpent_material(self, zaid_suffix='.31c'):
        """Returns the material in a string compatable with Serpent II"""
        mat_card = ['mat ' + self.material_tag + str(self.openmc_material.get_mass_density())]
        # should check if percent type is 'ao' or 'wo'

        for isotope in self.openmc_material.nuclides:
            if isotope[1][2] == 'ao':
                mat_card.append('     ' + self.isotope_to_zaid(isotope[1][0]) + zaid_suffix + ' ' + isotope[1][1])
            elif isotope[1][2] == 'wo':
                mat_card.append('     ' + self.isotope_to_zaid(isotope[1][0]) + zaid_suffix + ' -' + isotope[1][1])

        return '\n'.join(mat_card)

    def mcnp_material(self, id=1, zaid_suffix='.31c'):
        """Returns the material in a string compatable with MCNP6"""

        mat_card = []
        for i, isotope in enumerate(self.openmc_material.nuclides):

            if i == 0:
                start = 'M' + str(id)
            else:
                start = '     '

            if isotope[1][2] == 'ao':
                rest = self.isotope_to_zaid(isotope[1][0]) + zaid_suffix + ' ' + isotope[1][1]
            elif isotope[1][2] == 'wo':
                rest = self.isotope_to_zaid(isotope[1][0]) + zaid_suffix + ' -' + isotope[1][1]

            mat_card.append(start + rest)

        return '\n'.join(mat_card)

    def _populate_from_inbuilt_dictionary(self):
        """This runs on initilisation and if attributes of the Material object are not specified (left as None)
        then the internal material dictionary is checked to see if defaults are pressent for the particular material.
        If the attributed has defaults that are present in the internal dictionary then these are used to populated
        the attributes of the Material object when present.
        """

        if (
            self.temperature_in_C is None
            and "temperature_in_C" in material_dict[self.material_name].keys()
        ):
            self.temperature_in_C=material_dict[self.material_name][
                "temperature_in_C"
            ]

        if (
            self.temperature_in_K is None
            and "temperature_in_K" in material_dict[self.material_name].keys()
        ):
            self.temperature_in_K=material_dict[self.material_name][
                "temperature_in_K"
            ]

        if (
            self.pressure_in_Pa is None
            and "pressure_in_Pa" in material_dict[self.material_name].keys()
        ):
            self.pressure_in_Pa=material_dict[self.material_name]["pressure_in_Pa"]

        if (
            self.packing_fraction is None
            and "packing_fraction" in material_dict[self.material_name].keys()
        ):
            self.packing_fraction=material_dict[self.material_name][
                "packing_fraction"
            ]

        if (
            self.elements is None
            and "elements" in material_dict[self.material_name].keys()
        ):
            self.elements=material_dict[self.material_name]["elements"]

        if (
            self.isotopes is None
            and "isotopes" in material_dict[self.material_name].keys()
        ):
            self.isotopes=material_dict[self.material_name]["isotopes"]

        if (
            self.density is None
            and "density" in material_dict[self.material_name].keys()
        ):
            self.density=material_dict[self.material_name]["density"]

        if (
            self.density_equation is None
            and "density_equation" in material_dict[self.material_name].keys()
        ):
            self.density_equation=material_dict[self.material_name][
                "density_equation"
            ]

        if (
            self.atoms_per_unit_cell is None
            and "atoms_per_unit_cell" in material_dict[self.material_name].keys()
        ):
            self.atoms_per_unit_cell=material_dict[self.material_name][
                "atoms_per_unit_cell"
            ]

        if (
            self.volume_of_unit_cell_cm3 is None
            and "volume_of_unit_cell_cm3" in material_dict[self.material_name].keys()
        ):
            self.volume_of_unit_cell_cm3=material_dict[self.material_name][
                "volume_of_unit_cell_cm3"
            ]

        if (
            self.density_unit is None
            and "density_unit" in material_dict[self.material_name].keys()
        ):
            self.density_unit=material_dict[self.material_name]["density_unit"]

        if (
            self.percent_type is None
            and "percent_type" in material_dict[self.material_name].keys()
        ):
            self.percent_type=material_dict[self.material_name]["percent_type"]

        if (
            self.enrichment is None
            and "enrichment" in material_dict[self.material_name].keys()
        ):
            self.enrichment=material_dict[self.material_name]["enrichment"]

        if (
            self.enrichment_target is None
            and "enrichment_target" in material_dict[self.material_name].keys()
        ):
            self.enrichment_target=material_dict[self.material_name][
                "enrichment_target"
            ]

        if (
            self.enrichment_type is None
            and "enrichment_type" in material_dict[self.material_name].keys()
        ):
            self.enrichment_type=material_dict[self.material_name]["enrichment_type"]

        if (
            self.reference is None
            and "reference" in material_dict[self.material_name].keys()
        ):
            self.reference=material_dict[self.material_name]["reference"]

    def add_elements(self):
        """Adds elements from a dictionary or chemical formula to the Material"""

        if isinstance(self.elements, dict):

            if self.enrichment_target is not None:
                enrichment_element=re.split(
                    r"(\d+)", self.enrichment_target)[0]
            else:
                enrichment_element=None
            for element_symbol, element_number in zip(
                self.elements.keys(), self.elements.values()
            ):

                if element_symbol == enrichment_element:
                    self.openmc_material.add_element(
                        element_symbol,
                        element_number,
                        percent_type=self.percent_type,
                        enrichment=self.enrichment,
                        enrichment_target=self.enrichment_target,
                        enrichment_type=self.enrichment_type,
                    )
                else:
                    self.openmc_material.add_element(
                        element_symbol, element_number, self.percent_type
                    )

        elif isinstance(self.elements, str):

            self.chemical_equation=self.elements

            self.openmc_material.add_elements_from_formula(
                self.elements,
                percent_type=self.percent_type,
                enrichment=self.enrichment,
                enrichment_target=self.enrichment_target,
                enrichment_type=self.enrichment_type,
            )

    def add_isotopes(self):
        """Adds isotopes from a dictionary or chemical formula to the Material"""

        for isotope_symbol, isotope_number in zip(
            self.isotopes.keys(), self.isotopes.values()
        ):

            self.openmc_material.add_nuclide(
                isotope_symbol, isotope_number, self.percent_type
            )

    def add_density(self):
        """Calculates the density of the Material"""

        if isinstance(self.density, float):
            pass

        elif self.density is None and self.density_equation is not None:

            # Potentially used in the eval part
            temperature_in_K=self.temperature_in_K
            temperature_in_C=self.temperature_in_C
            pressure_in_Pa=self.pressure_in_Pa

            density=eval(self.density_equation)
            if density is None:
                raise ValueError(
                    "Density value of ",
                    self.material_name,
                    " can not be found")
            else:
                self.density=density

        elif self.atoms_per_unit_cell is not None and self.volume_of_unit_cell_cm3 is not None:

            molar_mass=(
                self.get_atoms_in_crystal() *
                self.openmc_material.average_molar_mass)

            mass=self.atoms_per_unit_cell * molar_mass * atomic_mass_unit_in_g

            self.density=mass / self.volume_of_unit_cell_cm3
        else:

            raise ValueError(
                "density can't be set for " +
                str(
                    self.material_name) +
                " provide either a density value, equation as a string, or atoms_per_unit_cell and volume_of_unit_cell_cm3",
            )

        self.openmc_material.set_density(
            self.density_unit, self.density * self.packing_fraction
        )

        return self.openmc_material

    def make_material(self):

        if self.material_tag is None:
            name=self.material_name
        else:
            name=self.material_tag
        self.openmc_material=openmc.Material(name=name)

        if self.isotopes is not None:

            self.add_isotopes()

        elif self.elements is not None:

            self.add_elements()

        self.add_density()

    def get_atoms_in_crystal(self):
        """Finds the number of atoms in the crystal lactic"""

        tokens=[
            a for a in re.split(
                r"([A-Z][a-z]*)",
                self.chemical_equation) if a]

        list_of_fractions=[]

        for counter in range(0, len(tokens)):
            if tokens[counter].isalpha():
                if counter == len(tokens) - 1:
                    list_of_fractions.append(1)
                elif not (tokens[counter + 1]).isalpha():
                    list_of_fractions.append(float(tokens[counter + 1]))
                else:
                    list_of_fractions.append(1)
        self.list_of_fractions=list_of_fractions
        return sum(list_of_fractions)

    def to_json(self):

        jsonified_object={
            "material_name": self.material_name,
            "material_tag": self.material_tag,
            "temperature_in_C": self.temperature_in_C,
            "temperature_in_K": self.temperature_in_K,
            "pressure_in_Pa": self.pressure_in_Pa,
            "packing_fraction": self.packing_fraction,
            "elements": self.elements,
            "isotopes": self.isotopes,
            "density": self.density,
            "density_equation": self.density_equation,
            "atoms_per_unit_cell": self.atoms_per_unit_cell,
            "volume_of_unit_cell_cm3": self.volume_of_unit_cell_cm3,
            "density_unit": self.density_unit,
            "percent_type": self.percent_type,
            "enrichment": self.enrichment,
            "enrichment_target": self.enrichment_target,
            "enrichment_type": self.enrichment_type,
            "reference": self.reference,
        }

        return jsonified_object
