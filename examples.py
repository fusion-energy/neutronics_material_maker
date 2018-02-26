import neutronics_material_maker as nmm
import sys
#from pyne.material import Material

# divertor_layer_1_m15 = nmm.Compound('W',density_g_per_cm3=19.2500)
# print(divertor_layer_1_m15.serpent_material_card)
#


#./
# mat_tungsten = nmm.Compound('W',density_g_per_cm3=19.2500)
# mat_Water = nmm.Compound('H2O',density_g_per_cm3=0.926)
# #print(mat_Water.serpent_material_card)
# mat_CuCrZr = nmm.Material('CuCrZr_with_impurities')
# #print(mat_CuCrZr.serpent_material_card)
# mat_copper = nmm.Compound('Cu',density_g_per_cm3=8.95)
# #print(mat_copper.serpent_material_card)
#
#
# divertor_layer_2_m74 =nmm.Homogenised_mixture([{'mix':mat_tungsten, 'volume_fraction':1-(0.328+0.184+0.0938)},
#                                                {'mix':mat_Water,    'volume_fraction':0.328},
#                                                {'mix':mat_CuCrZr,   'volume_fraction':0.184},
#                                                {'mix':mat_copper,   'volume_fraction':0.0938}])
# print(divertor_layer_2_m74.serpent_material_card)


# mat_Epoxy = nmm.Material('r-epoxy')
# mat_copper = nmm.Compound('Cu',density_g_per_cm3=8.96)
# mat_Nb3Sn = nmm.Compound('Nb3Sn',density_g_per_cm3=8.91) #'Nb0.746Sn0.254' density assumes perfect latice
# mat_liqHe = nmm.Compound('He',density_g_per_cm3=0.125)
# mat_ss316 = nmm.Material('SS-316LN-IG')
# mat_bronze = nmm.Material('Bronze')
#
#
# m25 =nmm.Homogenised_mixture([{'mix':mat_Epoxy, 'volume_fraction':0.18},
#                               {'mix':mat_copper,'volume_fraction':0.1169},
#                               {'mix': mat_Nb3Sn, 'volume_fraction': 0.02895},
#                               {'mix':mat_liqHe, 'volume_fraction':0.1682},
#                               {'mix':mat_ss316, 'volume_fraction':0.4319+0.00055},
#                               {'mix': mat_bronze, 'volume_fraction': 0.0735}])
#
# print(m25.serpent_material_card)




mat_ss316 = nmm.Material('SS-316LN-IG')
mat_water = nmm.Compound('H2O',density_g_per_cm3=0.926)


m60 =nmm.Homogenised_mixture([{'mix':mat_ss316, 'volume_fraction':0.6},
                              {'mix': mat_water, 'volume_fraction': 0.4}])

print(m60.serpent_material_card)

m75 =nmm.Homogenised_mixture([{'mix':mat_ss316, 'volume_fraction':0.46},
                              {'mix': mat_water, 'volume_fraction': 0.54}])

print(m75.serpent_material_card)