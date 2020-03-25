coolants = {
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
            "density_equation": "PropsSI('D', 'T', temperature_in_K, 'P', pressure_in_Pa, 'Water')/1000.",
            "density_unit": "g/cm3",
            # "density_unit": "kg/m3",
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
    }
}