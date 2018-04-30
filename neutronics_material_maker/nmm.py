import re
import numpy as np
import math
from pandas import DataFrame

NDATA = DataFrame.from_csv('nuclear_data.csv', index_col='Symbol')
NAT_NDATA = NDATA[NDATA['Natural']]


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError) as e:
        return False


def find_prefered_library(zaid, xsdir):
    try:
        xsdir_contents = open(xsdir, "r").readlines()
        for line in xsdir_contents:
            choped_up_line = line.split()[0].split('.')
            if choped_up_line[0] == zaid:
                return '.'+choped_up_line[1]
        return ''
    except:
        return ''


def find_prefered_library_file(zaid, xsdir):
    try:
        xsdir_contents = open(xsdir, "r").readlines()
        for line in xsdir_contents:
            choped_up_line = line.split()
            if choped_up_line[0].split('.')[0] == zaid:
                return choped_up_line[-1]
        return ''
    except:
        return ''


def color_manager(color):
        if type(color) not in (tuple, list, np.ndarray) or len(color) != 3:
            raise ValueError("3-length RGB color tuple please. "
                             "Not: ".format(color))
        return ' rgb ' + ' '.join([str(i) for i in np.array(color).clip(0,
                                   255)])


class Base(object):

    def serpent_header(self, name, color):
        name, color = self.kwarg_handler(name, color)
        if self.density_g_per_cm3 is None and self.density_atoms_per_barn_per_cm is None:
            raise ValueError('To produce a serpent material card the '
                             'density_g_per_cm3 or '
                             'density_atoms_per_barn_per_cm must be provided.')
        if self.density_g_per_cm3 is None:
            density = '  '+str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  '+str(self.density_g_per_cm3*self.packing_fraction)
        color = color_manager(color)
        mat_card = 'mat '+name+density+color+' \n'
        return mat_card

    def kwarg_handler(self, name, color):
        if name is None:
            name = self.material_card_name
            if name is None:
                name = self.name
        if color is None:
            color = self.color
            if color is None:
                color = (0, 0, 0)
        return name, color


class Isotope(Base):
    '''
    args: 2 of the 3 below
        :param: proton number  / atomic number
        :param: nucleon number / mass number
        :param: Element symbol (capitals)
    kwargs:
        :param: xsdir
        :param: nuclear_library
        :param: density_g_per_cm3
        :param: density_atoms_per_barn_per_cm
        :param: color...
        :param: abundance
    '''
    def __init__(self, *args, **kwargs):
        self.classname = self.__class__.__name__
        self._handle_kwargs(kwargs)
        self._handle_args(args)

        if self.nucleons is None:
            raise ValueError('To create an Isotope provide an nucleon number.')

        if self.protons is None and self.symbol is None: 
            raise ValueError('To create an Isotope provide either protons or '
                             'symbol please.')
        if self.protons is None:
            self.protons = self.find_protons_from_symbol()
        self._sanity()
        if self.symbol is None:
            self.symbol = self.find_symbol_from_protons()
        self.element_name = self.find_element_name()       
        self.name = self.element_name+'_'+str(self.nucleons)
        self.material_card_name = self.name  # TODO
        self.neutrons = self.nucleons-self.protons
        self.mass_amu = NDATA[(NDATA['Proton number'] == self.protons) & 
                              (NDATA['Nucleon number'] == self.nucleons)]['Mass amu'][0]
        self.natural_abundance = NDATA[(NDATA['Proton number'] == self.protons) & 
                                       (NDATA['Nucleon number'] == self.nucleons)]['Natural abundance'][0]

        self.abundance = kwargs.get('abundance', self.natural_abundance)
        if self.abundance and self.abundance > 1.0 or self.abundance < 0.0:
            raise ValueError('Abundance of isotope can not be greater than 1.0'
                             ' or less than 0.')
        self.zaid = str(self.protons)+str(self.nucleons).zfill(3)
        self._get_xs_files()

    def _handle_kwargs(self, kwargs):
        self.symbol = kwargs.get('symbol', None)
        self.protons = kwargs.get('protons', None)
        self.nucleons = kwargs.get('nucleons', None)
        self.color = kwargs.get('color', (0, 0, 0))
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3', None)
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm', None)

    def _handle_args(self, args):
        atomic_number_or_proton_number = []
        for arg in args:
            if isinstance(arg, str) and self.symbol is None:
                self.symbol = arg
                self.protons = self.find_protons_from_symbol()
            if isinstance(arg, int):
                atomic_number_or_proton_number.append(arg)
        if self.nucleons is None and len(atomic_number_or_proton_number) >= 1:
            self.nucleons = max(atomic_number_or_proton_number)
        if self.protons is None and len(atomic_number_or_proton_number) >= 1:
            self.protons = min(atomic_number_or_proton_number)

    def _sanity(self):
        if NDATA[(NDATA['Proton number'] == self.protons) &
                 (NDATA['Nucleon number'] == self.nucleons)].empty:
            raise ValueError('This isotope {}^{}_{} either does not exist, or '
                             'you have no data for it.'.format(self.symbol,
                                                               self.nucleons,
                                                               self.protons))

    def _get_xs_files(self, **kwargs):
        self.xsdir = kwargs.get('xsdir', '/opt/serpent2/xsdir.serp')
        self.nuclear_library = kwargs.get('nuclear_library',
                                          find_prefered_library(self.zaid,
                                                                self.xsdir))
        self.nuclear_library_file = find_prefered_library_file(self.zaid,
                                                               self.xsdir)
        self.material_card_name = self.name

    def find_symbol_from_protons(self):
        return NDATA.loc[NDATA['Proton number'] == self.protons].index[0]

    def find_protons_from_symbol(self):
        p = NDATA.loc[self.symbol]['Proton number']
        if type(p) == np.int64:
            return p
        else:
            return p.unique()[0]

    def find_element_name(self):
        n = NDATA.loc[self.symbol]['Name']
        if isinstance(n, str):
            return n
        else:
            return n.unique()[0]

    def serpent_material_card(self, name=None, color=None):
        mat_card = super().serpent_header(name, color)
        mat_card += '   '+(self.zaid+self.nuclear_library).ljust(11) +\
            ' 1'.ljust(22)+' % '+self.name+'\n'
        return mat_card


