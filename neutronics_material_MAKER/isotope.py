
from neutronics_material_MAKER.common_utils import (full_name,
                                                    natural_abundance,
                                                    mass_amu,
                                                    natural_isotopes_in_elements,
                                                    find_symbol_from_protons,
                                                    find_protons_from_symbol)  
from neutronics_material_MAKER.jsonable_object import NamedObject

class Isotope(NamedObject):
    def __init__(self, symbol_or_proton, atomic_number, abundance='Natural',
                 **kwargs):
        super(Isotope, self).__init__(**kwargs)

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

    # @property
    # def mass_amu(self):
    #     return self.mass_amu

    @property
    def description(self):
        return {'isotope ': self.symbol,
               'atomic_number ':self.atomic_number,
               'abundance':self.abundance,
               'abundance':self.abundance,  # TODO: why doubled? - mc
               'mass_amu':self.mass_amu,
               'protons':self.protons,
               'neutrons':self.neutrons
              }