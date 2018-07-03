# Python

import re

from natsort import natsorted

from neutronics_material_maker.utilities import (arevaluesthesame,
                                                 color_manager, is_number,
                                                 normalise_list)
import numpy as np

import pandas as pd

import pkg_resources


nuclear_data_file_path = pkg_resources.resource_filename('neutronics_material_maker', 'nuclear_data.csv')

NDATA = pd.read_csv(nuclear_data_file_path, index_col='Symbol')
NAT_NDATA = NDATA[NDATA['Natural']]
XSDIR = '/opt/serpent2/xsdir.serp'  # Default xsdir.serp file location

atomic_mass_unit_in_g = 1.660539040e-24
atomic_mass_unit_in_kg = 1.660539040e-27
Avogadros_number = 6.022140857e23

xsdir_isotopes_and_nuclear_libraries_list = []


def set_xsdir(xsdir_file_path):
    global xsdir_isotopes_and_nuclear_libraries_list
    xsdir_isotopes_and_nuclear_libraries_list = []
    try:
        filecontents = open(xsdir_file_path, "r").readlines()
        for line in filecontents:
            chopped_up_line = line.split()[0].split('.')
            xsdir_isotopes_and_nuclear_libraries_list.append(chopped_up_line)
    except:
        print('Warning xsdir file not found in default path /opt/serpent/xsdir.serp')
        print('Setting all nuclear library extensions to blank entries')


set_xsdir('/opt/serpent2/xsdir.serp')


def find_prefered_library(zaid):
    if len(xsdir_isotopes_and_nuclear_libraries_list) == 0:
        return ''
    for isotope_and_nuclear_library in xsdir_isotopes_and_nuclear_libraries_list:
        if isotope_and_nuclear_library[0] == zaid:
                return '.' + isotope_and_nuclear_library[1]
    return ''


def calculate_zaid(z, a):
    z, a = int(z), int(a)  # String formatting for screwed up with e.g. 11.0
    zaid = str(z) + str(a).zfill(3)
    return zaid


