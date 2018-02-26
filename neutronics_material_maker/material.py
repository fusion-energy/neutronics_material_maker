
import re
import sys
import json
import pprint

from neutronics_material_maker.isotope import Isotope
from neutronics_material_maker.element import Element
from neutronics_material_maker.jsonable_object import NamedObject


#todo future work : allow conversion to pyne material and then exporting to hdf5 file for use in DAGMC
# from pyne import material
# from pyne.material import Material
# nucvec = {10010:  1.0, 80160:  1.0, 691690: 1.0, 922350: 1.0,
#           922380: 1.0, 942390: 1.0, 942410: 1.0, 952420: 1.0,
#           962440: 1.0}
# mat = Material(nucvec) #assumes mass fraction
#
# mat = Material()
# mat.from_atom_frac(nucvec) #converts to volume fraction




class Material(NamedObject):
    def __init__(self, description,density_g_per_cm3=None,atom_density_per_barn_per_cm=None, elements_and_fractions=None):#,*enriched_isotopes):
        #super(Material, self).__init__()
        self.description = description

        if elements_and_fractions==None:
            self.element_mixtures = self.find_material_mass_or_atom_faction_mixture(description)
        else:
            self.element_mixtures = elements_and_fractions

        self.density_g_per_cm3 = density_g_per_cm3
        if density_g_per_cm3 ==None :
            self.density_g_per_cm3 = self.find_density_g_per_cm3()

        self.atom_density_per_barn_per_cm = atom_density_per_barn_per_cm
        if atom_density_per_barn_per_cm == None:
            self.atom_density_per_barn_per_cm = self.find_atom_density_per_barn_per_cm()



        self.elements = self.find_elements_in_material()

        self.element_atom_fractions = self.find_element_atom_fractions()
        self.element_mass_fractions = self.find_element_mass_fractions()
        #self.enriched_isotopes = enriched_isotopes
        #if enriched_isotopes:
        #    print('enriched materials not yet implemented')
        #    sys.exit()

    def find_material_mass_or_atom_faction_mixture(self, name):
        material_to_return=None

        if name == 'Eurofer_DEMO_models':
            material_to_return= [{'element':Element('Fe'),'mass_fraction':0.88821},
                                 {'element':Element('B') ,'mass_fraction':0.00001},
                                 {'element':Element('C') ,'mass_fraction':0.00105},
                                 {'element':Element('N') ,'mass_fraction':0.00040},
                                 {'element':Element('O') ,'mass_fraction':0.00001},
                                 {'element':Element('Al'),'mass_fraction':0.00004},
                                 {'element':Element('Si'),'mass_fraction':0.00026},
                                 {'element':Element('P') ,'mass_fraction':0.00002},
                                 {'element':Element('S') ,'mass_fraction':0.00003},
                                 {'element':Element('Ti'),'mass_fraction':0.00001},
                                 {'element':Element('V') ,'mass_fraction':0.00200},
                                 {'element':Element('Cr'),'mass_fraction':0.09000},
                                 {'element':Element('Mn'),'mass_fraction':0.00550},
                                 {'element':Element('Co'),'mass_fraction':0.00005},
                                 {'element':Element('Ni'),'mass_fraction':0.00010},
                                 {'element':Element('Cu'),'mass_fraction':0.00003},
                                 {'element':Element('Nb'),'mass_fraction':0.00005},
                                 {'element':Element('Mo'),'mass_fraction':0.00003},
                                 {'element':Element('Ta'),'mass_fraction':0.00120},
                                 {'element':Element('W') ,'mass_fraction':0.01100}
                                 ]

        if name == 'Eurofer':
            material_to_return= [{'element':Element('Fe'),'mass_fraction':0.88821},
                                 {'element':Element('B') ,'mass_fraction':0.00001},
                                 {'element':Element('C') ,'mass_fraction':0.00105},
                                 {'element':Element('N') ,'mass_fraction':0.00040},
                                 {'element':Element('O') ,'mass_fraction':0.00001},
                                 {'element':Element('Al'),'mass_fraction':0.00004},
                                 {'element':Element('Si'),'mass_fraction':0.00026},
                                 {'element':Element('P') ,'mass_fraction':0.00002},
                                 {'element':Element('S') ,'mass_fraction':0.00003},
                                 {'element':Element('Ti'),'mass_fraction':0.00001},
                                 ]

        if name == 'Bronze':
            material_to_return = [{'element':Element('Cu'),'atom_fraction':0.95} ,
                                  {'element':Element('Sn'),'atom_fraction':0.05}
                                 ]

        if name == 'CuCrZr_with_impurities':
            material_to_return = [{'element':Element(24),'atom_fraction':0.0074183845},
                                  {'element':Element(4), 'atom_fraction':0.0007268049},
                                  {'element':Element(8), 'atom_fraction':0.0011911158},
                                  {'element':Element(27),'atom_fraction':0.0006465533},
                                  {'element':Element(14),'atom_fraction':0.0002508775},
                                  {'element':Element(29),'atom_fraction':0.989766264}
                                  ]

        if name == 'SS-316LN-IG':
            material_to_return = [{'element':Element('Fe'),'mass_fraction':0.63684},
                                  {'element':Element('C') ,'mass_fraction':0.0003  },
                                  {'element':Element('Mn'),'mass_fraction':0.02   },
                                  {'element':Element('Si'),'mass_fraction':0.0050  },
                                  {'element':Element('P') ,'mass_fraction':0.00025 },
                                  {'element':Element('S') ,'mass_fraction':0.0001  },
                                  {'element':Element('Cr'),'mass_fraction':0.180  },
                                  {'element':Element('Ni'),'mass_fraction':0.1250 },
                                  {'element':Element('Mo'),'mass_fraction':0.0270  },
                                  {'element':Element('N') ,'mass_fraction':0.0008  },
                                  {'element':Element('B') ,'mass_fraction':0.00001 },
                                  {'element':Element('Cu'),'mass_fraction':0.0030  },
                                  {'element':Element('Co'),'mass_fraction':0.0005  },
                                  {'element':Element('Nb'),'mass_fraction':0.0001  },
                                  {'element':Element('Ti'),'mass_fraction':0.001  },
                                  {'element':Element('Ta'),'mass_fraction':0.0001  }
                                  ]

        if name == 'DT-plasma':
            material_to_return = [{'element':Element('H',enriched_isotopes=(Isotope('H', 2, 0.5),
                                                                            Isotope('H', 3, 0.5))),
                                                        'atom_fraction':1.0 }]
        if name == 'Glass-fibre':
            material_to_return = [{'element':Element('H') ,'atom_fraction':0.0000383948},
                                  {'element':Element('O') ,'atom_fraction':0.6328110447},
                                  {'element':Element(12),'atom_fraction':0.0499936947},
                                  {'element':Element(13),'atom_fraction':0.1026861642},
                                  {'element':Element(14),'atom_fraction':0.2144707015}]


        if name == 'Epoxy':
            material_to_return = [{'element':Element('H'),'atom_fraction':1.0414E-06},
                                  {'element':Element('C'),'atom_fraction':1.7164E-02},
                                  {'element':Element(7),'atom_fraction':  1.3560E-03},
                                  {'element':Element(8),'atom_fraction':  2.7852E-03}]

        if name == 'r-epoxy':
            material_to_return = [{'element': Element(1),'atom_fraction': 3.89340E-03},
                                  {'element': Element(6), 'atom_fraction': 3.40560E-03},
                                  {'element': Element(7), 'atom_fraction': 3.70800E-04 },
                                  {'element': Element(8), 'atom_fraction': 4.87080E-03 },
                                  {'element': Element(12), 'atom_fraction':1.69197E-04 +2.14200E-05+2.35834E-05},
                                  {'element': Element(13), 'atom_fraction':7.07400E-04 },
                                  {'element': Element(14), 'atom_fraction':1.32800E-03+6.72000E-05+4.46000E-03  },
                                  {'element': Element(16), 'atom_fraction':8.71457E-05+ 6.97680E-07+3.93822E-06+1.83600E-08   }]


        if material_to_return == None:
            print('Material is not in the database please specify the elements it is made from')
            sys.exit()
        else:
            return material_to_return

    def find_elements_in_material(self):
        list_of_elements=[]
        for element_element_fractions in self.element_mixtures:
            list_of_elements.append(element_element_fractions['element'])
        return list_of_elements


    @property
    def isotopes(self):
        print(self.description)
        print(self.element_atom_fractions)
        list_of_isotopes = []
        for fractions, element in zip(self.element_atom_fractions, self.elements):
            for isotope in element.isotopes:
                list_of_isotopes.append(isotope)

        return list_of_isotopes


    @property
    def isotopes_atom_fractions(self):
        print(self.description)
        print(self.element_atom_fractions)
        list_of_fractions = []
        for fractions, element in zip(self.element_atom_fractions, self.elements):
            for isotope in element.isotopes:
                list_of_fractions.append(isotope.abundance * fractions)
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

    def find_element_mass_fractions(self):

        if 'mass_fraction' not in self.element_mixtures[0].keys():
            return []

        list_of_fractions=[]
        for element_element_fractions in self.element_mixtures:
            list_of_fractions.append(element_element_fractions['mass_fraction'])


        a = sum(list_of_fractions)
        b = 1.0

        rtol = 1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            print('element mass fractions within a material must sum to 1')
            print('current mass factions are ',list_of_fractions)
            print('which sums to ',sum(list_of_fractions))
            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor * fraction)
            return normalised_list_of_fractions

        return list_of_fractions

    def find_element_atom_fractions(self):

        list_of_fractions = []
        if 'atom_fraction' not in self.element_mixtures[0].keys():
            for element_element_fractions in self.element_mixtures:
                list_of_fractions.append(element_element_fractions['mass_fraction']/
                                         element_element_fractions['element'].molar_mass_g)


        else:
            #material contains atom fraction information
            for element_element_fractions in self.element_mixtures:
                list_of_fractions.append(element_element_fractions['atom_fraction'])



        a = sum(list_of_fractions)
        b = 1.0

        rtol=1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            print("element atom fractions within a material don't sum to 1")
            print('current atom factions are ',list_of_fractions)
            print('which sums to ',sum(list_of_fractions))
            normalised_list_of_fractions=[]
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor*fraction)
            print('normalizing to ', normalised_list_of_fractions)
            return normalised_list_of_fractions

        return list_of_fractions


    def find_atom_density_per_barn_per_cm(self):
        if self.description == 'DT-plasma':
            return 1E-20
        if self.description == 'SS-316LN-IG':
            return 8.58294E-02
        else:
            print('material not found in atom_density_per_barn_per_cm function')
            print('perhaps try density_g_per_cm3 property')
            return None  #sys.exit()


    def find_density_g_per_cm3(self):
        if self.description == 'Eurofer':
            return  7.79800

        if self.description == 'SS-316LN-IG':
            return 7.93

        if self.description == 'Bronze':
            return 8.8775

        if self.description == 'Glass-fibre':
            return 2.49

        if self.description == 'Epoxy':
            return 1.18

        if self.description == 'CuCrZr_with_impurities':
            return 8.814

        if self.description == 'r-epoxy': #reference http://personalpages.to.infn.it/~tosello/EngMeet/ITSmat/SDD/CyanateEster.pdf
            return 1.207

        else:
            print('material not found in density_g_per_cm3 function')
            print('perhaps try atom_density_per_barn_per_cm property')
            return None #sys.exit()

    @property
    def serpent_material_card(self):

        density = self.atom_density_per_barn_per_cm
        if density == None :
            -1 * self.density_g_per_cm3

        material_card = 'mat ' + self.description + ' -' + str(self.density_g_per_cm3) + '\n'



        for counter, element_mixture in enumerate(self.element_mixtures):

            print(element_mixture)
            print(type(element_mixture))

            element=element_mixture['element']

            if 'atom_fraction' in element_mixture.keys():
                print('using atom fraction')
                element_atom_fraction = self.find_element_atom_fractions()[counter] #element_mixture['atom_fraction']
            else:
                print('using mass fraction')
                element_atom_fraction = self.find_element_mass_fractions()[counter]/element.molar_mass_g #element_mixture['mass_fraction']/element.molar_mass_g

            print('element.isotopes',element.isotopes)
            for isotope in element.isotopes:

                isotopes_atom_fraction=isotope.abundance * element_atom_fraction
                if isotopes_atom_fraction>0:

                    if isotope.zaid.startswith('160') :
                        #todo Serpent appears to be not compatible with particular Fendl libraries, check the updated version of Serpent
                        material_card = material_card + ('    ' + isotope.zaid + '.03c ' + str(isotopes_atom_fraction) + '\n')
                    else:
                        material_card = material_card + ('    ' + isotope.zaid + '.31c ' + str(isotopes_atom_fraction) + '\n')
                else:
                    print('isotope ', isotope.description, ' mass fraction is 0, so this is not being included in the material card')

        return material_card

# mat_name= 'Epoxy'#'Glass-fibre'#'DT-plasma'#'Bronze'#''SS-316LN-IG'
# for e in Material(mat_name).element_mixtures:
#     print('mixtures',e)
#
# for e in Material(mat_name).elements:
#     print('elements',e)
#
# for e in Material(mat_name).element_atom_fractions:
#     print('element_atom_fractions',e)
#
# for e in Material(mat_name).element_mass_fractions:
#     print('element_mass_fractions',e)
#
# print(Material(mat_name).serpent_material_card)