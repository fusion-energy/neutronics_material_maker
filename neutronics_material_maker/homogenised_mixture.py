
import re
import sys
import json
import pprint

from neutronics_material_maker.material import Material
from neutronics_material_maker.compound import Compound
from neutronics_material_maker.jsonable_object import NamedObject

class Homogenised_mixture(NamedObject):
    def __init__(self, list_of_items_and_fractions):
        super(Homogenised_mixture, self).__init__()


        # print(items)
        # print(volume_fractions)
        # print(mass_fractions)
        # sys.exit()
        self.description = self.find_description(list_of_items_and_fractions)
        self.mass_fractions=self.find_mass_fractions(list_of_items_and_fractions)
        self.volume_fractions=self.find_volume_fractions(list_of_items_and_fractions)
        self.items=self.find_items(list_of_items_and_fractions)
        self.density_g_per_cm3 = self.find_density_g_per_cm3(self.items,self.volume_fractions)



        self.serpent_material_card= self.find_serpent_material_card(self.density_g_per_cm3,
                                                                    self.items,
                                                                    self.volume_fractions,
                                                                    self.mass_fractions)




    def find_items(self,list_of_items_and_fractions):
        items=[]
        for item in list_of_items_and_fractions: #list_of_items_and_volume_fractions:
            print(item)
            items.append(item['mix'])
        return items



    def find_mass_fractions(self,list_of_items_and_fractions):
        print(list_of_items_and_fractions)
        mass_fraction_not_found=False
        for item in list_of_items_and_fractions:
            if 'mass_fraction' in item.keys():
                pass
            else:
                mass_fraction_not_found=True

        list_of_fractions=[]
        if mass_fraction_not_found==False:
            for item in list_of_items_and_fractions:
                list_of_fractions.append(item['mass_fraction'])
            if sum(list_of_fractions)==1.0:
                return list_of_fractions
            else:
                print('error 2 inputted mass fractions should add up to 1.0')

                sys.exit()

        else:
            cumlative_mass_fraction=0
            for item in list_of_items_and_fractions:
                # print(item.keys())

                item['mass_fraction'] =item['volume_fraction'] *item['mix'].density_g_per_cm3

                cumlative_mass_fraction = cumlative_mass_fraction + item['mass_fraction']

            factor = 1.0 / cumlative_mass_fraction

            for item in list_of_items_and_fractions:
                item['mass_fraction'] = item['mass_fraction'] * factor

                list_of_fractions.append(item['mass_fraction'])

                print('vol_frac', item['volume_fraction'], ' from mass fraction ', item['mass_fraction'], ' at density ',
                      item['mix'].density_g_per_cm3)

            a = sum(list_of_fractions)
            b = 1.0
            rtol = 1e-6

            if abs(a - b) <= rtol * max(abs(a), abs(b)):

            #if sum(list_of_fractions) == 1.0:

                return list_of_fractions

            else:

                print('error 1 inputted volume fractions should add up to 1.0')

                sys.exit()


    def find_volume_fractions(self,list_of_items_and_fractions):
        #print(list_of_items_and_fractions)
        print(list_of_items_and_fractions)
        volume_fraction_not_found = False
        for item in list_of_items_and_fractions:
            if 'volume_fraction' in item.keys():
                pass
            else:
                volume_fraction_not_found = True

        list_of_fractions = []
        if volume_fraction_not_found == False:
            for item in list_of_items_and_fractions:
                list_of_fractions.append(item['volume_fraction'])
            if sum(list_of_fractions)==1.0:
                return list_of_fractions
            else:
                print('error 3 inputted volume fractions should add up to 1.0')
                sys.exit()

        else:
            cumlative_vol_fraction=0
            for item in list_of_items_and_fractions:
                #print(item.keys())
                item['volume_fraction']=item['mass_fraction']/item['mix'].density_g_per_cm3
                cumlative_vol_fraction = cumlative_vol_fraction+ item['volume_fraction']
            factor = 1.0/cumlative_vol_fraction
            for item in list_of_items_and_fractions:
                item['volume_fraction'] = item['volume_fraction']*factor
                list_of_fractions.append(item['volume_fraction'])
                print('vol_frac',item['volume_fraction'],' from mass fraction ', item['mass_fraction'],' at density ',item['mix'].density_g_per_cm3)
            a = sum(list_of_fractions)
            b = 1.0
            rtol = 1e-6

            if abs(a - b) <= rtol * max(abs(a), abs(b)):
                return list_of_fractions
            else:
                print('error 4 inputted mass fractions should add up to 1.0')
                sys.exit()

    def find_density_g_per_cm3(self,items,volume_fractions):
        cumlative_density = 0
        for item, volume in zip(items,volume_fractions):
            cumlative_density = cumlative_density + (item.density_g_per_cm3 * volume)
        # todo allow density combinations involving atom_per_barn_cm2
        return cumlative_density



    def find_serpent_material_card(self,density_g_per_cm3,items, volume_fractions, mass_fractions):
        comment = '%   '
        material_card='mat '+self.description
        material_card = material_card + '  -' + str(density_g_per_cm3) + '\n'

        for item, volume_fraction, mass_fraction in zip(items, volume_fractions, mass_fractions):

            print(item.description)
            #print('    ',type(item))
            #print('    ',item.zaids)
            #print(item.molar_mass_g)
            #print('    sum',sum(item.isotopes_atom_fractions))


            average_mass_of_one_atom = 0.0
            for isotope, atom_fraction in zip(item.isotopes, item.isotopes_atom_fractions):
                print('    isotope.mass_amu * atom_fraction',isotope.mass_amu , atom_fraction)
                average_mass_of_one_atom = average_mass_of_one_atom + isotope.mass_amu * atom_fraction
            number_of_atoms_per_cm3_of_item = item.density_g_per_cm3 / (average_mass_of_one_atom * 1.66054e-24)

            print('    number_of_atoms_per_cm3_of_item',number_of_atoms_per_cm3_of_item)
            number_of_atoms_per_cm3_of_mix = number_of_atoms_per_cm3_of_item*volume_fraction/7.66e22
            print('    number_of_atoms_per_cm3_of_mix',number_of_atoms_per_cm3_of_mix)

            material_card = material_card + comment+'\n'+comment + item.description + ' with a density of '+ str(item.density_g_per_cm3) +'gcm-3 \n'
            material_card = material_card + comment+ 'volume fraction of ' + str(volume_fraction) + ' \n'
            material_card = material_card + comment+ 'mass fraction of ' + str(mass_fraction) + ' \n'
            for zaid, isotopes_atom_fraction in zip(item.zaids, item.isotopes_atom_fractions):
        #
        #
        #          print(zaid,isotopes_atom_fraction,volume_fraction)
                  if zaid.startswith('160'):
                      material_card = material_card + ('    '+zaid + '.03c ' + str(isotopes_atom_fraction*number_of_atoms_per_cm3_of_mix) + '\n')
                  else:
                      material_card = material_card + ('    '+zaid + '.31c ' + str(isotopes_atom_fraction*number_of_atoms_per_cm3_of_mix) + '\n')
        #
        return material_card


    def find_description(self,list_of_items_and_fractions):

        description_to_return=''
        print(list(list_of_items_and_fractions[0].keys()))

        try:
            for entry in list_of_items_and_fractions:
                item = entry['mix']
                volume = entry['volume_fraction']
                description_to_return = description_to_return+ item.description
                description_to_return = description_to_return+ '_vf_' + str(volume) + '_'
        except:
            print('exception found')
            for entry in list_of_items_and_fractions:
                item = entry['mix']
                volume = entry['mass_fraction']
                description_to_return = description_to_return+ item.description
                description_to_return = description_to_return+ '_mf_' + str(volume) + '_'

        if description_to_return.endswith('_'):
            description_to_return=description_to_return[:-1]

        return description_to_return

