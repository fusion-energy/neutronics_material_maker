#!/usr/bin/env python3

__author__ = "neutronics material maker development team"


import os
import re
import warnings
from json import JSONEncoder
from typing import Optional, Dict
import asteval
from CoolProp.CoolProp import PropsSI

from neutronics_material_maker import (
    make_fispact_material,
    make_serpent_material,
    make_mcnp_material,
    make_shift_material,
    material_dict,
    zaid_to_isotope,
)

OPENMC_AVAILABLE = True
try:
    import openmc
except ImportError:
    OPENMC_AVAILABLE = False
    warnings.warn(
        "OpenMC python package not found, .openmc_material, .serpent_material, \
            .mcnp_material, .fispact_material methods not avaiable")

atomic_mass_unit_in_g = 1.660539040e-24

# Set any custom symbols for use in asteval
asteval_user_symbols = {"PropsSI": PropsSI}


def _default(self, obj):
    """ monkey-patches json module so that the custom to_json
    method is used which allows Materials to be json dumped
    """
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder.default
JSONEncoder.default = _default


class Material:
    """
    Produces a material by looking up the material_name in a
    collection of prepared materials. Modifiers to the material
    isotopes are applied according to arguments such
    as enrichment. Modifiers to the material density are applied
    according to arguments like temperature_in_C and pressure_in_Pa
    where appropiate (gases, liquids). The collection of materials
    includes relationships between presure, temperature and density
    relationships. This allows the code to adjust the density of the
    material accordingly. The intended use is a tool to facilitate
    the use of a common materials library (internal or your own).
    However it is also possible to make complete Materials without
    using the reference collection but more inputs are needed from
    the user. The Material object is also json serializable

    Args:
        material_name (str): This is the reference name used to look up
            the material from the internal collection. Look up the available
            materials using AvailableMaterials()
        material_tag (str): This is a string that is assigned to the
            material as an identifier. This is used by neutronics
            codes to label the material with a unique identifier
        packing_fraction (float): This value is mutliplied by the density
            which allows packing_fraction to be taken into account for materials
            involving an amount of void. Recall that packing_fraction is equal
            to 1/void fraction
        enrichment (float): This is the percentage of isotope enrichment
            required for the material. This works for materials that have
            an enrichment_target specified. The internal material collection
            have Li6 specified as an enrichment_target for Lithium containing
            compounds. Enrichment of Li6 impacts the density of a material and
            the internal package materials take this into account. It is also
            possible to use this when making materials not included in the
            reference collection but an enrichment_target must also be provided.
        enrichment_target (str): The isotope to enrich e.g. Li6
        temperature_in_C (float): The temperature of the material in degrees
            Celsius. Temperature impacts the density of some materials in the
            collection. Materials in the collection that are impacted by
            temperature have density equations that depend on temperature.
            These tend to be liquids and gases used for coolants and even
            liquids such as lithium-lead and FLiBe that are used as a breeder
            materials. Convered to K and added to the openmc material object
            and the serpent material card.
        temperature_in_K (float): The temperature of the material in degrees
            Kelvin. Temperature impacts the density of some materials in the
            collection. Materials in the collection that are impacted by
            temperature have density equations that depend on temperature.
            These tend to be liquids and gases used for coolants and even
            liquids such as lithium-lead and FLiBe that are used as breeder
            materials. Added to the openmc material object and the serpent
            material card.
        pressure_in_Pa (float): The pressure of the material in Pascals
            Pressure impacts the density of some materials in the
            collection. Materials in the collection that are impacted by
            pressure have density equations that depend on pressure.
            These tend to be liquids and gases used for coolants such as
            H2O and CO2.
        zaid_suffix (str): The nuclear library to apply to the zaid, for
            example ".31c", this is used in MCNP and Serpent material cards.
        material_id (int): the id number or mat number used in the MCNP material
            card
        decimal_places (int): The number of decimal places to use in MCNP and
            Seprent material cards when they are printed out (default of 8).
        volume_in_cm3 (float): The volume of the material in cm3, used when
            creating fispact material cards
        elements (dict): A dictionary of keys and values with the element symbol
            (str) as the key and the amount of that element as the value (float)
            e.g. {'C': 0.3333, 'O': 0.666}
        chemical_equation (str): A chemical equation that identifies elements
            and numbers of elements to add to the material e.g. 'CO2' or 'H2O'
        isotopes (dict): A dictionary of keys and values with the isotope symbol
            (str) as the key and the amount of that isotope (float) as the value
            e.g. {'Li6': 0.9, 'Li7': 0.1} alternatively zaid representation
            can also be used instead of the symbol e.g. {'3006': 0.9, '4007': 0.1}
        percent_type (str): Atom "ao" or or weight fraction "wo"
        density (float): value to be used as the density
        density_unit (str): the units of density "g/cm3", "g/cc", "kg/m3",
            "atom/b-cm", "atom/cm3"
        density_equation (str): An equation to be evaluated to find the density,
            can contain temperature_in_C, temperature_in_K and pressure_in_Pa
            variables as part of the equation.
        atoms_per_unit_cell (int): The number of atoms in a unit cell of the
            crystal structure
        volume_of_unit_cell_cm3 (float): The volume of the unit cell in cm3
        reference (str): An entry used to store information on the source of the
            material data

    Returns:
        Material: a neutronics_material_maker.Material instance

    """

    def __init__(
        self,
        material_name: Optional[str] = None,
        packing_fraction: Optional[float] = 1.0,
        material_tag: Optional[str] = None,
        enrichment: Optional[float] = None,
        enrichment_target: Optional[str] = None,
        temperature_in_C: Optional[float] = None,
        temperature_in_K: Optional[float] = None,
        pressure_in_Pa: Optional[float] = None,
        elements: Optional[Dict[str, float]] = None,
        chemical_equation: Optional[str] = None,
        isotopes: Optional[Dict[str, float]] = None,
        percent_type: Optional[str] = None,
        density: Optional[float] = None,
        density_unit: Optional[str] = None,
        density_equation: Optional[str] = None,
        atoms_per_unit_cell: Optional[int] = None,
        volume_of_unit_cell_cm3: Optional[float] = None,
        enrichment_type: Optional[str] = None,
        reference: Optional[str] = None,
        zaid_suffix: Optional[str] = None,
        material_id: Optional[int] = None,
        decimal_places: Optional[int] = 8,
        volume_in_cm3: Optional[float] = None,
    ):

        self.material_name = material_name
        self.material_tag = material_tag
        self.temperature_in_C = temperature_in_C
        self.temperature_in_K = temperature_in_K
        self.pressure_in_Pa = pressure_in_Pa
        self.packing_fraction = packing_fraction
        self.elements = elements
        self.chemical_equation = chemical_equation
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
        self.zaid_suffix = zaid_suffix
        self.material_id = material_id
        self.decimal_places = decimal_places
        self.volume_in_cm3 = volume_in_cm3

        # derived values
        self.openmc_material = None
        self.serpent_material = None
        self.mcnp_material = None
        self.shift_material = None
        self.fispact_material = None
        self.list_of_fractions = None

        if chemical_equation is not None and elements is not None:
            raise ValueError(
                "Material.chemical_equation and Material.elements can not both be set"
            )

        if self.material_name in material_dict.keys():

            self._populate_from_inbuilt_dictionary()

            # checks that if we try to enrich a material by providing any of the
            # arguments, that the other arguments are also provided
            if self.enrichment is not None:
                if self.enrichment_target is None or self.enrichment_type is None:
                    raise ValueError(
                        "Material.enrichment_target and enrichment type are \
                        needed to enrich a material"
                    )

            if "temperature_dependant" in material_dict[self.material_name].keys(
            ):
                if temperature_in_K is None and temperature_in_C is None:
                    if self.material_name == "He":
                        raise ValueError(
                            "temperature_in_K or temperature_in_C is needed for",
                            self.material_name,
                            ". Typical helium cooled blankets are 400C and 8e6Pa",
                        )
                    elif self.material_name == "H2O":
                        raise ValueError(
                            "temperature_in_K or temperature_in_C is needed for",
                            self.material_name,
                            ". Typical water cooled blankets are 305C and 15.5e6Pa",
                        )
                    raise ValueError(
                        "temperature_in_K or temperature_in_C is needed for",
                        self.material_name,
                    )
                else:
                    if temperature_in_K is None:
                        self.temperature_in_K = temperature_in_C + 273.15
                    if temperature_in_C is None:
                        self.temperature_in_C = temperature_in_K - 273.15

            if "pressure_dependant" in material_dict[self.material_name].keys(
            ):
                if pressure_in_Pa is None:
                    raise ValueError(
                        "pressure_in_Pa is needed for",
                        self.material_name)

        # this populates the density of materials when density is provided by
        # equations and crystal latic information by making the openmc material
        # however it should also be possible to ininitialize nmm.Material
        # without openmc installed, hence the if
        if OPENMC_AVAILABLE:
            self._make_openmc_material()

    @property
    def openmc_material(self):
        """
        Returns an OpenMC version of the Material.

        :type: openmc.Material() object
        """
        self._openmc_material = self._make_openmc_material()
        return self._openmc_material

    @openmc_material.setter
    def openmc_material(self, value):
        self._openmc_material = value

    @property
    def serpent_material(self):
        """
        Returns a Serpent version of the Material.

        :type: str
        """

        self._serpent_material = make_serpent_material(self)
        return self._serpent_material

    @serpent_material.setter
    def serpent_material(self, value):
        self._serpent_material = value

    @property
    def mcnp_material(self):
        """
        Returns a MCNP version of the Material. Requires the
        Material.material_id to be set. Decimal places can be controlled with
        the Material.decimal_places attribute.
        Temperature of the material is set as 273K.

        :type: str
        """
        self._mcnp_material = make_mcnp_material(self)
        return self._mcnp_material

    @mcnp_material.setter
    def mcnp_material(self, value):
        self._mcnp_material = value

    @property
    def shift_material(self):
        """
        Returns a Shift version of the Material. Requires the
        Material.material_id to be set. Decimal places can be controlled with
        the Material.deicmal_places attribute.

        :type: str
        """
        self._shift_material = make_shift_material(self)
        return self._shift_material

    @shift_material.setter
    def shift_material(self, value):
        self._shift_material = value

    @property
    def fispact_material(self):
        """
        Returns a fispact version of the Material. Requires the
        Material.volume_in_cm3 to be set.

        :type: str
        """
        self._fispact_material = make_fispact_material(self)
        return self._fispact_material

    @fispact_material.setter
    def fispact_material(self, value):
        self._fispact_material = value

    @property
    def material_name(self):
        return self._material_name

    @material_name.setter
    def material_name(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(
                    "Material.material_name must be a string", value)
        self._material_name = value

    @property
    def material_tag(self):
        return self._material_tag

    @material_tag.setter
    def material_tag(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(
                    "Material.material_tag must be a string", value)
        self._material_tag = value

    @property
    def packing_fraction(self):
        return self._packing_fraction

    @packing_fraction.setter
    def packing_fraction(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError(
                "Material.packing_fraction must be a float or int")
        if value < 0.0:
            raise ValueError(
                "Material.packing_fraction must be greater than 0")
        if value > 1.0:
            raise ValueError(
                "Material.packing_fraction must be less than 1.")
        self._packing_fraction = float(value)

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        if isinstance(value, dict) or value is None:
            self._elements = value
        else:
            raise ValueError(
                "Material.elements must be dictionaries e.g. {'Li':0.07, 'Si': 0.93}"
            )

    @property
    def chemical_equation(self):
        return self._chemical_equation

    @chemical_equation.setter
    def chemical_equation(self, value):
        if isinstance(value, str) or value is None:
            self._chemical_equation = value
        else:
            raise ValueError(
                "Material.chemical_equation must be a string e.g. 'H2O'")

    @property
    def isotopes(self):
        return self._isotopes

    @isotopes.setter
    def isotopes(self, value):
        if isinstance(value, dict) or value is None:
            self._isotopes = value
        else:
            raise ValueError(
                "Material.isotopes must be dictionaries e.g. {'Li6':0.07, 'Li7': 0.93}"
            )

    @property
    def density_equation(self):
        return self._density_equation

    @density_equation.setter
    def density_equation(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(
                    "Material.density_equation should be a string")
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
                "Material.density_unit must be 'g/cm3', 'g/cc', 'kg/m3', \
                    'atom/b-cm' or 'atom/cm3'"
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
                "Material.percent_type only accepts 'ao' or 'wo' types")

    @property
    def enrichment_type(self):
        return self._enrichment_type

    @enrichment_type.setter
    def enrichment_type(self, value):
        if value is not None:
            if value not in ["ao", "wo"]:
                raise ValueError(
                    "Material.enrichment_type only accepts 'ao' or 'wo' types"
                )
        self._enrichment_type = value

    @property
    def atoms_per_unit_cell(self):
        return self._atoms_per_unit_cell

    @atoms_per_unit_cell.setter
    def atoms_per_unit_cell(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "Material.atoms_per_unit_cell must be greater than 0")
        self._atoms_per_unit_cell = value

    @property
    def volume_of_unit_cell_cm3(self):
        return self._volume_of_unit_cell_cm3

    @volume_of_unit_cell_cm3.setter
    def volume_of_unit_cell_cm3(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "Material.volume_of_unit_cell_cm3 must be greater than 0"
                )
        self._volume_of_unit_cell_cm3 = value

    @property
    def temperature_in_K(self):
        return self._temperature_in_K

    @temperature_in_K.setter
    def temperature_in_K(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "Material.temperature_in_K must be greater than 0")
        self._temperature_in_K = value

    @property
    def temperature_in_C(self):
        return self._temperature_in_C

    @temperature_in_C.setter
    def temperature_in_C(self, value):
        if value is not None:
            if value < -273.15:
                raise ValueError(
                    "Material.temperature_in_C must be greater than -273.15"
                )
        self._temperature_in_C = value

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if value is None:
            self._density = value
        else:
            if value < 0:
                raise ValueError("Material.density should be above 0", value)
            self._density = float(value)

    @property
    def enrichment(self):
        return self._enrichment

    @enrichment.setter
    def enrichment(self, value):
        if value is not None:
            if value < 0 or value > 100:
                raise ValueError(
                    "Material.enrichment must be between 0 and 100")
        self._enrichment = value

    @property
    def enrichment_target(self):
        return self._enrichment_target

    @enrichment_target.setter
    def enrichment_target(self, value):
        if value is not None:
            if value not in openmc.data.NATURAL_ABUNDANCE.keys():
                raise ValueError(
                    "Material.enrichment_target must be a naturally occuring \
                    isotope from this list",
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
                raise ValueError(
                    "Material.pressure_in_Pa must be greater than 0")
        self._pressure_in_Pa = value

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Material.reference must be a string")
        self._reference = value

    @property
    def zaid_suffix(self):
        return self._zaid_suffix

    @zaid_suffix.setter
    def zaid_suffix(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Material.zaid_suffix must be a string")
        self._zaid_suffix = value

    @property
    def material_id(self):
        return self._material_id

    @material_id.setter
    def material_id(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise ValueError("Material.material_id must be an int")
        self._material_id = value

    @property
    def volume_in_cm3(self):
        return self._volume_in_cm3

    @volume_in_cm3.setter
    def volume_in_cm3(self, value):
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise ValueError("Material.volume_in_cm3 must be an float")
        self._volume_in_cm3 = value

    def _make_openmc_material(self):

        original_cross_sections = os.environ.get("OPENMC_CROSS_SECTIONS")
        if original_cross_sections is not None:
            del os.environ["OPENMC_CROSS_SECTIONS"]

        if self.material_tag is None:
            name = self.material_name
        else:
            name = self.material_tag
        if self.material_id is not None:
            openmc_material = openmc.Material(
                material_id=self.material_id,
                name=name,
                temperature=self.temperature_in_K)
        else:
            openmc_material = openmc.Material(
                name=name,
                temperature=self.temperature_in_K)

        if self.isotopes is not None:

            openmc_material = self._add_isotopes(openmc_material)

        if self.elements is not None:

            openmc_material = self._add_elements_from_dict(openmc_material)

        if self.chemical_equation is not None:

            openmc_material = self._add_elements_from_equation(openmc_material)

        openmc_material = self._add_density(openmc_material)

        if original_cross_sections is not None:
            os.environ["OPENMC_CROSS_SECTIONS"] = original_cross_sections

        return openmc_material

    def _populate_from_inbuilt_dictionary(self):
        """This runs on initilisation and if attributes of the Material object
        are not specified (left as None) then the internal material dictionary
        is checked to see if defaults are pressent for the particular material.
        If the attributed has defaults that are present in the internal
        dictionary then these are used to populated the attributes of the
        Material object when present.
        """

        if (
            self.chemical_equation is None
            and "chemical_equation" in material_dict[self.material_name].keys()
        ):
            self.chemical_equation = material_dict[self.material_name][
                "chemical_equation"
            ]

        if (
            self.temperature_in_C is None
            and "temperature_in_C" in material_dict[self.material_name].keys()
        ):
            self.temperature_in_C = material_dict[self.material_name][
                "temperature_in_C"
            ]

        if (
            self.temperature_in_K is None
            and "temperature_in_K" in material_dict[self.material_name].keys()
        ):
            self.temperature_in_K = material_dict[self.material_name][
                "temperature_in_K"
            ]

        if (
            self.pressure_in_Pa is None
            and "pressure_in_Pa" in material_dict[self.material_name].keys()
        ):
            self.pressure_in_Pa = material_dict[self.material_name]["pressure_in_Pa"]

        if (
            self.packing_fraction is None
            and "packing_fraction" in material_dict[self.material_name].keys()
        ):
            self.packing_fraction = material_dict[self.material_name][
                "packing_fraction"
            ]

        if (
            self.elements is None
            and "elements" in material_dict[self.material_name].keys()
        ):
            self.elements = material_dict[self.material_name]["elements"]

        if (
            self.isotopes is None
            and "isotopes" in material_dict[self.material_name].keys()
        ):
            self.isotopes = material_dict[self.material_name]["isotopes"]

        if (
            self.density is None
            and "density" in material_dict[self.material_name].keys()
        ):
            self.density = material_dict[self.material_name]["density"]

        if (
            self.density_equation is None
            and "density_equation" in material_dict[self.material_name].keys()
        ):
            self.density_equation = material_dict[self.material_name][
                "density_equation"
            ]

        if (
            self.atoms_per_unit_cell is None
            and "atoms_per_unit_cell" in material_dict[self.material_name].keys()
        ):
            self.atoms_per_unit_cell = material_dict[self.material_name][
                "atoms_per_unit_cell"
            ]

        if (
            self.volume_of_unit_cell_cm3 is None
            and "volume_of_unit_cell_cm3" in material_dict[self.material_name].keys()
        ):
            self.volume_of_unit_cell_cm3 = material_dict[self.material_name][
                "volume_of_unit_cell_cm3"
            ]

        if (
            self.density_unit is None
            and "density_unit" in material_dict[self.material_name].keys()
        ):
            self.density_unit = material_dict[self.material_name]["density_unit"]

        if (
            self.percent_type is None
            and "percent_type" in material_dict[self.material_name].keys()
        ):
            self.percent_type = material_dict[self.material_name]["percent_type"]

        if (
            self.enrichment is None
            and "enrichment" in material_dict[self.material_name].keys()
        ):
            self.enrichment = material_dict[self.material_name]["enrichment"]

        if (
            self.enrichment_target is None
            and "enrichment_target" in material_dict[self.material_name].keys()
        ):
            self.enrichment_target = material_dict[self.material_name][
                "enrichment_target"
            ]

        if (
            self.enrichment_type is None
            and "enrichment_type" in material_dict[self.material_name].keys()
        ):
            self.enrichment_type = material_dict[self.material_name]["enrichment_type"]

        if (
            self.reference is None
            and "reference" in material_dict[self.material_name].keys()
        ):
            self.reference = material_dict[self.material_name]["reference"]

    def _add_elements_from_equation(self, openmc_material):
        """Adds elements from a dictionary or chemical equation to the Material"""

        openmc_material.add_elements_from_formula(
            self.chemical_equation,
            percent_type=self.percent_type,
            enrichment=self.enrichment,
            enrichment_target=self.enrichment_target,
            enrichment_type=self.enrichment_type,
        )

        return openmc_material

    def _add_elements_from_dict(self, openmc_material):
        """Adds elements from a dictionary or chemical formula to the Material"""

        if self.enrichment_target is not None:
            enrichment_element = re.split(r"(\d+)", self.enrichment_target)[0]
        else:
            enrichment_element = None

        for element_symbol, element_number in zip(
            self.elements.keys(), self.elements.values()
        ):

            if element_symbol == enrichment_element:
                openmc_material.add_element(
                    element_symbol,
                    element_number,
                    percent_type=self.percent_type,
                    enrichment=self.enrichment,
                    enrichment_target=self.enrichment_target,
                    enrichment_type=self.enrichment_type,
                )
            else:
                openmc_material.add_element(
                    element_symbol, element_number, self.percent_type
                )

        return openmc_material

    def _add_isotopes(self, openmc_material):
        """Adds isotopes from a dictionary or chemical formula to the Material"""

        for isotope_symbol, isotope_number in zip(
            self.isotopes.keys(), self.isotopes.values()
        ):
            # check for zaid entry
            if isinstance(isotope_symbol, int) or isotope_symbol.isdigit():
                isotope_symbol = zaid_to_isotope(isotope_symbol)
            openmc_material.add_nuclide(
                isotope_symbol, isotope_number, self.percent_type
            )

        return openmc_material

    def _add_density(self, openmc_material):
        """Calculates the density of the Material"""

        if not isinstance(self.density, float):

            if self.density is None and self.density_equation is not None:

                aeval = asteval.Interpreter(usersyms=asteval_user_symbols)

                # Potentially used in the eval part
                aeval.symtable["temperature_in_K"] = self.temperature_in_K
                aeval.symtable["temperature_in_C"] = self.temperature_in_C
                aeval.symtable["pressure_in_Pa"] = self.pressure_in_Pa

                density = aeval.eval(self.density_equation)

                if len(aeval.error) > 0:
                    raise aeval.error[0].exc(aeval.error[0].msg)

                if density is None:
                    raise ValueError(
                        "Density value of ",
                        self.material_name,
                        " can not be found")
                else:
                    self.density = density

            elif (
                self.atoms_per_unit_cell is not None
                and self.volume_of_unit_cell_cm3 is not None
            ):

                molar_mass = (
                    self._get_atoms_in_crystal() *
                    openmc_material.average_molar_mass)

                mass = self.atoms_per_unit_cell * molar_mass * atomic_mass_unit_in_g

                self.density = mass / self.volume_of_unit_cell_cm3
            else:

                raise ValueError(
                    "density can't be set for "
                    + str(self.material_name)
                    + " provide either a density_value, density_equation as a \
                        string, or atoms_per_unit_cell and \
                        volume_of_unit_cell_cm3"
                )

        openmc_material.set_density(
            self.density_unit, self.density * self.packing_fraction
        )

        return openmc_material

    def _get_atoms_in_crystal(self):
        """Finds the number of atoms in the crystal lactic"""

        tokens = [
            a for a in re.split(
                r"([A-Z][a-z]*)",
                self.chemical_equation) if a]

        list_of_fractions = []

        for counter in range(0, len(tokens)):
            if tokens[counter].isalpha():
                if counter == len(tokens) - 1:
                    list_of_fractions.append(1)
                elif not (tokens[counter + 1]).isalpha():
                    list_of_fractions.append(float(tokens[counter + 1]))
                else:
                    list_of_fractions.append(1)
        self.list_of_fractions = list_of_fractions
        return sum(list_of_fractions)

    def to_json(self):

        jsonified_object = {
            "material_name": self.material_name,
            "material_tag": self.material_tag,
            "temperature_in_C": self.temperature_in_C,
            "temperature_in_K": self.temperature_in_K,
            "pressure_in_Pa": self.pressure_in_Pa,
            "packing_fraction": self.packing_fraction,
            "elements": self.elements,
            "chemical_equation": self.chemical_equation,
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
            "zaid_suffix": self.zaid_suffix,
            "material_id": self.material_id,
            "decimal_places": self.decimal_places,
            "volume_in_cm3": self.volume_in_cm3,
        }

        return jsonified_object
