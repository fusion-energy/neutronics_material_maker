material_dict = {
    "He": {
        "elements": {"He": 1.0},
        #"density_equation": 'Chemical("He", T=temperature_in_K, P=pressure_in_Pa).rho',
        "density_equation": "PropsSI('D', 'T', temperature_in_K, 'P', pressure_in_Pa, 'Helium')",
        "density_unit": "kg/m3",
        "reference": "CoolProp python package for density equation",
        "temperature_dependant": True,
        "pressure_dependant": True,
        "percent_type": "ao"
    },
    "DT_plasma": {
        "isotopes": {"H2": 0.5, "H3": 0.5,},
        "density": 0.000001,
        "density_unit": "g/cm3",  # is this a case to support other units?
        "percent_type": "ao"
    },
    "WC": {"elements": "WC",
           "density": 18.0,
           "density_unit": "g/cm3",
           "percent_type": "ao"
          },
    "H2O": {"elements": "H2O",
            # "density_equation": 'Chemical("H2O", T=temperature_in_K, P=pressure_in_Pa).rho',
            "density_equation": "PropsSI('D', 'T', temperature_in_K, 'P', pressure_in_Pa, 'Water')",
            "density_unit": "kg/m3",
            "reference": "CoolProp python package",
            "temperature_dependant": True,
            "pressure_dependant": True,
            "percent_type": "ao"
           },
    "D2O": {
        "isotopes": {"H2": 2.0,
                     "O16": 0.99757+0.00205,
                     "O17": 0.00038,
                    #  "O18": 0.00205, #removed till mixed crosssections.xml files are avaialbe in openmc
                    },
        "density": 1.1,  # could be calculated using presure and temp
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "Nb3Sn": {"elements": "Nb3Sn",
              "density": 8.69,
              "density_unit": "g/cm3",
              "percent_type": "ao"
             },
    "Pb84.2Li15.8": {
        "elements": "Pb84.2Li15.8",
        "density_equation": "99.90*(0.1-16.8e-6*temperature_in_C)",
        "density_unit": "g/cm3",
        "reference": "density equation valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html",
        "temperature_dependant": True,
        "enrichable": True,
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "lithium-lead": {  # check whether this works because doesn't seem to be any elements
        "density_equation": "99.90*(0.1-16.8e-6*temperature_in_C)",
        "density_unit": "g/cm3",
        "reference": "density equation valid for in the range 240-350 C. source http://aries.ucsd.edu/LIB/PROPS/PANOS/lipb.html",
        "temperature_dependant": True,
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li": {
        "elements": "Li",
        "density_equation": "0.515 - 1.01e-4 * (temperature_in_C - 200)",
        "density_unit": "g/cm3",
        "reference": "http://aries.ucsd.edu/LIB/PROPS/PANOS/li.html",
        "temperature_dependant": True,
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "F2Li2BeF2": {
        "elements": "F2Li2BeF2",
        "density_equation": "2.214 - 4.2e-4 * temperature_in_C",
        "density_unit": "g/cm3",
        "reference": "source http://aries.ucsd.edu/LIB/MEETINGS/0103-TRANSMUT/gohar/Gohar-present.pdf",
        "temperature_dependant": True,
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li4SiO4": {
        "elements": "Li4SiO4",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.17162883501e-21,  # could be replaced by a space group
        "density_unit":'g/cm3',
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1188336 https://materialsproject.org/materials/mp-11737/",
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li2SiO3": {
        "elements": "Li2SiO3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.12255616623e-21,
        "density_unit":'g/cm3',
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1208560 https://materialsproject.org/materials/mp-5012/",
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li2ZrO3": {
        "elements": "Li2ZrO3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.12610426777e-21,
        "density_unit":'g/cm3',
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1207897 https://materialsproject.org/materials/mp-4156/",
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li2TiO3": {
        "elements": "Li2TiO3",
        "atoms_per_unit_cell": 4,
        "volume_of_unit_cell_cm3": 0.21849596020e-21,
        "density_unit":'g/cm3',
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1203676 https://materialsproject.org/materials/mp-2931/",
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Li8PbO6": {
        "elements": "Li8PbO6",
        "atoms_per_unit_cell": 1,
        "volume_of_unit_cell_cm3": 0.14400485967e-21,
        "density_unit":'g/cm3',
        "enrichable": True,
        "packable": True,
        "reference": "DOI 10.17188/1198772 https://materialsproject.org/materials/mp-22538/",
        "percent_type": "ao",
        "enrichment_target":"Li6",
        "enrichment_type":'ao'
    },
    "Pb": {
        "elements": "Pb",
        "density": "10.678 - 13.174e-4 * (temperature_in_K-600.6)",
        "density_unit": "g/cm3",
        "reference": "https://www.sciencedirect.com/science/article/abs/pii/0022190261802261",
        "percent_type": "ao",
    },
    "Be": {
        "elements": "Be",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.01587959994e-21,
        "density_unit": "g/cm3",
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1312591 https://materialsproject.org/materials/mp-87/",
        "percent_type": "ao"
    },
    "Be12Ti": {
        "elements": "Be12Ti",
        "atoms_per_unit_cell": 1,
        "volume_of_unit_cell_cm3": 0.11350517285e-21,
        "enrichable": False,
        "density_unit": "g/cm3",
        "packable": True,
        "reference": "DOI 10.17188/1187703 https://materialsproject.org/materials/mp-11280/",
        "percent_type": "ao"
    },
    "Ba5Pb3": {
        "elements": "Ba5Pb3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.74343377212e-21,
        "density_unit": "g/cm3",
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1278091 https://materialsproject.org/materials/mp-622106/",
        "percent_type": "ao"
    },
    "Nd5Pb4": {
        "elements": "Nd5Pb4",
        "atoms_per_unit_cell": 4,
        "volume_of_unit_cell_cm3": 1.17174024048e-21,
        "density_unit": "g/cm3",
        "enrichable": False,
        "packable": True,
        "reference": "https://materialsproject.org/materials/mp-1204902/",
        "percent_type": "ao"
    },
    "Zr5Pb3": {
        "elements": "Zr5Pb3",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.43511266920e-21,
        "density_unit": "g/cm3",
        "enrichable": False,
        "packable": True,
        "reference": "DOI 10.17188/1283750 https://materialsproject.org/materials/mp-681992/",
        "percent_type": "ao"
    },
    "Zr5Pb4": {   # Not updated, no entry in materials project
        "elements": "Zr5Pb4",
        "atoms_per_unit_cell": 2,
        "volume_of_unit_cell_cm3": 0.40435e-21,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SiC": {
        "elements": "SiC",
        "density": 3.,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "eurofer": {
        "elements": {
            "Fe": 0.88821,
            "B": 1e-05,
            "C": 0.00105,
            "N": 0.0004,
            "O": 1e-05,
            "Al": 4e-05,
            "Si": 0.00026,
            "P": 2e-05,
            "S": 3e-05,
            "Ti": 1e-05,
            "V": 0.002,
            "Cr": 0.09,
            "Mn": 0.0055,
            "Co": 5e-05,
            "Ni": 0.0001,
            "Cu": 3e-05,
            "Nb": 5e-05,
            "Mo": 3e-05,
            "Ta": 0.0012,
            "W": 0.011,
        },
        "density": 7.78,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        "percent_type": "ao"
    },
    "SS_316L_N_IG": {
        "elements": {
            "Fe": 62.973,
            "C": 0.030,
            "Mn": 2.00,
            "Si": 0.50,
            "P": 0.03,
            "S": 0.015,
            "Cr": 18.00,
            "Ni": 12.50,
            "Mo": 2.70,
            "N": 0.080,
            "B": 0.002,
            "Cu": 1.0,
            "Co": 0.05,
            "Nb": 0.01,
            "Ti": 0.10,
            "Ta": 0.01,
        },
        "density": 7.93,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        "percent_type": "ao"
    },
    "tungsten": {
        "elements": {
            "W": 0.999595,
            "Ag": 1e-05,
            "Al": 1.5e-05,
            "As": 5e-06,
            "Ba": 5e-06,
            "Ca": 5e-06,
            "Cd": 5e-06,
            "Co": 1e-05,
            "Cr": 2e-05,
            "Cu": 1e-05,
            "Fe": 3e-05,
            "K": 1e-05,
            "Mg": 5e-06,
            "Mn": 5e-06,
            "Na": 1e-05,
            "Nb": 1e-05,
            "Ni": 5e-06,
            "Pb": 5e-06,
            "Ta": 2e-05,
            "Ti": 5e-06,
            "Zn": 5e-06,
            "Zr": 5e-06,
            "Mo": 1e-04,
            "C": 3e-05,
            "H": 5e-06,
            "N": 5e-06,
            "O": 2e-05,
            "P": 2e-05,
            "S": 5e-06,
            "Si": 2e-05,
        },
        "density": 19.0,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        "percent_type": "ao"
    },
    "CuCrZr": {
        "elements": {
            "Cu": 0.9871,
            "Cr": 0.0075,
            "Zr": 0.0011,
            "Co": 0.0005,
            "Ta": 0.0001,
            "Nb": 0.001,
            "B": 1e-05,
            "O": 0.00032,
            "Mg": 0.0004,
            "Al": 3e-05,
            "Si": 0.0004,
            "P": 0.00014,
            "S": 4e-05,
            "Mn": 2e-05,
            "Fe": 0.0002,
            "Ni": 0.0006,
            "Zn": 0.0001,
            "As": 0.0001,
            "Sn": 0.0001,
            "Sb": 0.00011,
            "Pb": 0.0001,
            "Bi": 3e-05,
        },
        "density": 8.9,
        "density_unit": "g/cm3",
        "reference": "Eurofusion neutronics handbook",
        "percent_type": "ao"
    },
    "copper": {
        "elements": {"Cu": 1.0},
        "density": 8.5,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SS347": {
        "elements": {
            "Fe": 67.42,
            "Cr": 18,
            "Ni": 10.5,
            "Nb": 1,
            "Mn": 2,
            "Si": 1,
            "C": 0.08,
        },
        "density": 7.92,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SS321": {
        "elements": {
            "Fe": 67.72,
            "Cr": 18,
            "Ni": 10.5,
            "Ti": 0.7,
            "Mn": 2,
            "Si": 1,
            "C": 0.08,
        },
        "density": 7.92,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SS316": {
        "elements": {
            "Fe": 67, 
            "Cr": 17, 
            "Ni": 14, 
            "Mo": 2
        },
        "density": 7.97,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SS304": {
        "elements": {
            "Fe": 68.82,
            "Cr": 19,
            "Ni": 9.25,
            "Mn": 2,
            "Si": 0.75,
            "N": 0.1,
            "C": 0.08,
        },
        "density": 7.96,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "P91": {
        "elements": {
            "Fe": 89,
            "Cr": 9.1,
            "Mo": 1,
            "Mn": 0.5,
            "Si": 0.4
        },
        "density": 7.96,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SS316L": {
        "elements": {
            "C": 0.001384,
            "Si": 0.019722,
            "P": 0.000805,
            "S": 0.000518,
            "Cr": 0.181098,
            "Mn": 0.020165,
            "Fe": 0.648628,
            "Ni": 0.113247,
            "Mo": 0.014434
        },
        "density": 8.00,
        "density_unit": "g/cm3",
        "percent_type": "wo"
    },
    "ReBCO": {
        "elements": {
            "Y": 1.00,
            "Ba": 2.00,
            "Cu": 3.00,
            "O": 7.00
        },
        "density": 6.3,
        "density_unit": "g/cm3",
        "percent_type": "ao"
    },
    "SST91": {
        "elements": {
            "C": 0.10,
            "Mn": 0.45,
            "P": 0.02,
            "S": 0.01,
            "Si": 0.35,
            "Cr": 8.75,
            "Mo": 0.95,
            "V": 0.215,
            "N": 0.05,
            "Ni": 0.4,
            "Al": 0.04,
            "Nb": 0.08,
            "Fe": 88.585
        },
        "density": 7.77,
        "density_unit": "g/cm3",
        "percent_type": "wo"
    }
}