class Element(Isotope):
    def __init__(self, *args, **kwargs):

        if len(args)==1:
            protons_or_symbol=args[0]
        self.classname = self.__class__.__name__

        self.symbol = kwargs.get('symbol')

        self.protons = kwargs.get('protons')

        if self.protons == None and self.symbol == None:
            if isinstance(protons_or_symbol,int):
                self.protons=protons_or_symbol

            elif isinstance(protons_or_symbol,str):
                self.symbol = protons_or_symbol

        if self.symbol ==None:
            self.symbol = self.find_symbol_from_protons()
        if self.protons ==None:
            self.protons = self.find_protons_from_symbol()

        self.isotopes = kwargs.get('enriched_isotopes')
        if self.isotopes == None :
            self.isotopes = self.find_natural_isotopes_in_element_from_symbol(self.symbol)#looks at natural abundances
        else:
            self.isotopes = self.check_enriched_isotopes_in_element()

        self.packing_fraction=kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.material_card_name = kwargs.get('material_card_name')
        if self.material_card_name == None:

            self.material_card_name = self.find_element_name()

        self.molar_mass_g = self.find_molar_mass_g()

        self.color = kwargs.get('color')

    def check_enriched_isotopes_in_element(self):
        cumlative_abundance = 0
        for isotope in self.isotopes:

            cumlative_abundance = cumlative_abundance + isotope.abundance
            if isotope.symbol != self.symbol:
                raise ValueError(
                    'When creating an Element and specifying Isotopes present '
                    'they must be isotopes of that element')
        if cumlative_abundance != 1.0:
            raise ValueError('When creating and Element and specifying '
                             'Isotopes present within an Element their '
                             'abundance must sum to 1.0')
        return self.isotopes

    def find_natural_isotopes_in_element_from_symbol(self, symbol):
        isotopes_to_return = []
        isotopes = NAT_NDATA.loc[self.symbol]['Nucleon number']
        if isinstance(isotopes, np.float64):
            isotopes = [isotopes]
        else:
            isotopes = isotopes.values
        for i in isotopes:
            isotopes_to_return.append(Isotope(symbol=symbol, nucleons=i))
        if len(isotopes_to_return) == 0:
            raise ValueError('Natural composition of isotope not found for ',
                             symbol)
        return isotopes_to_return

    def find_molar_mass_g(self):
        element_mass = 0
        for isotope in self.isotopes:
            element_mass += isotope.abundance * isotope.mass_amu
        return element_mass

    def serpent_material_card(self, name=None, color=None):
        mat_card = super().serpent_header(name, color)
        for i in self.isotopes:
            mat_card += '   '+(i.zaid+i.nuclear_library).ljust(11)+' ' + \
                str(i.abundance).ljust(22)+' % '+i.material_card_name+'\n'
        return mat_card


