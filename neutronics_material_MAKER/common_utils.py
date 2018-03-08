import sys



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def full_name(symbol):  # returns full element name
        if (symbol == 'Ac'): return 'Actinium'
        if (symbol == 'Al'): return 'Aluminum'
        if (symbol == 'Am'): return 'Americium'
        if (symbol == 'Sb'): return 'Antimony'
        if (symbol == 'Ar'): return 'Argon'
        if (symbol == 'As'): return 'Arsenic'
        if (symbol == 'At'): return 'Astatine'
        if (symbol == 'Ba'): return 'Barium'
        if (symbol == 'Bk'): return 'Berkelium'
        if (symbol == 'Be'): return 'Beryllium'
        if (symbol == 'Bi'): return 'Bismuth'
        if (symbol == 'Bh'): return 'Bohrium'
        if (symbol == 'B'):  return 'Boron'
        if (symbol == 'Br'): return 'Bromine'
        if (symbol == 'Cd'): return 'Cadmium'
        if (symbol == 'Ca'): return 'Calcium'
        if (symbol == 'Cf'): return 'Californium'
        if (symbol == 'C'):  return 'Carbon'
        if (symbol == 'Ce'): return 'Cerium'
        if (symbol == 'Cs'): return 'Cesium'
        if (symbol == 'Cl'): return 'Chlorine'
        if (symbol == 'Cr'): return 'Chromium'
        if (symbol == 'Co'): return 'Cobalt'
        if (symbol == 'Cu'): return 'Copper'
        if (symbol == 'Cn'): return 'Copernicium'
        if (symbol == 'Cm'): return 'Curium'
        if (symbol == 'Ds'): return 'Darmstadtium'
        if (symbol == 'Db'): return 'Dubnium'
        if (symbol == 'Dy'): return 'Dysprosium'
        if (symbol == 'Es'): return 'Einsteinium'
        if (symbol == 'Er'): return 'Erbium'
        if (symbol == 'Eu'): return 'Europium'
        if (symbol == 'Fm'): return 'Fermium'
        if (symbol == 'F'):  return 'Fluorine'
        if (symbol == 'Fl'): return 'Flerovium'
        if (symbol == 'Fr'): return 'Francium'
        if (symbol == 'Gd'): return 'Gadolinium'
        if (symbol == 'Ga'): return 'Gallium'
        if (symbol == 'Ge'): return 'Germanium'
        if (symbol == 'Au'): return 'Gold'
        if (symbol == 'Hf'): return 'Hafnium'
        if (symbol == 'Hs'): return 'Hassium'
        if (symbol == 'He'): return 'Helium'
        if (symbol == 'Ho'): return 'Holmium'
        if (symbol == 'H'):  return 'Hydrogen'
        if (symbol == 'In'): return 'Indium'
        if (symbol == 'I'):  return 'Iodine'
        if (symbol == 'Ir'): return 'Iridium'
        if (symbol == 'Fe'): return 'Iron'
        if (symbol == 'Kr'): return 'Krypton'
        if (symbol == 'La'): return 'Lanthanum'
        if (symbol == 'Lr'): return 'Lawrencium'
        if (symbol == 'Pb'): return 'Lead'
        if (symbol == 'Li'): return 'Lithium'
        if (symbol == 'Lu'): return 'Lutetium'
        if (symbol == 'Mg'): return 'Magnesium'
        if (symbol == 'Mn'): return 'Manganese'
        if (symbol == 'Mt'): return 'Meitnerium'
        if (symbol == 'Md'): return 'Mendelevium'
        if (symbol == 'Mc'): return 'Moscovium'
        if (symbol == 'Hg'): return 'Mercury'
        if (symbol == 'Mo'): return 'Molybdenum'
        if (symbol == 'Nd'): return 'Neodymium'
        if (symbol == 'Ne'): return 'Neon'
        if (symbol == 'Np'): return 'Neptunium'
        if (symbol == 'Ni'): return 'Nickel'
        if (symbol == 'Nb'): return 'Niobium'
        if (symbol == 'N'):  return 'Nitrogen'
        if (symbol == 'No'): return 'Nobelium'
        if (symbol == 'Os'): return 'Osmium'
        if (symbol == 'O'):  return 'Oxygen'
        if (symbol == 'Pd'): return 'Palladium'
        if (symbol == 'P'): return 'Phosphorus'
        if (symbol == 'Pt'): return 'Platinum'
        if (symbol == 'Pu'): return 'Plutonium'
        if (symbol == 'Po'): return 'Polonium'
        if (symbol == 'K'): return 'Potassium'
        if (symbol == 'Pr'): return 'Praseodymium'
        if (symbol == 'Pm'): return 'Promethium'
        if (symbol == 'Pa'): return 'Protactinium'
        if (symbol == 'Ra'): return 'Radium'
        if (symbol == 'Rb'): return 'Rubidium'
        if (symbol == 'Rn'): return 'Radon'
        if (symbol == 'Re'): return 'Rhenium'
        if (symbol == 'Rh'): return 'Rhodium'
        if (symbol == 'Rg'): return 'Roentgenium'
        if (symbol == 'Ru'): return 'Ruthenium'
        if (symbol == 'Rf'): return 'Rutherfordium'
        if (symbol == 'Sm'): return 'Samarium'
        if (symbol == 'Sc'): return 'Scandium'
        if (symbol == 'Sg'): return 'Seaborgium'
        if (symbol == 'Se'): return 'Selenium'
        if (symbol == 'Si'): return 'Silicon'
        if (symbol == 'Ag'): return 'Silver'
        if (symbol == 'Na'): return 'Sodium'
        if (symbol == 'Sr'): return 'Strontium'
        if (symbol == 'S'): return 'Sulfur'
        if (symbol == 'Ta'): return 'Tantalum'
        if (symbol == 'Tc'): return 'Technetium'
        if (symbol == 'Te'): return 'Tellurium'
        if (symbol == 'Tb'): return 'Terbium'
        if (symbol == 'Tl'): return 'Thallium'
        if (symbol == 'Th'): return 'Thorium'
        if (symbol == 'Tm'): return 'Thulium'
        if (symbol == 'Sn'): return 'Tin'
        if (symbol == 'Ti'): return 'Titanium'
        if (symbol == 'W'): return 'Tungsten'
        if (symbol == 'U'): return 'Uranium'
        if (symbol == 'V'): return 'Vanadium'
        if (symbol == 'Xe'): return 'Xenon'
        if (symbol == 'Yb'): return 'Ytterbium'
        if (symbol == 'Y'): return 'Yttrium'
        if (symbol == 'Zn'): return 'Zinc'
        if (symbol == 'Zr'): return 'Zirconium'
        print('element symbol not found', symbol)
        sys.exit()
        
