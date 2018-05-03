
using SimpleScreenRecorder create a webm called input.webm
ffmpeg -i input.webm -vf scale=550:-1:flags=lanczos,fps=2 frames/ffout%03d.gif
convert -loop 0 frames/ffout*.png output.gif


ipython

from neutronics_material_maker.nmm import *

from pprint import pprint

example = Element('Sn',density_g_per_cm3=7.31)

pprint(example.serpent_material_card())
                       
example = Compound('Li4SiO4',
                   volume_of_unit_cell_cm3=1.1543e-21,
                   atoms_per_unit_cell=14,
                   enriched_isotopes=[Isotope('Li',7,abundance=0.4),
                                      Isotope('Li',6,abundance=0.6)])                  

pprint(example.serpent_material_card())                                 

example= Material(material_card_name='Steel',
                  density_g_per_cm3=7.93,
                  elements=[Element('Fe'),Element('C')],
                  mass_fractions=[0.95,0.05])

pprint(example.serpent_material_card())                                      
