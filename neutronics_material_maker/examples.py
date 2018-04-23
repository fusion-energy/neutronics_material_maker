
# from nmm import *
from neutronics_material_maker.nmm import *




mat_Li4SiO4 = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Li4SiO4.serpent_material_card())

mat_Li2SiO3 = Compound('Li2SiO3',
                       volume_of_unit_cell_cm3=0.23632e-21,
                       atoms_per_unit_cell=4,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Li2SiO3.serpent_material_card())

mat_Li2ZrO3 = Compound('Li2ZrO3',
                       volume_of_unit_cell_cm3=0.24479e-21,
                       atoms_per_unit_cell=4,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Li2ZrO3.serpent_material_card())


mat_Li2TiO3 = Compound('Li2TiO3',
                       volume_of_unit_cell_cm3=0.42701e-21,
                       atoms_per_unit_cell=8,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Li2TiO3.serpent_material_card())


mat_Be = Compound('Be',
                  volume_of_unit_cell_cm3=0.01622e-21,
                  atoms_per_unit_cell=2,
                  packing_fraction=0.6)
print(mat_Be.serpent_material_card())


mat_Be12Ti = Compound('Be12Ti',
                      volume_of_unit_cell_cm3= 0.22724e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Be12Ti.serpent_material_card())


mat_Ba5Pb3 = Compound('Ba5Pb3',
                      volume_of_unit_cell_cm3=1.37583e-21,
                      atoms_per_unit_cell=4,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Ba5Pb3.serpent_material_card())


mat_Nd5Pb4 = Compound('Nd5Pb4',
                      volume_of_unit_cell_cm3= 1.06090e-21,
                      atoms_per_unit_cell=4,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Nd5Pb4.serpent_material_card())


mat_Zr5Pb3 = Compound('Zr5Pb3',
                      volume_of_unit_cell_cm3=0.36925e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Zr5Pb3.serpent_material_card())


