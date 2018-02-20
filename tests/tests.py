
# these test cover the functionality of neutronics material maker

# to run type

# python -m pytest tests.py
# python3 -m pytest tests.py

# requires pytest (pip install pytest)

import neutronics_material_maker as nmm
import numpy
import random


def test_isotopes_zaid():
    new_isotope = nmm.Isotope('Li',7)
    assert new_isotope.zaid == '3007'

def test_isotopes_neutrons():
    new_isotope = nmm.Isotope('Li',7)    
    assert new_isotope.neutrons == 4

def test_isotope_symbol():
    new_isotope = nmm.Isotope('Li',7)    
    assert new_isotope.symbol == 'Li'

def test_isotope_protons():
    new_isotope = nmm.Isotope('Li',7)    
    assert new_isotope.protons == 3

def test_isotope_description():
    new_isotope = nmm.Isotope('Li',7)    
    assert type(new_isotope.description) == dict

def test_atomic_number():
    new_isotope = nmm.Isotope('Li',7)    
    assert new_isotope.atomic_number == 7



def test_element_protons():
    new_element = nmm.Element('Fe')
    assert new_element.protons == 26

def test_element_symbol():
    new_element = nmm.Element('Fe')
    assert new_element.symbol == 'Fe'

def test_element_enriched_isotope_natural():
    new_element = nmm.Element('Fe')
    assert new_element.enriched_isotopes == 'Natural'