def natural_abundance(symbol,atomic_number):
        if symbol == 'H' and atomic_number == 1: return 0.999885
        if symbol == 'H' and atomic_number == 2: return 0.000115
        if symbol == 'He' and atomic_number == 3: return 0.00000134
        if symbol == 'He' and atomic_number == 4: return 0.99999866
        if symbol == 'Li' and atomic_number == 6: return 0.0759
        if symbol == 'Li' and atomic_number == 7: return 0.9241
        if symbol == 'Be' and atomic_number == 9: return 1
        if symbol == 'B' and atomic_number == 10: return 0.199
        if symbol == 'B' and atomic_number == 11: return 0.801
        if symbol == 'C' and atomic_number == 12: return 0.9893
        if symbol == 'C' and atomic_number == 13: return 0.0107
        if symbol == 'C' and atomic_number == 14: return 0
        if symbol == 'N' and atomic_number == 14: return 0.99636
        if symbol == 'N' and atomic_number == 15: return 0.00364
        if symbol == 'O' and atomic_number == 16: return 0.99757
        if symbol == 'O' and atomic_number == 17: return 0.00038
        if symbol == 'O' and atomic_number == 18: return 0.00205
        if symbol == 'F' and atomic_number == 19: return 1
        if symbol == 'Ne' and atomic_number == 20: return 0.9048
        if symbol == 'Ne' and atomic_number == 21: return 0.0027
        if symbol == 'Ne' and atomic_number == 22: return 0.0925
        if symbol == 'Na' and atomic_number == 23: return 1
        if symbol == 'Mg' and atomic_number == 24: return 0.7899
        if symbol == 'Mg' and atomic_number == 25: return 0.1
        if symbol == 'Mg' and atomic_number == 26: return 0.1101
        if symbol == 'Al' and atomic_number == 27: return 1
        if symbol == 'Si' and atomic_number == 28: return 0.92223
        if symbol == 'Si' and atomic_number == 29: return 0.04685
        if symbol == 'Si' and atomic_number == 30: return 0.03092
        if symbol == 'P' and atomic_number == 31: return 1
        if symbol == 'S' and atomic_number == 32: return 0.9499
        if symbol == 'S' and atomic_number == 33: return 0.0075
        if symbol == 'S' and atomic_number == 34: return 0.0425
        if symbol == 'S' and atomic_number == 36: return 0.0001
        if symbol == 'Cl' and atomic_number == 35: return 0.7576
        if symbol == 'Cl' and atomic_number == 37: return 0.2424
        if symbol == 'Ar' and atomic_number == 36: return 0.003336
        if symbol == 'Ar' and atomic_number == 38: return 0.000629
        if symbol == 'Ar' and atomic_number == 40: return 0.996035
        if symbol == 'K' and atomic_number == 39: return 0.932581
        if symbol == 'K' and atomic_number == 40: return 0.000117
        if symbol == 'K' and atomic_number == 41: return 0.067302
        if symbol == 'Ca' and atomic_number == 40: return 0.96941
        if symbol == 'Ca' and atomic_number == 42: return 0.00647
        if symbol == 'Ca' and atomic_number == 43: return 0.00135
        if symbol == 'Ca' and atomic_number == 44: return 0.02086
        if symbol == 'Ca' and atomic_number == 46: return 0.00004
        if symbol == 'Ca' and atomic_number == 48: return 0.00187
        if symbol == 'Sc' and atomic_number == 45: return 1
        if symbol == 'Ti' and atomic_number == 46: return 0.0825
        if symbol == 'Ti' and atomic_number == 47: return 0.0744
        if symbol == 'Ti' and atomic_number == 48: return 0.7372
        if symbol == 'Ti' and atomic_number == 49: return 0.0541
        if symbol == 'Ti' and atomic_number == 50: return 0.0518
        if symbol == 'V' and atomic_number == 50: return 0.0025
        if symbol == 'V' and atomic_number == 51: return 0.9975
        if symbol == 'Cr' and atomic_number == 50: return 0.04345
        if symbol == 'Cr' and atomic_number == 52: return 0.83789
        if symbol == 'Cr' and atomic_number == 53: return 0.09501
        if symbol == 'Cr' and atomic_number == 54: return 0.02365
        if symbol == 'Mn' and atomic_number == 55: return 1.0
        if symbol == 'Fe' and atomic_number == 54: return 0.05845
        if symbol == 'Fe' and atomic_number == 56: return 0.91754
        if symbol == 'Fe' and atomic_number == 57: return 0.02119
        if symbol == 'Fe' and atomic_number == 58: return 0.00282
        if symbol == 'Co' and atomic_number == 59: return 1.0
        if symbol == 'Ni' and atomic_number == 58: return 0.68077
        if symbol == 'Ni' and atomic_number == 60: return 0.26223
        if symbol == 'Ni' and atomic_number == 61: return 0.011399
        if symbol == 'Ni' and atomic_number == 62: return 0.036346
        if symbol == 'Ni' and atomic_number == 64: return 0.009255
        if symbol == 'Cu' and atomic_number == 63: return 0.6915
        if symbol == 'Cu' and atomic_number == 65: return 0.3085
        if symbol == 'Zn' and atomic_number == 64: return 0.4917
        if symbol == 'Zn' and atomic_number == 66: return 0.2773
        if symbol == 'Zn' and atomic_number == 67: return 0.0404
        if symbol == 'Zn' and atomic_number == 68: return 0.1845
        if symbol == 'Zn' and atomic_number == 70: return 0.0061
        if symbol == 'Ga' and atomic_number == 69: return 0.60108
        if symbol == 'Ga' and atomic_number == 71: return 0.39892
        if symbol == 'Ge' and atomic_number == 70: return 0.2057
        if symbol == 'Ge' and atomic_number == 72: return 0.2745
        if symbol == 'Ge' and atomic_number == 73: return 0.0775
        if symbol == 'Ge' and atomic_number == 74: return 0.365
        if symbol == 'Ge' and atomic_number == 76: return 0.0773
        if symbol == 'As' and atomic_number == 75: return 1
        if symbol == 'Se' and atomic_number == 74: return 0.0089
        if symbol == 'Se' and atomic_number == 76: return 0.0937
        if symbol == 'Se' and atomic_number == 77: return 0.0763
        if symbol == 'Se' and atomic_number == 78: return 0.2377
        if symbol == 'Se' and atomic_number == 80: return 0.4961
        if symbol == 'Se' and atomic_number == 82: return 0.0873
        if symbol == 'Br' and atomic_number == 79: return 0.5069
        if symbol == 'Br' and atomic_number == 81: return 0.4931
        if symbol == 'Kr' and atomic_number == 78: return 0.00355
        if symbol == 'Kr' and atomic_number == 80: return 0.02286
        if symbol == 'Kr' and atomic_number == 82: return 0.11593
        if symbol == 'Kr' and atomic_number == 83: return 0.115
        if symbol == 'Kr' and atomic_number == 84: return 0.56987
        if symbol == 'Kr' and atomic_number == 86: return 0.17279
        if symbol == 'Rb' and atomic_number == 85: return 0.7217
        if symbol == 'Rb' and atomic_number == 87: return 0.2783
        if symbol == 'Sr' and atomic_number == 84: return 0.0056
        if symbol == 'Sr' and atomic_number == 86: return 0.0986
        if symbol == 'Sr' and atomic_number == 87: return 0.07
        if symbol == 'Sr' and atomic_number == 88: return 0.8258
        if symbol == 'Y' and atomic_number == 89: return 1
        if symbol == 'Zr' and atomic_number == 90: return 0.5145
        if symbol == 'Zr' and atomic_number == 91: return 0.1122
        if symbol == 'Zr' and atomic_number == 92: return 0.1715
        if symbol == 'Zr' and atomic_number == 94: return 0.1738
        if symbol == 'Zr' and atomic_number == 96: return 0.028
        if symbol == 'Nb' and atomic_number == 93: return 1
        if symbol == 'Mo' and atomic_number == 92: return 0.1453
        if symbol == 'Mo' and atomic_number == 94: return 0.0915
        if symbol == 'Mo' and atomic_number == 95: return 0.1584
        if symbol == 'Mo' and atomic_number == 96: return 0.1667
        if symbol == 'Mo' and atomic_number == 97: return 0.096
        if symbol == 'Mo' and atomic_number == 98: return 0.2439
        if symbol == 'Mo' and atomic_number == 100: return 0.0982
        if symbol == 'Ru' and atomic_number == 96: return 0.0554
        if symbol == 'Ru' and atomic_number == 98: return 0.0187
        if symbol == 'Ru' and atomic_number == 99: return 0.1276
        if symbol == 'Ru' and atomic_number == 100: return 0.126
        if symbol == 'Ru' and atomic_number == 101: return 0.1706
        if symbol == 'Ru' and atomic_number == 102: return 0.3155
        if symbol == 'Ru' and atomic_number == 104: return 0.1862
        if symbol == 'Rh' and atomic_number == 103: return 1
        if symbol == 'Pd' and atomic_number == 102: return 0.0102
        if symbol == 'Pd' and atomic_number == 104: return 0.1114
        if symbol == 'Pd' and atomic_number == 105: return 0.2233
        if symbol == 'Pd' and atomic_number == 106: return 0.2733
        if symbol == 'Pd' and atomic_number == 108: return 0.2646
        if symbol == 'Pd' and atomic_number == 110: return 0.1172
        if symbol == 'Ag' and atomic_number == 107: return 0.51839
        if symbol == 'Ag' and atomic_number == 109: return 0.48161
        if symbol == 'Cd' and atomic_number == 106: return 0.0125
        if symbol == 'Cd' and atomic_number == 108: return 0.0089
        if symbol == 'Cd' and atomic_number == 110: return 0.1249
        if symbol == 'Cd' and atomic_number == 111: return 0.128
        if symbol == 'Cd' and atomic_number == 112: return 0.2413
        if symbol == 'Cd' and atomic_number == 113: return 0.1222
        if symbol == 'Cd' and atomic_number == 114: return 0.2873
        if symbol == 'Cd' and atomic_number == 116: return 0.0749
        if symbol == 'In' and atomic_number == 113: return 0.0429
        if symbol == 'In' and atomic_number == 115: return 0.9571
        if symbol == 'Sn' and atomic_number == 112: return 0.0097
        if symbol == 'Sn' and atomic_number == 114: return 0.0066
        if symbol == 'Sn' and atomic_number == 115: return 0.0034
        if symbol == 'Sn' and atomic_number == 116: return 0.1454
        if symbol == 'Sn' and atomic_number == 117: return 0.0768
        if symbol == 'Sn' and atomic_number == 118: return 0.2422
        if symbol == 'Sn' and atomic_number == 119: return 0.0859
        if symbol == 'Sn' and atomic_number == 120: return 0.3258
        if symbol == 'Sn' and atomic_number == 122: return 0.0463
        if symbol == 'Sn' and atomic_number == 124: return 0.0579
        if symbol == 'Sb' and atomic_number == 121: return 0.5721
        if symbol == 'Sb' and atomic_number == 123: return 0.4279
        if symbol == 'Te' and atomic_number == 120: return 0.0009
        if symbol == 'Te' and atomic_number == 122: return 0.0255
        if symbol == 'Te' and atomic_number == 123: return 0.0089
        if symbol == 'Te' and atomic_number == 124: return 0.0474
        if symbol == 'Te' and atomic_number == 125: return 0.0707
        if symbol == 'Te' and atomic_number == 126: return 0.1884
        if symbol == 'Te' and atomic_number == 128: return 0.3174
        if symbol == 'Te' and atomic_number == 130: return 0.3408
        if symbol == 'I' and atomic_number == 127: return 1
        if symbol == 'Xe' and atomic_number == 124: return 0.000952
        if symbol == 'Xe' and atomic_number == 126: return 0.00089
        if symbol == 'Xe' and atomic_number == 128: return 0.019102
        if symbol == 'Xe' and atomic_number == 129: return 0.264006
        if symbol == 'Xe' and atomic_number == 130: return 0.04071
        if symbol == 'Xe' and atomic_number == 131: return 0.212324
        if symbol == 'Xe' and atomic_number == 132: return 0.269086
        if symbol == 'Xe' and atomic_number == 134: return 0.104357
        if symbol == 'Xe' and atomic_number == 136: return 0.088573
        if symbol == 'Cs' and atomic_number == 133: return 1
        if symbol == 'Ba' and atomic_number == 130: return 0.00106
        if symbol == 'Ba' and atomic_number == 132: return 0.00101
        if symbol == 'Ba' and atomic_number == 134: return 0.02417
        if symbol == 'Ba' and atomic_number == 135: return 0.06592
        if symbol == 'Ba' and atomic_number == 136: return 0.07854
        if symbol == 'Ba' and atomic_number == 137: return 0.11232
        if symbol == 'Ba' and atomic_number == 138: return 0.71698
        if symbol == 'La' and atomic_number == 138: return 0.0008881
        if symbol == 'La' and atomic_number == 139: return 0.9991119
        if symbol == 'Ce' and atomic_number == 136: return 0.00185
        if symbol == 'Ce' and atomic_number == 138: return 0.00251
        if symbol == 'Ce' and atomic_number == 140: return 0.8845
        if symbol == 'Ce' and atomic_number == 142: return 0.11114
        if symbol == 'Pr' and atomic_number == 141: return 1
        if symbol == 'Nd' and atomic_number == 142: return 0.27152
        if symbol == 'Nd' and atomic_number == 143: return 0.12174
        if symbol == 'Nd' and atomic_number == 144: return 0.23798
        if symbol == 'Nd' and atomic_number == 145: return 0.08293
        if symbol == 'Nd' and atomic_number == 146: return 0.17189
        if symbol == 'Nd' and atomic_number == 148: return 0.05756
        if symbol == 'Nd' and atomic_number == 150: return 0.05638
        if symbol == 'Sm' and atomic_number == 144: return 0.0307
        if symbol == 'Sm' and atomic_number == 147: return 0.1499
        if symbol == 'Sm' and atomic_number == 148: return 0.1124
        if symbol == 'Sm' and atomic_number == 149: return 0.1382
        if symbol == 'Sm' and atomic_number == 150: return 0.0738
        if symbol == 'Sm' and atomic_number == 152: return 0.2675
        if symbol == 'Sm' and atomic_number == 154: return 0.2275
        if symbol == 'Eu' and atomic_number == 151: return 0.4781
        if symbol == 'Eu' and atomic_number == 153: return 0.5219
        if symbol == 'Gd' and atomic_number == 152: return 0.002
        if symbol == 'Gd' and atomic_number == 154: return 0.0218
        if symbol == 'Gd' and atomic_number == 155: return 0.148
        if symbol == 'Gd' and atomic_number == 156: return 0.2047
        if symbol == 'Gd' and atomic_number == 157: return 0.1565
        if symbol == 'Gd' and atomic_number == 158: return 0.2484
        if symbol == 'Gd' and atomic_number == 160: return 0.2186
        if symbol == 'Tb' and atomic_number == 159: return 1
        if symbol == 'Dy' and atomic_number == 156: return 0.00056
        if symbol == 'Dy' and atomic_number == 158: return 0.00095
        if symbol == 'Dy' and atomic_number == 160: return 0.02329
        if symbol == 'Dy' and atomic_number == 161: return 0.18889
        if symbol == 'Dy' and atomic_number == 162: return 0.25475
        if symbol == 'Dy' and atomic_number == 163: return 0.24896
        if symbol == 'Dy' and atomic_number == 164: return 0.2826
        if symbol == 'Ho' and atomic_number == 165: return 1
        if symbol == 'Er' and atomic_number == 162: return 0.00139
        if symbol == 'Er' and atomic_number == 164: return 0.01601
        if symbol == 'Er' and atomic_number == 166: return 0.33503
        if symbol == 'Er' and atomic_number == 167: return 0.22869
        if symbol == 'Er' and atomic_number == 168: return 0.26978
        if symbol == 'Er' and atomic_number == 170: return 0.1491
        if symbol == 'Tm' and atomic_number == 169: return 1
        if symbol == 'Yb' and atomic_number == 168: return 0.00123
        if symbol == 'Yb' and atomic_number == 170: return 0.02982
        if symbol == 'Yb' and atomic_number == 171: return 0.1409
        if symbol == 'Yb' and atomic_number == 172: return 0.2168
        if symbol == 'Yb' and atomic_number == 173: return 0.16103
        if symbol == 'Yb' and atomic_number == 174: return 0.32026
        if symbol == 'Yb' and atomic_number == 176: return 0.12996
        if symbol == 'Lu' and atomic_number == 175: return 0.97401
        if symbol == 'Lu' and atomic_number == 176: return 0.02599
        if symbol == 'Hf' and atomic_number == 174: return 0.0016
        if symbol == 'Hf' and atomic_number == 176: return 0.0526
        if symbol == 'Hf' and atomic_number == 177: return 0.186
        if symbol == 'Hf' and atomic_number == 178: return 0.2728
        if symbol == 'Hf' and atomic_number == 179: return 0.1362
        if symbol == 'Hf' and atomic_number == 180: return 0.3508
        if symbol == 'Ta' and atomic_number == 180: return 0.0001201
        if symbol == 'Ta' and atomic_number == 181: return 0.9998799
        if symbol == 'W' and atomic_number == 180: return 0.0012
        if symbol == 'W' and atomic_number == 182: return 0.265
        if symbol == 'W' and atomic_number == 183: return 0.1431
        if symbol == 'W' and atomic_number == 184: return 0.3064
        if symbol == 'W' and atomic_number == 186: return 0.2843
        if symbol == 'Re' and atomic_number == 185: return 0.374
        if symbol == 'Re' and atomic_number == 187: return 0.626
        if symbol == 'Os' and atomic_number == 184: return 0.0002
        if symbol == 'Os' and atomic_number == 186: return 0.0159
        if symbol == 'Os' and atomic_number == 187: return 0.0196
        if symbol == 'Os' and atomic_number == 188: return 0.1324
        if symbol == 'Os' and atomic_number == 189: return 0.1615
        if symbol == 'Os' and atomic_number == 190: return 0.2626
        if symbol == 'Os' and atomic_number == 192: return 0.4078
        if symbol == 'Ir' and atomic_number == 191: return 0.373
        if symbol == 'Ir' and atomic_number == 193: return 0.627
        if symbol == 'Pt' and atomic_number == 190: return 0.00012
        if symbol == 'Pt' and atomic_number == 192: return 0.00782
        if symbol == 'Pt' and atomic_number == 194: return 0.3286
        if symbol == 'Pt' and atomic_number == 195: return 0.3378
        if symbol == 'Pt' and atomic_number == 196: return 0.2521
        if symbol == 'Pt' and atomic_number == 198: return 0.07356
        if symbol == 'Au' and atomic_number == 197: return 1
        if symbol == 'Hg' and atomic_number == 196: return 0.0015
        if symbol == 'Hg' and atomic_number == 198: return 0.0997
        if symbol == 'Hg' and atomic_number == 199: return 0.1687
        if symbol == 'Hg' and atomic_number == 200: return 0.231
        if symbol == 'Hg' and atomic_number == 201: return 0.1318
        if symbol == 'Hg' and atomic_number == 202: return 0.2986
        if symbol == 'Hg' and atomic_number == 204: return 0.0687
        if symbol == 'Tl' and atomic_number == 203: return 0.2952
        if symbol == 'Tl' and atomic_number == 205: return 0.7048
        if symbol == 'Pb' and atomic_number == 204: return 0.014
        if symbol == 'Pb' and atomic_number == 206: return 0.241
        if symbol == 'Pb' and atomic_number == 207: return 0.221
        if symbol == 'Pb' and atomic_number == 208: return 0.524
        if symbol == 'Bi' and atomic_number == 209: return 1
        if symbol == 'Th' and atomic_number == 232: return 1
        if symbol == 'Pa' and atomic_number == 231: return 1
        if symbol == 'U' and atomic_number == 234: return 0.000054
        if symbol == 'U' and atomic_number == 235: return 0.007204
        if symbol == 'U' and atomic_number == 238: return 0.992742