class Material(Base):
    def __init__(self, **kwargs):
        self.classname = self.__class__.__name__
        self.elements = kwargs.get('elements')
        self.atom_fractions = kwargs.get('atom_fractions')
        self.mass_fractions = kwargs.get('mass_fractions')
        self.description = kwargs.get('description')
        self.material_card_name = kwargs.get('material_card_name',
                                             self.description)
        self.packing_fraction=kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')
        self.color = kwargs.get('color')
        
        if self.elements is None:
            raise ValueError('A list of elements present within the material '
                             'must be specified.')

        self.material_card_name = kwargs.get('material_card_name',self.description)

        if self.elements == None:
            raise ValueError('A list of elements present within the material '
                             'must be specified.')

        if self.atom_fractions == None and self.mass_fractions == None:
            raise ValueError('To make a material either atom_fractions or '
                             'mass_fractions must be provided.')

        if self.atom_fractions is None:
            self.atom_fractions  = self.find_atom_fractions_from_mass_fractions()

        if self.mass_fractions is None:
            self.mass_fractions = self.find_mass_fractions_from_atom_fractions()

        if len(self.elements) != len(self.atom_fractions):
            raise ValueError('When making a material please provide the same '
                             'number of elements and atom/mass fractions.')
        self.isotopes = []
        for element in self.elements:
            for isotope in element.isotopes:
                self.isotopes.append(isotope)
        self.isotope_fractions = []
        for element, atom_fraction in zip(self.elements, self.atom_fractions):
            for isotope in element.isotopes:
                self.isotope_fractions.append(atom_fraction*isotope.abundance)

    def find_atom_fractions_from_mass_fractions(self):
        list_of_atom_fractions = []
        for mass_fraction, element in zip(self.mass_fractions, self.elements):
            list_of_atom_fractions.append(mass_fraction/element.molar_mass_g)
        return list_of_atom_fractions

    def find_mass_fractions_from_atom_fractions(self):
        list_of_mass_fractions = []
        for atom_fraction, element in zip(self.atom_fractions, self.elements):
            list_of_mass_fractions.append(atom_fraction*element.molar_mass_g)
        return list_of_mass_fractions

    def serpent_material_card(self, name=None, color=None):
        mat_card = super().serpent_header(name, color)
        for i, i_f in zip(self.isotopes, self.isotope_fractions):
            mat_card += '   '+(i.zaid + i.nuclear_library).ljust(11)+' ' + \
                str(i_f).ljust(22)+' % '+i.name+'\n'
        return mat_card