mat_Zr5Pb4 = Compound('Zr5Pb4',
                      volume_of_unit_cell_cm3=0.40435e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
print(mat_Zr5Pb4.serpent_material_card())


mat_Lithium_Lead = Compound('Pb84.2Li15.8',
                            density_atoms_per_barn_per_cm=3.2720171E-2,
                            enriched_isotopes=[Isotope('Li',7,abundance=0.247317371169),
                                               Isotope('Li',6,abundance=0.752682628831)])
print(mat_Lithium_Lead.serpent_material_card())







mat_Tungsten = Material(material_card_name='Tungsten',
                    density_g_per_cm3=19.0,
                    color=(10,128,128),
                    elements=[Element(symbol='W'),
                              Element(symbol='Ag'),
                              Element(symbol='Al'),
                              Element(symbol='As'),
                              Element(symbol='Ba'),
                              Element(symbol='Ca'),
                              Element(symbol='Cd'),
                              Element(symbol='Co'),
                              Element(symbol='Cr'),
                              Element(symbol='Cu'),
                              Element(symbol='Fe'),
                              Element(symbol='K'),
                              Element(symbol='Mg'),
                              Element(symbol='Mn'),
                              Element(symbol='Na'),
                              Element(symbol='Nb'),
                              Element(symbol='Ni'),
                              Element(symbol='Pb'),
                              Element(symbol='Ta'),
                              Element(symbol='Ti'),
                              Element(symbol='Zn'),
                              Element(symbol='Zr'),
                              Element(symbol='Mo'),
                              Element(symbol='C'),
                              Element(symbol='H'),
                              Element(symbol='N'),
                              Element(symbol='O'),
                              Element(symbol='P'),
                              Element(symbol='S'),
                              Element(symbol='Si'),
                             ],
                    mass_fractions=[1e6-405,
                                    10,
                                    15,
                                    5,
                                    5,
                                    5,
                                    5,
                                    10,
                                    20,
                                    10,
                                    30,
                                    10,
                                    5,
                                    5,
                                    10,
                                    10,
                                    5,
                                    5,
                                    20,
                                    5,
                                    5,
                                    5,
                                    100,
                                    30,
                                    5,
                                    5,
                                    20,
                                    20,
                                    5,
                                    20,])
#print(mat_Tungsten.serpent_material_card())

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

#print(mat_Eurofer.serpent_material_card())

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

#print(mat_SS316LN_IG.serpent_material_card())

mat_Bronze = Material(material_card_name='Bronze',
                    density_g_per_cm3=8.8775,
                    elements=[Element('Cu'),
                              Element('Sn')
                             ],
                    atom_fractions=[0.95,
                                    0.05
                    ])

#print(mat_Bronze.serpent_material_card())

#
mat_Glass_fibre = Material(material_card_name='Glass-fibre',
                    density_g_per_cm3=2.49,
                    elements=[Element('H'),
                              Element('O'),
                              Element(12),
                              Element(13),
                              Element(14)
                             ],
                    mass_fractions=[0.0000383948,
                                    0.6328110447,
                                    0.0499936947,
                                    0.1026861642,
                                    0.2144707015
                                    ])

mat_Epoxy = Material(material_card_name='Epoxy',
                     density_g_per_cm3=1.18,
                     elements=[Element('H'),
                               Element('C'),
                               Element(7),
                               Element(8)
                              ],
                     mass_fractions=[1.0414E-06,
                                     1.7164E-02,
                                     1.3560E-03,
                                     2.7852E-03
                                    ])

mat_CuCrZr = Material(material_card_name='CrCuZr',
                     density_g_per_cm3=8.9,
                     elements=[Element(24),
                               Element(4),
                               Element(8),
                               Element(27),
                               Element(14),
                               Element(29),
                              ],
                     mass_fractions=[0.75,
                                     0.11,
                                     0.03,
                                     0.06,
                                     0.011,
                                     99.039,
                                    ])

mat_r_epoxy = Material(material_card_name='r-epoxy',
                     density_g_per_cm3=1.207,
                     elements=[Element(1),
                                Element(6),
                                Element(7),
                                Element(8),
                                Element(12),
                                Element(13),
                                Element(14),
                                Element(16),
                                ],
                     mass_fractions=[3.89340E-03,
                                    3.40560E-03,
                                    3.70800E-04,
                                    4.87080E-03,
                                    1.69197E-04 +2.14200E-05+2.35834E-05,
                                    7.07400E-04,
                                    1.32800E-03+6.72000E-05+4.46000E-03,
                                    8.71457E-05+ 6.97680E-07+3.93822E-06+1.83600E-08,
                                    ]
                     )

mat_DT_plasma = Material(material_card_name='DT-plasma',
                     density_g_per_cm3=1.207,
                     elements=[Element(1,enriched_isotopes=[Isotope('H',2,abundance=0.5),
                                                            Isotope('H',3,abundance=0.5)])
                                ],
                     atom_fractions=[1.0]
                     )



mat_Void = Material(material_card_name='Void',
                     density_g_per_cm3=0,
                     elements=[  ],
                     mass_fractions=[  ]
                    )



comp_water = Compound('H2O',density_g_per_cm3=0.926)

mat_copper = Compound('Cu',density_g_per_cm3=8.96)


divertor_layer_1_m15=mat_Tungsten

divertor_layer_2_m74= Homogenised_mixture(mixtures=[mat_Tungsten,
                                                    comp_water,
                                                    mat_CuCrZr,
                                                    mat_copper
                                                    ],
                                           volume_fractions=[1.0-(0.328+0.184+0.0938),
                                                              0.328,
                                                              0.184,
                                                              0.0938
                                                              ]
                                          )

#print(divertor_layer_2_m74.serpent_material_card())

divertor_layer_3_m15 = divertor_layer_1_m15


divertor_layer_4_m75= Homogenised_mixture(mixtures=[mat_Eurofer,
                                                    comp_water,
                                                    ],
                                           volume_fractions=[0.54,
                                                             0.46
                                                            ]
                                          )


#print(divertor_layer_4_m75.serpent_material_card())



from pint import UnitRegistry
water_temperature = UnitRegistry().Quantity(200, UnitRegistry().degC)
water_temperature_K = water_temperature.to('degK').magnitude
water_pressure = UnitRegistry().Quantity(31, UnitRegistry().bar)
water_presssure_pa = water_pressure.to('pascal').magnitude
mat_water = Compound(chemical_equation='H2O',
                     state_of_matter='liquid',
                     pressure_Pa=water_presssure_pa,
                     temperature_K=water_temperature_K)
VV_Body_m60 = Homogenised_mixture(mixtures=[mat_SS316LN_IG,mat_water],
                                  volume_fractions=[0.60,0.40])
#print(VV_Body_m60.serpent_material_card())

VV_Shell_m50 = mat_SS316LN_IG

ShieldPort_m60 = VV_Body_m60

mat_Nb3Sn = Compound('Nb3Sn',density_g_per_cm3=8.91)
mat_liqHe = Compound('He',density_g_per_cm3=0.125)

TF_Magnet_m25=Homogenised_mixture(mixtures=[mat_r_epoxy,
                                            mat_copper,
                                            mat_Nb3Sn,
                                            mat_liqHe,
                                            mat_SS316LN_IG,
                                            mat_Bronze,
                                            mat_Void],
                                  volume_fractions=[0.18,
                                                    0.1169,
                                                    0.02895,
                                                    0.1682,
                                                    0.4319,
                                                    0.0735,
                                                    0.00055
                                                   ]
                                  )

#print(TF_Magnet_m25.serpent_material_card())

TF_Casing_m50=mat_SS316LN_IG

Central_solenoid_m25=TF_Magnet_m25



mat_He_in_coolant_plates = Compound('He',pressure_Pa=8.0E6,temperature_K=823 ,state_of_matter='liquid')
mat_He_in_end_caps = mat_He_in_coolant_plates
mat_He_in_first_walls = mat_He_in_coolant_plates
mat_He_coolant_back_plate=mat_He_in_coolant_plates

mat_cooling_plates_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_coolant_plates],
                                                    volume_fractions=[0.727,0.273])