def mass_amu(symbol,atomic_number):
        if symbol == 'H' and atomic_number == 1: return 1.0078250322
        if symbol == 'H' and atomic_number == 2: return 2.0141017781
        if symbol == 'H' and atomic_number == 3: return 3.0160492779
        if symbol == 'He' and atomic_number == 3: return 3.0160293201
        if symbol == 'He' and atomic_number == 4: return 4.0026032541
        if symbol == 'Li' and atomic_number == 6: return 6.0151228874
        if symbol == 'Li' and atomic_number == 7: return 7.0160034366
        if symbol == 'Be' and atomic_number == 9: return 9.012183065
        if symbol == 'B' and atomic_number == 10: return 10.01293695
        if symbol == 'B' and atomic_number == 11: return 11.00930536
        if symbol == 'C' and atomic_number == 12: return 12.0
        if symbol == 'C' and atomic_number == 13: return 13.0033548351
        if symbol == 'C' and atomic_number == 14: return 14.0032419884
        if symbol == 'N' and atomic_number == 14: return 14.0030740044
        if symbol == 'N' and atomic_number == 15: return 15.0001088989
        if symbol == 'O' and atomic_number == 16: return 15.9949146196
        if symbol == 'O' and atomic_number == 17: return 16.99913175650
        if symbol == 'O' and atomic_number == 18: return 17.99915961286
        if symbol == 'F' and atomic_number == 19: return 18.9984031627
        if symbol == 'Ne' and atomic_number == 20: return 19.9924401762
        if symbol == 'Ne' and atomic_number == 21: return 20.993846685
        if symbol == 'Ne' and atomic_number == 22: return 21.991385114
        if symbol == 'Na' and atomic_number == 23: return 22.989769282
        if symbol == 'Mg' and atomic_number == 24: return 23.985041697
        if symbol == 'Mg' and atomic_number == 25: return 24.985836976
        if symbol == 'Mg' and atomic_number == 26: return 25.982592968
        if symbol == 'Al' and atomic_number == 27: return 26.98153853
        if symbol == 'Si' and atomic_number == 28: return 27.9769265347
        if symbol == 'Si' and atomic_number == 29: return 28.9764946649
        if symbol == 'Si' and atomic_number == 30: return 29.973770136
        if symbol == 'P' and atomic_number == 31: return 30.9737619984
        if symbol == 'S' and atomic_number == 32: return 31.9720711744
        if symbol == 'S' and atomic_number == 33: return 32.9714589098
        if symbol == 'S' and atomic_number == 34: return 33.967867004
        if symbol == 'S' and atomic_number == 36: return 35.96708071
        if symbol == 'Cl' and atomic_number == 35: return 34.968852682
        if symbol == 'Cl' and atomic_number == 37: return 36.965902602
        if symbol == 'Ar' and atomic_number == 36: return 35.967545105
        if symbol == 'Ar' and atomic_number == 38: return 37.96273211
        if symbol == 'Ar' and atomic_number == 40: return 39.9623831237
        if symbol == 'K' and atomic_number == 39: return 38.9637064864
        if symbol == 'K' and atomic_number == 40: return 39.963998166
        if symbol == 'K' and atomic_number == 41: return 40.9618252579
        if symbol == 'Ca' and atomic_number == 40: return 39.962590863
        if symbol == 'Ca' and atomic_number == 42: return 41.95861783
        if symbol == 'Ca' and atomic_number == 43: return 42.95876644
        if symbol == 'Ca' and atomic_number == 44: return 43.95548156
        if symbol == 'Ca' and atomic_number == 46: return 45.953689
        if symbol == 'Ca' and atomic_number == 48: return 47.95252276
        if symbol == 'Sc' and atomic_number == 45: return 44.95590828
        if symbol == 'Ti' and atomic_number == 46: return 45.95262772
        if symbol == 'Ti' and atomic_number == 47: return 46.95175879
        if symbol == 'Ti' and atomic_number == 48: return 47.94794198
        if symbol == 'Ti' and atomic_number == 49: return 48.94786568
        if symbol == 'Ti' and atomic_number == 50: return 49.94478689
        if symbol == 'V' and atomic_number == 50: return 49.94715601
        if symbol == 'V' and atomic_number == 51: return 50.94395704
        if symbol == 'Cr' and atomic_number == 50: return 49.94604183
        if symbol == 'Cr' and atomic_number == 52: return 51.94050623
        if symbol == 'Cr' and atomic_number == 53: return 52.94064815
        if symbol == 'Cr' and atomic_number == 54: return 53.93887916
        if symbol == 'Mn' and atomic_number == 55: return 54.93804391
        if symbol == 'Fe' and atomic_number == 54: return 53.93960899
        if symbol == 'Fe' and atomic_number == 56: return 55.93493633
        if symbol == 'Fe' and atomic_number == 57: return 56.93539284
        if symbol == 'Fe' and atomic_number == 58: return 57.93327443
        if symbol == 'Co' and atomic_number == 59: return 58.93319429
        if symbol == 'Ni' and atomic_number == 58: return 57.93534241
        if symbol == 'Ni' and atomic_number == 60: return 59.93078588
        if symbol == 'Ni' and atomic_number == 61: return 60.93105557
        if symbol == 'Ni' and atomic_number == 62: return 61.92834537
        if symbol == 'Ni' and atomic_number == 64: return 63.92796682
        if symbol == 'Cu' and atomic_number == 63: return 62.92959772
        if symbol == 'Cu' and atomic_number == 65: return 64.9277897
        if symbol == 'Zn' and atomic_number == 64: return 63.92914201
        if symbol == 'Zn' and atomic_number == 66: return 65.92603381
        if symbol == 'Zn' and atomic_number == 67: return 66.92712775
        if symbol == 'Zn' and atomic_number == 68: return 67.92484455
        if symbol == 'Zn' and atomic_number == 70: return 69.9253192
        if symbol == 'Ga' and atomic_number == 69: return 68.9255735
        if symbol == 'Ga' and atomic_number == 71: return 70.92470258
        if symbol == 'Ge' and atomic_number == 70: return 69.92424875
        if symbol == 'Ge' and atomic_number == 72: return 71.922075826
        if symbol == 'Ge' and atomic_number == 73: return 72.923458956
        if symbol == 'Ge' and atomic_number == 74: return 73.921177761
        if symbol == 'Ge' and atomic_number == 76: return 75.921402726
        if symbol == 'As' and atomic_number == 75: return 74.92159457
        if symbol == 'Se' and atomic_number == 74: return 73.922475934
        if symbol == 'Se' and atomic_number == 76: return 75.919213704
        if symbol == 'Se' and atomic_number == 77: return 76.919914154
        if symbol == 'Se' and atomic_number == 78: return 77.91730928
        if symbol == 'Se' and atomic_number == 80: return 79.9165218
        if symbol == 'Se' and atomic_number == 82: return 81.9166995
        if symbol == 'Br' and atomic_number == 79: return 78.9183376
        if symbol == 'Br' and atomic_number == 81: return 80.9162897
        if symbol == 'Kr' and atomic_number == 78: return 77.92036494
        if symbol == 'Kr' and atomic_number == 80: return 79.91637808
        if symbol == 'Kr' and atomic_number == 82: return 81.91348273
        if symbol == 'Kr' and atomic_number == 83: return 82.91412716
        if symbol == 'Kr' and atomic_number == 84: return 83.9114977282
        if symbol == 'Kr' and atomic_number == 86: return 85.9106106269
        if symbol == 'Rb' and atomic_number == 85: return 84.9117897379
        if symbol == 'Rb' and atomic_number == 87: return 86.909180531
        if symbol == 'Sr' and atomic_number == 84: return 83.9134191
        if symbol == 'Sr' and atomic_number == 86: return 85.9092606
        if symbol == 'Sr' and atomic_number == 87: return 86.9088775
        if symbol == 'Sr' and atomic_number == 88: return 87.9056125
        if symbol == 'Y' and atomic_number == 89: return 88.9058403
        if symbol == 'Zr' and atomic_number == 90: return 89.9046977
        if symbol == 'Zr' and atomic_number == 91: return 90.9056396
        if symbol == 'Zr' and atomic_number == 92: return 91.9050347
        if symbol == 'Zr' and atomic_number == 94: return 93.9063108
        if symbol == 'Zr' and atomic_number == 96: return 95.9082714
        if symbol == 'Nb' and atomic_number == 93: return 92.906373
        if symbol == 'Mo' and atomic_number == 92: return 91.90680796
        if symbol == 'Mo' and atomic_number == 94: return 93.9050849
        if symbol == 'Mo' and atomic_number == 95: return 94.90583877
        if symbol == 'Mo' and atomic_number == 96: return 95.90467612
        if symbol == 'Mo' and atomic_number == 97: return 96.90601812
        if symbol == 'Mo' and atomic_number == 98: return 97.90540482
        if symbol == 'Mo' and atomic_number == 100: return 99.9074718
        if symbol == 'Ru' and atomic_number == 96: return 95.90759025
        if symbol == 'Ru' and atomic_number == 98: return 97.9052868
        if symbol == 'Ru' and atomic_number == 99: return 98.9059341
        if symbol == 'Ru' and atomic_number == 100: return 99.9042143
        if symbol == 'Ru' and atomic_number == 101: return 100.9055769
        if symbol == 'Ru' and atomic_number == 102: return 101.9043441
        if symbol == 'Ru' and atomic_number == 104: return 103.9054275
        if symbol == 'Rh' and atomic_number == 103: return 102.905498
        if symbol == 'Pd' and atomic_number == 102: return 101.9056022
        if symbol == 'Pd' and atomic_number == 104: return 103.9040305
        if symbol == 'Pd' and atomic_number == 105: return 104.9050796
        if symbol == 'Pd' and atomic_number == 106: return 105.9034804
        if symbol == 'Pd' and atomic_number == 108: return 107.9038916
        if symbol == 'Pd' and atomic_number == 110: return 109.9051722
        if symbol == 'Ag' and atomic_number == 107: return 106.9050916
        if symbol == 'Ag' and atomic_number == 109: return 108.9047553
        if symbol == 'Cd' and atomic_number == 106: return 105.9064599
        if symbol == 'Cd' and atomic_number == 108: return 107.9041834
        if symbol == 'Cd' and atomic_number == 110: return 109.90300661
        if symbol == 'Cd' and atomic_number == 111: return 110.90418287
        if symbol == 'Cd' and atomic_number == 112: return 111.90276287
        if symbol == 'Cd' and atomic_number == 113: return 112.90440813
        if symbol == 'Cd' and atomic_number == 114: return 113.90336509
        if symbol == 'Cd' and atomic_number == 116: return 115.90476315
        if symbol == 'In' and atomic_number == 113: return 112.90406184
        if symbol == 'In' and atomic_number == 115: return 114.903878776
        if symbol == 'Sn' and atomic_number == 112: return 111.90482387
        if symbol == 'Sn' and atomic_number == 114: return 113.9027827
        if symbol == 'Sn' and atomic_number == 115: return 114.903344699
        if symbol == 'Sn' and atomic_number == 116: return 115.9017428
        if symbol == 'Sn' and atomic_number == 117: return 116.90295398
        if symbol == 'Sn' and atomic_number == 118: return 117.90160657
        if symbol == 'Sn' and atomic_number == 119: return 118.90331117
        if symbol == 'Sn' and atomic_number == 120: return 119.90220163
        if symbol == 'Sn' and atomic_number == 122: return 121.9034438
        if symbol == 'Sn' and atomic_number == 124: return 123.9052766
        if symbol == 'Sb' and atomic_number == 121: return 120.903812
        if symbol == 'Sb' and atomic_number == 123: return 122.9042132
        if symbol == 'Te' and atomic_number == 120: return 119.9040593
        if symbol == 'Te' and atomic_number == 122: return 121.9030435
        if symbol == 'Te' and atomic_number == 123: return 122.9042698
        if symbol == 'Te' and atomic_number == 124: return 123.9028171
        if symbol == 'Te' and atomic_number == 125: return 124.9044299
        if symbol == 'Te' and atomic_number == 126: return 125.9033109
        if symbol == 'Te' and atomic_number == 128: return 127.90446128
        if symbol == 'Te' and atomic_number == 130: return 129.906222748
        if symbol == 'I' and atomic_number == 127: return 126.9044719
        if symbol == 'Xe' and atomic_number == 124: return 123.905892
        if symbol == 'Xe' and atomic_number == 126: return 125.9042983
        if symbol == 'Xe' and atomic_number == 128: return 127.903531
        if symbol == 'Xe' and atomic_number == 129: return 128.9047808611
        if symbol == 'Xe' and atomic_number == 130: return 129.903509349
        if symbol == 'Xe' and atomic_number == 131: return 130.90508406
        if symbol == 'Xe' and atomic_number == 132: return 131.9041550856
        if symbol == 'Xe' and atomic_number == 134: return 133.90539466
        if symbol == 'Xe' and atomic_number == 136: return 135.907214484
        if symbol == 'Cs' and atomic_number == 133: return 132.905451961
        if symbol == 'Ba' and atomic_number == 130: return 129.9063207
        if symbol == 'Ba' and atomic_number == 132: return 131.9050611
        if symbol == 'Ba' and atomic_number == 134: return 133.90450818
        if symbol == 'Ba' and atomic_number == 135: return 134.90568838
        if symbol == 'Ba' and atomic_number == 136: return 135.90457573
        if symbol == 'Ba' and atomic_number == 137: return 136.90582714
        if symbol == 'Ba' and atomic_number == 138: return 137.905247
        if symbol == 'La' and atomic_number == 138: return 137.9071149
        if symbol == 'La' and atomic_number == 139: return 138.9063563
        if symbol == 'Ce' and atomic_number == 136: return 135.90712921
        if symbol == 'Ce' and atomic_number == 138: return 137.905991
        if symbol == 'Ce' and atomic_number == 140: return 139.9054431
        if symbol == 'Ce' and atomic_number == 142: return 141.9092504
        if symbol == 'Pr' and atomic_number == 141: return 140.9076576
        if symbol == 'Nd' and atomic_number == 142: return 141.907729
        if symbol == 'Nd' and atomic_number == 143: return 142.90982
        if symbol == 'Nd' and atomic_number == 144: return 143.910093
        if symbol == 'Nd' and atomic_number == 145: return 144.9125793
        if symbol == 'Nd' and atomic_number == 146: return 145.9131226
        if symbol == 'Nd' and atomic_number == 148: return 147.9168993
        if symbol == 'Nd' and atomic_number == 150: return 149.9209022
        if symbol == 'Sm' and atomic_number == 144: return 143.9120065
        if symbol == 'Sm' and atomic_number == 147: return 146.9149044
        if symbol == 'Sm' and atomic_number == 148: return 147.9148292
        if symbol == 'Sm' and atomic_number == 149: return 148.9171921
        if symbol == 'Sm' and atomic_number == 150: return 149.9172829
        if symbol == 'Sm' and atomic_number == 152: return 151.9197397
        if symbol == 'Sm' and atomic_number == 154: return 153.9222169
        if symbol == 'Eu' and atomic_number == 151: return 150.9198578
        if symbol == 'Eu' and atomic_number == 153: return 152.921238
        if symbol == 'Gd' and atomic_number == 152: return 151.9197995
        if symbol == 'Gd' and atomic_number == 154: return 153.9208741
        if symbol == 'Gd' and atomic_number == 155: return 154.9226305
        if symbol == 'Gd' and atomic_number == 156: return 155.9221312
        if symbol == 'Gd' and atomic_number == 157: return 156.9239686
        if symbol == 'Gd' and atomic_number == 158: return 157.9241123
        if symbol == 'Gd' and atomic_number == 160: return 159.9270624
        if symbol == 'Tb' and atomic_number == 159: return 158.9253547
        if symbol == 'Dy' and atomic_number == 156: return 155.9242847
        if symbol == 'Dy' and atomic_number == 158: return 157.9244159
        if symbol == 'Dy' and atomic_number == 160: return 159.9252046
        if symbol == 'Dy' and atomic_number == 161: return 160.9269405
        if symbol == 'Dy' and atomic_number == 162: return 161.9268056
        if symbol == 'Dy' and atomic_number == 163: return 162.9287383
        if symbol == 'Dy' and atomic_number == 164: return 163.9291819
        if symbol == 'Ho' and atomic_number == 165: return 164.9303288
        if symbol == 'Er' and atomic_number == 162: return 161.9287884
        if symbol == 'Er' and atomic_number == 164: return 163.9292088
        if symbol == 'Er' and atomic_number == 166: return 165.9302995
        if symbol == 'Er' and atomic_number == 167: return 166.9320546
        if symbol == 'Er' and atomic_number == 168: return 167.9323767
        if symbol == 'Er' and atomic_number == 170: return 169.9354702
        if symbol == 'Tm' and atomic_number == 169: return 168.9342179
        if symbol == 'Yb' and atomic_number == 168: return 167.9338896
        if symbol == 'Yb' and atomic_number == 170: return 169.9347664
        if symbol == 'Yb' and atomic_number == 171: return 170.9363302
        if symbol == 'Yb' and atomic_number == 172: return 171.9363859
        if symbol == 'Yb' and atomic_number == 173: return 172.9382151
        if symbol == 'Yb' and atomic_number == 174: return 173.9388664
        if symbol == 'Yb' and atomic_number == 176: return 175.9425764
        if symbol == 'Lu' and atomic_number == 175: return 174.9407752
        if symbol == 'Lu' and atomic_number == 176: return 175.9426897
        if symbol == 'Hf' and atomic_number == 174: return 173.9400461
        if symbol == 'Hf' and atomic_number == 176: return 175.9414076
        if symbol == 'Hf' and atomic_number == 177: return 176.9432277
        if symbol == 'Hf' and atomic_number == 178: return 177.9437058
        if symbol == 'Hf' and atomic_number == 179: return 178.9458232
        if symbol == 'Hf' and atomic_number == 180: return 179.946557
        if symbol == 'Ta' and atomic_number == 180: return 179.9474648
        if symbol == 'Ta' and atomic_number == 181: return 180.9479958
        if symbol == 'W' and atomic_number == 180: return 179.9467108
        if symbol == 'W' and atomic_number == 182: return 181.94820394
        if symbol == 'W' and atomic_number == 183: return 182.95022275
        if symbol == 'W' and atomic_number == 184: return 183.95093092
        if symbol == 'W' and atomic_number == 186: return 185.9543628
        if symbol == 'Re' and atomic_number == 185: return 184.9529545
        if symbol == 'Re' and atomic_number == 187: return 186.9557501
        if symbol == 'Os' and atomic_number == 184: return 183.9524885
        if symbol == 'Os' and atomic_number == 186: return 185.953835
        if symbol == 'Os' and atomic_number == 187: return 186.9557474
        if symbol == 'Os' and atomic_number == 188: return 187.9558352
        if symbol == 'Os' and atomic_number == 189: return 188.9581442
        if symbol == 'Os' and atomic_number == 190: return 189.9584437
        if symbol == 'Os' and atomic_number == 192: return 191.961477
        if symbol == 'Ir' and atomic_number == 191: return 190.9605893
        if symbol == 'Ir' and atomic_number == 193: return 192.9629216
        if symbol == 'Pt' and atomic_number == 190: return 189.9599297
        if symbol == 'Pt' and atomic_number == 192: return 191.9610387
        if symbol == 'Pt' and atomic_number == 194: return 193.9626809
        if symbol == 'Pt' and atomic_number == 195: return 194.9647917
        if symbol == 'Pt' and atomic_number == 196: return 195.96495209
        if symbol == 'Pt' and atomic_number == 198: return 197.9678949
        if symbol == 'Au' and atomic_number == 197: return 196.96656879
        if symbol == 'Hg' and atomic_number == 196: return 195.9658326
        if symbol == 'Hg' and atomic_number == 198: return 197.9667686
        if symbol == 'Hg' and atomic_number == 199: return 198.96828064
        if symbol == 'Hg' and atomic_number == 200: return 199.96832659
        if symbol == 'Hg' and atomic_number == 201: return 200.97030284
        if symbol == 'Hg' and atomic_number == 202: return 201.9706434
        if symbol == 'Hg' and atomic_number == 204: return 203.97349398
        if symbol == 'Tl' and atomic_number == 203: return 202.9723446
        if symbol == 'Tl' and atomic_number == 205: return 204.9744278
        if symbol == 'Pb' and atomic_number == 204: return 203.973044
        if symbol == 'Pb' and atomic_number == 206: return 205.9744657
        if symbol == 'Pb' and atomic_number == 207: return 206.9758973
        if symbol == 'Pb' and atomic_number == 208: return 207.9766525
        if symbol == 'Bi' and atomic_number == 209: return 208.9803991
        if symbol == 'Th' and atomic_number == 232: return 232.0380558
        if symbol == 'Pa' and atomic_number == 231: return 231.0358842
        if symbol == 'U' and atomic_number == 234: return 234.0409523
        if symbol == 'U' and atomic_number == 235: return 235.0439301
        if symbol == 'U' and atomic_number == 238: return 238.0507884
        else:
            print('symbol atomic number combination not found no isotope mass to return ')
            print('symbol=',symbol,'atomic_number',atomic_number)

