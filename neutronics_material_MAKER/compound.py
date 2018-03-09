
import re
import sys
import json
import pprint

from neutronics_material_MAKER.common_utils import is_number
from neutronics_material_MAKER.element import Element
from neutronics_material_MAKER.common_utils import natural_isotopes_in_elements
from neutronics_material_MAKER.common_utils import read_in_xsdir_file

from neutronics_material_MAKER.jsonable_object import NamedObject

class Compound(NamedObject):

    def __init__(self, chemical_equation, packing_fraction=1,
                 theoretical_density=1,
                 pressure_Pa=8.0E6, temperature_K=823.0,
                 enriched_isotopes='Natural',
                 density_g_per_cm3=None, state_of_matter='solid',
                 xsdir_filename='/opt/serpent2/xsdir.serp', **kwargs):
        super(Compound, self).__init__(**kwargs)

        self.xsdir_filename= xsdir_filename
        self.state_of_matter = state_of_matter
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
    def element_atom_fractions(self):
        list_of_fractions = []
        for counter in range(0, len(self.list)):
            if not is_number(self.list[counter]):
                try:
                    if is_number(self.list[counter + 1]):
                        list_of_fractions.append(float(self.list[counter + 1]))
                    else:
                        list_of_fractions.append(1)
                except:
                    list_of_fractions.append(1)


        a = sum(list_of_fractions)
        b = 1.0

        rtol = 1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor * fraction)

            return normalised_list_of_fractions

        return list_of_fractions

    @property
    def isotopes(self):
        list_of_isotopes = []
        for fractions, element in zip(self.fractions_coefficients, self.elements):
            for isotope in element.isotopes:
                list_of_isotopes.append(isotope)
        # print('list_isotopes_mass_fraction',list_isotopes_mass_fraction)


        return list_of_isotopes

    @property
    def isotopes_atom_fractions(self):
        list_of_fractions = []
        for fractions, element in zip(self.fractions_coefficients, self.elements):
            for isotope in element.isotopes:
                list_of_fractions.append(isotope.abundance * float(fractions))
        # print('list_isotopes_mass_fraction',list_isotopes_mass_fraction)

        a = sum(list_of_fractions)
        b = 1.0

        rtol = 1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor * fraction)

            return normalised_list_of_fractions

        return list_of_fractions

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

        list_of_isotope_zaid_or_name, list_of_associated_libraries = read_in_xsdir_file(self.xsdir_filename)

        #print('checking for density')
        material_card = 'mat ' + self.description + ' -' + str(self.density_g_per_cm3) + '\n'
        #for zaid, isotopes_atom_fraction in zip(self.zaids, self.isotopes_atom_fractions):
        for isotope, isotopes_atom_fraction in zip(self.isotopes, self.isotopes_atom_fractions):

            if isotopes_atom_fraction > 0:
                if isotope.zaid in list_of_isotope_zaid_or_name:
                    index_of_zaid = list_of_isotope_zaid_or_name.index(isotope.zaid)
                    lib = list_of_associated_libraries[index_of_zaid]
                    material_card = material_card + ('    ' + (isotope.zaid + '.' + lib).ljust(12) + ' ' + str(isotopes_atom_fraction).ljust(25) + ' % ' + isotope.symbol + ' \n')
                else:
                    #print('isotope not found in xsdir, using default library ')
                    #print('isotope.zaid=', isotope.zaid)
                    material_card = material_card + ('    ' + (isotope.zaid).ljust(12) + ' ' + str(isotopes_atom_fraction).ljust(25) + ' % ' + isotope.symbol + ' not in xsdir \n')
            else:
                print('isotope ', isotope.description,' mass fraction is 0, so this is not being included in the material card')


            #
            # if isotopes_atom_fraction > 0:
            #     if zaid.startswith('160'):
            #         material_card = material_card +'    '+ zaid + '.03c ' + str(isotopes_atom_fraction) + '\n'
            #     else:
            #         material_card = material_card +'    '+ zaid + '.31c ' + str(isotopes_atom_fraction) + '\n'
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
            vol = 1.1543
            units = 'nm3'
            molecules_per_unit_cell = 14.0
        if self.chemical_equation == 'Li2SiO3':
            vol = 0.23632
            units = 'nm3'
            molecules_per_unit_cell = 4.0
        if self.chemical_equation == 'Li2ZrO3':
            vol = 0.24479
            units = 'nm3'
            molecules_per_unit_cell = 4.0
        if self.chemical_equation == 'Li2TiO3':
            vol = 0.42701
            units = 'nm3'
            molecules_per_unit_cell = 8.0
        if self.chemical_equation == 'Be':
            vol = 0.01622
            units = 'nm3'
            molecules_per_unit_cell = 2.0
        if self.chemical_equation == 'Be12Ti':
            vol = 0.22724
            molecules_per_unit_cell = 2.0
            units = 'nm3'
        if self.chemical_equation == 'Ba5Pb3':
            vol = 1.37583
            molecules_per_unit_cell = 4.0
            units = 'nm3'
        if self.chemical_equation == 'Nd5Pb4':
            vol = 1.06090
            molecules_per_unit_cell = 4.0
            units = 'nm3'
        if self.chemical_equation == 'Zr5Pb3':
            vol = 0.36925
            molecules_per_unit_cell = 2.0
            units = 'nm3'
        if self.chemical_equation == 'Zr5Pb4':
            vol = 0.40435
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
            # print('density =',self.density_g_per_cm3)
            print('\nNo density provided')
            print('Tried to calculate density by first finding the crystaline volume')
            print('Crystaline volume not found for ', self.chemical_equation)
            print('Solve this with one of the following suggestions ...')
            print('1. Add the density when creating the material')
            print('2. Add the crystaline volume to the internal database')
            print('3. Specifiy the state_of_matter="liquid" and allow the code to find the density of the liquid')
            print('4. Specifiy the state_of_matter="gas" and allow the code to find the density of the liquid')
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


    def density_g_per_cm3_idea_gas(self):
        molar_mass = self.molar_mass_g #4.002602
        density_kg_m3 = (self.pressure_Pa / (8.31 * self.temperature_K)) * molar_mass * 6.023e23 * 1.66054e-27
        return density_kg_m3

    def density_g_per_cm3_liquid(self):
        from thermo.chemical import Chemical
        hot_pressurized_liquid = Chemical(self.chemical_equation, T=self.temperature_K, P=self.pressure_Pa)
        return hot_pressurized_liquid.rho * 0.001


    @property
    def find_density_g_per_cm3(self):

        if self.state_of_matter == 'solid':
            density = (self.mass_kg / self.volume_m3)  * 0.001
        if self.state_of_matter == 'gas':
            density = self.density_g_per_cm3_idea_gas()
        if self.state_of_matter == 'liquid':
            density =self.density_g_per_cm3_liquid()

        return density
