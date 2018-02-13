
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
class Material(NamedObject):
    def __init__(self,name):#,*enriched_isotopes):
        super(Material, self).__init__()
        self.name = name
        self.elements = self.find_elements_in_material(name)
        self.element_fractions = self.element_fractions(name)
        #self.enriched_isotopes = enriched_isotopes
        #if enriched_isotopes:
        #    print('enriched materials not yet implemented')
        #    sys.exit()

    def element_fractions(self,name):
        if name =='Tungsten':
            fractions =elements=[1.0]
        if name == 'Eurofer':
            fractions = [88.935/100.0,
                        0.005/100.0,
                        0.11/100.0,
                        0.03/100.0,
                        # Element(8),
                        # Element(13),
                        0.05/100.0,
                        # Element(15),
                        # Element(16),
                        # Element(22),
                        0.25/100.0,
                        9.0/100.0,
                        0.4/100.0,
                        # Element(27),
                        # Element(28),
                        # Element(29),
                        # Element(41),
                        # Element(42),
                        0.12/100.0,
                        1.1/100.0
                        ]
            return fractions


    def find_elements_in_material(self,name):
        print('name',name)
        if name =='Tungsten':
            elements=[Element('W')
            ]
        if name == 'Eurofer':
            elements = [Element(26),
                        Element(5),
                        Element(6),
                        Element(7),
                        # Element(8),
                        # Element(13),
                        Element(14),
                        # Element(15),
                        # Element(16),
                        # Element(22),
                        Element(23),
                        Element(24),
                        Element(25),
                        # Element(27),
                        # Element(28),
                        # Element(29),
                        # Element(41),
                        # Element(42),
                        Element(73),
                        Element(74)
                        ]
            #[26054, 26056, 26057, 26058,
            # 5010, 5011,
            # 6012,
            # 7014, 7015,
            # 8016,
            # 13027,
            # 14028, 14029, 14030,
            # 15031, 16032,
             # 16033, 16034, 16036,
            # 22046, 22047, 22048,
            # 22049, 22050,
            # 23050, 23051,
            # 24050, 24052, 24053, 24054,
            # 25055,
             # 27059,
            # 28058, 28060, 28061, 28062, 28064,
            # 29063, 29065,
            # 41093,
            # 42092, 42094, 42095, 42096, 42097, 42098, 42100,
            # 73181,
            # 74182, 74183, 74184, 74186]
        return elements



    @property
    def available_materials(self):
        return ['Tungsten','Eurofer','Homogenous_Magnet','DT_plasma','SS-316L-IG']



    @property
    def is_this_available(self):
        if self.name in ['Tungsten','Eurofer','Homogenous_Magnet','DT_plasma','SS-316L-IG']:
            return True
        else: return False


    @property
    def zaids(self):
        if self.is_this_available:
            if self.name == 'Eurofer':
                list_of_zaids = [26054, 26056, 26057, 26058, 5010, 5011, 6012, 7014, 7015, 8016, 13027, 14028, 14029, 14030, 15031,16032, 16033, 16034, 16036, 22046, 22047, 22048, 22049, 22050, 23050, 23051, 24050, 24052, 24053,             24054, 25055, 27059, 28058, 28060, 28061, 28062, 28064, 29063, 29065, 41093, 42092, 42094, 42095,42096, 42097, 42098, 42100, 73181, 74182, 74183, 74184, 74186]
            if self.name == 'Homogenous_Magnet':
                list_of_zaids = [1001,6012,7014,8016,12024,12025,12026,13027,14028,14029,14030,16032,16033,16034,16036,29063,29065,41093,50112,50114,50115,50116,50117,50118,50119,50120,50122,50124,2004,5010,5011,6012,7014,8016,13027,14028,15031,16032,16033,16034,16036,19039,19040,19041,22046,22047,22048,22049,22050,23050,23051,24050,24052,24053,24054,25055,26054,26056,26057,26058,27059,28058,28060,28061,28062,28064,29063,29065,40090,40091,40092,40094,40096,41093,42092,42094,42095,42096,42097,42098,42100,50112,50114,50115,50116,50117,50118,50119,50120,50122,50124,73181,74182,74183,74184,74186,82206,82207,82208,83209,29063,29065,50112,50114,50115,50116,50117,50118,50119,50120,50122,50124]
            if self.name == 'SS-316L-IG':
                list_of_zaids = [26054,26056,26057,26058, 6012,25055,14028,14029,14030,15031,16032,16033,16034,16036,24050,24052,24053,24054,28058,28060,28061,28062,28064,42092,42094,42095,42096,42097,42098,42100, 7014, 7015, 5010, 5011,29063,29065,27059,41093,22046,22047,22048,22049,22050,73181]
            if self.name == 'DT_plasma':
                list_of_zaids = [1002,1003]
            if self.name == 'Tungsten':
                list_of_zaids = [74182,74183,74184,74186]
            list_of_zaids_string=[]
            for item in list_of_zaids:
                list_of_zaids_string.append(str(item)) #.zfill(3)
            return list_of_zaids_string
        else:
            return self.name +' is not in the available materials please ask Jon to add it'




    @property
    def atom_density_per_barn_per_cm(self):
        if self.name == 'DT_plasma':
            return 1E-20
        if self.name == 'Homogenous_Magnet':
            return 7.194E-02
        else:
            print('material not found, current materials available are ',self.available_materials)
            print('perhaps try density_g_per_cm3 property')
            sys.exit()

    @property
    def density_g_per_cm3(self):
        if self.name == 'Eurofer':
            return 7750.0/1000.0

        if self.name == 'SS-316L-IG':
            return 7930.0/1000.0

        if self.name == 'Tungsten':
            return 19298.0/1000.0

        # if self.name == 'plasma':
        #     return self.atom_density_per_barn_per_cm * 1E24 * ((Isotope('H',2).mass_amu+Isotope('H',2).mass_amu)/2.0)*1.660539040E-27*1000.0

        else:
            print('material not found, current materials available are ',self.is_this_available)
            print('perhaps try atom_density_per_barn_per_cm property')
            sys.exit()

    @property
    def isotopes_mass_fractions(self):
        isotope_list = []
        if self.name == 'Eurofer':
            return [4.56563E-03, 6.91110E-02, 1.56807E-03, 2.05084E-04, 9.43123E-07, 3.45108E-06, 4.14310E-04, 1.34911E-04,4.65085E-07, 2.95487E-06, 7.02121E-06, 4.05884E-05, 1.98991E-06, 1.26804E-06, 3.05762E-06, 4.21784E-06,3.27443E-08, 1.79397E-07, 7.89886E-10, 8.49986E-08, 7.50223E-08, 7.27880E-07, 5.23259E-08, 4.90993E-08,4.651675e-8, 0.00001856018, 3.70662E-04, 6.87292E-03, 7.64630E-04, 1.86808E-04, 4.73931E-04, 4.01637E-06,5.56272E-06, 2.07132E-06, 8.85630E-08, 2.77823E-07, 6.85423E-08, 1.56104E-06, 6.74368E-07, 2.54802E-06,2.29342E-07, 1.39911E-07, 2.38263E-07, 2.47037E-07, 1.39981E-07, 3.50081E-07, 1.36919E-07, 3.14209E-05,7.59071E-05, 4.07659E-05, 8.68119E-05, 7.96842E-05]
        if self.name == 'Homogenous_Magnet':
            return [3.89340E-03,3.40560E-03,3.70800E-04,4.87080E-03,1.69197E-04,2.14200E-05,2.35834E-05,7.07400E-04,1.32800E-03,6.72000E-05,4.46000E-03,8.71457E-05,6.97680E-07,3.93822E-06,1.83600E-08,6.83585E-03,3.05684E-03,1.18439E-03,3.82953E-06,2.60566E-06,1.34231E-06,5.74035E-05,3.03204E-05,9.56198E-05,3.39131E-05,1.28625E-04,1.82791E-05,2.28587E-05,3.08888E-03,4.06294E-07,1.48738E-06,1.70203E-04,2.77382E-04,2.55621E-06,2.27302E-04,7.27891E-05,1.65004E-05,8.47338E-07,6.78371E-09,3.82922E-08,1.78519E-10,2.43807E-07,3.05877E-11,1.75950E-08,1.40904E-06,1.27070E-06,1.259086E-05,9.23990E-07,8.84708E-07,4.013075e-9,0.00000160121,3.03427E-04,5.67045E-03,6.34294E-04,1.55150E-04,5.58169E-04,1.46579E-03,2.21899E-02,5.16004E-04,7.24415E-05,1.73444E-05,2.89354E-03,1.07976E-03,5.07463E-05,1.46193E-04,4.48851E-05,2.24477E-05,9.72920E-06,2.30510E-07,5.02686E-08,7.68366E-08,7.78671E-08,1.25448E-08,1.21022E-05,6.32488E-05,3.94240E-05,6.78518E-05,7.10910E-05,4.24074E-05,1.02843E-04,4.10435E-05,3.34089E-09,2.27319E-09,1.17103E-09,5.00790E-08,2.64516E-08,8.34190E-08,2.95859E-08,1.12213E-07,1.59467E-08,1.99420E-08,5.64891E-08,2.96623E-08,1.60908E-08,3.40070E-08,3.12220E-08,1.78732E-08,1.78578E-08,4.19446E-08,7.82589E-08,3.38912E-03,1.51554E-03,2.54666E-06,1.73278E-06,8.92643E-07,3.81736E-05,2.01632E-05,6.35877E-05,2.25524E-05,8.55362E-05,1.21557E-05,1.52012E-0]
        if self.name == 'SS-316L-IG':
            return [3.29181E-03,4.98289E-02,1.13058E-03,1.47865E-04,1.19277E-04,1.73653E-03,7.86496E-04,3.85593E-05,2.45713E-05,3.85117E-05,1.41667E-05,1.09980E-07,6.02549E-07,2.65303E-09,7.46975E-04,1.38506E-02,1.54092E-03,3.76464E-04,7.00641E-03,2.60890E-03,1.11548E-04,3.49927E-04,8.63311E-05,2.07981E-04,1.26880E-04,2.16071E-04,2.24028E-04,1.26943E-04,3.17475E-04,1.24166E-04,2.71878E-04,9.37261E-07,9.50314E-07,3.47739E-06,1.57294E-04,6.79509E-05,4.04699E-05,5.13489E-06,8.56466E-06,7.55943E-06,7.33429E-05,5.27248E-06,4.94736E-06,2.63837E-06]
        if self.name == 'DT_plasma':
            return [0.5, 0.5]
        if self.name == 'Tungsten':
            return [1.6733E-02,9.0295E-03,1.9322E-02,1.7933E-02]
        else:
            print('material mass fraction not found, current materials available are ',self.is_this_available)

    @property
    def serpent_material_card_zaid(self):
        try:
            material_card = 'mat ' + self.name + ' -' + str(self.density_g_per_cm3) + '\n'
        except:
            material_card = 'mat ' + self.name + ' ' + str(self.atom_density_per_barn_per_cm) + '\n'

        for element , element_fractions in zip(self.elements,self.element_fractions):
            for isotope in element.isotopes:
                isotopes_mass_fraction=str(isotope.abundance * element_fractions)

                if isotope.zaid.startswith('160'):
                    material_card = material_card + ('  l  ' + isotope.zaid + '.03c ' + isotopes_mass_fraction + '\n')
                else:
                    material_card = material_card + ('  l  ' + isotope.zaid + '.31c ' + isotopes_mass_fraction + '\n')

        # old method
        # for zaid, isotopes_mass_fraction in zip(self.zaids, self.isotopes_mass_fractions):
        #     #str_zaid = str(zaid).zfill(6)
        #     if zaid.startswith('160'):
        #         material_card = material_card + ('    '+zaid + '.03c ' + str(isotopes_mass_fraction) + '\n')
        #     else:
        #         material_card = material_card + ('    '+zaid + '.31c ' + str(isotopes_mass_fraction) + '\n')

        return material_card

    @property
    def description(self):

        # list_of_enriched_isotope_keys = []
        # if self.enriched_isotopes:
        #     list_of_enriched_isotope_keys.append('_')
        #     for enriched_isotope in self.enriched_isotopes:
        #         for entry in enriched_isotope:
        #             list_of_enriched_isotope_keys.append(
        #                 entry.symbol + str(entry.atomic_number) + '_' + str(entry.abundance))
        #
        #     return self.name + '_'.join(list_of_enriched_isotope_keys)
        # else:
        return self.name
