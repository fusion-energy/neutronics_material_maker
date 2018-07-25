
from neutronics_material_maker.nmm import *
from pint import UnitRegistry


mat_Li4SiO4 = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li', 7, abundance=0.6),
                                          Isotope('Li', 6, abundance=0.4)])
#print(type(mat_Li4SiO4.material_card()))


mat_Li2SiO3 = Compound('Li2SiO3',
                       volume_of_unit_cell_cm3=0.23632e-21,
                       atoms_per_unit_cell=4,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li', 7, abundance=0.6),
                                          Isotope('Li',6,abundance=0.4)])
#print(mat_Li2SiO3.material_card())

mat_Li2ZrO3 = Compound('Li2ZrO3',
                       volume_of_unit_cell_cm3=0.24479e-21,
                       atoms_per_unit_cell=4,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li', 7, abundance=0.6),
                                          Isotope('Li', 6, abundance=0.4)])
#print(mat_Li2ZrO3.material_card())


mat_Li2TiO3 = Compound('Li2TiO3',
                       volume_of_unit_cell_cm3=0.42701e-21,
                       atoms_per_unit_cell=8,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Li2TiO3.material_card())


mat_Be = Compound('Be',
                  volume_of_unit_cell_cm3=0.01622e-21,
                  atoms_per_unit_cell=2,
                  packing_fraction=0.6)
#print(mat_Be.material_card())


mat_Be12Ti = Compound('Be12Ti',
                      volume_of_unit_cell_cm3= 0.22724e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Be12Ti.material_card())


mat_Ba5Pb3 = Compound('Ba5Pb3',
                      volume_of_unit_cell_cm3=1.37583e-21,
                      atoms_per_unit_cell=4,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Ba5Pb3.material_card())


mat_Nd5Pb4 = Compound('Nd5Pb4',
                      volume_of_unit_cell_cm3= 1.06090e-21,
                      atoms_per_unit_cell=4,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Nd5Pb4.material_card())


mat_Zr5Pb3 = Compound('Zr5Pb3',
                      volume_of_unit_cell_cm3=0.36925e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Zr5Pb3.material_card())


mat_Zr5Pb4 = Compound('Zr5Pb4',
                      volume_of_unit_cell_cm3=0.40435e-21,
                      atoms_per_unit_cell=2,
                      packing_fraction=0.6,
                      enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])
#print(mat_Zr5Pb4.material_card())


mat_Lithium_Lead = Compound('Pb84.2Li15.8',
                            color=((1.0/256)*0,(1.0/256)*111,(1.0/256)*69),#ukaea green
                            density_atoms_per_barn_per_cm=3.2720171E-2,
                            enriched_isotopes=[Isotope('Li',7,abundance=0.247317371169),
                                               Isotope('Li',6,abundance=0.752682628831)])
#print(mat_Lithium_Lead.material_card())


