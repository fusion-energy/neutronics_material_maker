
import re
import sys
import json
import pprint

from common_utils import is_number
from element import Element
from common_utils import natural_isotopes_in_elements

class NamedObject(object):
    def __init__(self):
        self.classname = self.__class__.__name__

    def to_dict(self):

        def obj_dict(obj):
            return obj.__dict__

        return json.loads(json.dumps(self, default=obj_dict))#, indent=4, sort_keys=False))




class Compound(NamedObject):
    def __init__(self, chemical_equation, packing_fraction=1, theoretical_density=1, pressure_Pa=8.0E6,temperature_K=823.0, enriched_isotopes='Natural',density_g_per_cm3=None):
        super(Compound, self).__init__()
        self.chemical_equation = chemical_equation
        self.list = [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]
        self.enriched_isotopes = enriched_isotopes
        self.packing_fraction = packing_fraction
        self.theoretical_density = theoretical_density
        self.pressure_Pa = pressure_Pa
        self.temperature_K = temperature_K
        if density_g_per_cm3 != None:
            #print('setting density',density_g_per_cm3)
            self.density_g_per_cm3=density_g_per_cm3
        else:
            #print('tyring to find density')
            self.density_g_per_cm3=self.find_density_g_per_cm3
            #print('finding density',self.density_g_per_cm3)


    @property
    def density_g_per_cm3_idea_gas(self):
        molar_mass = Element('He').molar_mass_g #4.002602
        density_kg_m3 = (self.pressure_Pa / (8.31 * self.temperature_K)) * molar_mass * 6.023e23 * 1.66054e-27
        return density_kg_m3


    @property
    def elements(self):

        list_elements = []
        for counter in range(0, len(self.list)):
            # print(self.list[counter])
            if not is_number(self.list[counter]):
                #print(' a letter? ',self.list[counter])
                if self.enriched_isotopes!='Natural':


                    if self.enriched_isotopes[0].symbol == self.list[counter]:

                        list_elements.append(Element(self.list[counter], self.enriched_isotopes))
                    else:

                        list_elements.append(Element(self.list[counter]))

                else:
                    list_elements.append(Element(self.list[counter]))
        return list_elements

    @property
    def fractions_coefficients(self):
        list_fraction = []
        for counter in range(0, len(self.list)):
            if not is_number(self.list[counter]):
                try:
                    if is_number(self.list[counter + 1]):
                        list_fraction.append(self.list[counter + 1])
                    else:
                        list_fraction.append('1')
                except:
                    list_fraction.append('1')
        return list_fraction

    @property
    def isotopes_mass_fractions(self):
        list_isotopes_mass_fraction = []
        for fractions, element in zip(self.fractions_coefficients, self.elements):
            for isotope in element.isotopes:
                list_isotopes_mass_fraction.append(isotope.abundance * float(fractions))
        # print('list_isotopes_mass_fraction',list_isotopes_mass_fraction)
        return list_isotopes_mass_fraction

    @property
    def zaids(self):
        list_of_zaids = []
        for element in self.elements:
            for isotope in element.isotopes:
                list_of_zaids.append(str(isotope.protons) + str(isotope.atomic_number).zfill(3))
                #list_of_zaids.append(str(isotope.protons).zfill(3) + str(isotope.atomic_number).zfill(3))
        return list_of_zaids

    @property
    def serpent_material_card(self):
        #print('checking for density')
        material_card = 'mat ' + self.description + ' -' + str(self.density_g_per_cm3) + '\n'
        for zaid, isotopes_mass_fraction in zip(self.zaids, self.isotopes_mass_fractions):
            if zaid.startswith('160'):
                material_card = material_card +'    '+ zaid + '.03c ' + str(isotopes_mass_fraction) + '\n'
            else:
                material_card = material_card +'    '+ zaid + '.31c ' + str(isotopes_mass_fraction) + '\n'
        return material_card

    @property
    def molar_mass_g(self):
        masses = []
        for element in self.elements:
            element_mass = 0
            for isotope in element.isotopes:
                # isotope.print_details
                # print(isotope.abundance, isotope.mass_amu)
                element_mass = element_mass + isotope.abundance * isotope.mass_amu
            masses.append(element_mass)

        cumlative_molar_mass = 0
        # print('mass, fraction')
        for mass, fraction in zip(masses, self.fractions_coefficients):
            # print(mass, fraction)
            cumlative_molar_mass = cumlative_molar_mass + (mass * float(fraction))
        # print(self.chemical_equation,' molar_mass=',cumlative_molar_mass)
        return cumlative_molar_mass

    @property
    def mass_kg(self):
        return (
               self.molar_mass_g * 1000 * 1.66054e-27 * self.packing_fraction * self.theoretical_density) / 1000  # convert moles to kg to g

    @property
    def volume_m3(self):
        units = ''
        if self.chemical_equation == 'Li4SiO4':
            vol = 1.1543  # http://materials.springer.com/isp/crystallographic/docs/sd_1404772
            units = 'nm3'
            molecules_per_unit_cell = 14.0
        if self.chemical_equation == 'Li2SiO3':
            vol = 0.23632  # http://materials.springer.com/isp/crystallographic/docs/sd_1703282
            units = 'nm3'
            molecules_per_unit_cell = 4.0
        if self.chemical_equation == 'Li2ZrO3':
            vol = 0.24479  # http://materials.springer.com/isp/crystallographic/docs/sd_1520554
            units = 'nm3'
            molecules_per_unit_cell = 4.0
        if self.chemical_equation == 'Li2TiO3':
            vol = 0.42701  # http://materials.springer.com/isp/crystallographic/docs/sd_1716489
            units = 'nm3'
            molecules_per_unit_cell = 8.0
        if self.chemical_equation == 'Be':
            vol = 0.01622  # http://materials.springer.com/isp/crystallographic/docs/sd_0261739
            units = 'nm3'
            molecules_per_unit_cell = 2.0
        if self.chemical_equation == 'Be12Ti':
            vol = 0.22724  # http://materials.springer.com/isp/crystallographic/docs/sd_0528340
            molecules_per_unit_cell = 2.0
            units = 'nm3'
        if self.chemical_equation == 'Ba5Pb3':
            vol = 1.37583  # http://materials.springer.com/isp/crystallographic/docs/sd_0528381
            molecules_per_unit_cell = 4.0
            units = 'nm3'
        if self.chemical_equation == 'Nd5Pb4':
            vol = 1.06090  # http://materials.springer.com/isp/crystallographic/docs/sd_0252125
            molecules_per_unit_cell = 4.0
            units = 'nm3'
        if self.chemical_equation == 'Zr5Pb3':
            vol = 0.36925  # http://materials.springer.com/isp/crystallographic/docs/sd_0307360
            molecules_per_unit_cell = 2.0
            units = 'nm3'
        if self.chemical_equation == 'Zr5Pb4':
            vol = 0.40435  # http://materials.springer.com/isp/crystallographic/docs/sd_0451962
            molecules_per_unit_cell = 2.0
            units = 'nm3'
        if self.chemical_equation == 'Pb84.2Li15.8':
            atoms_per_barn_cm2 = 3.2720171E-2
            atoms_per_cm3 = atoms_per_barn_cm2 * 1e24
            units = 'cm3'
            vol = 10000 / atoms_per_cm3
            molecules_per_unit_cell = 100

            # https://www.sciencedirect.com/science/article/pii/S0022311508000809 states density is 10.52
            # MCNP input decks from Eurofusion IDM state atoms per barn cm2 is 3.2720171E-2
            # the difference is due to temperature see http://www-ferp.ucsd.edu/LIB/PROPS/PANOS/lipb.html
            # atoms_per_barn_cm2 = 3.2720171E-2
            # atoms_per_cm3 = atoms_per_barn_cm2 * 1e24
            # units = 'cm3'
            # print('molar mass = ' ,self.molar_mass_g)
            # print('atoms in one mole = ' ,6.0221409e+23)
            # print('1cm3 mass (density) = ' ,self.molar_mass_g/( 6.0221409e+23/atoms_per_cm3 ))

        if units == 'nm3':
            vol = (vol * 1.0e-27) / molecules_per_unit_cell
        if units == 'cm3':
            vol = (vol * 1.0e-6) / molecules_per_unit_cell
        if units != '':
            return vol
        else:
            print('density =',self.density_g_per_cm3)
            print('Compound volume not found for ', self.chemical_equation)
            sys.exit()

    @property
    def description(self):

        list_of_enriched_isotope_keys = []
        if self.enriched_isotopes!='Natural':
            list_of_enriched_isotope_keys.append('_')
            #print('self.enriched_isotopes',self.enriched_isotopes)
            #print('self.enriched_isotopes',self.chemical_equation)
            for enriched_isotope in self.enriched_isotopes:
                #for entry in enriched_isotope:
                 list_of_enriched_isotope_keys.append(enriched_isotope.symbol + str(enriched_isotope.atomic_number) + '_' + str(enriched_isotope.abundance))

        return self.chemical_equation + '_'.join(list_of_enriched_isotope_keys)

    @property
    def find_density_kg_per_m3(self):

        if self.chemical_equation == 'He':
            density = self.density_g_per_cm3_idea_gas
        else:
            density = self.mass_kg / self.volume_m3
        return density

    @property
    def find_density_g_per_cm3(self):
        density = self.find_density_kg_per_m3 * 0.001
        return density
