
import re
import sys
import json
import pprint

from neutronics_material_maker.isotope import Isotope
from neutronics_material_maker.element import Element
from neutronics_material_maker.jsonable_object import NamedObject
from neutronics_material_maker.common_utils import read_in_xsdir_file

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
    def __init__(self, description,density_g_per_cm3=None,
                 atom_density_per_barn_per_cm=None,
                 elements_and_fractions=None,
                 xsdir_filename= '/opt/serpent2/xsdir.serp'):#,*enriched_isotopes):
        #super(Material, self).__init__()
        self.description = description
        self.xsdir_filename= xsdir_filename
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

        if name == 'Eurofer': #gl
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
                                 {'element':Element('V') ,'mass_fraction':0.000200},#see neutronics guidlines V was too high in the demo model
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

        if name == 'Tungsten': #gl
            material_to_return= [{'element':Element('W'),'mass_fraction':1e6-405},#balance
                                 {'element':Element('Ag'),'mass_fraction':10},
                                 {'element':Element('Al'),'mass_fraction':15},
                                 {'element':Element('As'),'mass_fraction':5},
                                 {'element':Element('Ba'),'mass_fraction':5},
                                 {'element':Element('Ca'),'mass_fraction':5},
                                 {'element':Element('Cd'),'mass_fraction':5},
                                 {'element':Element('Co'),'mass_fraction':10},
                                 {'element':Element('Cr'),'mass_fraction':20},
                                 {'element':Element('Cu'),'mass_fraction':10},
                                 {'element':Element('Fe'),'mass_fraction':30},
                                 {'element':Element('K'), 'mass_fraction':10},
                                 {'element':Element('Mg'),'mass_fraction':5},
                                 {'element':Element('Mn'),'mass_fraction':5},
                                 {'element':Element('Na'),'mass_fraction':10},
                                 {'element':Element('Nb'),'mass_fraction':10},
                                 {'element':Element('Ni'),'mass_fraction':5},
                                 {'element':Element('Pb'),'mass_fraction':5},
                                 {'element':Element('Ta'),'mass_fraction':20},
                                 {'element':Element('Ti'),'mass_fraction':5},
                                 {'element':Element('Zn'),'mass_fraction':5},
                                 {'element':Element('Zr'),'mass_fraction':5},
                                 {'element':Element('Mo'),'mass_fraction':100},
                                 {'element':Element('C'), 'mass_fraction':30},
                                 {'element':Element('H'), 'mass_fraction':5},
                                 {'element':Element('N'), 'mass_fraction':5},
                                 {'element':Element('O'), 'mass_fraction':20},
                                 {'element':Element('P'), 'mass_fraction':20},
                                 {'element':Element('S'), 'mass_fraction':5},
                                 {'element':Element('Si'),'mass_fraction':20}
                                 ]

        if name == 'Bronze':
            material_to_return = [{'element':Element('Cu'),'atom_fraction':0.95} ,
                                  {'element':Element('Sn'),'atom_fraction':0.05}
                                 ]

        if name == 'CuCrZr':
            material_to_return = [{'element':Element(24),'mass_fraction':0.75},#Cr
                                  {'element':Element(4), 'mass_fraction':0.11},#zr #Demo model has 0.11 in description but 0.011 in the calculation , this should be 0.011 to make everything sum to 100
                                  {'element':Element(8), 'mass_fraction':0.03},#O
                                  {'element':Element(27),'mass_fraction':0.06},#Co
                                  {'element':Element(14),'mass_fraction':0.011},#Si
                                  {'element':Element(29),'mass_fraction':99.039}#Cu
                                  ]

            # material_to_return = [{'element':Element(24),'atom_fraction':0.0074183845},
            #                       {'element':Element(4), 'atom_fraction':0.0007268049},
            #                       {'element':Element(8), 'atom_fraction':0.0011911158},
            #                       {'element':Element(27),'atom_fraction':0.0006465533},
            #                       {'element':Element(14),'atom_fraction':0.0002508775},
            #                       {'element':Element(29),'atom_fraction':0.989766264}
            #                       ]

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

        if name == 'Copper':
            material_to_return = [{'element':Element('Cu'),'atom_fraction':1.0}]

        if name == 'Void':
            material_to_return = []

        if material_to_return == None:
            print('Material '+name+' is not in the database please specify the elements it is made from')
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
        #print(self.description)
        #print(self.element_atom_fractions)
        list_of_isotopes = []
        for fractions, element in zip(self.element_atom_fractions, self.elements):
            for isotope in element.isotopes:
                list_of_isotopes.append(isotope)

        return list_of_isotopes

    @property
    def isotopes_atom_fractions(self):

        if self.description == 'Void':
            return []
        #print(self.description)
        #print(self.element_atom_fractions)
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
        if self.description == 'Void':
            return []
        if 'mass_fraction' not in self.element_mixtures[0].keys():
            return []

        list_of_fractions=[]
        for element_element_fractions in self.element_mixtures:
            list_of_fractions.append(element_element_fractions['mass_fraction'])


        a = sum(list_of_fractions)
        b = 1.0

        rtol = 1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            #print('element mass fractions within a material must sum to 1')
            #print('current mass factions are ',list_of_fractions)
            #print('which sums to ',sum(list_of_fractions))
            #print('normalising ...')
            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor * fraction)
            return normalised_list_of_fractions

        return list_of_fractions

    def find_element_atom_fractions(self):
        if self.description == 'Void':
            return []
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

            #print("element atom fractions within a material don't sum to 1")
            #print('current atom factions are ',list_of_fractions)
            #print('which sums to ',sum(list_of_fractions))
            normalised_list_of_fractions=[]
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor*fraction)
            #print('normalizing to ', normalised_list_of_fractions)
            return normalised_list_of_fractions

        return list_of_fractions


    def find_atom_density_per_barn_per_cm(self):
        if self.description == 'DT-plasma':
            return 1E-20

        if self.description == 'SS-316LN-IG':
            return 8.58294E-02

        if self.description == 'Eurofer_DEMO_models':
            return  8.43211E-02

        #print('material not found in atom_density_per_barn_per_cm function')
        #print('perhaps try density_g_per_cm3 property')
        return None  #sys.exit()


    def find_density_g_per_cm3(self):

        if self.description == 'Eurofer':
            return 7.87

        if self.description == 'Tungsten':
            return 19.0

        if self.description == 'SS-316LN-IG':
            return 7.93

        if self.description == 'Bronze':
            return 8.8775

        if self.description == 'Glass-fibre':
            return 2.49

        if self.description == 'Epoxy':
            return 1.18

        if self.description == 'CuCrZr':
            return 8.9

        if self.description == 'r-epoxy': #reference http://personalpages.to.infn.it/~tosello/EngMeet/ITSmat/SDD/CyanateEster.pdf
            return 1.207

        if self.description == 'Copper':
            return 8.96

        if self.description == 'Void':
            return 0.0

        #print('material '+self.description+' not found in density_g_per_cm3 function')
        #print('perhaps try atom_density_per_barn_per_cm property')
        return None #sys.exit()

    @property
    def serpent_material_card(self):

        list_of_isotope_zaid_or_name, list_of_associated_libraries = read_in_xsdir_file(self.xsdir_filename)

        density = self.atom_density_per_barn_per_cm
        if density == None :
            density = -1 * self.density_g_per_cm3

        material_card = 'mat ' + self.description + ' ' + str(density) + '\n'

        for counter, element_mixture in enumerate(self.element_mixtures):

            #print(element_mixture)
            #print(type(element_mixture))

            element=element_mixture['element']

            if 'atom_fraction' in element_mixture.keys():
                #print('using atom fraction')
                element_atom_fraction = self.find_element_atom_fractions()[counter] #element_mixture['atom_fraction']
            else:
                #print('using mass fraction')
                element_mass_fraction = self.find_element_mass_fractions()[counter] #element_mixture['mass_fraction']/element.molar_mass_g
                element_atom_fraction = element_mass_fraction/element.molar_mass_g

            #print('element.isotopes',element.isotopes)
            for isotope in element.isotopes:

                isotopes_atom_fraction=isotope.abundance * element_atom_fraction
                if isotopes_atom_fraction>0:
                    if isotope.zaid in list_of_isotope_zaid_or_name:
                        index_of_zaid = list_of_isotope_zaid_or_name.index(isotope.zaid)
                        lib= list_of_associated_libraries[index_of_zaid]
                        material_card = material_card + ('    ' + (isotope.zaid +'.'+ lib).ljust(12)+ ' ' + str(isotopes_atom_fraction).ljust(25) + ' % '+isotope.symbol+' \n')
                    else:
                        #print('isotope not found in xsdir, using default library ')
                        #print('isotope.zaid=',isotope.zaid)
                        material_card = material_card + ('    ' + (isotope.zaid).ljust(12)+' ' +str(isotopes_atom_fraction).ljust(25) + ' % '+isotope.symbol+' not in xsdir \n')
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