mat_Tungsten = Material(material_card_name='Tungsten',
                        density_g_per_cm3=19.0,
                        color=((1.0/256)*248,(1.0/256)*151,(1.0/256)*29), #ccfe orange
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
                        element_mass_fractions=[1e6-405,
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
#print(mat_Tungsten.material_card())

mat_Eurofer = Material(material_card_name='Eurofer',
                    density_g_per_cm3=7.87,
                    color=(134,134,134),
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

#print(mat_Eurofer.material_card())

mat_SS316LN_IG = Material(material_card_name='SS316LN-IG',
                    density_g_per_cm3=7.93,
                    color=(150,150,150),
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

#print(mat_SS316LN_IG.material_card())

mat_Bronze = Material(material_card_name='Bronze',
                      density_g_per_cm3=8.8775,
                      color=(0,204,102),
                      elements=[Element('Cu'),
                                Element('Sn')],
                      element_atom_fractions=[0.95,
                                              0.05]
                      )

#print(mat_Bronze.material_card())

mat_Glass_fibre = Material(material_card_name='Glass-fibre',
                    density_g_per_cm3=2.49,
                    elements=[Element('H'),
                              Element('O'),
                              Element(12),
                              Element(13),
                              Element(14)
                             ],
                    element_mass_fractions=[0.0000383948,
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
                     element_mass_fractions=[1.0414E-06,
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
                     element_mass_fractions=[0.75,
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
                     element_mass_fractions=[3.89340E-03,
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
                     density_atoms_per_barn_per_cm=1e-20,
                     color=(239, 0, 255),
                     elements=[Element(1,enriched_isotopes=[Isotope('H',2,abundance=0.5),
                                                            Isotope('H',3,abundance=0.5)])
                                ],
                     element_atom_fractions=[1.0]
                     )

mat_plasma_void = Material(material_card_name='plasma-void',
                    color=(239, 0, 255),
                    density_g_per_cm3=0,
                    elements=[  ],
                    element_mass_fractions=[  ]
                    )

mat_Void = Material(material_card_name='void',
                    density_g_per_cm3=0,
                    elements=[  ],
                    element_mass_fractions=[  ]
                    )

water_temperature = UnitRegistry().Quantity(200, UnitRegistry().degC)

water_temperature_K = water_temperature.to('degK').magnitude

water_pressure = UnitRegistry().Quantity(31, UnitRegistry().bar)

water_presssure_pa = water_pressure.to('pascal').magnitude

mat_water_by_pres_temp = Compound(chemical_equation='H2O',
                                  state_of_matter='non_solid',
                                  pressure_Pa=water_presssure_pa,
                                  temperature_K=water_temperature_K)


mat_water_by_density = Compound('H2O',density_g_per_cm3=mat_water_by_pres_temp.density_g_per_cm3)

mat_copper = Compound('Cu',density_g_per_cm3=8.96)

mat_divertor_layer_1_m15=mat_Tungsten

mat_divertor_layer_2_m74= Homogenised_mixture(mixtures=[mat_Tungsten,
                                                    mat_water_by_density,
                                                    mat_CuCrZr,
                                                    mat_copper
                                                    ],
                                              squashed=True,
                                           volume_fractions=[1.0-(0.328+0.184+0.0938),
                                                              0.328,
                                                              0.184,
                                                              0.0938
                                                              ]
                                          )

#print(divertor_layer_2_m74.material_card())

mat_divertor_layer_3_m15 = mat_divertor_layer_1_m15

mat_divertor_layer_4_m75= Homogenised_mixture(mixtures=[mat_Eurofer,
                                                        mat_water_by_density],
                                              volume_fractions=[0.54,
                                                                0.46]
                                              )

#print(divertor_layer_4_m75.material_card())





mat_VV_Body_m60 = Homogenised_mixture(mixtures=[mat_SS316LN_IG, mat_water_by_pres_temp],
                                      volume_fractions=[0.60, 0.40])
#print(VV_Body_m60.material_card())

mat_VV_Shell_m50 = mat_SS316LN_IG

mat_ShieldPort_m60 = mat_VV_Body_m60

mat_Nb3Sn = Compound('Nb3Sn',density_g_per_cm3=8.91)
mat_liqHe = Compound('He',density_g_per_cm3=0.125)

mat_TF_Magnet_m25=Homogenised_mixture(material_card_name='mat_tf_magnet_m25',
                                      mixtures=[mat_r_epoxy,
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

#print(TF_Magnet_m25.material_card())

mat_TF_Casing_m50 = mat_SS316LN_IG

mat_central_solenoid_m25 = mat_TF_Magnet_m25

mat_He_in_coolant_plates_with_pressure_and_temperature = Compound('He',
                                    pressure_Pa=8.0E6,
                                    temperature_K=823 ,
                                    color=((1.0/256)*0,(1.0/256)*128,(1.0/256)*202), #ukaea light blue
                                    state_of_matter='idea_gas')

#this uses the density of the previous one so that there is no tmp card on the serpent output
mat_He_in_coolant_plates = Compound('He',
                                    density_g_per_cm3=mat_He_in_coolant_plates_with_pressure_and_temperature.density_g_per_cm3,
                                    color=((1.0/256)*0,(1.0/256)*128,(1.0/256)*202), #ukaea light blue
                                    state_of_matter='solid')


mat_He_in_end_caps = mat_He_in_coolant_plates

mat_He_in_first_walls = mat_He_in_coolant_plates

mat_He_coolant_back_plate=mat_He_in_coolant_plates


mat_mixed_pebble_bed = Homogenised_mixture(mixtures=[mat_Be12Ti,mat_Li2TiO3],
                                            volume_fractions=[0.5,0.5])


mat_cooling_plates_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_coolant_plates],
                                                    volume_fractions=[0.727,0.273])


mat_end_caps_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_end_caps],
                                              volume_fractions=[0.9,0.1])


mat_first_wall_homogenised =Homogenised_mixture(mixtures=[mat_Eurofer,mat_He_in_first_walls],
                                                    volume_fractions=[0.727,0.273])

all_examples = [mat_Li4SiO4,mat_Li2SiO3,mat_Li2ZrO3,mat_Li2TiO3,mat_Be,mat_Be12Ti,mat_Ba5Pb3,
                mat_Nd5Pb4,mat_Zr5Pb3,mat_Zr5Pb4,mat_Lithium_Lead,mat_Tungsten,mat_Eurofer,
                mat_SS316LN_IG,mat_Bronze,mat_Glass_fibre,mat_Epoxy,mat_CuCrZr,mat_r_epoxy,
                mat_DT_plasma,mat_Void,mat_water_by_density,mat_copper,mat_divertor_layer_1_m15,
                mat_divertor_layer_2_m74,mat_divertor_layer_3_m15,mat_divertor_layer_4_m75,
                mat_water_by_pres_temp,mat_VV_Body_m60,mat_Nb3Sn,mat_liqHe,mat_TF_Magnet_m25,
                mat_TF_Casing_m50,mat_He_in_coolant_plates,mat_mixed_pebble_bed,mat_cooling_plates_homogenised,
                mat_end_caps_homogenised,mat_end_caps_homogenised,mat_first_wall_homogenised]


print('example materials imported')
