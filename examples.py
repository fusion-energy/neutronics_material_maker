import neutronics_material_maker as nmm
import sys

divertor_layer_1_m15 = nmm.Compound('W',density_g_per_cm3=19.2500)
print(divertor_layer_1_m15.serpent_material_card)


mat_tungsten = nmm.Compound('W',density_g_per_cm3=19.2500)
mat_Water = nmm.Compound('H2O',density_g_per_cm3=0.926)
print(mat_Water.serpent_material_card)
mat_CuCrZr = nmm.Material('CuCrZr_with_impurities')
print(mat_CuCrZr.serpent_material_card)
mat_copper = nmm.Compound('Cu',density_g_per_cm3=8.95)
print(mat_copper.serpent_material_card)

divertor_layer_2_m74 =nmm.Homogenised_mixture([(mat_tungsten,1-(0.328+0.184+0.0928)),
                         (mat_Water,0.328),
                         (mat_CuCrZr,0.184),
                         (mat_copper,0.0928)])

print(divertor_layer_2_m74.serpent_material_card)
# c      W
# c
# c      at. den.= 6.30413E-02  mat. den.= 1.92500E+01
# c
# m15    74180.32c   8.37225E-05  $  W  100.0 %
#        74182.32c   1.67516E-02  $
#        74183.32c   9.05850E-03  $
#        74184.32c   1.93227E-02  $
#        74186.32c   1.78248E-02  $