def natural_isotopes_in_elements(symbol):
        from neutronics_material_MAKER.isotope import Isotope
        if symbol == 'Sn': return [Isotope(symbol, 112), Isotope(symbol, 114), Isotope(symbol, 115),
                                        Isotope(symbol, 116), Isotope(symbol, 117),
                                        Isotope(symbol, 118), Isotope(symbol, 119), Isotope(symbol, 120),
                                        Isotope(symbol, 122), Isotope(symbol, 124)]
        if symbol == 'Xe': return [Isotope(symbol, 124), Isotope(symbol, 126), Isotope(symbol, 128),
                                        Isotope(symbol, 129), Isotope(symbol, 130),
                                        Isotope(symbol, 131), Isotope(symbol, 132), Isotope(symbol, 134),
                                        Isotope(symbol, 136)]
        if symbol == 'Cd': return [Isotope(symbol, 106), Isotope(symbol, 108), Isotope(symbol, 110),
                                        Isotope(symbol, 111), Isotope(symbol, 112), Isotope(symbol, 113),
                                        Isotope(symbol, 114), Isotope(symbol, 116)]
        if symbol == 'Te': return [Isotope(symbol, 120), Isotope(symbol, 122), Isotope(symbol, 123),
                                        Isotope(symbol, 124), Isotope(symbol, 125), Isotope(symbol, 126),
                                        Isotope(symbol, 128), Isotope(symbol, 130)]
        if symbol == 'Ba': return [Isotope(symbol, 130), Isotope(symbol, 132), Isotope(symbol, 134),
                                        Isotope(symbol, 135), Isotope(symbol, 136), Isotope(symbol, 137),
                                        Isotope(symbol, 138)]
        if symbol == 'Dy': return [Isotope(symbol, 156), Isotope(symbol, 158), Isotope(symbol, 160),
                                        Isotope(symbol, 161), Isotope(symbol, 162), Isotope(symbol, 163),
                                        Isotope(symbol, 164)]
        if symbol == 'Gd': return [Isotope(symbol, 152), Isotope(symbol, 154), Isotope(symbol, 155),
                                        Isotope(symbol, 156), Isotope(symbol, 157), Isotope(symbol, 158),
                                        Isotope(symbol, 160)]
        if symbol == 'Hg': return [Isotope(symbol, 196), Isotope(symbol, 198), Isotope(symbol, 199),
                                        Isotope(symbol, 200), Isotope(symbol, 201), Isotope(symbol, 202),
                                        Isotope(symbol, 204)]
        if symbol == 'Mo': return [Isotope(symbol, 92), Isotope(symbol, 94), Isotope(symbol, 95),
                                        Isotope(symbol, 96), Isotope(symbol, 97), Isotope(symbol, 98),
                                        Isotope(symbol, 100)]
        if symbol == 'Nd': return [Isotope(symbol, 142), Isotope(symbol, 143), Isotope(symbol, 144),
                                        Isotope(symbol, 145), Isotope(symbol, 146), Isotope(symbol, 148),
                                        Isotope(symbol, 150)]
        if symbol == 'Os': return [Isotope(symbol, 184), Isotope(symbol, 186), Isotope(symbol, 187),
                                        Isotope(symbol, 188), Isotope(symbol, 189), Isotope(symbol, 190),
                                        Isotope(symbol, 192)]
        if symbol == 'Ru': return [Isotope(symbol, 96), Isotope(symbol, 98), Isotope(symbol, 99),
                                        Isotope(symbol, 100), Isotope(symbol, 101),
                                        Isotope(symbol, 102), Isotope(symbol, 104)]
        if symbol == 'Sm': return [Isotope(symbol, 144), Isotope(symbol, 147), Isotope(symbol, 148),
                                        Isotope(symbol, 149), Isotope(symbol, 150),
                                        Isotope(symbol, 152), Isotope(symbol, 154)]
        if symbol == 'Yb': return [Isotope(symbol, 168), Isotope(symbol, 170), Isotope(symbol, 171),
                                        Isotope(symbol, 172), Isotope(symbol, 173),
                                        Isotope(symbol, 174), Isotope(symbol, 176)]
        if symbol == 'Ca': return [Isotope(symbol, 40), Isotope(symbol, 42), Isotope(symbol, 43),
                                        Isotope(symbol, 44), Isotope(symbol, 46), Isotope(symbol, 48)]
        if symbol == 'Er': return [Isotope(symbol, 162), Isotope(symbol, 164), Isotope(symbol, 166),
                                        Isotope(symbol, 167), Isotope(symbol, 168), Isotope(symbol, 170)]
        if symbol == 'Hf': return [Isotope(symbol, 174), Isotope(symbol, 176), Isotope(symbol, 177),
                                        Isotope(symbol, 178), Isotope(symbol, 179), Isotope(symbol, 180)]
        if symbol == 'Kr': return [Isotope(symbol, 78), Isotope(symbol, 80), Isotope(symbol, 82),
                                        Isotope(symbol, 83), Isotope(symbol, 84), Isotope(symbol, 86)]
        if symbol == 'Pd': return [Isotope(symbol, 102), Isotope(symbol, 104), Isotope(symbol, 105),
                                        Isotope(symbol, 106), Isotope(symbol, 108), Isotope(symbol, 110)]
        if symbol == 'Pt': return [Isotope(symbol, 190), Isotope(symbol, 192), Isotope(symbol, 194),
                                        Isotope(symbol, 195), Isotope(symbol, 196), Isotope(symbol, 198)]
        if symbol == 'Se': return [Isotope(symbol, 74), Isotope(symbol, 76), Isotope(symbol, 77),
                                        Isotope(symbol, 78), Isotope(symbol, 80), Isotope(symbol, 82)]
        if symbol == 'Ge': return [Isotope(symbol, 70), Isotope(symbol, 72), Isotope(symbol, 73),
                                        Isotope(symbol, 74), Isotope(symbol, 76)]
        if symbol == 'Ni': return [Isotope(symbol, 58), Isotope(symbol, 60), Isotope(symbol, 61),
                                        Isotope(symbol, 62), Isotope(symbol, 64)]
        if symbol == 'Ti': return [Isotope(symbol, 46), Isotope(symbol, 47), Isotope(symbol, 48),
                                        Isotope(symbol, 49), Isotope(symbol, 50)]
        if symbol == 'W': return [Isotope(symbol, 180), Isotope(symbol, 182), Isotope(symbol, 183),
                                       Isotope(symbol, 184), Isotope(symbol, 186)]
        if symbol == 'Zn': return [Isotope(symbol, 64), Isotope(symbol, 66), Isotope(symbol, 67),
                                        Isotope(symbol, 68), Isotope(symbol, 70)]
        if symbol == 'Zr': return [Isotope(symbol, 90), Isotope(symbol, 91), Isotope(symbol, 92),
                                        Isotope(symbol, 94), Isotope(symbol, 96)]
        if symbol == 'Ce': return [Isotope(symbol, 136), Isotope(symbol, 138), Isotope(symbol, 140),
                                        Isotope(symbol, 142)]
        if symbol == 'Cr': return [Isotope(symbol, 50), Isotope(symbol, 52), Isotope(symbol, 53),
                                        Isotope(symbol, 54)]
        if symbol == 'Fe': return [Isotope(symbol, 54), Isotope(symbol, 56), Isotope(symbol, 57),
                                        Isotope(symbol, 58)]
        if symbol == 'Pb': return [Isotope(symbol, 204), Isotope(symbol, 206), Isotope(symbol, 207),
                                        Isotope(symbol, 208)]
        if symbol == 'S': return [Isotope(symbol, 32), Isotope(symbol, 33), Isotope(symbol, 34),
                                       Isotope(symbol, 36)]
        if symbol == 'Sr': return [Isotope(symbol, 84), Isotope(symbol, 86), Isotope(symbol, 87),
                                        Isotope(symbol, 88)]
        if symbol == 'Ar': return [Isotope(symbol, 36), Isotope(symbol, 38), Isotope(symbol, 40)]
        if symbol == 'C': return [Isotope(symbol, 12), Isotope(symbol, 13)]#, Isotope(symbol, 14)]
        if symbol == 'K': return [Isotope(symbol, 39), Isotope(symbol, 40), Isotope(symbol, 41)]
        if symbol == 'Mg': return [Isotope(symbol, 24), Isotope(symbol, 25), Isotope(symbol, 26)]
        if symbol == 'Ne': return [Isotope(symbol, 20), Isotope(symbol, 21), Isotope(symbol, 22)]
        if symbol == 'Si': return [Isotope(symbol, 28), Isotope(symbol, 29), Isotope(symbol, 30)]
        if symbol == 'U': return [Isotope(symbol, 234), Isotope(symbol, 235), Isotope(symbol, 238)]
        if symbol == 'Ag': return [Isotope(symbol, 107), Isotope(symbol, 109)]
        if symbol == 'B': return [Isotope(symbol, 10), Isotope(symbol, 11)]
        if symbol == 'Br': return [Isotope(symbol, 79), Isotope(symbol, 81)]
        if symbol == 'Cl': return [Isotope(symbol, 35), Isotope(symbol, 37)]
        if symbol == 'Cu': return [Isotope(symbol, 63), Isotope(symbol, 65)]
        if symbol == 'Eu': return [Isotope(symbol, 151), Isotope(symbol, 153)]
        if symbol == 'Ga': return [Isotope(symbol, 69), Isotope(symbol, 71)]
        if symbol == 'H':  return [Isotope(symbol, 1), Isotope(symbol, 2)]
        if symbol == 'He': return [Isotope(symbol, 3), Isotope(symbol, 4)]
        if symbol == 'In': return [Isotope(symbol, 113), Isotope(symbol, 115)]
        if symbol == 'Ir': return [Isotope(symbol, 191), Isotope(symbol, 193)]
        if symbol == 'La': return [Isotope(symbol, 138), Isotope(symbol, 139)]
        if symbol == 'Li': return [Isotope(symbol, 6), Isotope(symbol, 7)]
        if symbol == 'Lu': return [Isotope(symbol, 175), Isotope(symbol, 176)]
        if symbol == 'N':  return [Isotope(symbol, 14), Isotope(symbol, 15)]
        if symbol == 'Rb': return [Isotope(symbol, 85), Isotope(symbol, 87)]
        if symbol == 'Re': return [Isotope(symbol, 185), Isotope(symbol, 187)]
        if symbol == 'Sb': return [Isotope(symbol, 121), Isotope(symbol, 123)]
        if symbol == 'Ta': return [Isotope(symbol, 180), Isotope(symbol, 181)]
        if symbol == 'Tl': return [Isotope(symbol, 203), Isotope(symbol, 205)]
        if symbol == 'V':  return [Isotope(symbol, 50), Isotope(symbol, 51)]
        if symbol == 'Be': return [Isotope(symbol, 9)]
        if symbol == 'O':  return [Isotope(symbol, 16),Isotope(symbol, 17),Isotope(symbol, 18)]
        if symbol == 'F':  return [Isotope(symbol, 19)]
        if symbol == 'Na': return [Isotope(symbol, 23)]
        if symbol == 'Al': return [Isotope(symbol, 27)]
        if symbol == 'P':  return [Isotope(symbol, 31)]
        if symbol == 'Sc': return [Isotope(symbol, 45)]
        if symbol == 'Mn': return [Isotope(symbol, 55)]
        if symbol == 'Co': return [Isotope(symbol, 59)]
        if symbol == 'As': return [Isotope(symbol, 75)]
        if symbol == 'Y':  return [Isotope(symbol, 89)]
        if symbol == 'Nb': return [Isotope(symbol, 93)]
        if symbol == 'Rh': return [Isotope(symbol, 103)]
        if symbol == 'I':  return [Isotope(symbol, 127)]
        if symbol == 'Cs': return [Isotope(symbol, 133)]
        if symbol == 'Pr': return [Isotope(symbol, 141)]
        if symbol == 'Tb': return [Isotope(symbol, 159)]
        if symbol == 'Ho': return [Isotope(symbol, 165)]
        if symbol == 'Tm': return [Isotope(symbol, 169)]
        if symbol == 'Au': return [Isotope(symbol, 197)]
        if symbol == 'Bi': return [Isotope(symbol, 209)]
        if symbol == 'Th': return [Isotope(symbol, 232)]
        if symbol == 'Pa': return [Isotope(symbol, 231)]

        else:
            print('natural composition of isotope not found', symbol)
            sys.exit()