# mat_Epoxy = Material('r-epoxy')
# mat_copper = Compound('Cu', density_g_per_cm3=8.96)
# mat_Nb3Sn = Compound('Nb3Sn', density_g_per_cm3=8.91)  # 'Nb0.746Sn0.254' density assumes perfect latice
# mat_liqHe = Compound('He', density_g_per_cm3=0.125)
# mat_ss316 = Material('SS-316LN-IG')
# mat_bronze = Material('Bronze')
#
#
#
# m25 =Homogenised_mixture([{'mix':mat_Epoxy,      'volume_fraction':0.18},
#                               {'mix':mat_copper, 'volume_fraction':0.1169},
#                               {'mix':mat_Nb3Sn,  'volume_fraction': 0.02895},
#                               {'mix':mat_liqHe,  'volume_fraction':0.1682},
#                               {'mix':mat_ss316,  'volume_fraction':0.4319+0.00055},
#                               {'mix': mat_bronze,'volume_fraction': 0.0735}])
#
#
# print(m25.serpent_material_card)

# mat_bronze = Material('Bronze')
# print(mat_bronze.density_g_per_cm3)
#
# mat_water = Compound('H2O', density_g_per_cm3=0.926)
# print(mat_water.density_g_per_cm3)
#
# # mat_mix = Homogenised_mixture([{'mix':mat_water,'volume_fraction':0.20},
# #                                {'mix':mat_bronze, 'volume_fraction': 0.80}
# #                               ])
#
# mat_mix = Homogenised_mixture([{'mix':mat_water,'mass_fraction':0.20},
#                                {'mix':mat_bronze, 'mass_fraction': 0.80}
#                               ])
#
# print(mat_mix.volume_fractions)

#
# mat_CuCrZr = Compound('CuCrZr', density_g_per_cm3=8.814)
# print(mat_CuCrZr.density_g_per_cm3)
# mat_mix = Homogenised_mixture([(mat_water, 0.20), (mat_CuCrZr, 0.30), (mat_bronze, 0.5)])
# print(mat_mix.density_g_per_cm3)
# print(mat_mix.serpent_material_card)