print(mat_cooling_plates_homogenised.serpent_material_card())


mat_end_caps_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_end_caps],
                                              volume_fractions=[0.9,0.1])


mat_first_wall_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_first_walls],
                                                    volume_fractions=[0.727,0.273])










# ace_files_needed = []
# for mat in [Central_solenoid_m25,TF_Casing_m50,TF_Magnet_m25,ShieldPort_m60,VV_Body_m60,divertor_layer_4_m75,divertor_layer_2_m74,divertor_layer_1_m15]:
#     if mat.classname == 'Homogenised_mixture':
#         for item in mat.mixtures:
#             for isotope in item.isotopes:
#                 if isotope.nuclear_library_file not in ace_files_needed:
#                     ace_files_needed.append(isotope.nuclear_library_file)

#     else:
#         for isotope in mat.isotopes:
#             if isotope.nuclear_library_file not in ace_files_needed:
#                 ace_files_needed.append(isotope.nuclear_library_file)



#print(Isotope(symbol='U',atomic_number=235,color=(0,128,128),density_g_per_cm3=12).serpent_material_card())
#print(Element(symbol='U',density_g_per_cm3=12,color=(0,128,128)).serpent_material_card()) #color=(0,128,128)


#print((Element(symbol='U',
               # isotopes=[Isotope(symbol='U',
               #                   atomic_number = 238,
               #                   abundance=0.5),
               #           Isotope(symbol='U' ,
               #                   atomic_number = 235,
               #                   abundance=0.4)],
               # density_g_per_cm3=12)
               # ).serpent_material_card())


# print(Isotope('Li',9,density_g_per_cm3=6).serpent_material_card())
# print(Isotope(3,9,density_g_per_cm3=6).serpent_material_card())
# print(Isotope('Li',3,9,density_g_per_cm3=6).serpent_material_card())

#
# comp_Li4SiO4 = Compound(chemical_equation='Li4SiO4',packing_fraction=0.5,volume_of_unit_cell_cm3=1.1543e-21,atoms_per_unit_cell=14)
#
# print(comp_Li4SiO4.molar_mass)
# print(comp_Li4SiO4.serpent_material_card())
#

# for isotope in Tungsten.isotopes:
#     print(isotope.nuclear_library_file)