def find_symbol_from_protons(protons):
    if protons ==  1 : return 'H'
    if protons ==  2 : return 'He'
    if protons ==  3 : return 'Li'
    if protons ==  4 : return 'Be'
    if protons ==  5 : return 'B'
    if protons ==  6 : return 'C'
    if protons ==  7 : return 'N'
    if protons ==  8 : return 'O'
    if protons ==  9 : return 'F'
    if protons ==  10 : return 'Ne'
    if protons ==  11 : return 'Na'
    if protons ==  12 : return 'Mg'
    if protons ==  13 : return 'Al'
    if protons ==  14 : return 'Si'
    if protons ==  15 : return 'P'
    if protons ==  16 : return 'S'
    if protons ==  17 : return 'Cl'
    if protons ==  18 : return 'Ar'
    if protons ==  19 : return 'K'
    if protons ==  20 : return 'Ca'
    if protons ==  21 : return 'Sc'
    if protons ==  22 : return 'Ti'
    if protons ==  23 : return 'V'
    if protons ==  24 : return 'Cr'
    if protons ==  25 : return 'Mn'
    if protons ==  26 : return 'Fe'
    if protons ==  27 : return 'Co'
    if protons ==  28 : return 'Ni'
    if protons ==  29 : return 'Cu'
    if protons ==  30 : return 'Zn'
    if protons ==  31 : return 'Ga'
    if protons ==  32 : return 'Ge'
    if protons ==  33 : return 'As'
    if protons ==  34 : return 'Se'
    if protons ==  35 : return 'Br'
    if protons ==  36 : return 'Kr'
    if protons ==  37 : return 'Rb'
    if protons ==  38 : return 'Sr'
    if protons ==  39 : return 'Y'
    if protons ==  40 : return 'Zr'
    if protons ==  41 : return 'Nb'
    if protons ==  42 : return 'Mo'
    if protons ==  43 : return 'Tc'
    if protons ==  44 : return 'Ru'
    if protons ==  45 : return 'Rh'
    if protons ==  46 : return 'Pd'
    if protons ==  47 : return 'Ag'
    if protons ==  48 : return 'Cd'
    if protons ==  49 : return 'In'
    if protons ==  50 : return 'Sn'
    if protons ==  51 : return 'Sb'
    if protons ==  52 : return 'Te'
    if protons ==  53 : return 'I'
    if protons ==  54 : return 'Xe'
    if protons ==  55 : return 'Cs'
    if protons ==  56 : return 'Ba'
    if protons ==  57 : return 'La'
    if protons ==  58 : return 'Ce'
    if protons ==  59 : return 'Pr'
    if protons ==  60 : return 'Nd'
    if protons ==  61 : return 'Pm'
    if protons ==  62 : return 'Sm'
    if protons ==  63 : return 'Eu'
    if protons ==  64 : return 'Gd'
    if protons ==  65 : return 'Tb'
    if protons ==  66 : return 'Dy'
    if protons ==  67 : return 'Ho'
    if protons ==  68 : return 'Er'
    if protons ==  69 : return 'Tm'
    if protons ==  70 : return 'Yb'
    if protons ==  71 : return 'Lu'
    if protons ==  72 : return 'Hf'
    if protons ==  73 : return 'Ta'
    if protons ==  74 : return 'W'
    if protons ==  75 : return 'Re'
    if protons ==  76 : return 'Os'
    if protons ==  77 : return 'Ir'
    if protons ==  78 : return 'Pt'
    if protons ==  79 : return 'Au'
    if protons ==  80 : return 'Hg'
    if protons ==  81 : return 'Tl'
    if protons ==  82 : return 'Pb'
    if protons ==  83 : return 'Bi'
    if protons ==  84 : return 'Po'
    if protons ==  85 : return 'At'
    if protons ==  86 : return 'Rn'
    if protons ==  87 : return 'Fr'
    if protons ==  88 : return 'Ra'
    if protons ==  89 : return 'Ac'
    if protons ==  90 : return 'Th'
    if protons ==  91 : return 'Pa'
    if protons ==  92 : return 'U'
    if protons ==  93 : return 'Np'
    if protons ==  94 : return 'Pu'
    if protons ==  95 : return 'Am'
    if protons ==  96 : return 'Cm'
    if protons ==  97 : return 'Bk'
    if protons ==  98 : return 'Cf'
    if protons ==  99 : return 'Es'
    if protons ==  100 : return 'Fm'
    if protons ==  101 : return 'Md'
    if protons ==  102 : return 'No'
    if protons ==  103 : return 'Lr'
    if protons ==  104 : return 'Rf'
    if protons ==  105 : return 'Db'
    if protons ==  106 : return 'Sg'
    if protons ==  107 : return 'Bh'
    if protons ==  108 : return 'Hs'
    if protons ==  109 : return 'Mt'
    if protons ==  110 : return 'Ds'
    if protons ==  111 : return 'Rg'
    if protons ==  112 : return 'Cn'
    if protons ==  113 : return 'Nh'
    if protons ==  114 : return 'Fl'
    if protons ==  115 : return 'Mc'
    if protons ==  116 : return 'Lv'
    if protons ==  117 : return 'Ts'
    if protons ==  118 : return 'Og'
    print('proton number ' + str(protons) + ' not found')
    sys.exit()

