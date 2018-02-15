
import re
import sys
import json
import pprint

class NamedObject(object):
    def __init__(self):
        self.classname = self.__class__.__name__

    def to_dict(self):

        def obj_dict(obj):
            return obj.__dict__

        return json.loads(json.dumps(self, default=obj_dict))#, indent=4, sort_keys=False))

class Homogenised_mixture(NamedObject):
    def __init__(self, list_of_items_and_volume_fractions):
        super(Homogenised_mixture, self).__init__()

        volume_fractions,items=[],[]
        for item in list_of_items_and_volume_fractions:
            volume_fractions.append(item[1])
            items.append(item[0])

        self.volume_fractions=volume_fractions
        self.items=items

        if sum(self.volume_fractions) == 1.0:
            pass
        else:
            print('Volume fractions must be between 0 and 1 and add upto 1')
            print(volume_fractions)
            print(sum(self.volume_fractions))
            sys.exit()

    @property
    def density_g_per_cm3(self):
        cumlative_density = 0
        for item, volume in zip(self.items,self.volume_fractions):
            cumlative_density = cumlative_density + (item.density_g_per_cm3 * volume)
        #print('cumlative_density',cumlative_density)
        return cumlative_density

    @property
    def serpent_material_card_zaid(self):

        material_card='mat '+self.description
        material_card = material_card + '  -' + str(self.density_g_per_cm3) + '\n'

        #for compound, volume_fraction in zip([self.compound1,self.compound2],[self.volume_fraction1,self.volume_fraction2]):
        for item, volume_fraction in zip(self.items, self.volume_fractions):
            for zaid, isotopes_mass_fraction in zip(item.zaids, item.isotopes_mass_fractions):
                if zaid.startswith('160'):
                    material_card = material_card + ('    '+zaid + '.03c ' + str(isotopes_mass_fraction*volume_fraction) + '\n')
                else:
                    material_card = material_card + ('    '+zaid + '.31c ' + str(isotopes_mass_fraction*volume_fraction) + '\n')

        return material_card

    @property
    def description(self):

        description_to_return=''

        for item, volume in zip(self.items, self.volume_fractions):
            description_to_return = description_to_return+ item.description
            # if compound.enriched_isotopes!='Natural':
            #     print('compound.enriched_isotopes',compound.enriched_isotopes)
            #     for enriched_isotopes in compound.enriched_isotopes:
            #         description_to_return = description_to_return +'_'+ enriched_isotopes.symbol + str(enriched_isotopes.atomic_number) + '_' + str(enriched_isotopes.abundance)
            description_to_return = description_to_return+ '_vf_' + str(volume) + '_'


        return description_to_return


mat_steel = Material('SS-316LN-IG')


mat_bronze = Material('Bronze')


mat_Tungsten = Material('Tungsten')


mat_divertor_layer_2 = Homogenised_mixture([(mat_water, 0.25), (mat_CuCrZr, 0.25), (mat_copper,0.5)])