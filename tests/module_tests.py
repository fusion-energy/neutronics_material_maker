



from neutronics_material_maker.nmm import *

import random
import unittest
import pytest




class Isotope_tests(unittest.TestCase):

    def test_isotopes_class_name(self):
        example_iso = Isotope(symbol='Li',atomic_number=6)
        print(example_iso.classname)
        assert example_iso.classname=='Isotope'

    def test_isotopes_zaid(self):
        new_isotope = Isotope('Li',7)
        assert new_isotope.zaid == '3007'

    def test_isotopes_neutrons(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.neutrons == 4

    def test_isotope_symbol(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.symbol == 'Li'

    def test_isotope_protons(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.protons == 3

    def test_isotope_material_card_name(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.material_card_name == 'Lithium_7'

    def test_isotope_atomic_number(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.atomic_number == 7

    # def test_isotope_symbol_setting():

    # def test_isotope_atomic_number_setting():

    # def test_isotope_protons_setting():

    def test_material_card_name(self):
        example_iso = Isotope(symbol='Li',atomic_number=6)
        assert example_iso.material_card_name == 'Lithium_6'

    def test_failed_isotope_creation(self):
        with pytest.raises(ValueError):
            example_iso = Isotope(atomic_number=6) # not enough information provided, should fail

class Element_tests(unittest.TestCase):

    def test_element_protons(self):
        new_element = Element('Fe')
        assert new_element.protons == 26

    def test_element_symbol(self):
        new_element = Element('Fe')
        assert new_element.symbol == 'Fe'

    def test_element_enriched_isotopes(self):
        new_element = Element('Li',isotopes=[Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)])
        assert len(new_element.isotopes) == 2
    # todo another test for enriched element to check actual isotopes are correct

    def test_element_molar_mass_g(self):
        new_element = Element('Fe')
        assert new_element.molar_mass_g == 55.845144433865904

    def test_element_isotopes(self):
        new_element = Element('Fe')
        assert len(new_element.isotopes) == 4

    def test_all_elements_have_natural_isotope_fractions_summing_to_1(self):
        all_elements = Natural_Elements().all_natural_elements

        for element in all_elements:

            print(element.isotopes)
            isotopes = element.isotopes
            sum_of_isotope_abundances = 0
            for isotope in isotopes:
                sum_of_isotope_abundances = sum_of_isotope_abundances + isotope.abundance
            a = 1.0
            b = sum_of_isotope_abundances

            rtol = 1e-15

            if abs(a - b) <= rtol * max(abs(a), abs(b)):
                print('isotope fraction sum to 1 or nearly 1')
                assert True
            else:
                print("isotope fractions don't sum to 1.0")
                print("element = ", element.symbol)
                # for isotope in isotopes:
                # print(isotope.abundance)
                print(sum_of_isotope_abundances)
                assert False



class Compound_tests(unittest.TestCase):

    def test_compound_class_name(self):
        example_iso = Compound(chemical_equation='Li4SiO4')
        print(example_iso.classname)
        assert example_iso.classname=='Compound'

    def test_compound_chemical_equation(self):
         new_compound = Compound('Li4SiO4')
         assert new_compound.chemical_equation == 'Li4SiO4'  

    def test_compound_enriched_isotopes(self):
        new_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
        assert len(new_compound.enriched_isotopes) == 2

    def test_compound_packing_fraction(self):
        new_compound = Compound('Li4SiO4',packing_fraction=0.64)
        assert new_compound.packing_fraction == 0.64

    def test_compound_creation_broken(self):
        with pytest.raises(ValueError):
            z = Compound('zzzz', density_g_per_cm3=1)
            test_mat_card = z.serpent_material_card()



class Material_tests(unittest.TestCase):

    def test_material_serpent_card_creation(self):

        mat_Eurofer = Material(material_card_name='Eurofer',
                               density_g_per_cm3=7.87,
                               density_atoms_per_barn_per_cm=8.43211E-02,
                               elements=[Element('Fe'),
                                         Element('B'),
                                         Element('C'),
                                         Element('N'),
                                         Element('O'),
                                         Element('Al'),
                                         Element('Si'),
                                         Element('P'),
                                         Element('S'),
                                         Element('Ti'),
                                         Element('V'),
                                         Element('Cr'),
                                         Element('Mn'),
                                         Element('Co'),
                                         Element('Ni'),
                                         Element('Cu'),
                                         Element('Nb'),
                                         Element('Mo'),
                                         Element('Ta'),
                                         Element('W')
                                         ],
                               mass_fractions=[0.88821,
                                               0.00001,
                                               0.00105,
                                               0.00040,
                                               0.00001,
                                               0.00004,
                                               0.00026,
                                               0.00002,
                                               0.00003,
                                               0.00001,
                                               0.00020,
                                               0.09000,
                                               0.00550,
                                               0.00005,
                                               0.00010,
                                               0.00003,
                                               0.00005,
                                               0.00003,
                                               0.00120,
                                               0.01100
                                               ])

        assert type(mat_Eurofer.serpent_material_card()) == str


    def test_material_atom_density_g_per_cm3(self):

        mat_SS316LN_IG = Material(material_card_name='SS316LN-IG',
                                  density_g_per_cm3=7.93,
                                  density_atoms_per_barn_per_cm=8.58294E-02,
                                  elements=[Element('Fe'),
                                            Element('C'),
                                            Element('Mn'),
                                            Element('Si'),
                                            Element('P'),
                                            Element('S'),
                                            Element('Cr'),
                                            Element('Ni'),
                                            Element('Mo'),
                                            Element('N'),
                                            Element('B'),
                                            Element('Cu'),
                                            Element('Co'),
                                            Element('Nb'),
                                            Element('Ti'),
                                            Element('Ta')
                                            ],
                                  mass_fractions=[0.63684,
                                                  0.0003,
                                                  0.02,
                                                  0.0050,
                                                  0.00025,
                                                  0.0001,
                                                  0.180,
                                                  0.1250,
                                                  0.0270,
                                                  0.0008,
                                                  0.00001,
                                                  0.0030,
                                                  0.0005,
                                                  0.0001,
                                                  0.001,
                                                  0.0001,
                                                  ])

        assert mat_SS316LN_IG.density_g_per_cm3 == 7.93

    def test_material_description(self):

        mat_SS316LN_IG = Material(material_card_name='SS316LN-IG',
                                  density_g_per_cm3=7.93,
                                  density_atoms_per_barn_per_cm=8.58294E-02,
                                  elements=[Element('Fe'),
                                            Element('C'),
                                            Element('Mn'),
                                            Element('Si'),
                                            Element('P'),
                                            Element('S'),
                                            Element('Cr'),
                                            Element('Ni'),
                                            Element('Mo'),
                                            Element('N'),
                                            Element('B'),
                                            Element('Cu'),
                                            Element('Co'),
                                            Element('Nb'),
                                            Element('Ti'),
                                            Element('Ta')
                                            ],
                                  mass_fractions=[0.63684,
                                                  0.0003,
                                                  0.02,
                                                  0.0050,
                                                  0.00025,
                                                  0.0001,
                                                  0.180,
                                                  0.1250,
                                                  0.0270,
                                                  0.0008,
                                                  0.00001,
                                                  0.0030,
                                                  0.0005,
                                                  0.0001,
                                                  0.001,
                                                  0.0001,
                                                  ])

        assert mat_SS316LN_IG.material_card_name == 'SS316LN-IG'

    def test_material_element_mixtures_type(self):
        mat_SS316LN_IG = Material(material_card_name='SS316LN-IG',
                                  density_g_per_cm3=7.93,
                                  density_atoms_per_barn_per_cm=8.58294E-02,
                                  elements=[Element('Fe'),
                                            Element('C'),
                                            Element('Mn'),
                                            Element('Si'),
                                            Element('P'),
                                            Element('S'),
                                            Element('Cr'),
                                            Element('Ni'),
                                            Element('Mo'),
                                            Element('N'),
                                            Element('B'),
                                            Element('Cu'),
                                            Element('Co'),
                                            Element('Nb'),
                                            Element('Ti'),
                                            Element('Ta')
                                            ],
                                  mass_fractions=[0.63684,
                                                  0.0003,
                                                  0.02,
                                                  0.0050,
                                                  0.00025,
                                                  0.0001,
                                                  0.180,
                                                  0.1250,
                                                  0.0270,
                                                  0.0008,
                                                  0.00001,
                                                  0.0030,
                                                  0.0005,
                                                  0.0001,
                                                  0.001,
                                                  0.0001,
                                                  ])

        assert type(mat_SS316LN_IG.elements) == list


    def test_all_natural_elements(self):
        all_elements = Natural_Elements().all_natural_element_symbols
        for fuss_test in range(0,500):
            chemical_equation_to_test = ''
            equation_length = random.randint(1, 5)
            for x in range(0, random.randint(1, equation_length)):
                randint1 = random.randint(0, len(all_elements)-1)
                randint2 = random.randint(1, 100)
                next_element = Element(all_elements[randint1])
                next_multiplier = str(randint2)
                chemical_equation_to_test = chemical_equation_to_test + next_element.symbol + next_multiplier

                random_density = random.uniform(0, 23)
                print('fuzzy test',chemical_equation_to_test,random_density)
                fuzzy_test_compound = Compound(chemical_equation_to_test, density_g_per_cm3=random_density)
                #fuzzy_test_compound = Compound('zzzz', density_g_per_cm3=1)
                try:
                    test_mat_card = fuzzy_test_compound.serpent_material_card
                    assert fuzzy_test_compound.chemical_equation == chemical_equation_to_test
                    assert type(fuzzy_test_compound.serpent_material_card()) == str
                    assert fuzzy_test_compound.density_g_per_cm3 == random_density
                except:
                    assert False