class Compound(Base):

    def __init__(self, chemical_equation, **kwargs):
        self.classname = self.__class__.__name__
        self.packing_fraction = kwargs.get('packing_fraction', 1.0)
        self.color = kwargs.get('color')
        self.chemical_equation = chemical_equation
        self.material_card_name = kwargs.get('material_card_name',
                                             self.chemical_equation)
        self.state_of_matter = kwargs.get('state_of_matter', 'solid')
        self.enriched_isotopes = kwargs.get('enriched_isotopes', None)
        self.volume_of_unit_cell_cm3 = kwargs.get('volume_of_unit_cell_cm3')
        self.atoms_per_unit_cell = kwargs.get('atoms_per_unit_cell')
        self.temperature_K = kwargs.get('temperature_K')
        self.pressure_Pa = kwargs.get('pressure_Pa')
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.fractions_coefficients = self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)
        self.elements = self.find_elements_in_chemical_equation(chemical_equation)

        self.atom_fractions = self.get_atom_fractions_from_chemical_equations(chemical_equation)
        self.isotopes = self.find_isotopes_in_chemical_equation()
        self.isotope_fractions = self.find_isotope_fractions_in_chemical_equation()
        self.molar_mass = self.find_molar_mass()

        self.average_atom_mass = self.find_average_atom_mass()
        if self.density_g_per_cm3 is None:
            self.density_g_per_cm3 = self.find_density_g_per_cm3()
        if self.density_atoms_per_barn_per_cm is None:
            self.density_atoms_per_barn_per_cm = self.find_density_atoms_per_barn_per_cm()

    def find_isotope_fractions_in_chemical_equation(self):
        isotope_fractions = []
        for element, atom_fraction in zip(self.elements, self.atom_fractions):
            for isotope in element.isotopes:
                isotope_fractions.append(atom_fraction*isotope.abundance)
        return isotope_fractions

    def find_isotopes_in_chemical_equation(self):
        isotopes = []
        for element in self.elements:
            for isotope in element.isotopes:
                isotopes.append(isotope)
        return isotopes

    def serpent_material_card(self, name=None, color=None):
        mat_card = super().serpent_header(name, color)
        for i, i_f in zip(self.isotopes, self.isotope_fractions):
            mat_card += '   '+(i.zaid+i.nuclear_library).ljust(11)+' ' + \
                str(i_f).ljust(22)+' % '+i.material_card_name+'\n'
        return mat_card

    def find_average_atom_mass(self):
        masses = []
        for e, n_e_a in zip(self.elements, self.fractions_coefficients):
            element_mass = 0
            for isotope in e.isotopes:
                element_mass += isotope.abundance * isotope.mass_amu
            masses.append(element_mass*n_e_a)
        return (sum(masses)/sum(self.fractions_coefficients))*1.66054e-24

    @staticmethod
    def _read_chem_eq(chemical_equation):
        return [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]

    def find_elements_in_chemical_equation(self, chemical_equation):
        chemical_equation_chopped_up = self._read_chem_eq(chemical_equation)
        list_elements = []
        enriched_element_symbol = ''
        if self.enriched_isotopes is not None:
            enriched_element_symbol = self.enriched_isotopes[0].symbol
            for isotope in self.enriched_isotopes:
                if isotope.symbol != enriched_element_symbol:
                    raise ValueError('Enriched isotopes must all be from the '
                                     'same element.')
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                element_symbol = chemical_equation_chopped_up[counter]
                if element_symbol == enriched_element_symbol:
                    list_elements.append(Element(symbol=element_symbol,
                                                 enriched_isotopes=self.enriched_isotopes))
                else:
                    list_elements.append(Element(symbol=element_symbol))
        return list_elements

    def get_atom_fractions_from_chemical_equations(self, chemical_equation):
        list_of_fractions = []
        chemical_equation_chopped_up = self._read_chem_eq(chemical_equation)
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                try:
                    if is_number(chemical_equation_chopped_up[counter+1]):
                        list_of_fractions.append(float(chemical_equation_chopped_up[counter + 1]))
                    else:
                        list_of_fractions.append(1)
                except:
                    list_of_fractions.append(1)
        a = sum(list_of_fractions)
        b = 1.0
        rtol = 1e-6
        if not abs(a-b) <= rtol*max(abs(a), abs(b)):
            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor *
                                                    fraction)
            return normalised_list_of_fractions
        return list_of_fractions

    def find_fractions_coefficients_in_chemical_equation(self, chemical_equation):
        chemical_equation_chopped_up = self._read_chem_eq(chemical_equation)
        list_fraction = []
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                try:
                    if is_number(chemical_equation_chopped_up[counter + 1]):
                        list_fraction.append(float(chemical_equation_chopped_up[counter + 1]))
                    else:
                        list_fraction.append(1.0)
                except:
                    list_fraction.append(1.0)
        return list_fraction        

    def find_molar_mass(self):
        masses = []
        for element in self.elements:
            element_mass = 0
            for i in element.isotopes:
                element_mass = element_mass+i.abundance*i.mass_amu
            masses.append(element_mass)
        cumlative_molar_mass = 0
        for mass, fraction in zip(masses, self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)):
            cumlative_molar_mass = cumlative_molar_mass+(mass*float(fraction))
        return cumlative_molar_mass

    def density_g_per_cm3_idea_gas(self):
        density_kg_m3 = (self.pressure_Pa/(8.3* self.temperature_K)) * \
                        self.molar_mass * 6.023e23*1.66054e-27
        density_g_cm3 = density_kg_m3/1000.0
        return density_g_cm3

    def density_g_per_cm3_liquid(self):
        from thermo.chemical import Chemical
        hot_pressurized_liquid = Chemical(self.chemical_equation,
                                          T=self.temperature_K,
                                          P=self.pressure_Pa)
        return hot_pressurized_liquid.rho*0.001

    def find_density_g_per_cm3(self):
        if self.state_of_matter == 'solid' and self.volume_of_unit_cell_cm3 is not None and self.atoms_per_unit_cell is not None:
            return (self.molar_mass*1.66054e-24*self.atoms_per_unit_cell / self.volume_of_unit_cell_cm3)
        if self.density_atoms_per_barn_per_cm is not None:
            return (self.density_atoms_per_barn_per_cm/1e-24)*self.average_atom_mass
        if self.state_of_matter == 'gas' and self.pressure_Pa is not None and self.temperature_K is not None:
            return self.density_g_per_cm3_idea_gas()
        if self.state_of_matter == 'liquid' and self.pressure_Pa is not None and self.temperature_K is not None:
            return self.density_g_per_cm3_liquid()
        return None

    def find_density_atoms_per_barn_per_cm(self):
        if self.atoms_per_unit_cell is not None and self.volume_of_unit_cell_cm3 is not None:
            return (self.atoms_per_unit_cell/self.volume_of_unit_cell_cm3)*1e-24
        if self.density_g_per_cm3 is not None and self.volume_of_unit_cell_cm3 is not None:
            return (self.density_g_per_cm3/self.molar_mass)*6.023e23*1e-24
        return None