def find_protons_from_symbol(symbol):
        #print(symbol)
        if symbol == 'H': return 1
        if symbol == 'He': return 2
        if symbol == 'Li': return 3
        if symbol == 'Be': return 4
        if symbol == 'B': return 5
        if symbol == 'C': return 6
        if symbol == 'N': return 7
        if symbol == 'O': return 8
        if symbol == 'F': return 9
        if symbol == 'Ne': return 10
        if symbol == 'Na': return 11
        if symbol == 'Mg': return 12
        if symbol == 'Al': return 13
        if symbol == 'Si': return 14
        if symbol == 'P': return 15
        if symbol == 'S': return 16
        if symbol == 'Cl': return 17
        if symbol == 'Ar': return 18
        if symbol == 'K': return 19
        if symbol == 'Ca': return 20
        if symbol == 'Sc': return 21
        if symbol == 'Ti': return 22
        if symbol == 'V': return 23
        if symbol == 'Cr': return 24
        if symbol == 'Mn': return 25
        if symbol == 'Fe': return 26
        if symbol == 'Co': return 27
        if symbol == 'Ni': return 28
        if symbol == 'Cu': return 29
        if symbol == 'Zn': return 30
        if symbol == 'Ga': return 31
        if symbol == 'Ge': return 32
        if symbol == 'As': return 33
        if symbol == 'Se': return 34
        if symbol == 'Br': return 35
        if symbol == 'Kr': return 36
        if symbol == 'Rb': return 37
        if symbol == 'Sr': return 38
        if symbol == 'Y': return 39
        if symbol == 'Zr': return 40
        if symbol == 'Nb': return 41
        if symbol == 'Mo': return 42
        if symbol == 'Tc': return 43
        if symbol == 'Ru': return 44
        if symbol == 'Rh': return 45
        if symbol == 'Pd': return 46
        if symbol == 'Ag': return 47
        if symbol == 'Cd': return 48
        if symbol == 'In': return 49
        if symbol == 'Sn': return 50
        if symbol == 'Sb': return 51
        if symbol == 'Te': return 52
        if symbol == 'I': return 53
        if symbol == 'Xe': return 54
        if symbol == 'Cs': return 55
        if symbol == 'Ba': return 56
        if symbol == 'La': return 57
        if symbol == 'Ce': return 58
        if symbol == 'Pr': return 59
        if symbol == 'Nd': return 60
        if symbol == 'Pm': return 61
        if symbol == 'Sm': return 62
        if symbol == 'Eu': return 63
        if symbol == 'Gd': return 64
        if symbol == 'Tb': return 65
        if symbol == 'Dy': return 66
        if symbol == 'Ho': return 67
        if symbol == 'Er': return 68
        if symbol == 'Tm': return 69
        if symbol == 'Yb': return 70
        if symbol == 'Lu': return 71
        if symbol == 'Hf': return 72
        if symbol == 'Ta': return 73
        if symbol == 'W': return 74
        if symbol == 'Re': return 75
        if symbol == 'Os': return 76
        if symbol == 'Ir': return 77
        if symbol == 'Pt': return 78
        if symbol == 'Au': return 79
        if symbol == 'Hg': return 80
        if symbol == 'Tl': return 81
        if symbol == 'Pb': return 82
        if symbol == 'Bi': return 83
        if symbol == 'Po': return 84
        if symbol == 'At': return 85
        if symbol == 'Rn': return 86
        if symbol == 'Fr': return 87
        if symbol == 'Ra': return 88
        if symbol == 'Ac': return 89
        if symbol == 'Th': return 90
        if symbol == 'Pa': return 91
        if symbol == 'U': return 92
        if symbol == 'Np': return 93
        if symbol == 'Pu': return 94
        if symbol == 'Am': return 95
        if symbol == 'Cm': return 96
        if symbol == 'Bk': return 97
        if symbol == 'Cf': return 98
        if symbol == 'Es': return 99
        if symbol == 'Fm': return 100
        if symbol == 'Md': return 101
        if symbol == 'No': return 102
        if symbol == 'Lr': return 103
        if symbol == 'Rf': return 104
        if symbol == 'Db': return 105
        if symbol == 'Sg': return 106
        if symbol == 'Bh': return 107
        if symbol == 'Hs': return 108
        if symbol == 'Mt': return 109
        if symbol == 'Ds': return 110
        if symbol == 'Rg': return 111
        if symbol == 'Cn': return 112
        if symbol == 'Nh': return 113
        if symbol == 'Fl': return 114
        if symbol == 'Mc': return 115
        if symbol == 'Lv': return 116
        if symbol == 'Ts': return 117
        if symbol == 'Og': return 118
        return ('proton number for ' + symbol + ' not found')