class Base(object):

    def material_card_header(self, material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3, **kwargs):

        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = self.kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3)
        if self.density_g_per_cm3 is None and self.density_atoms_per_barn_per_cm is None:
            raise ValueError('To produce a material card the '
                             'density_g_per_cm3 or '
                             'density_atoms_per_barn_per_cm must be provided.')

        if self.density_g_per_cm3 is None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm)
        else:
            density = ' -' + str(self.density_g_per_cm3)

        color = color_manager(color)

        if code == 'serpent':
            tmp = ' tmp ' + str(temperature_K) + ' '
            mat_card = [comment, comment + material_card_comment,
                        'mat ' + material_card_name + density + tmp + color]
        elif code == 'mcnp':
            if type(material_card_number) != int:

                print('WARNING. To create an MCNP materail card the material_card_name must include an integer value. For example material_card_name="M1"')

            mat_card = [comment,
                        comment + material_card_comment,
                        comment + 'density =' + str(self.density_g_per_cm3) + ' g/cm3',
                        comment + 'density =' + str(self.density_atoms_per_barn_per_cm) + ' atoms per barn cm2',
                        comment + 'temperature =' + str(temperature_K) + ' K',
                        'M' + str(material_card_number)]

        elif code == 'fispact':
            if self.classname == 'Isotope':
                number_of_isotopes = '1'
            else:
                number_of_isotopes = str(len(self.isotopes))
            mat_card = [comment + material_card_name + end_comment,
                        comment + material_card_comment + end_comment,
                        #comment + 'density ='+str(self.density_g_per_cm3) + ' g/cm3' + end_comment,
                        comment + 'density ='+str(self.density_atoms_per_barn_per_cm) + ' atoms per barn cm2' + end_comment,
                        comment + 'temperature ='+str(temperature_K) + ' K' + end_comment,
                        'DENSITY ' +str(self.density_g_per_cm3),
                        'FUEL '+number_of_isotopes]



        return mat_card

 
    def find_symbol_from_protons(self):
        return NDATA.loc[NDATA['Proton number'] == self.protons].index[0]

    def find_protons_from_symbol(self):
        p = NDATA.loc[self.symbol]['Proton number']
        if type(p) == np.int64:
            return p
        else:
            return p.unique()[0]    
    
    def find_protons_from_zaid(self):
        if "." in self.zaid:
            k = self.zaid.find(".")
        else:
            k = len(self.zaid) + 1
        zaid = self.zaid[:k]
        protons = int(zaid[:-3])
        return protons
        
    def find_nucleons_from_zaid(self):
        if "." in self.zaid:
            k = self.zaid.find(".")
        else:
            k = len(self.zaid) + 1
        zaid = self.zaid[:k]
        nucleons = int(zaid[-3:])
        #print('looking for ',self.zaid,' found ',nucleons)
        return nucleons

    def find_element_name(self):
        n = NDATA.loc[self.symbol]['Name']
        if isinstance(n, str):
            return n
        else:
            return n.unique()[0]

    def find_molar_mass_g_per_mol(self):
        #equations from https://en.wikipedia.org/wiki/Molar_mass
        cumlative_molar_mass=0

        if self.isotope_atom_fractions != None:
            for i, i_a_f in zip(self.isotopes, self.isotope_atom_fractions):
                cumlative_molar_mass = cumlative_molar_mass+(i.mass_amu*i_a_f)
        elif self.isotope_mass_fractions != None:
            for i, i_m_f in zip(self.isotopes, self.isotope_mass_fractions):
                cumlative_molar_mass = cumlative_molar_mass+(i_m_f/i.mass_amu)
            cumlative_molar_mass=1.0/cumlative_molar_mass

        return cumlative_molar_mass

    def find_density_of_atoms_per_cm3(self):

        if self.classname == 'Isotope':
            return self.density_g_per_cm3/self.mass_amu

        if self.isotopes == []:
            return 0
        if(self.density_g_per_cm3)==None:
            return None
        #todo use the density_g_per_barn_cm as an option if density_g_per_cm3 is not available

        a = 0.0  # Average_mass_of_one_atom
        for iso, a_f in zip(self.isotopes, self.isotope_atom_fractions):
            a += iso.mass_amu*a_f

        # Number_of_atoms_per_cm3_of_item
        
        number_of_atoms = self.density_g_per_cm3/(a*atomic_mass_unit_in_g)
        return number_of_atoms

    def kwarg_handler(self, material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3):
        if material_card_name is None:
            material_card_name = self.material_card_name
        if material_card_name is None:
            material_card_name = 'unnamed_material' 
        if material_card_comment is None:
            material_card_comment = self.material_card_comment
            if material_card_comment is None:
                material_card_comment= 'Made with https://github.com/ukaea/neutronics_material_maker'           

        if material_card_number is None:
            material_card_number = self.material_card_number

        if color is None:
            color = self.color
            if color is None:
                color = (0, 0, 0) 

        if fractions is None or fractions == 'isotope atom fractions':
            fractions = 'isotope atom fractions'
            fractions_prefix = ' '
        elif fractions=='isotope mass fractions':
            fractions_prefix = ' -'

        if temperature_K is None:
            temperature_K= self.temperature_K

        if volume_cm3 is None:
            volume_cm3= self.volume_cm3
            if code =='fispact' and volume_cm3 == None:
                raise ValueError('To produce a fispact material card the '
                                 'volume_cm3 must be provided')

        if code is None or code =='serpent':
            code = 'serpent'
            end_comment = ' % '
            comment = '%  '
        elif code.lower() =='mcnp':
            end_comment = ' $ ' 
            comment = 'c  '
            code ='mcnp'
        elif code.lower() =='fispact':
            end_comment = ' >> ' 
            comment = '<< '
            code ='fispact'            

        return material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3




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

        self.symbol = kwargs.get('symbol', None)
        self.zaid = kwargs.get('zaid', None)
        self.protons = kwargs.get('protons', None)
        self.nucleons = kwargs.get('nucleons', None)
        self.color = kwargs.get('color', (0, 0, 0))

        self._handle_args(args)

        self.temperature_K = kwargs.get('temperature_K',293.15)

        if self.nucleons is None and self.zaid is None:
            raise ValueError('To create an Isotope provide an isotope the symbol / proton number along with a nucleon number or a zaid.')

        if self.protons is None and self.symbol is None and self.zaid is None:
            raise ValueError('To create an Isotope provide either protons or '
                             'symbol or zaid please.')
        


        if self.zaid!= None:
            self.protons = self.find_protons_from_zaid()
            self.nucleons = self.find_nucleons_from_zaid()
            
        if self.protons is None:
            self.protons = self.find_protons_from_symbol()
        if self.symbol is None:
            self.symbol = self.find_symbol_from_protons()
        self._sanity()

        self.mass_amu = NDATA[(NDATA['Proton number'] == self.protons) & 
                              (NDATA['Nucleon number'] == self.nucleons)]['Mass amu'][0]        
        self._handle_kwargs(kwargs)

        self.element_name = self.find_element_name()
        self.name = self.element_name+'_'+str(self.nucleons)

        self.material_card_name = kwargs.get('material_card_name')
        self.material_card_number = kwargs.get('material_card_number')
        self.material_card_comment = kwargs.get('material_card_comment')

        if self.material_card_name == None:
            self.material_card_name = self.name 
        self.neutrons = self.nucleons-self.protons
        self.natural_abundance = NDATA[(NDATA['Proton number'] == self.protons) & 
                                       (NDATA['Nucleon number'] == self.nucleons)]['Natural abundance'][0]

        self.abundance = kwargs.get('abundance', self.natural_abundance)
        if self.abundance and self.abundance > 1.0 or self.abundance < 0.0:
            raise ValueError('Abundance of isotope can not be greater than 1.0'
                             ' or less than 0.')
                             
        self.zaid = calculate_zaid(self.protons, self.nucleons)
        self._get_xs_files()
        self.volume_cm3 = kwargs.get('volume_cm3')

    def _handle_kwargs(self, kwargs):


        self.packing_fraction=kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3', None)
        #self.density_atoms_cm3 = kwargs.get('density_atoms_per_cm3', None)
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm', None)
        self.density_atoms_per_cm3 = kwargs.get('density_atoms_per_cm3',None)

        #adjust densities with packing fraction
        if self.density_g_per_cm3 !=None:
            self.density_g_per_cm3 = self.density_g_per_cm3*self.packing_fraction
        if self.density_atoms_per_barn_per_cm != None:
            self.density_atoms_per_barn_per_cm = self.density_atoms_per_barn_per_cm*self.packing_fraction
        if self.density_atoms_per_cm3 != None:
            self.density_atoms_per_cm3 = self.density_atoms_per_cm3*self.packing_fraction
        if self.density_atoms_per_cm3 == None:
            self.density_atoms_per_cm3 = self.find_density_of_atoms_per_cm3() 

        # if self.density_atoms_per_cm3 != None:
        #     self.density_atoms_per_cm3 = self.density_atoms_per_cm3*self.packing_fraction


    def _handle_args(self, args):

        atomic_number_or_proton_number = []
        if len(args)==1 and self.zaid is None:
                self.zaid = args[0]
                self.protons = self.find_protons_from_zaid()
                self.nucleons = self.find_nucleons_from_zaid()
                self.symbol = self.find_symbol_from_protons()
        else:        

            for arg in args:
                if isinstance(arg, str) and self.symbol is None and len(arg)<=2:
                    self.symbol = arg
                    self.protons = self.find_protons_from_symbol()                
                elif isinstance(arg, int):
                    atomic_number_or_proton_number.append(arg)

            if self.nucleons is None and len(atomic_number_or_proton_number) >= 1:
                self.nucleons = max(atomic_number_or_proton_number)
            if self.protons is None and len(atomic_number_or_proton_number) >= 1:
                self.protons = min(atomic_number_or_proton_number)



    def _sanity(self):
        if NDATA[(NDATA['Proton number'] == self.protons) &
                 (NDATA['Nucleon number'] == self.nucleons)].empty:
            raise ValueError('This isotope Symbol={} nucleons={} protons={} either does not exist, or '
                             'you have no data for it.'.format(self.symbol,
                                                               self.nucleons,
                                                               self.protons))

    def find_density_of_atoms_per_cm3(self):
        if self.density_g_per_cm3 != None:
            return self.density_g_per_cm3/(self.mass_amu*atomic_mass_unit_in_g)
        else:
            return None

    def find_density_atoms_per_barn_per_cm(self):
        if self.density_g_per_cm3 == 0:
            return 0
        if self.density_g_per_cm3 is not None and self.molar_mass_g_per_mol is not None:
            return (self.density_g_per_cm3/self.molar_mass_g_per_mol)*Avogadros_number*1e-24

    def find_density_g_per_cm3(self):
        if self.density_atoms_per_barn_per_cm == 0:
            return 0        
        if self.density_atoms_per_barn_per_cm is not None:
            return (self.density_atoms_per_barn_per_cm/1e-24)*self.average_atom_mass


    def _get_xs_files(self, **kwargs):

        self.xsdir = kwargs.get('xsdir', XSDIR)

        self.nuclear_library = kwargs.get('nuclear_library',
                                          find_prefered_library(self.zaid))



    def material_card(self, material_card_comment=None, material_card_name=None, material_card_number=None, fractions=None, color=None,code=None, temperature_K=None, volume_cm3=None):
        mat_card=super(Isotope,self).material_card_header(material_card_comment,material_card_name, material_card_number, color, code, fractions,temperature_K,volume_cm3)
        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = super(Isotope,self).kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3)

        if code == 'mcnp' or code == 'serpent':
            if fractions == 'isotope atom fractions':
                mat_card.append('   '+(self.zaid+self.nuclear_library).ljust(11) +' 1'.ljust(24)+end_comment+self.name)
                
            if fractions == 'isotope mass fractions':
                mat_card.append('   '+(self.zaid+self.nuclear_library).ljust(11) +' -1'.ljust(24)+end_comment+self.name)


        elif code == 'fispact':

            mat_card.append(self.symbol + str(self.nucleons)+' '+ str(self.density_atoms_per_cm3 * 1.0 * volume_cm3))

        return '\n'.join(mat_card)


