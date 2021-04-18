#!/usr/bin/env python3

__author__ = "neutronics material maker development team"


import json
import os
import re
import warnings
from json import JSONEncoder
from typing import Dict, List, Optional, Union

import asteval
from CoolProp.CoolProp import PropsSI

from neutronics_material_maker import (NATURAL_ABUNDANCE,
                                       check_add_additional_end_lines,
                                       make_fispact_material,
                                       make_mcnp_material,
                                       make_serpent_material,
                                       make_shift_material, material_dict,
                                       zaid_to_isotope)

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
    Produces a material from input arguments that can be output in formats
    suitable for several different neutronics codes.

    Args:
        name: This is a string that is assigned to the material as an
            identifier. This is used by neutronics codes to label the material
            with a unique identifier.
        packing_fraction: This value is mutliplied by the density
            which allows packing_fraction to be taken into account for materials
            involving an amount of void. Recall that packing_fraction is equal
            to 1/void fraction
        enrichment: This is the percentage of isotope enrichment
            required for the material. This works for materials that have
            an enrichment_target and enrichment_type also specified.
        enrichment_target: The isotope to enrich e.g. Li6
        temperature: The temperature of the material in degrees
            Kelvin. Temperature impacts the density of some materials in the
            collection. Materials in the collection that are impacted by
            temperature have density equations that depend on temperature.
            These tend to be liquids and gases used for coolants and even
            liquids such as lithium-lead and FLiBe that are used as breeder
            materials. Added to the openmc material object and the serpent
            material card.
        temperature_to_neutronics_code: The temperature args are often used to
            find the material density via density equations. However it can be
            desirable to not make use of this temperature in the neutronics
            codes. Typically this is due to missing cross section data.
            Defaults to True which makes use of any material temperature in the
            neutronics material. Can be set to False which doesn't propagate
            temperature data to the neutroics material. This only impacts
            openmc and serpent materials. As shift materials require the use of
            temperature and fispact/mcnp materials don't make use of
            temperature on the material card.
        pressure: The pressure of the material in Pascals. Pressure impacts the
            density of some materials in the collection. Materials in the
            collection that are impacted by pressure have density equations
            that depend on pressure. These tend to be liquids and gases used
            for coolants such as H2O and CO2.
        zaid_suffix: The nuclear library to apply to the zaid, for
            example ".31c", this is used in MCNP and Serpent material cards.
        material_id: the id number or mat number used in the MCNP material card
        decimal_places: The number of decimal places to use in MCNP and
            Seprent material cards when they are printed out (default of 8).
        volume_in_cm3: The volume of the material in cm3, used when
            creating fispact material cards
        elements: A dictionary of keys and values with the element symbol
            (str) as the key and the amount of that element as the value (float)
            e.g. {'C': 0.3333, 'O': 0.666}
        chemical_equation: A chemical equation that identifies elements
            and numbers of elements to add to the material e.g. 'CO2' or 'H2O'
        isotopes: A dictionary of keys and values with the isotope symbol
            (str) as the key and the amount of that isotope (float) as the value
            e.g. {'Li6': 0.9, 'Li7': 0.1} alternatively zaid representation
            can also be used instead of the symbol e.g. {'3006': 0.9, '4007': 0.1}
        percent_type: Atom "ao" or or weight fraction "wo"
        density: value to be used as the density. Can be a number or a string.
            if a string then it will be evaluated as an equation to find the
            density and can contain temperature and pressure varibles.
            variables as part of the equation.
        density_unit: the units of density "g/cm3", "g/cc", "kg/m3",
            "atom/b-cm", "atom/cm3"
        atoms_per_unit_cell: The number of atoms in a unit cell of the
            crystal structure
        volume_of_unit_cell_cm3: The volume of the unit cell in cm3
        comment: An entry used to store information on the source of the
            material data
        additional_end_lines: Additional lines of test that are added to the end of
            the material card. Compatable with MCNP, Serpent, Fispact outputs
            which are string based. Agument should be a dictionary specifying
            the code and a list of lines to be added, besure to include any
            white required spaces in the string. This example will add a single
            S(a,b) card to an MCNP card {'mnnp': ['        mt24 lwtr.01']}.

    Returns:
        Material: a neutronics_material_maker.Material instance

    """

    def __init__(
        self,
        name: Optional[str] = None,
        packing_fraction: Optional[float] = 1.,
        enrichment: Optional[float] = None,
        enrichment_target: Optional[str] = None,
        temperature: Optional[float] = None,
        temperature_to_neutronics_code: Optional[bool] = True,
        pressure: Optional[float] = None,
        elements: Optional[Dict[str, float]] = None,
        chemical_equation: Optional[str] = None,
        isotopes: Optional[Dict[str, float]] = None,
        percent_type: Optional[str] = None,
        density: Optional[float] = None,
        density_unit: Optional[str] = None,
        atoms_per_unit_cell: Optional[int] = None,
        volume_of_unit_cell_cm3: Optional[float] = None,
        enrichment_type: Optional[str] = None,
        comment: Optional[str] = None,
        zaid_suffix: Optional[str] = None,
        material_id: Optional[int] = None,
        decimal_places: Optional[int] = 8,
        volume_in_cm3: Optional[float] = None,
        additional_end_lines: Optional[Dict[str, List[str]]] = None,
    ):

        self.name = name
        self.temperature = temperature
        self.temperature_to_neutronics_code = temperature_to_neutronics_code
        self.pressure = pressure
        self.packing_fraction = packing_fraction
        self.elements = elements
        self.chemical_equation = chemical_equation
        self.isotopes = isotopes
        self.density = density
        self.atoms_per_unit_cell = atoms_per_unit_cell
        self.volume_of_unit_cell_cm3 = volume_of_unit_cell_cm3
        self.density_unit = density_unit
        self.percent_type = percent_type
        self.enrichment = enrichment
        self.enrichment_target = enrichment_target
        self.enrichment_type = enrichment_type
        self.comment = comment
        self.zaid_suffix = zaid_suffix
        self.material_id = material_id
        self.decimal_places = decimal_places
        self.volume_in_cm3 = volume_in_cm3
        self.additional_end_lines = additional_end_lines

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

        # It should also be possible to ininitialize nmm.Material without
        # OpenMC
        if OPENMC_AVAILABLE:
            self._make_openmc_material()

    @property
    def additional_end_lines(self):
        """Returns a dictionary of lists where each entry in the list is a to
        be added to the end of the material card and each key is the name of
        the neutronics code to add the line to.

        Returns:
            dictionary of neutronics codes each with a list of lines to add
        """
        return self._additional_end_lines

    @additional_end_lines.setter
    def additional_end_lines(self, value):
        check_add_additional_end_lines(value)

        self._additional_end_lines = value

    @property
    def openmc_material(self):
        """Creates an OpenMC version of the Material.

        Returns:
            openmc.Material() object
        """
        self._openmc_material = self._make_openmc_material()
        return self._openmc_material

    @openmc_material.setter
    def openmc_material(self, value):
        self._openmc_material = value

    @property
    def serpent_material(self):
        """Creates a a Serpent version of the Material with '\n' as line
        endings. Decimal places can be controlled with the
        Material.decimal_places attribute.

        Returns:
            str: A Serpent material card
        """

        return make_serpent_material(self)

    @serpent_material.setter
    def serpent_material(self, value):
        self._serpent_material = value

    @property
    def mcnp_material(self):
        """Creates a a MCNP version of the Material with '\n' as line endings.
        Requires the Material.material_id to be set. Decimal places can be
        controlled with the Material.decimal_places attribute.

        Returns:
            str: A MCNP material card
        """

        return make_mcnp_material(self)

    @mcnp_material.setter
    def mcnp_material(self, value):
        self._mcnp_material = value

    @property
    def shift_material(self):
        """Creates a a Shift version of the Material with '\n' as line endings.
        Requires the Material.material_id and Material.temperature to be set.
        Decimal places can be controlled with the Material.deicmal_places
        attribute.

        Returns:
            str: A Shift material card
        """

        return make_shift_material(self)

    @shift_material.setter
    def shift_material(self, value):
        self._shift_material = value

    @property
    def fispact_material(self) -> str:
        """Creates a a FISPACT version of the Material with '\n' as line
        endings. Requires the Material.volume_in_cm3 to be set.

        Returns:
            str: A FISPACT material card
        """

        return make_fispact_material(self)

    @fispact_material.setter
    def fispact_material(self, value):
        self._fispact_material = value

    @property
    def name(self) -> str:
        """
        The name of the material, used to look up the material from the
        internal database of material names available
        """
        return self._name

    @name.setter
    def name(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(
                    "Material.name must be a string", value)
        self._name = value

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
    def elements(self) -> dict:
        """
        A dictionary of all the elements present in the material
        """
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
    def chemical_equation(self) -> str:
        """
        A chemical equation of the material represented as a string e.g. 'H20'.
        Only integer multipliers are permitted.
        """
        return self._chemical_equation

    @chemical_equation.setter
    def chemical_equation(self, value):
        if isinstance(value, str) or value is None:
            self._chemical_equation = value
        else:
            raise ValueError(
                "Material.chemical_equation must be a string e.g. 'H2O'")

    @property
    def isotopes(self) -> dict:
        """
        A dictionary of all the isotopes present in the material
        """
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
    def density_unit(self) -> float:
        """
        The units of density to use, either "g/cm3", "g/cc", "kg/m3",
        "atom/b-cm", "atom/cm3"
        """
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
    def percent_type(self, value) -> float:
        """
        The units of percentage to use, either atom 'ao' or weight 'wo' based.
        """
        if value in ["ao", "wo", None]:
            self._percent_type = value
        else:
            raise ValueError(
                "Material.percent_type only accepts 'ao' or 'wo' types")

    @property
    def enrichment_type(self) -> float:
        """
        The units of enrichment to use, either atom 'ao' or weight 'wo' based.

        """
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
        """
        The volume of the crystal unit cell. Can be used in a density string as
        part of the equation calculations if 'volume_of_unit_cell_cm3' is used
        in the density attribute.

        :type: float
        """
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
    def temperature(self):
        """
        The temperature of the material in Kelvin

        :type: float
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "Material.temperature must be greater than 0 Kelvin")
        self._temperature = value

    @property
    def density(self):
        """
        The density of the material in the units specified by the of
        density_unit attribute

        :type: float
        """
        return self._density

    @density.setter
    def density(self, value):
        if value is None:
            self._density = value
        elif isinstance(value, str):
            self._density = value
        elif isinstance(value, (int, float)):
            if value < 0:
                raise ValueError("Material.density should be above 0", value)
            self._density = float(value)

    @property
    def enrichment(self):
        """
        The enrichment of the enrichment_target in percentage. Must be between
        0. and 100. in the units specified by the of enrichment_type attribute

        :type: float
        """
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
        """
        Identifies the isotope to enrich when the enrichment attribtue is set.
        In fusion breeder blankets this is often Li6.

        :type: float
        """
        return self._enrichment_target

    @enrichment_target.setter
    def enrichment_target(self, value):
        if value is not None:
            if value not in NATURAL_ABUNDANCE.keys():
                raise ValueError(
                    "Material.enrichment_target must be a naturally occuring "
                    "isotope from this list",
                    NATURAL_ABUNDANCE.keys(),
                )
        self._enrichment_target = value

    @property
    def pressure(self):
        """
        The pressure of the material in Pascals. Must be a possive number. Used
        to calculate the density if it appears in the density attribute.

        :type: float
        """
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        if value is not None:
            if value < 0.0:
                raise ValueError(
                    "Material.pressure must be greater than 0")
        self._pressure = value

    @property
    def comment(self):
        """
        A comment string to state where the material properties information
        came from

        :type: str
        """
        return self._comment

    @comment.setter
    def comment(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Material.comment must be a string")
        self._comment = value

    @property
    def zaid_suffix(self):
        """
        The zaid suffix to add to materials after the ZAID. Refers to a cross
        section such as .31c. Used when producing Serpent and MCNP materials

        :type: str
        """
        return self._zaid_suffix

    @zaid_suffix.setter
    def zaid_suffix(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Material.zaid_suffix must be a string")
        self._zaid_suffix = value

    @property
    def material_id(self):
        """
        The material id to assign to the material

        :type: int
        """
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
        """
        The volume of the material in cm3. Used when writing Fispact materials
        and can also be used in density equation calculation if volume_in_cm3
        appears in density attribute.

        :type: float
        """
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise ValueError("Material.volume_in_cm3 must be an float")
        self._volume_in_cm3 = value

    def _make_openmc_material(self):
        """Makes an openmc.Material() object that is used to make other
        material tpyes (e.g. Serpent, MCNP, Shift, Fispact). If elements are
        specified then makes material using natural adundances of isotopes.
        This is slightly different to the native openmc method that uses
        isotopes available in the cross_sections.xml file"""

        original_cross_sections = os.environ.get("OPENMC_CROSS_SECTIONS")
        if original_cross_sections is not None:
            del os.environ["OPENMC_CROSS_SECTIONS"]

        if self.material_id is not None:
            openmc_material = openmc.Material(
                material_id=self.material_id,
                name=self.name)
        else:
            openmc_material = openmc.Material(
                name=self.name)

        if self.temperature_to_neutronics_code is True:
            openmc_material.temperature = self.temperature

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

    def _check_enrichment_attributes(self):

        if self.enrichment is None:
            return None

        elif (self.enrichment_type is not None and self.enrichment_target is not None):
            return re.split(r"(\d+)", self.enrichment_target)[0]

        elif (self.enrichment is not None or self.enrichment_type is not None or self.enrichment_target is not None):
            raise ValueError(
                "Material.enrichment_target, Material.enrichment_type and "
                "Material.enrichment are all needed to enrich a material"
            )

        return None

    def _add_elements_from_equation(self, openmc_material):
        """Adds elements from a dictionary or chemical equation to the Material"""

        self._check_enrichment_attributes()

        openmc_material.add_elements_from_formula(
            self.chemical_equation,
            percent_type=self.percent_type,
            enrichment=self.enrichment,
            enrichment_target=self.enrichment_target,
            enrichment_type=self.enrichment_type,
        )

        return openmc_material

    def _add_elements_from_dict(self, openmc_material):
        """Adds elements from a dictionary or chemical formula to the Material

        Arguments:
            openmc_material: the material to add additional elements to

        Returns:
            openmc material object with additional elements
        """

        enrichment_element = self._check_enrichment_attributes()

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
        """Adds isotopes from a dictionary or chemical formula to the Material

        Arguments:
            openmc_material: the material to add additional isotopes to

        Returns:
            openmc material object with additional isotopes
        """

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
        """Calculates the density of the Material

        Arguments:
            openmc_material: the material to add the density to

        Returns:
            openmc material object with density set
        """

        if isinstance(self.density, float):
            density = self.density

        # a density equation is being used
        elif isinstance(self.density, str):
            aeval = asteval.Interpreter(usersyms=asteval_user_symbols)

            if "temperature" in self.density and self.temperature is None:
                raise ValueError(
                    "Material.temperature is needed to calculate the density")

            if "pressure" in self.density and self.pressure is None:
                raise ValueError(
                    "Material.pressure is needed to calculate the density"
                )

            # Potentially used in the eval part
            aeval.symtable["temperature"] = self.temperature
            aeval.symtable["pressure"] = self.pressure

            density = aeval.eval(self.density)

            if len(aeval.error) > 0:
                raise aeval.error[0].exc(aeval.error[0].msg)

            if density is None:
                raise ValueError(
                    "Density value of ",
                    self.name,
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
                + str(self.name) +
                " provide either a density value as a number or density "
                "as a string, or atoms_per_unit_cell and "
                "volume_of_unit_cell_cm3"
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

    def from_json_file(
        filename: str,
        name: str,
        **kwargs
    ):

        with open(filename, "r") as file:
            new_data = json.load(file)

        print(new_data)
        print(new_data.keys())

        entry = new_data[name]

        # customisation of the library entry
        for key, value in kwargs.items():
            entry[key] = value

        return Material(name=name, **entry)

    def from_library(
        name: str,
        **kwargs
    ):
        # TODO allow discreat libraries to be searched library: List('str')

        if name not in material_dict.keys():

            raise ValueError(
                'name of ', name, 'not found in the internal library'
            )

        entry = material_dict[name].copy()

        # customisation of the library entry
        for key, value in kwargs.items():
            entry[key] = value

        return Material(name=name, **entry)

    def from_mixture(
        materials,
        fracs: List[float],
        percent_type: Optional[str] = 'vo',
        name: Optional[str] = None,
        packing_fraction: Optional[float] = 1.,
        temperature: Optional[float] = None,
        temperature_to_neutronics_code: Optional[bool] = True,
        pressure: Optional[float] = None,
        comment: Optional[str] = None,
        zaid_suffix: Optional[str] = None,
        material_id: Optional[int] = None,
        decimal_places: Optional[int] = 8,
        volume_in_cm3: Optional[float] = None,
        additional_end_lines: Optional[Dict[str, List[str]]] = None,
    ):
        if sum(fracs) != 1.0:
            warnings.warn(
                "warning sum of MutliMaterials.fracs do not sum to 1."
                + str(fracs)
                + " = "
                + str(sum(fracs)),
                UserWarning,
            )

        openmc_material_objects = []
        for material in materials:
            if isinstance(material, openmc.Material):
                openmc_material_objects.append(material)
            elif isinstance(material, Material):
                openmc_material_objects.append(material.openmc_material)
            else:
                raise ValueError(
                    "only openmc.Material or neutronics_material_maker. \
                    Materials are accepted. Not", type(material),
                )

        openmc_material = openmc.Material.mix_materials(
            materials=openmc_material_objects,
            fracs=fracs,
            percent_type=percent_type,
        )

        isotopes = {}
        for nuclide in sorted(openmc_material.nuclides):
            isotopes[nuclide.name] = nuclide.percent

        return Material(
            percent_type=nuclide.percent_type,
            isotopes=isotopes,
            density=openmc_material.get_mass_density(),
            density_unit='g/cm3',
            packing_fraction=packing_fraction,
            name=name,
            temperature=temperature,
            temperature_to_neutronics_code=temperature_to_neutronics_code,
            pressure=pressure,
            comment=comment,
            zaid_suffix=zaid_suffix,
            material_id=material_id,
            decimal_places=decimal_places,
            volume_in_cm3=volume_in_cm3,
            additional_end_lines=additional_end_lines,
        )

    def to_json(self) -> dict:
        """
        Json serializable version of the material
        """

        contents = {
            "temperature": self.temperature,
            "pressure": self.pressure,
            "packing_fraction": self.packing_fraction,
            "elements": self.elements,
            "chemical_equation": self.chemical_equation,
            "isotopes": self.isotopes,
            "density": self.density,
            "atoms_per_unit_cell": self.atoms_per_unit_cell,
            "volume_of_unit_cell_cm3": self.volume_of_unit_cell_cm3,
            "density_unit": self.density_unit,
            "percent_type": self.percent_type,
            "enrichment": self.enrichment,
            "enrichment_target": self.enrichment_target,
            "enrichment_type": self.enrichment_type,
            "comment": self.comment,
            "zaid_suffix": self.zaid_suffix,
            "material_id": self.material_id,
            "decimal_places": self.decimal_places,
            "volume_in_cm3": self.volume_in_cm3,
        }

        for key, value in dict(contents).items():
            if value is None:
                del contents[key]

        jsonified_object = {
            self.name: contents
        }

        return jsonified_object
