import neutronics_material_maker as nmm
import sys
#from pyne.material import Material





a=nmm.Compound('Pb84.2Li15.8')  
print(a.density_g_per_cm3)  

a=nmm.Compound('Li4SiO4')  
print(a.density_g_per_cm3)                           

# divertor_layer_1_m15 = nmm.Compound('W',density_g_per_cm3=19.2500)
# print(divertor_layer_1_m15.serpent_material_card)
#


# mat_Tungsten = nmm.Material('Tungsten')
# print(mat_Tungsten.serpent_material_card)
# input()
# #
# mat_Epoxy = nmm.Material('r-epoxy')
# mat_copper = nmm.Compound('Cu',density_g_per_cm3=8.96)
# mat_Nb3Sn = nmm.Compound('Nb3Sn',density_g_per_cm3=8.91) #'Nb0.746Sn0.254' density assumes perfect latice
# mat_liqHe = nmm.Compound('He',density_g_per_cm3=0.125)
# mat_ss316 = nmm.Material('SS-316LN-IG')
# mat_bronze = nmm.Material('Bronze')
# mat_void = nmm.Material('Void')

# m25 =nmm.Homogenised_mixture([{'mix':mat_Epoxy, 'volume_fraction':0.18},
#                               {'mix':mat_copper,'volume_fraction':0.1169},
#                               {'mix':mat_Nb3Sn, 'volume_fraction':0.02895},
#                               {'mix':mat_liqHe, 'volume_fraction':0.1682},
#                               {'mix':mat_ss316, 'volume_fraction':0.4319},
#                               {'mix':mat_bronze,'volume_fraction':0.0735},
#                               {'mix':mat_void , 'volume_fraction':0.00055}])

# print(m25.serpent_material_card)




# mat_ss316 = nmm.Material('SS-316LN-IG')
# mat_water = nmm.Compound('H2O',density_g_per_cm3=0.926)
#
#
# m60 =nmm.Homogenised_mixture([{'mix':mat_ss316, 'volume_fraction':0.6},
#                               {'mix': mat_water, 'volume_fraction': 0.4}])
#
# print(m60.serpent_material_card)
#

#
# m5 = nmm.Material('newmat',density_g_per_cm3=7.8,elements_and_fractions=[{'element':nmm.Element('Fe'),'mass_fraction':0.88821},{'element':nmm.Element('B') ,'mass_fraction':0.00001}])
#
#m5 = nmm.Material('Eurofer')
#print(m5.serpent_material_card)


# def return_material_m60():
#     from pint import UnitRegistry
#     water_temperature = UnitRegistry().Quantity(200, UnitRegistry().degC)
#     water_temperature_K = water_temperature.to('degK').magnitude
#     water_pressure = UnitRegistry().Quantity(31, UnitRegistry().bar)
#     water_presssure_pa = water_pressure.to('pascal').magnitude
#     print('water_presssure_pa',water_presssure_pa)
#     print('water_temperature_K',water_temperature_K)
#     mat_water = nmm.Compound('H2O',state_of_matter='liquid',pressure_Pa=water_presssure_pa,temperature_K=water_temperature_K)
#     print(mat_water.density_g_per_cm3)
#     input()
#     mat_ss316 = nmm.Material('SS-316LN-IG')
#     m60 =nmm.Homogenised_mixture([{'mix':mat_ss316, 'volume_fraction':0.60},
#                                   {'mix':mat_water, 'volume_fraction': 0.40}])

#     #print(m60.serpent_material_card)

# return_material_m60()




# mat_Eurofer = nmm.Material('Eurofer')
# mat_water = nmm.Compound('H2O',density_g_per_cm3=0.926)
# m75 =nmm.Homogenised_mixture([{'mix':mat_Eurofer, 'volume_fraction':0.54},
#                               {'mix': mat_water, 'volume_fraction': 0.46}])
#
# print(m75.serpent_material_card)


#
# mat_Tungsten = nmm.Material('Tungsten')
# comp_water = nmm.Compound('H2O',density_g_per_cm3=0.926)
# mat_CuCrZr = nmm.Material('CuCrZr')
# mat_copper = nmm.Compound('Cu',density_g_per_cm3=8.96)
# #mat_copper = nmm.Material('Copper')
# m74 =nmm.Homogenised_mixture([{'mix':mat_Tungsten, 'volume_fraction':1.0-(0.328+0.184+0.0938)},
#                               {'mix':comp_water, 'volume_fraction':0.328},
#                               {'mix': mat_CuCrZr, 'volume_fraction': 0.184},
#                               {'mix': mat_copper, 'volume_fraction': 0.0938}])
#
# print(m74.serpent_material_card)