def all_natural_elements_symbols():
        return ['Sn', 'Xe', 'Cd', 'Te', 'Ba', 'Dy', 'Gd', 'Hg', 'Mo', 'Nd', 'Os', 'Ru', 'Sm', 'Yb', 'Ca', 'Er', 'Hf',
                'Kr', 'Pd', 'Pt', 'Se', 'Ge', 'Ni', 'Ti', 'W', 'Zn', 'Zr', 'Ce', 'Cr', 'Fe', 'Pb', 'S', 'Sr', 'Ar', 'C',
                'K', 'Mg', 'Ne', 'Si', 'U', 'Ag', 'B', 'Br', 'Cl', 'Cu', 'Eu', 'Ga', 'H', 'He', 'In', 'Ir', 'La', 'Li',
                'Lu', 'N', 'Rb', 'Re', 'Sb', 'Ta', 'Tl', 'V', 'Be', 'O', 'F', 'Na', 'Al', 'P', 'Sc', 'Mn', 'Co', 'As',
                'Y', 'Nb', 'Rh', 'I', 'Cs', 'Pr', 'Tb', 'Ho', 'Tm', 'Au', 'Bi', 'Th', 'Pa']

def all_natural_elements():
        from neutronics_material_MAKER.element import Element
        return [Element(e) for e in all_natural_elements_symbols()]
