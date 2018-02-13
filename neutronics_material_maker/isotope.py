
import re
import sys
import json
import pprint

#from common_utils import full_name
from common_utils import natural_abundance
from common_utils import mass_amu
from common_utils import natural_isotopes_in_elements
from common_utils import find_symbol_from_protons
from common_utils import find_protons_from_symbol
  
from jsonable_object import NamedObject

class Isotope(NamedObject):
    def __init__(self, symbol_or_proton, atomic_number, abundance='Natural'):
        super(Isotope, self).__init__()

        if type(symbol_or_proton) == int or symbol_or_proton.isdigit():
            self.protons = symbol_or_proton
            self.symbol = find_symbol_from_protons(symbol_or_proton)
        else:
            self.symbol = symbol_or_proton
            self.protons = find_protons_from_symbol(symbol_or_proton)

        self.atomic_number = atomic_number
        self.mass_amu = mass_amu(self.symbol,self.atomic_number)

        if abundance == 'Natural':
            self.abundance = natural_abundance(self.symbol,self.atomic_number)
        else:
            self.abundance = abundance

    @property
    def zaid(self):
        return str(self.protons) + str(self.atomic_number).zfill(3)

 
    @property
    def neutrons(self):
        return self.atomic_number - self.protons


    @property
    def description(self):
        return {'isotope ': self.symbol,
               'atomic_number ':self.atomic_number,
               'abundance':self.abundance,
               'abundance':self.abundance,
               'mass_amu':self.mass_amu,
               'protons':self.protons,
               'neutrons':self.neutrons
              }