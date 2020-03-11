
import openmc 

from neutronics_material_maker import Material 

test_material = Material(material_name='Li4SiO4', enrichment=50, enrichment_target='Li6', enrichment_type='ao').neutronics_material

print(test_material)