# =============================================================================
#         return [Element('Sn'), Element('Xe'), Element('Cd'), Element('Te'), Element('Ba'), Element('Dy'),
#                 Element('Gd'), Element('Hg'), Element('Mo'), Element('Nd'), Element('Os'), Element('Ru'),
#                 Element('Sm'), Element('Yb'), Element('Ca'), Element('Er'), Element('Hf'), Element('Kr'),
#                 Element('Pd'), Element('Pt'), Element('Se'), Element('Ge'), Element('Ni'), Element('Ti'),
#                 Element('W'), Element('Zn'), Element('Zr'), Element('Ce'), Element('Cr'), Element('Fe'),
#                 Element('Pb'), Element('S'), Element('Sr'), Element('Ar'), Element('C'), Element('K'),
#                 Element('Mg'), Element('Ne'), Element('Si'), Element('U'), Element('Ag'), Element('B'),
#                 Element('Br'), Element('Cl'), Element('Cu'), Element('Eu'), Element('Ga'), Element('H'),
#                 Element('He'), Element('In'), Element('Ir'), Element('La'), Element('Li'), Element('Lu'),
#                 Element('N'), Element('Rb'), Element('Re'), Element('Sb'), Element('Ta'), Element('Tl'),
#                 Element('V'), Element('Be'), Element('O'), Element('F'), Element('Na'), Element('Al'),
#                 Element('P'), Element('Sc'), Element('Mn'), Element('Co'), Element('As'), Element('Y'),
#                 Element('Nb'), Element('Rh'), Element('I'), Element('Cs'), Element('Pr'), Element('Tb'),
#                 Element('Ho'), Element('Tm'), Element('Au'), Element('Bi'), Element('Th'), Element('Pa')]
# =============================================================================

def all_natural_isotopes():
    from neutronics_material_MAKER.element import Element
    from neutronics_material_MAKER.isotope import Isotope
    isotope_list=[]
    for element in all_natural_elements():
        isotope_list= isotope_list+natural_isotopes_in_elements(element.symbol)
    return isotope_list
