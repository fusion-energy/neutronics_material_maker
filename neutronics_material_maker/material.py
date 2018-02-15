
import re
import sys
import json
import pprint

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



from element import Element

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
        self.element_mixture = self.find_element_mass_faction_mixture(name)
        self.elements = self.find_elements_in_material(name)
        self.element_atom_fractions = self.find_element_atom_fractions()
        self.element_mass_fractions = self.find_element_mass_fractions()
        #self.enriched_isotopes = enriched_isotopes
        #if enriched_isotopes:
        #    print('enriched materials not yet implemented')
        #    sys.exit()



    # todo export material as pyne material
    # example
    # pyne.material.Material(
    #     {922350000: 0.07359999999999998, 922380000: 0.8464, 942390000: 0.03999999999999998, 942410000: 0.03999999999999998},
    #     50.0, -1.0, -1.0, {})

    def find_element_mass_faction_mixture(self, name):

        if name == 'Eurofer':
            #weight fractions
            return [(Element('Fe'),0.88821),
                    (Element('B') ,0.00001),
                    (Element('C') ,0.00105),
                    (Element('N') ,0.00040),
                    (Element('O') ,0.00001),
                    (Element('Al'),0.00004),
                    (Element('Si'),0.00026),
                    (Element('P') ,0.00002),
                    (Element('S') ,0.00003),
                    (Element('Ti'),0.00001),
                    (Element('V') ,0.00200),
                    (Element('Cr'),0.09000),
                    (Element('Mn'),0.00550),
                    (Element('Co'),0.00005),
                    (Element('Ni'),0.00010),
                    (Element('Cu'),0.00003),
                    (Element('Nb'),0.00005),
                    (Element('Mo'),0.00003),
                    (Element('Ta'),0.00120),
                    (Element('W') ,0.01100),
                    ]
        if name == 'SS-316-LN': #(cryogenic steel)
            'SS-316L(n)-IG'
            'r-epoxy'

        # if name == 'SS-316L-IG':
        # if name == 'DT-plasma':

    def find_elements_in_material(self,name):
       list_of_elements=[]
       for element_element_fractions in self.element_mixture:
            list_of_elements.append(element_element_fractions[0])
       return list_of_elements


    def find_element_mass_fractions(self):
        list_of_fractions=[]
        for element_element_fractions in self.element_mixture:
            list_of_fractions.append(element_element_fractions[1])

        a = sum(list_of_fractions)
        b = 1.0

        rtol=1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            print('element mass fractions within a material must sum to 1')
            print('current mass factions are ',list_of_fractions)
            print('which sums to ',sum(list_of_fractions))
            sys.exit()

        return list_of_fractions

    def find_element_atom_fractions(self):
        list_of_fractions=[]
        for element_element_fractions in self.element_mixture:

            print('element_element_fractions[1]',element_element_fractions[1])
            print('element_element_fractions[0].molar_mass_g',element_element_fractions[0].molar_mass_g)
            list_of_fractions.append(element_element_fractions[1]/element_element_fractions[0].molar_mass_g)


        # todo normalise the mass fractions so the add up to 1
        # this commend out code below will check the fractions add up to 1
        # a = sum(list_of_fractions)
        # b = 1.0
        #
        # rtol=1e-6
        #
        # if not abs(a - b) <= rtol * max(abs(a), abs(b)):
        #
        #     print('element atom fractions within a material must sum to 1')
        #     print('current atom factions are ',list_of_fractions)
        #     print('which sums to ',sum(list_of_fractions))
        #     sys.exit()

        return list_of_fractions          

                        


    @property
    def atom_density_per_barn_per_cm(self):
        if self.name == 'DT_plasma':
            return 1E-20
        if self.name == 'SS-316L(n)-IG':
            return 8.58294E-02
        else:
            print('material not found in atom_density_per_barn_per_cm function')
            print('perhaps try density_g_per_cm3 property')
            sys.exit()

    @property
    def density_g_per_cm3(self):
        if self.name == 'Eurofer':
            return  7.79800

        if self.name == 'SS-316L(n)-IG':
            return 7.93

        if self.name == 'Tungsten':
            return 19298.0/1000.0

        else:
            print('material not found in density_g_per_cm3 function')
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

        for element_element_fractions,element_atom_fraction in zip(self.element_mixture,self.element_atom_fractions):

            element=element_element_fractions[0]
            #element_mass_fraction=element_element_fractions[1]

            for isotope in element.isotopes:
                isotopes_mass_fraction=isotope.abundance * element_atom_fraction
                if isotopes_mass_fraction>0:
                    isotopes_mass_fraction=str(isotopes_mass_fraction)
                    if isotope.zaid.startswith('160') :
                        #todo Serpent appears to be not compatible with particular Fendl libraries, check the updated version of Serpent
                        material_card = material_card + ('    ' + isotope.zaid + '.03c ' + isotopes_mass_fraction + '\n')
                    else:
                        material_card = material_card + ('    ' + isotope.zaid + '.31c ' + isotopes_mass_fraction + '\n')
                else:
                    print('isotope massfraction is 0, ignoring')
                    print(isotope.abundance ,'*', element_fractions)

        return material_card


for e in Material('Eurofer').element_mixture:
    print(e)

for e in Material('Eurofer').elements:
    print(e)

for e in Material('Eurofer').element_mass_fractions:
    print(e)

print(Material('Eurofer').serpent_material_card_zaid)