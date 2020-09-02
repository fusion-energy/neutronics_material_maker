#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import json
from json import JSONEncoder

try:
    import openmc
except ImportError as err:
    raise err('OpenMC not found, .openmc_material, .serpent_material, .mcnp_material, .fispact_material not avaiable')

from CoolProp.CoolProp import PropsSI
import neutronics_material_maker as nmm

from neutronics_material_maker import make_fispact_material, make_serpent_material, make_mcnp_material

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
    Produces a mixed material from several indivdual materials.
    This class extends the existing openmc.Material.mix_materials
    to perform this mixing of neutronics_materail_maker.Materials
    and openmc.Materials. The MultiMaterial object is json serializable.

    Args:
        material_tag (str): this is a string that is assigned to the
            material as an identifier. This is used by neutronics
            codes that the material labeling with a unique identifier
        materials (list): a list of neutronics_material_maker.Materials
            or openmc.Materials that are to be mixed
        fracs (list of floats): a list of fractions that represent the amount of
            each material to mix
        percent_type (str): Type of frac percentage, must be one of
            atom percent 'ao', weight percent 'wo', or volume percent 'vo'.
            Defaults to 'vo'
        packing_fraction (float): this value is mutliplier by the density
            which allows packing_fraction to be taken into account for materials
            involving an amount of void. Recall that packing_fraction is equal
            to 1/void fraction
        zaid_suffix (str): the nuclear library to apply to the zaid, for example
            .31c this is used in MCNP and Serpent material cards.
        id (int): the id number or mat number used in the MCNP material card
        volume_in_cm3 (float): the volume of the material in cm3, used when creating
            fispact material cards

    Returns:
        Material: a neutronics_material_maker.Material instance

    """

    def __init__(
        self,
        material_tag=None,
        materials=[],
        fracs=[],
        percent_type="vo",
        packing_fraction=1.0,
        zaid_suffix=None,
        id=None,
        volume_in_cm3=None,
    ):
        self.material_tag = material_tag
        self.materials = materials
        self.fracs = fracs
        self.percent_type = percent_type
        self.packing_fraction = packing_fraction
        self.zaid_suffix = zaid_suffix
        self.id = id
        self.volume_in_cm3 = volume_in_cm3

        # derived values
        self.openmc_material = None
        self.serpent_material = None
        self.mcnp_material = None
        self.fispact_material = None

        if len(self.fracs) != len(self.materials):
            raise ValueError(
                "There must be equal numbers of fracs and materials")

        if sum(self.fracs) != 1.0:
            print(
                "warning sum of MutliMaterials do not sum to 1.",
                self.fracs,
                " = ",
                sum(self.fracs),
            )

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
    def openmc_material(self):
        """
        Returns an OpenMC version of the Material.

        :type: openmc.Material() object
        """
        self._openmc_material = self.make_openmc_material()
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

    def make_openmc_material(self):

        openmc_material_objects = []
        for material in self.materials:
            if isinstance(material, openmc.Material):
                openmc_material_objects.append(material)
            elif isinstance(material, nmm.Material):
                openmc_material_objects.append(material.openmc_material)
            else:
                raise ValueError(
                    "only openmc.Material or neutronics_material_maker.Materials are accepted. Not",
                    type(material),
                )

        openmc_material = openmc.Material.mix_materials(  # name = self.material_tag,
            materials=openmc_material_objects,
            fracs=self.fracs,
            percent_type=self.percent_type,
        )

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
                })

        jsonified_object = {
            "material_tag": self.material_tag,
            "materials": materials_list,
            "fracs": self.fracs,
            "percent_type": self.percent_type,
            "packing_fraction": self.packing_fraction,
        }

        return jsonified_object