def test_element_enriched_isotopes():
    new_element = nmm.Element('Li',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
    assert len(new_element.enriched_isotopes) == 2
# todo another test for enriched element to check actual isotopes are correct

def test_element_molar_mass_g():
    new_element = nmm.Element('Fe')
    assert new_element.molar_mass_g == 55.845144433865904

def test_element_isotopes():
    new_element = nmm.Element('Fe')
    assert len(new_element.isotopes) == 4   



def test_compound_chemical_equation():
    new_compound = nmm.Compound('Li4SiO4')
    assert new_compound.chemical_equation == 'Li4SiO4'  

def test_compound_enriched_isotopes_natural():
    new_compound = nmm.Compound('Li4SiO4')
    assert new_compound.enriched_isotopes == 'Natural' 

def test_compound_enriched_isotopes():
    new_compound = nmm.Compound('Li4SiO4',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
    assert len(new_compound.enriched_isotopes) == 2


def test_compound_packing_fraction():
    new_compound = nmm.Compound('Li4SiO4',packing_fraction=0.64)
    assert new_compound.packing_fraction == 0.64 

def test_compound_packing_fraction():
    new_compound_solid = nmm.Compound('Li4SiO4')
    new_compound_pebble = nmm.Compound('Li4SiO4',packing_fraction=0.64)
    assert (numpy.isclose(new_compound_solid.density_g_per_cm3*0.64,new_compound_pebble.density_g_per_cm3,rtol=1e-15)) == True
    #assert new_compound_solid.density_g_per_cm3*0.64==new_compound_pebble.density_g_per_cm3

def test_material_serpent_material_card_type():
    new_material = nmm.Material('SS-316LN-IG')
    assert type(new_material.serpent_material_card) == str

def test_material_atom_density_per_barn_per_cm():
    new_material = nmm.Material('SS-316LN-IG')
    assert new_material.density_g_per_cm3 > 0

def test_material_density_g_per_cm3():
    new_material = nmm.Material('SS-316LN-IG')
    assert new_material.density_g_per_cm3 > 0


def test_material_description():
    new_material = nmm.Material('SS-316LN-IG')
    assert new_material.description == 'SS-316LN-IG'

def test_material_element_mixtures_type():
    new_material = nmm.Material('SS-316LN-IG')
    assert type(new_material.element_mixtures) == list

def test_material_find_material_mass_or_atom_faction_mixture_length():
    new_material = nmm.Material('SS-316LN-IG')
    assert len(new_material.find_material_mass_or_atom_faction_mixture('SS-316LN-IG'))==len(new_material.element_mixtures)

def test_material_find_material_mass_or_atom_faction_mixture_length():
    new_material = nmm.Material('DT-plasma')
    assert len(new_material.find_material_mass_or_atom_faction_mixture('DT-plasma')) == len(new_material.element_mixtures)

# def test_all_natural_elements():
#     all_elements = nmm.all_natural_elements()
#     for x in range(0,rand.randint(1,5)):
#         rand.randint(0,len(all_elements))

def test_broken_element():
    z = nmm.Compound('zzzz', density_g_per_cm3=1)
    try:
        test_mat_card = z.serpent_material_card
        assert False
    except:
        assert True




def test_all_natural_elements():
    all_elements = nmm.all_natural_elements()
    for fuss_test in range(0,1500):
        chemical_equation_to_test = ''
        equation_length = random.randint(1, 5)
        for x in range(0, random.randint(1, equation_length)):
            randint1 = random.randint(0, len(all_elements)-1)
            randint2 = random.randint(1, 100)
            next_element = all_elements[randint1].symbol
            next_multiplier = str(randint2)
            chemical_equation_to_test = chemical_equation_to_test + next_element + next_multiplier

            random_density = random.uniform(0, 23)
            print('fuzzy test',chemical_equation_to_test,random_density)
            fuzzy_test_compound = nmm.Compound(chemical_equation_to_test, density_g_per_cm3=random_density)
            #fuzzy_test_compound = nmm.Compound('zzzz', density_g_per_cm3=1)
            try:
                test_mat_card = fuzzy_test_compound.serpent_material_card
                assert fuzzy_test_compound.chemical_equation == chemical_equation_to_test
                assert type(fuzzy_test_compound.serpent_material_card) == str
                assert fuzzy_test_compound.density_g_per_cm3 == random_density
            except:
                assert False


# todo more tests on compounds
# theoretical_density
# pressure_Pa
# temperature_K
# density_g_per_cm3
# density_g_per_cm3_idea_gas
# elements
# fractions_coefficients
# isotopes_mass_fractions
# zaids
# serpent_material_card_zaid
# molar_mass_g
# mass_kg
# volume_m3
# description
# find_density_kg_per_m3
# find_density_g_per_cm3

    #[Isotope(symbol, 54), Isotope(symbol, 56), Isotope(symbol, 57),Isotope(symbol, 58)]
    # todo perhaps also test isotopes produced are correct isotopes

#
# import numpy
#
#
# mat_bronze = nmm.Material('Bronze')
# print(mat_bronze.density_g_per_cm3)
#
# mat_water = nmm.Compound('H2O', density_g_per_cm3=0.926)
# print(mat_water.density_g_per_cm3)
#
# mat_CuCrZr = nmm.Compound('CuCrZr', density_g_per_cm3=8.814)
# print(mat_CuCrZr.density_g_per_cm3)
# mat_mix = nmm.Homogenised_mixture([(mat_water, 0.20), (mat_CuCrZr, 0.30), (mat_bronze, 0.5)])
# print(mat_mix.density_g_per_cm3)
# print(mat_mix.serpent_material_card)
#
# for enrichment in numpy.linspace(0, 1, num=5):
#     example_compound = nmm.Compound('Li4SiO4', enriched_isotopes=(
#     nmm.Isotope('Li', 6, enrichment), nmm.Isotope('Li', 7, 1.0 - enrichment)))
#     print(enrichment)
#     print(example_compound.density_g_per_cm3)
#     print(example_compound.element_atom_fractions)
#     print(example_compound.serpent_material_card)





#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

# class test_Compound():

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)





# if __name__ == "__main__":

#     mat_tung = Material('Eurofer')
#     print(mat_tung.serpent_material_card_zaid)
    #print(mat_tung.density_g_per_cm3)
    #print(mat_tung.elements)
    #for element in mat_tung.elements:
    #    print(element.full_name)

    #com_tung = Compound('W',density_g_per_cm3=19.298)
    #print(com_tung.serpent_material_card_zaid)
    # example_element = Element('Li')
    # example_element = Element('Li', enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
    #
    # print(example_element.natural_isotopes_in_elements)
    #
    # print(example_element.molar_mass_g)
    #
    # print(example_element.protons)
    #
    # print(example_element.isotopes)
    #
    # print(example_element.full_name)


    # #plain isotopes
    #iso1 = Isotope('Li',7,0.5)
    #print(iso1.abundance)
    # iso2 = Isotope(3, 6)
    # print(iso1.__dict__)
    # print(iso2.description)
    #
    # #plain material
    # mat =Material('Eurofer')
    # print(mat.name)
    # print(mat.isotopes)
    # print(mat.density_g_per_cm3)
    # print(mat.isotopes_mass_fractions)
    # print(mat.serpent_material_card_zaid)
    #
    # # #plain compound
    # mat = Compound('Li4SiO4')
    # mat.density_g_per_cm3
    # print(mat.description)
    # #print(mat.serpent_material_card_zaid)
    # #
    # # #enriched compound
    # mat = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
    # print(mat.serpent_material_card_zaid)
    #mat = Compound('Li4SiO4',packing_fraction=0.68,theoretical_density=0.98,enriched_isotopes=(Isotope('Li',6,0.9),Isotope('Li',7,0.1)))
    # mat = Compound('Pb84.2Li15.8')#,packing_fraction=1.0,theoretical_density=1.0,enriched_isotopes=(Isotope('Li',6,0.9),Isotope('Li',7,0.1)))
    # print(mat.description)
    # print(mat.density_g_per_cm3)
    # print(mat.serpent_material_card_zaid)
    #
    # #pebble bed compound
    # mat_pebble = Compound('Be12Ti', packing_fraction=0.64)
    # mat_solid = Compound('Be12Ti')
    # print('density pebble ',mat_pebble.density_g_per_cm3)
    # print('density solid ',mat_solid.density_g_per_cm3)
    #
    # #gaseous compound
    # mat = Compound('He', pressure_Pa = 8.0E6, temperature_K = 823.0)
    # print('density of high temperature high pressure ideal gas = ',mat.density_g_per_cm3_idea_gas)

    #mixed compound
    #mat1 = Compound('Li4SiO4',packing_fraction=0.64,  enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
    #mat2 = Compound('Be12Ti', packing_fraction=0.64)
    #mat3 = Homogenised_mixture([(mat1,0.5),(mat2,0.5)])
    #print(mat3.serpent_material_card_zaid)

    # #plain material
    #mat = Material('Eurofer')
    #print(mat.serpent_material_card_zaid)
    #
    # #mixed material
    #mat1 = Compound(chemical_equation='Li4SiO4',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
    #print(mat1.to_dict())
    #mat2 = Compound(chemical_equation='He', pressure_Pa = 8.0E6, temperature_K = 823.0)
    # print(mat1.__dict__)
    #hom_mat = Homogenised_mixture([(mat1, 0.8), (mat2, 0.2)])
    # print(hom_mat.serpent_material_card_zaid)
    #print(hom_mat.to_dict())
    #pprint.pprint(hom_mat.to_dict())

    # mat_water = Compound('H2O',density_g_per_cm3=0.926)
    # print(mat_water.density_g_per_cm3)
    # print(mat_water.serpent_material_card_zaid)
    #
    # mat_CuCrZr = Compound('CuCrZr',density_g_per_cm3=8.814)
    # print(mat_CuCrZr.density_g_per_cm3) #m74 32.8% water, 18.4% CuCrZr, 9.38% copper, (remainder 39.42 Tungsten)
    # print(mat_CuCrZr.serpent_material_card_zaid)
    # #
    # mat_copper = Material('SS-316L-IG')
    # print(mat_copper.density_g_per_cm3) #m74 32.8% water, 18.4% CuCrZr, 9.38% copper, (remainder 39.42 Tungsten)
    # print(mat_copper.serpent_material_card_zaid)

    # mat_Tungsten = Material('DT_plasma')
    # print(mat_Tungsten.atom_density_per_barn_per_cm)
    # print(mat_Tungsten.serpent_material_card_zaid)
    #
    # mat_Tungsten = Material('Tungsten')
    # print(mat_Tungsten.density_g_per_cm3)
    # print(mat_Tungsten.serpent_material_card_zaid)
    # #
    #mat_divertor_layer_2 = Homogenised_mixture([(mat_water, 0.328), (mat_CuCrZr, 0.184), (mat_copper,0.0938), (mat_Tungsten,0.3942)])
    # mat_divertor_layer_2 = Homogenised_mixture([(mat_water, 0.25), (mat_CuCrZr, 0.25), (mat_copper,0.5)])
    #
    # print(mat_divertor_layer_2.density_g_per_cm3)
    # print(mat_divertor_layer_2.serpent_material_card_zaid)
    #
    #
    #

    # for enrichment in [0.25,0.50,0.75,1.0]:
    #     example_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, enrichment), Isotope('Li', 7, 1.0-enrichment)))
    #     print(example_compound.density_g_per_cm3)