class Element(Base):
    def __init__(self, *args, **kwargs):

        if len(args) == 1:
            protons_or_symbol_or_zaid=args[0]
        self.classname = self.__class__.__name__
        self.symbol = kwargs.get('symbol')
        self.protons = kwargs.get('protons')
        self.zaid = kwargs.get('zaid')
        if self.protons == None and self.symbol == None and self.zaid == None:
            if isinstance(protons_or_symbol_or_zaid,int):
                self.protons=protons_or_symbol_or_zaid

            elif isinstance(protons_or_symbol_or_zaid,str) and protons_or_symbol_or_zaid[0].isdigit()==False:
                self.symbol = protons_or_symbol_or_zaid
                
            else:
                self.zaid = protons_or_symbol_or_zaid
                

        self.temperature_K = kwargs.get('temperature_K',293.15)

        
        if self.zaid != None:
            self.protons = self.find_protons_from_zaid()
        if self.symbol ==None:
            self.symbol = self.find_symbol_from_protons()
        if self.protons ==None:
            self.protons = self.find_protons_from_symbol()

        self.isotopes = kwargs.get('enriched_isotopes')
        if self.isotopes == None :
            self.isotopes = self.find_natural_isotopes_in_element_from_symbol(self.symbol)#looks at natural abundances
        else:
            self.isotopes = self.check_enriched_isotopes_in_element()


        self.isotope_atom_fractions=[]
        for i in self.isotopes: 
            self.isotope_atom_fractions.append(i.abundance)

        self.molar_mass_g_per_mol = self.find_molar_mass_g_per_mol()

        self.isotope_mass_fractions=[]
        for i in self.isotopes:
            self.isotope_mass_fractions.append((i.mass_amu*i.abundance)/self.molar_mass_g_per_mol)

        self.volume_cm3 = kwargs.get('volume_cm3')
        self.packing_fraction=kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_cm3 = kwargs.get('density_atoms_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.material_card_name = kwargs.get('material_card_name')
        self.material_card_number = kwargs.get('material_card_number')
        self.material_card_comment = kwargs.get('material_card_comment')

        if self.material_card_name == None:
            self.material_card_name = self.find_element_name()           

        self.color = kwargs.get('color')

        #adjust densities with packing fraction
        if self.density_g_per_cm3 !=None:
            self.density_g_per_cm3 = self.density_g_per_cm3*self.packing_fraction
        if self.density_atoms_per_barn_per_cm != None:
            self.density_atoms_per_barn_per_cm = self.density_atoms_per_barn_per_cm*self.packing_fraction
        if self.density_atoms_per_cm3 != None:
             self.density_atoms_per_cm3 = self.density_atoms_per_cm3*self.packing_fraction
        if self.density_atoms_per_cm3 == None:
            self.density_atoms_per_cm3 = super(Element,self).find_density_of_atoms_per_cm3()             


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
        isotopes=[int(i) for i in isotopes]
        for i in isotopes:
            isotopes_to_return.append(Isotope(symbol=symbol, nucleons=i))
        if len(isotopes_to_return) == 0:
            raise ValueError('Natural composition of isotope not found for ',
                             symbol)
        return isotopes_to_return




    def material_card(self, material_card_comment=None, material_card_name=None, material_card_number=None, color=None,code=None, fractions=None, temperature_K=None, volume_cm3=None):

        mat_card = super(Element, self).material_card_header(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K,volume_cm3)
        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = super(Element,self).kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3)


        if code == 'mcnp' or code == 'serpent':
            if fractions=='isotope atom fractions':
                for i , a_f in zip(self.isotopes,self.isotope_atom_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11)+
                                    fractions_prefix + str(a_f).ljust(24)+
                                    end_comment+i.name)

            if fractions=='isotope mass fractions':
                for i , m_f in zip(self.isotopes, self.isotope_mass_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11) +
                                    fractions_prefix + str(m_f).ljust(24) +
                                    end_comment + i.name)

        elif code == 'fispact':
            for i, i_a_f in zip(self.isotopes, self.isotope_atom_fractions):
                mat_card.append(i.symbol + str(i.nucleons)+' '+ str(self.density_atoms_per_cm3 * i_a_f * volume_cm3))

        return '\n'.join(mat_card)


