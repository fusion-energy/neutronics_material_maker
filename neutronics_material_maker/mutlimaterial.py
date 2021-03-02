#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import warnings
from json import JSONEncoder
from typing import List, Optional, Union

import neutronics_material_maker as nmm
from neutronics_material_maker import (make_fispact_material,
                                       make_mcnp_material,
                                       make_shift_material,
                                       make_serpent_material)

OPENMC_AVAILABLE = True
try:
    import openmc
except ImportError:
    OPENMC_AVAILABLE = False
    warnings.warn(
        "OpenMC python package not found, .openmc_material, .serpent_material, \
            .mcnp_material, .fispact_material methods not avaiable")


atomic_mass_unit_in_g = 1.660539040e-24


def _default(self, obj):
    """ monkey-patches json module so that the custom to_json
    method is used which allows Materials to be json dumped
    """
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder.default
JSONEncoder.default = _default


class MultiMaterial:
    """
    Produces a mixed material from several individual materials.
    This class extends the existing openmc.Material.mix_materials
    to perform this mixing of neutronics_material_maker.Materials
    and openmc.Materials. The MultiMaterial object is json serializable.

    Args:
        material_tag (str): This is a string that is assigned to the
            material as an identifier. This is used by neutronics
            codes to label the material with a unique identifier
        materials (list): a list of neutronics_material_maker.Materials
            or openmc.Materials that are to be mixed
        fracs (list of floats): A list of fractions that represent the amount of
            each material to mix
        percent_type (str): Type of frac percentage, must be one of
            atom percent 'ao', weight percent 'wo', or volume percent 'vo'.
            Defaults to 'vo'
        packing_fraction (float): This value is multiplied by the density
            which allows packing_fraction to be taken into account for materials
            involving an amount of void. Recall that packing_fraction is equal
            to 1/void fraction
        zaid_suffix (str): The nuclear library to apply to the zaid, for example
            ".31c", this is used in MCNP and Serpent material cards.
        material_id (int): The id number or mat number used in the MCNP material
            card
        decimal_places (int): The number of decimal places to use in MCNP and
            Seprent material cards when they are printed out (default of 8).
        volume_in_cm3 (float): The volume of the material in cm3, used when
            creating fispact material cards
        temperature_in_C (float): The temperature of the material in degrees
            Celsius. Convered to K and added to the openmc material object and
            the serpent material card
        temperature_in_K (float): The temperature of the material in degrees
            Kelvin. Added to the openmc material object and the serpent
            material card

    Returns:
        Material: a neutronics_material_maker.Material instance

    """

    def __init__(
        self,
        material_tag: Optional[str] = None,
        materials: List[Union[nmm.Material, openmc.Material]] = [],
        fracs: List[float] = [],
        percent_type: Optional[str] = "vo",
        packing_fraction: float = 1.0,
        zaid_suffix: Optional[str] = None,
        material_id: Optional[int] = None,
        decimal_places: Optional[int] = 8,
        volume_in_cm3: Optional[float] = None,
        temperature_in_C: Optional[float] = None,
        temperature_in_K: Optional[float] = None
    ):
        self.material_tag = material_tag
        self.materials = materials
        self.fracs = fracs
        self.percent_type = percent_type
        self.packing_fraction = packing_fraction
        self.zaid_suffix = zaid_suffix
        self.material_id = material_id
        self.decimal_places = decimal_places
        self.volume_in_cm3 = volume_in_cm3
        self.temperature_in_C = temperature_in_C
        self.temperature_in_K = temperature_in_K

        # derived values
        self.openmc_material = None
        self.serpent_material = None
        self.mcnp_material = None
        self.shift_material = None
        self.fispact_material = None

        if len(self.fracs) != len(self.materials):
            raise ValueError(
                "There must be equal numbers of fracs and materials")

        if sum(self.fracs) != 1.0:
            warnings.warn(
                "warning sum of MutliMaterials.fracs do not sum to 1."
                + str(self.fracs)
                + " = "
                + str(sum(self.fracs)),
                UserWarning,
            )

        if temperature_in_K is not None or temperature_in_C is not None:
            if temperature_in_K is None:
                self.temperature_in_K = temperature_in_C + 273.15
            if temperature_in_C is None:
                self.temperature_in_C = temperature_in_K - 273.15

        if OPENMC_AVAILABLE:
            self._make_openmc_material()

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
    def packing_fraction(self):
        return self._packing_fraction

    @packing_fraction.setter
    def packing_fraction(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError(
                "MultiMaterial.packing_fraction must be a float or int")
        if value < 0.0:
            raise ValueError(
                "MultiMaterial.packing_fraction must be greater than 0")
        if value > 1.0:
            raise ValueError(
                "MultiMaterial.packing_fraction must be less than 1.")
        self._packing_fraction = float(value)

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
        Returns a MCNP version of the Material.

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
        Returns a Shift version of hte Material.

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
        Returns a fispact version of the Material.

        :type: str
        """
        self._fispact_material = make_fispact_material(self)
        return self._fispact_material

    @fispact_material.setter
    def fispact_material(self, value):
        self._fispact_material = value

    def _make_openmc_material(self):

        openmc_material_objects = []
        for material in self.materials:
            if isinstance(material, openmc.Material):
                openmc_material_objects.append(material)
            elif isinstance(material, nmm.Material):
                openmc_material_objects.append(material.openmc_material)
            else:
                raise ValueError(
                    "only openmc.Material or neutronics_material_maker. \
                    Materials are accepted. Not", type(material),
                )

        openmc_material = openmc.Material.mix_materials(
            name=self.material_tag,
            materials=openmc_material_objects,
            fracs=self.fracs,
            percent_type=self.percent_type,
        )

        if self.temperature_in_K is not None:
            openmc_material.temperature = self.temperature_in_K

        # this modifies the density by the packing fraction of the material
        if self.packing_fraction != 1.0:
            density_in_g_per_cm3 = openmc_material.get_mass_density()

            openmc_material.set_density(
                "g/cm3", density_in_g_per_cm3 * self.packing_fraction
            )

        return openmc_material

    def to_json(self):

        materials_list = []
        for material in self.materials:
            materials_list.append(
                {
                    "material_name": material.material_name,
                    "material_tag": material.material_tag,
                    "temperature_in_C": material.temperature_in_C,
                    "temperature_in_K": material.temperature_in_K,
                    "pressure_in_Pa": material.pressure_in_Pa,
                    "packing_fraction": material.packing_fraction,
                    "elements": material.elements,
                    "chemical_equation": material.chemical_equation,
                    "isotopes": material.isotopes,
                    "density": material.density,
                    "density_equation": material.density_equation,
                    "atoms_per_unit_cell": material.atoms_per_unit_cell,
                    "volume_of_unit_cell_cm3": material.volume_of_unit_cell_cm3,
                    "density_unit": material.density_unit,
                    "percent_type": material.percent_type,
                    "enrichment": material.enrichment,
                    "enrichment_target": material.enrichment_target,
                    "enrichment_type": material.enrichment_type,
                    "reference": material.reference,
                    "zaid_suffix": material.zaid_suffix,
                    "material_id": material.material_id,
                    "decimal_places": material.decimal_places,
                    "volume_in_cm3": material.volume_in_cm3,
                })

        jsonified_object = {
            "material_tag": self.material_tag,
            "materials": materials_list,
            "fracs": self.fracs,
            "percent_type": self.percent_type,
            "packing_fraction": self.packing_fraction,
            "zaid_suffix": self.zaid_suffix,
            "material_id": self.material_id,
            "decimal_places": self.decimal_places,
            "volume_in_cm3": self.volume_in_cm3,
        }

        return jsonified_object
