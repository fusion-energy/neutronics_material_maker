#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import json
from json import JSONEncoder

import openmc
from CoolProp.CoolProp import PropsSI
import neutronics_material_maker

atomic_mass_unit_in_g = 1.660539040e-24


def _default(self, obj):
    """ monkey-patches json module so that the custom to_json
    method is used which allows Materials to be json dumped
    """
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder.default
JSONEncoder.default = _default


class MultiMaterial:
    """Produces a mixed material from several indivdual materials.
        This class extends the existing openmc.Material.mix_materials
        to perform this mixing on neutronics_materail_maker.Materials
        and packing fractions (inverse of void fraction) to be applied

       :param material_tag: this is a string that is assigned to the
        multimaterial as an identifier. This is used by neutronics
        codes that need to access materials via a unique identifier
       :type material_tag: string
       :param materials: a list of neutronics_material_maker.Materials
        or openmc.Materials that are to be mixed
       :type materials: list of Material objects
       :param fracs: a list of fractions that represent the amount of
        each material to mix
       :type fracs: a list of floats
       :param percent_type: Type of frac percentage, must be one of
        'ao', 'wo', or 'vo', to signify atom percent (molar percent),
        weight percent, or volume percent, optional. Defaults to 'vo'
       :type percent_type: string
       :param packing_fraction: this value is mutliplier by the density
        which allows packing_fraction to be taken into account for materials
        involving an amount of void. Recall that packing_fraction is equal
        to 1/void fraction
       :type packing_fraction: float

        :return: a neutronics_material_maker.MultiMaterial object that has
        isotopes and density based on the input materials and modifiers.
        The MultiMaterial has can return a openmc_material using the
        .openmc_material property
        :rtype: neutronics_material_maker.MultiMaterial
    """

    def __init__(
        self,
        material_tag=None,
        materials=[],
        fracs=[],
        percent_type="vo",
        packing_fraction=1.0,
    ):
        self.material_tag = material_tag
        self.materials = materials
        self.fracs = fracs
        self.percent_type = percent_type
        self.packing_fraction = packing_fraction

        # derived values
        self.openmc_material_obj = None

        self.make_material()

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

    def openmc_material(self):
        return self.openmc_material_obj

    def make_material(self):

        if len(self.fracs) != len(self.materials):
            raise ValueError("There must be equal numbers of fracs and materials")

        if sum(self.fracs) != 1.0:
            print(
                "warning sum of MutliMaterials do not sum to 1.",
                self.fracs,
                " = ",
                sum(self.fracs),
            )

        openmc_material_objects = []
        for material in self.materials:
            if isinstance(material, openmc.Material):
                openmc_material_objects.append(material)
            elif isinstance(material, neutronics_material_maker.Material):
                openmc_material_objects.append(material.openmc_material())
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

        self.openmc_material_obj = openmc_material

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
                }
            )

        jsonified_object = {
            "material_tag": self.material_tag,
            "materials": materials_list,
            "fracs": self.fracs,
            "percent_type": self.percent_type,
            "packing_fraction": self.packing_fraction,
        }

        return jsonified_object
