



from neutronics_material_maker.nmm import *
from neutronics_material_maker.examples import *

import random
import unittest
import pytest
import math



class Isotope_tests(unittest.TestCase):

    def test_isotopes_class_name(self):
        example_iso = Isotope(symbol='Li',nucleons=6)
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

    def test_isotope_material_card_mass_fraction_prefix(self):
        new_isotope = Isotope('Li',7,abundance=0.6,density_g_per_cm3=7)
        material_card = new_isotope.material_card(fractions ='isotope mass fractions')
        string_value = material_card.split('\n')[-1].split()[1]
        numeric_value = float(string_value)
        assert numeric_value == -1
        assert string_value == '-1'

    def test_isotope_material_card_atom_fraction_prefix(self):
        new_isotope = Isotope('Li',7,abundance=0.6,density_g_per_cm3=7)
        material_card = new_isotope.material_card(fractions ='isotope atom fractions')
        string_value = material_card.split('\n')[-1].split()[1]
        numeric_value = float(string_value)
        assert numeric_value == 1
        assert string_value == '1'

    def test_isotope_atomic_number(self):
        new_isotope = Isotope('Li',7)    
        assert new_isotope.nucleons == 7

    # def test_isotope_symbol_setting():

    # def test_isotope_atomic_number_setting():

    # def test_isotope_protons_setting():

    def test_isotope_material_card_name(self):
        example_iso = Isotope(symbol='Li',nucleons=6)
        assert example_iso.material_card_name == 'Lithium_6'

    def test_isotope_nuclear_library(self):
        example_iso = Isotope(symbol='Li',nucleons=6)
        options = ['','.31c']
        assert example_iso.nuclear_library in options        

    def test_failed_isotope_creation(self):
        with pytest.raises(ValueError):
            example_iso = Isotope(nucleons=6) # not enough information provided, should fail

   
    def test_default_temperature_in_material_cards(self):

      mat_isotope = Isotope('Li',7,abundance=0.6,density_g_per_cm3=7)

      assert 'temperature =293.15 K' in mat_isotope.material_card(code='mcnp')
      assert 'tmp 293.15' in mat_isotope.material_card(code='serpent')

   
    def test_specified_temperature_in_material_cards(self):

      mat_isotope = Isotope('Li',7,abundance=0.6,density_g_per_cm3=7,temperature_K =500)

      assert 'temperature =500 K' in mat_isotope.material_card(code='mcnp')
      assert 'tmp 500' in mat_isotope.material_card(code='serpent')      

    def test_overwritten_temperature_in_material_cards(self):

      mat_isotope = Isotope('Li',7,abundance=0.6,density_g_per_cm3=7,temperature_K =500)

      assert 'temperature =600 K' in mat_isotope.material_card(code='mcnp',temperature_K =600)
      assert 'tmp 600' in mat_isotope.material_card(code='serpent',temperature_K =600)            



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
        assert math.isclose(new_element.molar_mass_g_per_mol, 55.845144433865904)

    def test_element_isotopes(self):
        new_element = Element('Fe')
        assert len(new_element.isotopes) == 4

    def test_element_nuclear_library(self):
        new_element = Element('Fe')
        options = ['','.31c']
        for iso in new_element.isotopes:
          assert iso.nuclear_library in options             

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


    def test_element_material_card_type(self):
        new_element = Element('W',density_g_per_cm3=19.6)
        assert type(new_element.material_card())== str

    def test_element_mass_and_atom_fractions_summation(self):

        new_element = Element('W',density_g_per_cm3=19.6)
        assert math.isclose(sum(new_element.isotope_mass_fractions),1)
        assert math.isclose(sum(new_element.isotope_atom_fractions),1)      

        new_element = Element('Al',density_g_per_cm3=19.6)
        assert math.isclose(sum(new_element.isotope_mass_fractions),1)
        assert math.isclose(sum(new_element.isotope_atom_fractions),1)    

    def test_default_temperature_in_material_cards(self):

      new_element = Element('W',density_g_per_cm3=19.6)

      assert 'temperature =293.15 K' in new_element.material_card(code='mcnp')
      assert 'tmp 293.15' in new_element.material_card(code='serpent')

   
    def test_specified_temperature_in_material_cards(self):

      new_element = Element('W',density_g_per_cm3=19.6,temperature_K =500)
    
      assert 'temperature =500 K' in new_element.material_card(code='mcnp')
      assert 'tmp 500' in new_element.material_card(code='serpent')      

    def test_overwritten_temperature_in_material_cards(self):

      new_element = Element('W',density_g_per_cm3=19.6,temperature_K =500)

      assert 'temperature =600 K' in new_element.material_card(code='mcnp',temperature_K =600)
      assert 'tmp 600' in new_element.material_card(code='serpent',temperature_K =600)   


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
        with pytest.raises(KeyError):
            z = Compound('zzzz', density_g_per_cm3=1)
            test_mat_card = z.material_card()

    def test_element_nuclear_library(self):
        new_compound = Compound('Li2Fe2')
        options = ['','.31c']
        for iso in new_compound.isotopes:
          assert iso.nuclear_library in options

    def test_compound_material_card_creation(self):
        new_compound = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14)
        assert type(new_compound.material_card()) == str           

    def test_default_temperature_in_material_cards(self):

      new_compound = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14)

      assert 'temperature =293.15 K' in new_compound.material_card(code='mcnp')
      assert 'tmp 293.15' in new_compound.material_card(code='serpent')

   
    def test_specified_temperature_in_material_cards(self):

      new_compound = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14,
                       temperature_K =500)
    
      assert 'temperature =500 K' in new_compound.material_card(code='mcnp')
      assert 'tmp 500' in new_compound.material_card(code='serpent')      

    def test_overwritten_temperature_in_material_cards(self):

      new_compound = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14,
                       temperature_K =500)

      assert 'temperature =600 K' in new_compound.material_card(code='mcnp',temperature_K =600)
      assert 'tmp 600' in new_compound.material_card(code='serpent',temperature_K =600)   

    def test_compound_atom_and_mass_fractions_sumations(self):
        mat_Li = Compound('Li',
                               volume_of_unit_cell_cm3=0.42701e-21,
                               atoms_per_unit_cell=8,
                               packing_fraction=0.6,
                               enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])

        assert math.isclose(sum(mat_Li.isotope_atom_fractions),1)
        assert math.isclose(sum(mat_Li.isotope_mass_fractions),1)#==1

        mat_Li3 = Compound('Li3',
                               volume_of_unit_cell_cm3=0.42701e-21,
                               atoms_per_unit_cell=8,
                               packing_fraction=0.6,
                               enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])

        assert math.isclose(sum(mat_Li3.isotope_atom_fractions),1)
        assert math.isclose(sum(mat_Li3.isotope_mass_fractions),1)


        mat_Li3O = Compound('Li30',
                               volume_of_unit_cell_cm3=0.42701e-21,
                               atoms_per_unit_cell=8,
                               packing_fraction=0.6,
                               enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])

        assert math.isclose(sum(mat_Li3O.isotope_atom_fractions),1)
        assert math.isclose(sum(mat_Li3O.isotope_mass_fractions),1)

        mat_Li3O2 = Compound('Li302',
                               volume_of_unit_cell_cm3=0.42701e-21,
                               atoms_per_unit_cell=8,
                               packing_fraction=0.6,
                               enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])

        assert math.isclose(sum(mat_Li3O2.isotope_atom_fractions),1)
        assert math.isclose(sum(mat_Li3O2.isotope_mass_fractions),1)


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
                               element_mass_fractions=[0.88821,
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

        assert type(mat_Eurofer.material_card()) == str


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
                                  element_mass_fractions=[0.63684,
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
                                  element_mass_fractions=[0.63684,
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
                                  element_mass_fractions=[0.63684,
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




    def test_Material_mass_and_atom_fractions_single_isotope_element(self):
        mat_1 = Material(material_card_name='M1',
                            density_g_per_cm3=20.0,
                            elements=[Element(symbol='Al')],
                            element_mass_fractions=[1])

        mat_2 = Material(material_card_name='M1',
                            density_g_per_cm3=20.0,
                            elements=[Element(symbol='Al')],
                            element_atom_fractions=[1])
   
        assert mat_1.isotope_atom_fractions == [1]
        assert mat_1.isotope_mass_fractions == [1]
        assert mat_2.isotope_atom_fractions == [1]
        assert mat_2.isotope_mass_fractions == [1]



    def test_Material_mass_and_atom_fractions_multi_isotope_element(self):
        mat_1 = Material(material_card_name='M1',
                            density_g_per_cm3=20.0,
                            elements=[Element(symbol='Sn')],
                            element_mass_fractions=[1])

        mat_2 = Material(material_card_name='M2',
                            density_g_per_cm3=10.0,
                            elements=[Element(symbol='Sn')],
                            element_atom_fractions=[1])

        assert math.isclose(sum(mat_1.isotope_atom_fractions) , 1)
        assert math.isclose(sum(mat_1.isotope_mass_fractions) , 1)
        assert math.isclose(sum(mat_2.isotope_atom_fractions) , 1)
        assert math.isclose(sum(mat_2.isotope_mass_fractions) , 1)



    def test_Material_mass_fraction_multi_elements(self):
        # Defintion for portland from Compendium of Material Composition Data for Radiation Transport Modeling 
        # https://www.pnnl.gov/main/publications/external/technical_reports/pnnl-15870.pdf
        mat_portland = Material(material_card_name='M1',
                            density_g_per_cm3=2.30 ,
                            elements=[Element(symbol='H'),
                                      Element(symbol='C'),
                                      Element(symbol='O'),
                                      Element(symbol='Na'),
                                      Element(symbol='Mg'),
                                      Element(symbol='Al'),
                                      Element(symbol='Si'),
                                      Element(symbol='K'),
                                      Element(symbol='Ca'),
                                      Element(symbol='Fe')],
                            #element_mass_fractions=[0.010000,0.001000,0.529107,0.01600,0.002000,0.033872,0.337021,0.013000,0.044000,0.014000]
                            element_atom_fractions=[0.168759,0.001416,0.562522,0.011838,0.001400,0.021354,0.204115,0.005656,0.018674,0.004264]
                            )
        print(mat_portland.material_card(fractions='isotope mass fractions'))
        print('sum m_f',sum(mat_portland.element_mass_fractions))
        print('m_f',mat_portland.element_mass_fractions)

        print('sum a_f',sum(mat_portland.element_atom_fractions))
        print('a_f',mat_portland.element_atom_fractions)

        known_m_fs=[0.010000,0.001000,0.529107,0.01600,0.002000,0.033872,0.337021,0.013000,0.044000,0.014000]

        for calc_m_f, known_m_f in zip(mat_portland.element_mass_fractions,known_m_fs):
          assert math.isclose(calc_m_f, known_m_f,rel_tol=5e-04)

    def test_Material_atom_fraction_multi_elements(self):
        # Defintion for portland from Compendium of Material Composition Data for Radiation Transport Modeling 
        # https://www.pnnl.gov/main/publications/external/technical_reports/pnnl-15870.pdf
        mat_portland = Material(material_card_name='M1',
                            density_g_per_cm3=2.3,
                            elements=[Element(symbol='H'),
                                      Element(symbol='C'),
                                      Element(symbol='O'),
                                      Element(symbol='Na'),
                                      Element(symbol='Mg'),
                                      Element(symbol='Al'),
                                      Element(symbol='Si'),
                                      Element(symbol='K'),
                                      Element(symbol='Ca'),
                                      Element(symbol='Fe')],
                            element_mass_fractions=[0.010000,0.001000,0.529107,0.01600,0.002000,0.033872,0.337021,0.013000,0.044000,0.014000]
                            #element_atom_fractions=[0.168759,0.001416,0.562522,0.011838,0.001400,0.021354,0.204115,0.005656,0.018674,0.004264]
                            )
        print(mat_portland.material_card(fractions='isotope mass fractions'))
        print('sum m_f',sum(mat_portland.element_mass_fractions))
        print('m_f',mat_portland.element_mass_fractions)

        print('sum a_f',sum(mat_portland.element_atom_fractions))
        print('a_f',mat_portland.element_atom_fractions)

        known_a_fs=[0.010000,0.001000,0.529107,0.01600,0.002000,0.033872,0.337021,0.013000,0.044000,0.014000]

        for calc_a_f, known_a_f in zip(mat_portland.element_mass_fractions,known_a_fs):
          assert math.isclose(calc_a_f, known_a_f,rel_tol=5e-04)          


    def test_default_temperature_in_material_cards(self):

      new_material = Material(material_card_name='M2',
                    density_g_per_cm3=10.0,
                    elements=[Element(symbol='Sn')],
                    element_atom_fractions=[1])

      assert 'temperature =293.15 K' in new_material.material_card(code='mcnp')
      assert 'tmp 293.15' in new_material.material_card(code='serpent')

   
    def test_specified_temperature_in_material_cards(self):

      new_material = Material(material_card_name='M2',
                    density_g_per_cm3=10.0,
                    elements=[Element(symbol='Sn')],
                    element_atom_fractions=[1],
                    temperature_K=500)
    
      assert 'temperature =500 K' in new_material.material_card(code='mcnp')
      assert 'tmp 500' in new_material.material_card(code='serpent')      

    def test_overwritten_temperature_in_material_cards(self):

      new_material = Material(material_card_name='M2',
                    density_g_per_cm3=10.0,
                    elements=[Element(symbol='Sn')],
                    element_atom_fractions=[1],
                    temperature_K=500)

      assert 'temperature =600 K' in new_material.material_card(code='mcnp',temperature_K =600)
      assert 'tmp 600' in new_material.material_card(code='serpent',temperature_K =600)  


    def test_all_natural_elements(self):
        all_elements = Natural_Elements().all_natural_element_symbols
        for fuss_test in range(0,50):
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
                    test_mat_card = fuzzy_test_compound.material_card
                    assert fuzzy_test_compound.chemical_equation == chemical_equation_to_test
                    assert type(fuzzy_test_compound.material_card()) == str
                    assert fuzzy_test_compound.density_g_per_cm3 == random_density
                except:
                    assert False

class Homogenised_mixture_tests(unittest.TestCase):


  def test_Homogenised_mixture_card_creation1(self):
    mat_He_in_coolant_plates = Compound('He',pressure_Pa=8.0E6,temperature_K=823 ,state_of_matter='liquid')
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
                      element_mass_fractions=[0.88821,
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
    mat_cooling_plates_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_coolant_plates],
                                                        volume_fractions=[0.727,0.273])

    assert type(mat_cooling_plates_homogenised.material_card(code='serpent',fractions='isotope atom fractions')) == str
    assert type(mat_cooling_plates_homogenised.material_card(code='mcnp', fractions='isotope atom fractions')) == str
    assert type(mat_cooling_plates_homogenised.material_card(code='serpent', fractions='isotope mass fractions')) == str
    assert type(mat_cooling_plates_homogenised.material_card(code='mcnp', fractions='isotope mass fractions')) == str
    assert type(mat_cooling_plates_homogenised.material_card(code='mcnp')) == str
    assert type(mat_cooling_plates_homogenised.material_card()) == str
    assert type(mat_cooling_plates_homogenised.volume_fractions) == list
    assert type(mat_cooling_plates_homogenised.mixtures) == list

  def test_Homogenised_mixture_density_1(self):
    mat_Li4SiO4 = Compound('Li4SiO4',
                         volume_of_unit_cell_cm3=1.1543e-21,
                         atoms_per_unit_cell=14,
                         packing_fraction=0.6,
                         enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
    mat_Be = Compound('Be',
                    volume_of_unit_cell_cm3=0.01622e-21,
                    atoms_per_unit_cell=2,
                    packing_fraction=0.3)

    mat_mixed_pebble_bed = Homogenised_mixture(mixtures=[mat_Be,mat_Li4SiO4],
                                                volume_fractions=[0.6,0.4])
    mix1 = mat_Be.density_g_per_cm3*0.6
    mix2 = mat_Li4SiO4.density_g_per_cm3*0.4

    assert mat_mixed_pebble_bed.density_g_per_cm3 == mix1+mix2

  def test_Homogenised_mixture_isotope_atom_and_mass_fractions_in_symertrical_mix(self):

    mat_Li_a = Compound('Li',
                           volume_of_unit_cell_cm3=0.42701e-21,
                           atoms_per_unit_cell=8,
                           packing_fraction=0.6,
                           enriched_isotopes=[Isotope('Li',7,abundance=0.5),Isotope('Li',6,abundance=0.5)])

    mat_Li_b = Compound('Li',
                           volume_of_unit_cell_cm3=0.42701e-21,
                           atoms_per_unit_cell=8,
                           packing_fraction=0.6,
                           enriched_isotopes=[Isotope('Li',7,abundance=0.5),Isotope('Li',6,abundance=0.5)])

    mat_mixed_pebble_bed_vol_combined = Homogenised_mixture(mixtures=[mat_Li_a,mat_Li_b],
                                                        volume_fractions=[0.5,0.5])



    for mf in mat_mixed_pebble_bed_vol_combined.mass_fractions:
        assert mf == 0.5
        

    for vf in mat_mixed_pebble_bed_vol_combined.volume_fractions:
        assert vf == 0.5

    for i_a_f in mat_mixed_pebble_bed_vol_combined.isotope_atom_fractions:
        assert i_a_f == 0.25

    assert mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[0]+mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[1]==mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[2]+mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[3]
    assert mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[0]==mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[2]
    assert mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[1]==mat_mixed_pebble_bed_vol_combined.isotope_mass_fractions[3]

    mat_mixed_pebble_bed_mass_combined = Homogenised_mixture(mixtures=[mat_Li_a,mat_Li_b],
                                                        mass_fractions=[0.5,0.5])    

    for mf in mat_mixed_pebble_bed_mass_combined.mass_fractions:
        assert mf == 0.5

    for vf in mat_mixed_pebble_bed_mass_combined.volume_fractions:
        assert vf == 0.5

    for i_a_f in mat_mixed_pebble_bed_mass_combined.isotope_atom_fractions:
        assert i_a_f == 0.25

    assert mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[0]+mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[1]==mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[2]+mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[3]
    assert mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[0]==mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[2]
    assert mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[1]==mat_mixed_pebble_bed_mass_combined.isotope_mass_fractions[3] 





class Example_materials_tests(unittest.TestCase):

  def test_material_example_materials(self):
    assert type(mat_Li4SiO4.material_card())==str
    assert type(mat_Li2SiO3.material_card())==str
    assert type(mat_Li2ZrO3.material_card())==str
    assert type(mat_Li2TiO3.material_card())==str
    assert type(mat_Be.material_card())==str
    assert type(mat_Be12Ti.material_card())==str
    assert type(mat_Ba5Pb3.material_card())==str
    assert type(mat_Nd5Pb4.material_card())==str
    assert type(mat_Zr5Pb3.material_card())==str
    assert type(mat_Zr5Pb4.material_card())==str
    assert type(mat_Lithium_Lead.material_card())==str
    assert type(mat_Tungsten.material_card())==str
    assert type(mat_Eurofer.material_card())==str
    assert type(mat_SS316LN_IG.material_card())==str
    assert type(mat_Bronze.material_card())==str
    assert type(mat_Glass_fibre.material_card())==str
    assert type(mat_Epoxy.material_card())==str
    assert type(mat_CuCrZr.material_card())==str
    assert type(mat_r_epoxy.material_card())==str
    assert type(mat_DT_plasma.material_card())==str
    assert type(mat_Void.material_card())==str
    assert type(mat_water_by_density.material_card())==str
    assert type(mat_copper.material_card())==str
    assert type(mat_divertor_layer_1_m15.material_card())==str
    assert type(mat_divertor_layer_2_m74.material_card())==str
    assert type(mat_divertor_layer_3_m15.material_card())==str
    assert type(mat_divertor_layer_4_m75.material_card())==str
    assert type(mat_water_by_pres_temp.material_card())==str
    assert type(mat_VV_Body_m60.material_card())==str
    assert type(mat_VV_Shell_m50.material_card())==str
    assert type(mat_ShieldPort_m60.material_card())==str
    assert type(mat_Nb3Sn.material_card())==str
    assert type(mat_liqHe.material_card())==str
    assert type(mat_TF_Magnet_m25.material_card())==str
    assert type(mat_TF_Casing_m50.material_card())==str
    assert type(mat_central_solenoid_m25.material_card())==str
    assert type(mat_He_in_coolant_plates.material_card())==str
    assert type(mat_He_in_end_caps.material_card())==str
    assert type(mat_He_in_first_walls.material_card())==str
    assert type(mat_He_coolant_back_plate.material_card())==str
    assert type(mat_mixed_pebble_bed.material_card())==str
    assert type(mat_cooling_plates_homogenised.material_card())==str
    assert type(mat_end_caps_homogenised.material_card())==str
    assert type(mat_first_wall_homogenised.material_card())==str
    assert type(mat_mixed_pebble_bed.material_card())==str