class Material(Base):
    def __init__(self, **kwargs):
        self.classname = self.__class__.__name__
        self.elements = kwargs.get('elements', None)
        self.element_atom_fractions = kwargs.get('element_atom_fractions', None)
        self.element_mass_fractions = kwargs.get('element_mass_fractions', None)
        self.isotopes = kwargs.get('isotopes', None)
        self.isotope_mass_fractions = kwargs.get('isotope_mass_fractions', None)
        self.isotope_atom_fractions = kwargs.get('isotope_atom_fractions', None)

        self.material_card_name = kwargs.get('material_card_name', 'unnamed_material')
        self.material_card_number = kwargs.get('material_card_number')
        self.material_card_comment = kwargs.get('material_card_comment')

        self.temperature_K = kwargs.get('temperature_K', 293.15)

        self.packing_fraction = kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')
        self.density_atoms_per_cm3 = kwargs.get('density_atoms_per_cm3')
        self.volume_cm3 = kwargs.get('volume_cm3')

        self.color = kwargs.get('color')

        if self.elements == None and self.isotopes == None:
            raise ValueError('A list of elements or isotopes within the '
                             ' material must be specified.')

        # if self.element_atom_fractions == None and self.element_mass_fractions == None:
        #     raise ValueError('To make a material from elements either element_atom_fractions or '
        #                      'element_mass_fractions must be provided.')

        if self.elements != None:
            if self.element_atom_fractions == None:
                self.element_atom_fractions  = self.find_element_atom_fractions_from_element_mass_fractions()

            if self.element_mass_fractions == None:
                self.element_mass_fractions = self.find_element_mass_fractions_from_element_atom_fractions()

            if len(self.elements) != len(self.element_atom_fractions):
                raise ValueError('When making a material please provide the same'
                                 'number of elements and atom/mass fractions.')

        if self.isotopes == None and self.elements != None:
            self.isotopes=[]
            for element in self.elements:
                for isotope in element.isotopes:
                    self.isotopes.append(isotope)

        if self.isotope_atom_fractions == None and self.elements != None:
            self.isotope_atom_fractions=[]
            for element, atom_fraction in zip(self.elements, self.element_atom_fractions):
                for isotope in element.isotopes:
                    self.isotope_atom_fractions.append(atom_fraction*isotope.abundance)

        self.molar_mass_g_per_mol = self.find_molar_mass_g_per_mol()
        self.average_atom_mass = self.molar_mass_g_per_mol / Avogadros_number

        if self.isotope_atom_fractions == None and self.isotope_mass_fractions!=None:     
            self.isotope_atom_fractions = []
            for isotope, isotope_mass_fraction in zip(self.isotopes, self.isotope_mass_fractions):
                self.isotope_atom_fractions.append(isotope_mass_fraction / (isotope.mass_amu/self.molar_mass_g_per_mol)) 

        if self.isotope_mass_fractions == None:
            self.isotope_mass_fractions = []
            for isotope, isotope_atom_fraction in zip(self.isotopes, self.isotope_atom_fractions):
                self.isotope_mass_fractions.append(isotope_atom_fraction * (isotope.mass_amu/self.molar_mass_g_per_mol))

        self.isotope_mass_fractions = normalise_list(self.isotope_mass_fractions)
        self.isotope_atom_fractions = normalise_list(self.isotope_atom_fractions)

        if self.density_g_per_cm3 == None:
            self.density_g_per_cm3 = self.find_density_g_per_cm3()
        if self.density_atoms_per_barn_per_cm == None:
            self.density_atoms_per_barn_per_cm = self.find_density_atoms_per_barn_per_cm()
        if self.density_atoms_per_cm3 == None:
            self.density_atoms_per_cm3 = super(Material,self).find_density_of_atoms_per_cm3() 

        self.density_g_per_cm3 = self.density_g_per_cm3*self.packing_fraction
        self.density_atoms_per_barn_per_cm = self.density_atoms_per_barn_per_cm*self.packing_fraction
        self.density_atoms_per_cm3 = self.density_atoms_per_cm3*self.packing_fraction

    def find_element_atom_fractions_from_element_mass_fractions(self):
        if self.element_mass_fractions == []:
            return []
        list_of_fractions = []
        for mass_fraction, element in zip(self.element_mass_fractions, self.elements):
            a_f = mass_fraction / element.molar_mass_g_per_mol

            list_of_fractions.append(a_f)

        a = sum(list_of_fractions)
        b = 1.0
        rtol = 1e-6
        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            normalised_list_of_fractions = normalise_list(list_of_fractions)

            return normalised_list_of_fractions

        return list_of_fractions

    def find_element_mass_fractions_from_element_atom_fractions(self):
        if self.element_atom_fractions == []:
            return []
        list_of_fractions = []
        for atom_fraction, element in zip(self.element_atom_fractions, self.elements):
            list_of_fractions.append(atom_fraction * element.molar_mass_g_per_mol)

        a = sum(list_of_fractions)
        b = 1.0
        rtol = 1e-6
        if not abs(a - b) <= rtol * max(abs(a), abs(b)):
            normalised_list_of_fractions = normalise_list(list_of_fractions)

            return normalised_list_of_fractions
        return list_of_fractions

    def material_card(self, material_card_comment=None, material_card_name=None, material_card_number=None, color=None, code=None, fractions=None, temperature_K=None, volume_cm3=None):

        mat_card = super(Material, self).material_card_header(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K,volume_cm3)
        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = super(Material,self).kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions, temperature_K, volume_cm3)

        if code == 'serpent' or code == 'mcnp':
            if fractions == 'isotope atom fractions':
                for i, a_f, m_f in zip(self.isotopes, self.isotope_atom_fractions, self.isotope_mass_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11)+fractions_prefix + str(a_f).ljust(24)+end_comment+i.name)

            elif fractions == 'isotope mass fractions':
                for i, a_f, m_f in zip(self.isotopes, self.isotope_atom_fractions, self.isotope_mass_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11)+fractions_prefix + str(m_f).ljust(24)+end_comment+i.name)   

        elif code == 'fispact':
            for i, i_a_f in zip(self.isotopes, self.isotope_atom_fractions):
                mat_card.append(i.symbol + str(i.nucleons) + ' ' + str(self.density_atoms_per_cm3 * i_a_f * volume_cm3))

        return '\n'.join(mat_card)

    def find_density_atoms_per_barn_per_cm(self):
        if self.density_g_per_cm3 == 0:
            return 0
        if self.density_g_per_cm3 is not None and self.molar_mass_g_per_mol is not None:
            return (self.density_g_per_cm3 / self.molar_mass_g_per_mol) * Avogadros_number * 1e-24

    def find_density_g_per_cm3(self):
        if self.density_atoms_per_barn_per_cm == 0:
            return 0
        if self.density_atoms_per_barn_per_cm is not None:
            return (self.density_atoms_per_barn_per_cm / 1e-24) * self.average_atom_mass