class Homogenised_mixture(Base):

    def __init__(self, mixtures, **kwargs):
        self.classname = self.__class__.__name__
        self.color = kwargs.get('color')
        self.mixtures = mixtures
        self.mass_fractions = kwargs.get('mass_fractions')
        self.volume_fractions = kwargs.get('volume_fractions')
        self.packing_fraction=kwargs.get('packing_fraction', 1.0)
        # self.packing_fractions=self.find_packing_fractions_of_mixtures(self.mixtures)

        if self.volume_fractions is None and self.mass_fractions is None:
            raise ValueError('volume_fractions or mass_fractions must be '
                             'specified.')
        if self.volume_fractions is None:
            self.volume_fractions = self.find_volume_fractions_from_mass_fractions()
            self.material_card_name = self.find_material_card_name_with_mass_fractions()
        if self.mass_fractions is None:
            self.mass_fractions = self.find_mass_fractions_from_volume_fractions()
            self.material_card_name = self.find_material_card_name_with_volume_fractions()

        self.density_g_per_cm3 = self.find_density_g_per_cm3(self.mixtures,self.volume_fractions)
        
    def find_volume_fractions_from_mass_fractions(self):
        if math.isclose(sum(self.mass_fractions), 1.0,rel_tol=1e-09)==False:
            raise ValueError('The provided mass fractions should sum to 1 not ',
                             sum(self.volume_fractions))

        list_of_non_normalised_volume_fractions = []
        cumlative_vol_fraction = 0
        for mix,mass_fraction in zip(self.mixtures,self.mass_fractions):
            non_normalised_volume_fractions = mass_fraction/mix.density_g_per_cm3
            list_of_non_normalised_volume_fractions.append(non_normalised_volume_fractions)
            cumlative_vol_fraction = cumlative_vol_fraction+ non_normalised_volume_fractions
        factor = 1.0/cumlative_vol_fraction

        normalised_volume_fractions=[]
        for non_normalised_volume_fractions in list_of_non_normalised_volume_fractions:
            normalised_volume_fractions.append(non_normalised_volume_fractions*factor)
        return normalised_volume_fractions
        
    def find_mass_fractions_from_volume_fractions(self):
        if math.isclose(sum(self.volume_fractions), 1.0,rel_tol=1e-09)==False:
        #if sum(self.volume_fractions) != 1.0:
            raise ValueError('The provided volume fractions should sum to 1 not ',
                             sum(self.volume_fractions))
        list_of_non_normalised_mass_fractions = []
        cumlative_mass_fraction = 0
        for mix, vol_fraction in zip(self.mixtures, self.volume_fractions):
            non_normalised_mass_fractions = vol_fraction * mix.density_g_per_cm3
            list_of_non_normalised_mass_fractions.append(non_normalised_mass_fractions)
            cumlative_mass_fraction = cumlative_mass_fraction + non_normalised_mass_fractions
        factor = 1.0 / cumlative_mass_fraction

        normalised_mass_fractions = []
        for non_normalised_mass_fractions in list_of_non_normalised_mass_fractions:
            normalised_mass_fractions.append(non_normalised_mass_fractions * factor)
        return normalised_mass_fractions

    def find_density_g_per_cm3(self,mixtures,volume_fractions):
        cumlative_density = 0
        for mixture, volume in zip(mixtures,volume_fractions):
            cumlative_density = cumlative_density + (mixture.density_g_per_cm3 * volume *mixture.packing_fraction)
        # TODO: allow density combinations involving atom_per_barn_cm2
        return cumlative_density

    def find_material_card_name_with_volume_fractions(self):
        description_to_return = ''
        for item, vol_frac in zip(self.mixtures,self.volume_fractions):
            description_to_return += item.material_card_name+'_vf_'+str(vol_frac)+'_'
        return  description_to_return[:-1]

    # def find_packing_fractions_of_mixtures(self,mixtures):
    #     packing_fractions=[]
    #     print(self.mixtures)
    #     for mixture, in mixtures:
    #         packing_fractions.append(mixture.packing_fraction)
    #     return  packing_fractions      

    def find_material_card_name_with_mass_fractions(self):
        description_to_return = ''
        for item, frac in zip(self.mixtures, self.mass_fractions):
            description_to_return += item.material_card_name + '_mf_' + str(frac)+'_'
        return description_to_return[:-1]

    def serpent_material_card(self, name=None, color=None):
        comment = '%  '
        mat_card = super().serpent_header(name, color)
        for item, v_f, m_f in zip(self.mixtures, self.volume_fractions,
                                  self.mass_fractions):
            if item.isotopes == []:
                mat_card += comment+'\n'+comment+item.material_card_name + \
                    ' with a density of '+str(item.density_g_per_cm3) + \
                    ' g per cm3 \n'
                mat_card += comment+'volume fraction of '+str(v_f)+' \n'
                # makes no sense to have a void mass fraction material_card = material_card + comment + 'mass fraction of ' + str(mass_fraction) + ' \n'
            else:
                a = 0.0  # Average_mass_of_one_atom
                for iso, a_f in zip(item.isotopes, item.isotope_fractions):
                    a += iso.mass_amu*a_f
                # Number_of_atoms_per_cm3_of_item
                n_a_item = item.density_g_per_cm3/(a*1.66054e-24)
                # Number_of_atoms_per_cm3_of_mix
                n_a_mix = n_a_item*v_f/7.66e22
                mat_card += comment+'\n'+comment+item.material_card_name + \
                    ' with a density of '+str(item.density_g_per_cm3) + \
                    ' g per cm3 \n'
                mat_card += comment+'packing fraction of '+str(item.packing_fraction)+' \n'
                mat_card += comment+'volume fraction of '+str(v_f)+' \n'
                mat_card += comment+'mass fraction of '+str(m_f)+' \n'
                for i, a_f in zip(item.isotopes, item.isotope_fractions):
                    if a_f > 0:
                        mat_card += '   '+(i.zaid+i.nuclear_library).ljust(11) + \
                            ' '+str(a_f*n_a_mix).ljust(22)+' % '+i.name + '\n'
        return mat_card
    
# Presently unused?
class Natural_Isotopes():
    def __init__(self):
             
        self.all_natural_isotopes = self.find_all_natural_isotopes()

        #self.natural_isotopes = self.find_natural_isotopes_from_symbol(self.symbol)

    def find_all_natural_isotopes(self):
        all_isotopes = []
        for element in Natural_Elements().all_natural_elements:

            isotopes_in_element = element.isotopes
            
            all_isotopes= all_isotopes +isotopes_in_element

        return all_isotopes
            #self.find_natural_isotopes_from_symbol(element.symbol) for element in ]


class Natural_Elements():
    def __init__(self):

        self.all_natural_elements = self.find_all_natural_elements()

        self.all_natural_element_symbols = self.find_all_natural_element_symbols()


    def find_all_natural_element_symbols(self):
        return list(set(NAT_NDATA.index))

    def find_all_natural_elements(self):
        return [Element(e) for e in list(set(NAT_NDATA.index))]

