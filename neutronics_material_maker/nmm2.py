# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 12:34:28 2018

@author: matti
"""

from pandas import DataFrame

NDATA = DataFrame.from_csv('nuclear_data.csv', index_col='Symbol')
#NDATA.set_index(['Proton number', 'Symbol', 'Name', 'Nucleon number'],
#                inplace=True)

NAT_ELEMENT_SYMBOLS =  ['Sn', 'Xe', 'Cd', 'Te', 'Ba', 'Dy', 'Gd', 'Hg', 'Mo',
                        'Nd', 'Os', 'Ru', 'Sm', 'Yb', 'Ca', 'Er', 'Hf', 'Kr',
                        'Pd', 'Pt', 'Se', 'Ge', 'Ni', 'Ti', 'W', 'Zn', 'Zr',
                        'Ce', 'Cr', 'Fe', 'Pb', 'S', 'Sr', 'Ar', 'C', 'K',
                        'Mg', 'Ne', 'Si', 'U', 'Ag', 'B', 'Br', 'Cl', 'Cu',
                        'Eu', 'Ga', 'H', 'He', 'In', 'Ir', 'La', 'Li', 'Lu',
                        'N', 'Rb', 'Re', 'Sb', 'Ta', 'Tl', 'V', 'Be', 'O', 'F',
                        'Na', 'Al', 'P', 'Sc', 'Mn', 'Co', 'As', 'Y', 'Nb',
                        'Rh', 'I', 'Cs', 'Pr', 'Tb', 'Ho', 'Tm', 'Au', 'Bi',
                        'Th', 'Pa']


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
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


class Isotope(object):
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
            self.protons = NDATA.loc[self.symbol]['Proton number'].unique()[0]
        self._sanity()
        if self.symbol is None:
            self.symbol = NDATA.loc[NDATA['Proton number'] == self.protons].index[0]
        self.element_name = NDATA.loc[self.symbol]['Name'].unique()[0]        
        self.name = self.element_name +'_'+ str(self.nucleons)
        self.mass_amu = NDATA[(NDATA['Proton number'] == self.protons) & 
                              (NDATA['Nucleon number'] == self.nucleons)]['Mass amu'][0]
        self.natural_abundance = NDATA[(NDATA['Proton number'] == self.protons) & 
                                       (NDATA['Nucleon number'] == self.nucleons)]['Natural abundance'][0]

        self.abundance = kwargs.get('abundance', self.natural_abundance)
        if self.abundance and self.abundance > 1.0 or self.abundance < 0.0:
            raise ValueError('Abundance of isotope can not be greater than 1.0'
                             ' or less than 0.')
        self.zaid = str(self.protons) + str(self.nucleons).zfill(3)        
        self._get_xs_files()

    def _handle_kwargs(self, kwargs):
        self.symbol = kwargs.get('symbol', None)
        self.protons = kwargs.get('protons', None)
        self.nucleons = kwargs.get('nucleons', None)
        self.color = kwargs.get('color', (0, 0, 0))
        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')
        
    def _handle_args(self, args):
        atomic_number_or_proton_number = []
        for arg in args:
            if isinstance(arg, str) and self.symbol is None:
                self.symbol = arg
                self.protons = NDATA.loc[self.symbol]['Proton number'].unique()[0]
            if isinstance(arg, int):
                atomic_number_or_proton_number.append(arg)
        if self.nucleons is None and len(atomic_number_or_proton_number) >= 1:
            self.nucleons = max(atomic_number_or_proton_number)
        if self.protons is None:
            self.protons = min(atomic_number_or_proton_number)
            
    def _sanity(self):
        if NDATA[(NDATA['Proton number'] == self.protons) & 
                 (NDATA['Nucleon number'] == self.nucleons)].empty:
            raise ValueError('This isotope either does not exist, or you have '
                             'no data for it.')

    def _get_xs_files(self, **kwargs):
        self.xsdir = kwargs.get('xsdir','/opt/serpent2/xsdir.serp')
        self.nuclear_library = kwargs.get('nuclear_library',
                                          find_prefered_library(self.zaid,
                                                                self.xsdir))
        self.nuclear_library_file = find_prefered_library_file(self.zaid,
                                                               self.xsdir)

    def serpent_material_card(self):

        if self.density_g_per_cm3 == None and self.density_atoms_per_barn_per_cm == None:
            raise ValueError(
                "To produce a serpent material card the density_g_per_cm3 or density_atoms_per_barn_per_cm must be provided")

        if self.density_g_per_cm3 == None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  ' + str(self.density_g_per_cm3*self.packing_fraction)

        if self.color == None:

            color = ''

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")

        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)])

        mat_card = 'mat ' + self.material_card_name + density + color + ' \n'

        mat_card = mat_card+ '   '+(self.zaid + self.nuclear_library).ljust(11)+ ' 1'.ljust(22)+' % ' +self.name +'\n'

        return mat_card

if __name__ is '__main__':
    H = Isotope(2, 1)
    H = Isotope('H', 3)