class Compound(Base):

    def __init__(self, chemical_equation, **kwargs):
        self.classname = self.__class__.__name__
        self.color = kwargs.get('color')
        self.chemical_equation = chemical_equation

        self.material_card_name = kwargs.get('material_card_name')
        self.material_card_number = kwargs.get('material_card_number')
        self.material_card_comment = kwargs.get('material_card_comment')

        if self.material_card_name == None:
            self.material_card_name = self.chemical_equation
        if self.material_card_number == None:
            self.material_card_number = '?' 

        self.state_of_matter = kwargs.get('state_of_matter', 'solid')
        self.enriched_isotopes = kwargs.get('enriched_isotopes', None)
        self.volume_of_unit_cell_cm3 = kwargs.get('volume_of_unit_cell_cm3')
        self.atoms_per_unit_cell = kwargs.get('atoms_per_unit_cell')
        self.temperature_K = kwargs.get('temperature_K',293.15)
        self.pressure_Pa = kwargs.get('pressure_Pa')

        self.volume_cm3 = kwargs.get('volume_cm3')

        self.packing_fraction = kwargs.get('packing_fraction', 1.0)
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3', None)
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm', None)
        self.density_atoms_per_cm3 = kwargs.get('density_atoms_per_cm3', None)

        self.fractions_coefficients = self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)
        self.elements = self.find_elements_in_chemical_equation(chemical_equation)

        self.element_atom_fractions = self.get_element_atom_fractions_from_chemical_equations(chemical_equation)
        self.isotopes = self.find_isotopes_in_chemical_equation()
        self.isotope_atom_fractions = self.find_isotope_atom_fractions_in_chemical_equation()
        self.molar_mass_g_per_mol = self.find_molar_mass_g_per_mol()

        self.isotope_mass_fractions=[]
        for isotope,isotope_atom_fraction in zip(self.isotopes,self.isotope_atom_fractions):
            self.isotope_mass_fractions.append(isotope_atom_fraction*(isotope.mass_amu/self.molar_mass_g_per_mol)*sum(self.fractions_coefficients))

        self.average_atom_mass = self.find_average_atom_mass()
        if self.density_g_per_cm3 == None:
            self.density_g_per_cm3 = self.find_density_g_per_cm3()
        if self.density_atoms_per_barn_per_cm == None:
            self.density_atoms_per_barn_per_cm = self.find_density_atoms_per_barn_per_cm()
        if self.density_atoms_per_cm3 == None:
            self.density_atoms_per_cm3 = super(Compound,self).find_density_of_atoms_per_cm3()            

        if self.density_g_per_cm3 != None:
            self.density_g_per_cm3 = self.density_g_per_cm3*self.packing_fraction
        if self.density_atoms_per_barn_per_cm != None:
            self.density_atoms_per_barn_per_cm = self.density_atoms_per_barn_per_cm*self.packing_fraction
        if self.density_atoms_per_cm3 != None:
            self.density_atoms_per_cm3 = self.density_atoms_per_cm3*self.packing_fraction

    # no longer needed ?
    # def find_isotope_mass_fractions_from_isotope_atom_fractions(self):
    #     isotope_mass_fractions = []
    #     for element, atom_fraction in zip(self.elements, self.fractions_coefficients):
    #         for isotope in element.isotopes:
    #             print(atom_fraction,isotope.mass_amu,self.molar_mass_g_per_mol)
    #             isotope_mass_fractions.append(atom_fraction*(isotope.mass_amu)/self.molar_mass_g_per_mol)
    #     return isotope_mass_fractions

    def find_isotope_atom_fractions_in_chemical_equation(self):
        isotope_atom_fractions = []
        for element, atom_fraction in zip(self.elements, self.element_atom_fractions):
            for isotope in element.isotopes:
                isotope_atom_fractions.append(atom_fraction*isotope.abundance)
        return isotope_atom_fractions

    def find_isotopes_in_chemical_equation(self):
        isotopes = []
        for element in self.elements:
            for isotope in element.isotopes:
                isotopes.append(isotope)
        return isotopes


    def material_card(self, material_card_comment=None, material_card_name=None, material_card_number=None, color=None, code=None, fractions=None, temperature_K=None, volume_cm3=None):

        mat_card = super(Compound, self).material_card_header(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K,volume_cm3)
        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = super(Compound,self).kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3)

        if code == 'mcnp' or code == 'serpent':

            if fractions == 'isotope atom fractions':
                for i, a_f, m_f in zip(self.isotopes, self.isotope_atom_fractions, self.isotope_mass_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11)+fractions_prefix + str(a_f).ljust(24)+end_comment+i.name)

            elif fractions == 'isotope mass fractions':
                for i, a_f, m_f in zip(self.isotopes, self.isotope_atom_fractions, self.isotope_mass_fractions):
                    mat_card.append('   ' + (i.zaid + i.nuclear_library).ljust(11)+fractions_prefix + str(m_f).ljust(24)+end_comment+i.name)   


        elif code == 'fispact':
            for i, i_a_f in zip(self.isotopes, self.isotope_atom_fractions):
                mat_card.append(i.symbol + str(i.nucleons) + ' ' + str(self.density_atoms_per_cm3 * i_a_f * volume_cm3))


        return '\n'.join(mat_card)


    def find_average_atom_mass(self):
        masses = []
        for e, n_e_a in zip(self.elements, self.fractions_coefficients):
            element_mass = 0
            for isotope in e.isotopes:
                element_mass += isotope.abundance * isotope.mass_amu
            masses.append(element_mass * n_e_a)
        return (sum(masses) / sum(self.fractions_coefficients)) * atomic_mass_unit_in_g

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

    def get_element_atom_fractions_from_chemical_equations(self, chemical_equation):
        list_of_fractions = []
        chemical_equation_chopped_up = self._read_chem_eq(chemical_equation)
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                try:
                    if is_number(chemical_equation_chopped_up[counter + 1]):
                        list_of_fractions.append(float(chemical_equation_chopped_up[counter + 1]))
                    else:
                        list_of_fractions.append(1)
                except:
                    list_of_fractions.append(1)
        a = sum(list_of_fractions)
        b = 1.0
        rtol = 1e-6
        if not abs(a - b) <= rtol * max(abs(a), abs(b)):
            normalised_list_of_fractions = normalise_list(list_of_fractions)
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

    def find_molar_mass_g_per_mol(self):
        masses = []
        for element in self.elements:
            element_mass = 0
            for i in element.isotopes:
                element_mass = element_mass + i.abundance * i.mass_amu
            masses.append(element_mass)
        cumlative_molar_mass = 0
        for mass, fraction in zip(masses, self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)):
            cumlative_molar_mass = cumlative_molar_mass + (mass * float(fraction))
        return cumlative_molar_mass

    def density_g_per_cm3_idea_gas(self):
        density_kg_m3 = (self.pressure_Pa / (8.3 * self.temperature_K)) * \
                         self.molar_mass * Avogadros_number * atomic_mass_unit_in_kg
        density_g_cm3 = density_kg_m3 / 1000.0
        return density_g_cm3

    def density_g_per_cm3_liquid(self):
        from thermo.chemical import Chemical
        hot_pressurized_liquid = Chemical(self.chemical_equation,
                                          T=self.temperature_K,
                                          P=self.pressure_Pa)
        return hot_pressurized_liquid.rho * 0.001

    def find_density_g_per_cm3(self):
        if self.density_atoms_per_barn_per_cm is not None:
            return (self.density_atoms_per_barn_per_cm/1e-24)*self.average_atom_mass
        if self.state_of_matter == 'solid' and self.volume_of_unit_cell_cm3 is not None and self.atoms_per_unit_cell is not None:
            return (self.molar_mass_g_per_mol * atomic_mass_unit_in_g*self.atoms_per_unit_cell / self.volume_of_unit_cell_cm3)
        if self.state_of_matter == 'gas' and self.pressure_Pa is not None and self.temperature_K is not None:
            return self.density_g_per_cm3_idea_gas()
        if self.state_of_matter == 'liquid' and self.pressure_Pa is not None and self.temperature_K is not None:
            return self.density_g_per_cm3_liquid()
        return None

    def find_density_atoms_per_barn_per_cm(self):
        if self.atoms_per_unit_cell is not None and self.volume_of_unit_cell_cm3 is not None:
            return (self.atoms_per_unit_cell / self.volume_of_unit_cell_cm3) * 1e-24
        if self.density_g_per_cm3 is not None:
            return (self.density_g_per_cm3 / self.molar_mass_g_per_mol) * Avogadros_number * 1e-24
        return None


class Homogenised_mixture(Base):

    def __init__(self, mixtures, **kwargs):
        self.classname = self.__class__.__name__
        self.color = kwargs.get('color')
        self.mixtures = mixtures
        self.mass_fractions = kwargs.get('mass_fractions')
        self.volume_fractions = kwargs.get('volume_fractions')

        self.temperature_K = kwargs.get('temperature_K',293.15)
        self.volume_cm3 = kwargs.get('volume_cm3')

        if self.volume_fractions is None and self.mass_fractions is None:
            raise ValueError('volume_fractions or mass_fractions must be specified.')
        if self.volume_fractions is None:
            self.volume_fractions = self.find_volume_fractions_from_mass_fractions()
        if self.mass_fractions is None:
            self.mass_fractions = self.find_mass_fractions_from_volume_fractions()

        self.material_card_name = kwargs.get('material_card_name')
        self.material_card_number = kwargs.get('material_card_number')
        self.material_card_comment = kwargs.get('material_card_comment')

        if self.material_card_name == None:
            if self.volume_fractions is None:
                self.material_card_name = self.find_material_card_name_with_mass_fractions()
            elif self.volume_fractions is None:
                self.material_card_name = self.find_material_card_name_with_volume_fractions()
        if self.material_card_number == None:
            self.material_card_number = '?'

        self.packing_fraction = kwargs.get('packing_fraction', 1.0)
        self.density_atoms_per_cm3 = self.find_density_atoms_per_cm3() * self.packing_fraction
        self.density_g_per_cm3 = self.find_density_g_per_cm3() * self.packing_fraction
        self.density_atoms_per_barn_per_cm = self.find_density_atoms_per_barn_per_cm()*self.packing_fraction


        # self.molar_mass_g_per_mol = self.find_molar_mass_g_per_mol()

        #         self.isotope_mass_fractions=[]
        # for isotope,isotope_atom_fraction in zip(self.isotopes,self.isotope_atom_fractions):
        #     self.isotope_mass_fractions.append(isotope_atom_fraction*(isotope.mass_amu/self.molar_mass_g_per_mol)*sum(self.fractions_coefficients))


        self.isotopes= self.find_isotopes()
        self.isotope_atom_fractions = self.find_isotope_atom_fractions()
        self.isotope_mass_fractions = self.find_isotope_mass_fractions()

    # def find_molar_mass_g_per_mol():
    #     molar_mass = 
    #     for mix in self.mixtures:


    def find_isotopes(self):
        isotopes = []
        for mixture, mix_v_f, mix_m_f in zip(self.mixtures, self.volume_fractions,self.mass_fractions):
            for i in mixture.isotopes:
                isotopes.append(i)
        return isotopes

    def find_isotope_atom_fractions(self):
        fractions = []
        for mixture, mix_v_f, mix_m_f in zip(self.mixtures, self.volume_fractions,self.mass_fractions):
            n_a_mix = (mixture.density_atoms_per_cm3 * mix_v_f) / self.density_atoms_per_cm3 # 

            for i, a_f, m_f in zip(mixture.isotopes, mixture.isotope_atom_fractions, mixture.isotope_mass_fractions):
                fractions.append(a_f * mix_v_f)

        return fractions

    def find_isotope_mass_fractions(self):
        fractions = []
        for mixture, mix_v_f, mix_m_f in zip(self.mixtures, self.volume_fractions,self.mass_fractions):
            # n_a_mix= (mixture.density_atoms_per_cm3*mix_v_f)/self.density_atoms_per_cm3 # 

            for i, a_f, m_f in zip(mixture.isotopes, mixture.isotope_atom_fractions, mixture.isotope_mass_fractions):
                fractions.append(m_f * mix_m_f)

        return fractions


    def find_volume_fractions_from_mass_fractions(self):
        if arevaluesthesame(sum(self.mass_fractions), 1.0,1e-09)==False:
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
            normalised_volume_fractions.append(non_normalised_volume_fractions * factor)
        return normalised_volume_fractions

    def find_mass_fractions_from_volume_fractions(self):
        if arevaluesthesame(sum(self.volume_fractions), 1.0,1e-09) == False:
            raise ValueError('The provided volume fractions should sum to 1 not ',
                             sum(self.volume_fractions))

        # total_mass = 0
        # for mix, vol_fraction in zip(self.mixtures, self.volume_fractions):
        #     total_mass+=mix.density_g_per_cm3*vol_fraction
        # print('total_mass',total_mass)

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

    def find_density_atoms_per_cm3(self):
        cumlative_density = 0
        for mixture, v_f in zip(self.mixtures, self.volume_fractions):
            if mixture.isotopes == []:
                cumlative_density += 0
            else:
                cumlative_density += mixture.density_atoms_per_cm3 * v_f#*mixture.packing_fraction
        return cumlative_density

    def find_density_g_per_cm3(self):
        cumlative_density = 0
        for mixture, v_f in zip(self.mixtures,self.volume_fractions):
            cumlative_density += mixture.density_g_per_cm3 * v_f #* mixture.packing_fraction
        # TODO: allow density combinations involving atom_per_barn_cm2
        return cumlative_density

    def find_density_atoms_per_barn_per_cm(self):
        cumlative_density = 0
        for mixture, v_f in zip(self.mixtures,self.volume_fractions):
            cumlative_density += mixture.density_atoms_per_barn_per_cm * v_f# *mixture.packing_fraction
        # TODO: allow density combinations involving atom_per_barn_cm2
        return cumlative_density

    def find_material_card_name_with_volume_fractions(self):
        description_to_return = ''
        for item, vol_frac in zip(self.mixtures, self.volume_fractions):
            description_to_return += item.material_card_name + '_vf_' + str(vol_frac) + '_'
        return description_to_return[:-1]

    def find_material_card_name_with_mass_fractions(self):
        description_to_return = ''
        for item, frac in zip(self.mixtures, self.mass_fractions):
            description_to_return += item.material_card_name + '_mf_' + str(frac) + '_'
        return description_to_return[:-1]

    def combine_duplicate_isotopes(self, list_of_dictionaries, same, combine,):
            zaids = []
            iso_frac = []
            isotopes = []
            for entry in list_of_dictionaries:
                if entry != {}:
                    if entry[same].zaid in zaids:
                        index = zaids.index(entry[same].zaid)
                        iso_frac[index] = iso_frac[index] + entry[combine]
                    else:
                        zaids.append(entry[same].zaid)
                        isotopes.append(entry[same])
                        iso_frac.append(entry[combine])
            zaids, iso_frac, isotopes = zip(*natsorted(zip(zaids, iso_frac, isotopes)))

            # new_list_of_zaids = []
            # for z, i_f, name in zip(zaids, iso_frac,names):
            #     new_list_of_zaids.append()

            return isotopes, iso_frac


    def material_card(self, material_card_comment=None, material_card_name=None, material_card_number=None, color=None, fractions=None,code=None,squashed=False,temperature_K=None, volume_cm3=None):

        mat_card_printed=super(Homogenised_mixture,self).material_card_header(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K,volume_cm3)
        material_card_comment, material_card_name, material_card_number, color, code, fractions, fractions_prefix, comment, end_comment, temperature_K, volume_cm3 = super(Homogenised_mixture,self).kwarg_handler(material_card_comment, material_card_name, material_card_number, color, code, fractions,temperature_K, volume_cm3)

        mat_card=[]
        if code == 'fispact':
            fractions='number of atoms'
            for mixture, mix_v_f, mix_m_f in zip(self.mixtures, self.volume_fractions,self.mass_fractions):

                if mixture.isotopes == []:
                    # A void material has no isotope fractions but prints a header
                    mat_card.append({'string': comment + end_comment})
                    mat_card.append({'string': comment + mixture.material_card_name+end_comment})
                    mat_card.append({'string': comment + ' with a density of '+ str(mixture.density_g_per_cm3) + ' g per cm3' + end_comment})
                    mat_card.append({'string': comment + ' volume fraction of '+ str(mix_v_f)+end_comment})
                else:
                    mat_card.append({'string': comment + end_comment})
                    mat_card.append({'string': comment + mixture.material_card_name+end_comment})
                    mat_card.append({'string': comment + 'with a density of '+ str(mixture.density_g_per_cm3) + ' g per cm3' + end_comment})
                    mat_card.append({'string': comment + 'packing fraction of '+ str(mixture.packing_fraction) + end_comment})
                    mat_card.append({'string': comment + 'volume fraction of '+ str(mix_v_f) + end_comment})
                    mat_card.append({'string': comment + 'mass fraction of '+ str(mix_m_f) + end_comment})

                    atoms_in_mixture = self.volume_cm3 * mix_v_f * mixture.density_atoms_per_cm3

                    for i, a_f in zip(mixture.isotopes, mixture.isotope_atom_fractions):
                        if a_f > 0:
                            mat_card.append({'number of atoms': (a_f * atoms_in_mixture),
                                             'isotope': i})

            list_of_strings = [{k: v for k, v in i.items() if k == 'string'} for i in mat_card]

            condensed_mat_card_non_strings = [{k: v for k, v in i.items() if k !='string'} for i in mat_card]

            isotopes, iso_frac = self.combine_duplicate_isotopes(list_of_dictionaries=condensed_mat_card_non_strings,
                                                                 same='isotope',
                                                                 combine='number of atoms',
                                                                 )

            mat_card.append({'string': comment + end_comment})
            for i in list_of_strings:
                if i !={}:
                    mat_card_printed.append(i['string'])
            mat_card_printed.append(comment)        
            for i,iso_frac in zip(isotopes,iso_frac):
                mat_card_printed.append('   '+ (i.zaid).ljust(11) + ' ' + str(iso_frac).ljust(24))





        elif code == 'mcnp' or code == 'serpent':
            for mixture, mix_v_f, mix_m_f in zip(self.mixtures, self.volume_fractions,self.mass_fractions):
                if mixture.isotopes == []:
                    # A void material has no isotope fractions but prints a header
                    mat_card.append({'string': comment})
                    mat_card.append({'string': comment +mixture.material_card_name})
                    mat_card.append({'string': comment +' with a density of '+ str(mixture.density_g_per_cm3) +' g per cm3'})
                    mat_card.append({'string': comment +' volume fraction of '+ str(mix_v_f)})
                else:
                    n_a_mix= (mixture.density_atoms_per_cm3 * mix_v_f) / self.density_atoms_per_cm3 # a fraction of total number of atoms
                    amount_of_mass_in_mix = (mixture.density_g_per_cm3 * mix_v_f)/self.density_g_per_cm3

                    mat_card.append({'string': comment})
                    mat_card.append({'string': comment + mixture.material_card_name})
                    mat_card.append({'string': comment + 'with a density of '+ str(mixture.density_g_per_cm3) + ' g per cm3'})
                    mat_card.append({'string': comment + 'packing fraction of '+str(mixture.packing_fraction)})
                    mat_card.append({'string': comment + 'volume fraction of '+ str(mix_v_f)})
                    mat_card.append({'string': comment + 'mass fraction of '+ str(mix_m_f)})

                    for i, a_f, m_f in zip(mixture.isotopes, mixture.isotope_atom_fractions, mixture.isotope_mass_fractions):
                        if a_f > 0:
                            mat_card.append({'isotope': i,
                                             'isotope atom fractions': (a_f * n_a_mix),
                                             'isotope mass fractions': (m_f * mix_m_f)})

            if squashed == False:
                for item in mat_card:
                    if list(item.keys()) == ['string']:
                        mat_card_printed.append(item['string'])
                    else:
                        isotope = item['isotope']
                        line = '   ' + (isotope.zaid + isotope.nuclear_library).ljust(11)+' '+str(item[fractions]).ljust(24)+ end_comment + isotope.name
                        mat_card_printed.append(line)
                return '\n'.join(mat_card_printed)
            else:

                # a method of squashing / combining identical zaids

                list_of_strings = [{k: v for k, v in i.items() if k == 'string'} for i in mat_card]
                list_of_zaids = [{k: v for k, v in i.items() if k != 'string'} for i in mat_card]

                zaids, iso_frac, names = self.combine_duplicate_isotopes(list_of_zaids=list_of_zaids,same='zaid_lib',combine='fractions',keep='name')

                mat_card.append({'string':comment})
                for i in list_of_strings:
                    if i !={}:
                        mat_card_printed.append(i['string'])
                mat_card_printed.append(comment)        
                      

                for zaid,iso_frac,name in zip(zaids,iso_frac,names):
                    mat_card_printed.append('   '+(zaid).ljust(11) + ' '+str(iso_frac).ljust(24)+end_comment+name)

        return '\n'.join(mat_card_printed)     
        
# Presently unused?
class Natural_Isotopes():

    def __init__(self):
        self.all_natural_isotopes = self.find_all_natural_isotopes()

    def find_all_natural_isotopes(self):
        all_isotopes = []
        for element in Natural_Elements().all_natural_elements:

            isotopes_in_element = element.isotopes
            all_isotopes= all_isotopes +isotopes_in_element

        return all_isotopes

class Natural_Elements():
    def __init__(self):

        self.all_natural_elements = self.find_all_natural_elements()

        self.all_natural_element_symbols = self.find_all_natural_element_symbols()

    def find_all_natural_element_symbols(self):
        return list(set(NAT_NDATA.index))

    def find_all_natural_elements(self):
        return [Element(e) for e in list(set(NAT_NDATA.index))]
