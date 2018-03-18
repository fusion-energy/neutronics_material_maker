import re
import sys
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Isotope:
    def __init__(self,*args,**kwargs):

        self.symbol = kwargs.get('symbol')
        self.protons = kwargs.get('protons')
        self.atomic_number = kwargs.get('atomic_number')

        atomic_number_or_proton_number=[]
        for arg in args:
            if isinstance(arg,str) and self.symbol == None:
                self.symbol=arg
                self.find_protons_from_symbol(self.symbol)
            if isinstance(arg,int):
                atomic_number_or_proton_number.append(arg)

        if self.atomic_number == None and len(atomic_number_or_proton_number)>=1:
            self.atomic_number = max(atomic_number_or_proton_number)

        if self.protons == None and len(atomic_number_or_proton_number)==2:
            self.protons = min(atomic_number_or_proton_number)

        self.classname = self.__class__.__name__

        if self.atomic_number == None:
            raise ValueError('To create an Isotope provide an atomic_number ')

        if self.protons == None and self.symbol == None: 
            raise ValueError("To create an Isotope provide either protons or symbol please")

        if self.symbol ==None:
            self.symbol = self.find_symbol_from_protons(self.protons)

        if self.protons ==None:
            self.protons = self.find_protons_from_symbol(self.symbol) 

        self.element_name = self.find_element_name(self.symbol)
        self.name = self.element_name +'_'+ str(self.atomic_number)
        self.material_card_name = kwargs.get('material_card_name')
        if self.material_card_name == None:
            self.material_card_name = self.name

        self.mass_amu = self.find_mass_amu(self.symbol,self.atomic_number)

        self.natural_abundance = self.find_natural_abundance(self.symbol,self.atomic_number)

        self.abundance = kwargs.get('abundance',self.natural_abundance)

        if self.abundance != None and self.abundance > 1.0 or self.abundance < 0.0:
            raise ValueError('abundance of isotope can not be greater than 1.0 or less than 0')

        self.zaid = str(self.protons) + str(self.atomic_number).zfill(3)

        self.neutrons = self.atomic_number - self.protons

        self.xsdir = kwargs.get('xsdir','/opt/serpent2/xsdir.serp')

        self.nuclear_library = kwargs.get('nuclear_library',self.find_prefered_library(self.zaid,self.xsdir))

        self.nuclear_library_file = self.find_prefered_library_file(self.zaid,self.xsdir)

        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')

        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.color = kwargs.get('color')

    def find_natural_abundance(self,symbol,atomic_number):
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

    def find_symbol_from_protons(self,protons):
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

    def find_protons_from_symbol(self,symbol):
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

    def find_element_name(self,symbol):  # returns full element name
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

    def find_mass_amu(self,symbol,atomic_number):
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
            return None

    def find_prefered_library(self,zaid,xsdir):
        xsdir_contents = open(xsdir, "r").readlines() 
        for line in xsdir_contents:
            choped_up_line = line.split()[0].split('.')
            if choped_up_line[0] == zaid:
                return '.'+choped_up_line[1]
        return ''

    def find_prefered_library_file(self,zaid,xsdir):
        xsdir_contents = open(xsdir, "r").readlines() 
        for line in xsdir_contents:
            choped_up_line = line.split()

            if choped_up_line[0].split('.')[0] == zaid:
                #print('line = ',choped_up_line[-1])
                return choped_up_line[-1]
        return ''        

    def serpent_material_card(self):

        if self.density_g_per_cm3 == None and self.density_atoms_per_barn_per_cm == None:
            raise ValueError(
                "To produce a serpent material card the density_g_per_cm3 or density_atoms_per_barn_per_cm must be provided")

        if self.density_g_per_cm3 == None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  ' + str(self.density_g_per_cm3*self.packing_fraction)

        if self.color == None:

            color = ''

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")

        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)])

        mat_card = 'mat ' + self.material_card_name + density + color + ' \n'

        mat_card = mat_card+ '   '+(self.zaid + self.nuclear_library).ljust(11)+ ' 1'.ljust(22)+' % ' +self.name +'\n'

        return mat_card        

class Natural_Isotopes():
    def __init__(self,**kwargs):
             
        self.all_natural_isotopes = self.find_all_natural_isotopes()

        #self.natural_isotopes = self.find_natural_isotopes_from_symbol(self.symbol)

    def find_all_natural_isotopes(self):
        all_isotopes = []
        for element in Natural_Elements().all_natural_elements:

            isotopes_in_element = element.isotopes
            
            all_isotopes= all_isotopes +isotopes_in_element

        return all_isotopes
            #self.find_natural_isotopes_from_symbol(element.symbol) for element in ]

class Natural_Elements():
    def __init__(self,**kwargs):

        self.all_natural_elements = self.find_all_natural_elements()

    def find_all_natural_elements(self):
        return [Element(symbol='Sn'),
                Element(symbol='Xe'),
                Element(symbol='Cd'),
                Element(symbol='Te'),
                Element(symbol='Ba'),
                Element(symbol='Dy'),
                Element(symbol='Gd'),
                Element(symbol='Hg'),
                Element(symbol='Mo'),
                Element(symbol='Nd'),
                Element(symbol='Os'),
                Element(symbol='Ru'),
                Element(symbol='Sm'),
                Element(symbol='Yb'),
                Element(symbol='Ca'),
                Element(symbol='Er'),
                Element(symbol='Hf'),
                Element(symbol='Kr'),
                Element(symbol='Pd'),
                Element(symbol='Pt'),
                Element(symbol='Se'),
                Element(symbol='Ge'),
                Element(symbol='Ni'),
                Element(symbol='Ti'),
                Element(symbol='W'),
                Element(symbol='Zn'),
                Element(symbol='Zr'),
                Element(symbol='Ce'),
                Element(symbol='Cr'),
                Element(symbol='Fe'),
                Element(symbol='Pb'),
                Element(symbol='S'),
                Element(symbol='Sr'),
                Element(symbol='Ar'),
                Element(symbol='C'),
                Element(symbol='K'),
                Element(symbol='Mg'),
                Element(symbol='Ne'),
                Element(symbol='Si'),
                Element(symbol='U'),
                Element(symbol='Ag'),
                Element(symbol='B'),
                Element(symbol='Br'),
                Element(symbol='Cl'),
                Element(symbol='Cu'),
                Element(symbol='Eu'),
                Element(symbol='Ga'),
                Element(symbol='H'),
                Element(symbol='He'),
                Element(symbol='In'),
                Element(symbol='Ir'),
                Element(symbol='La'),
                Element(symbol='Li'),
                Element(symbol='Lu'),
                Element(symbol='N'),
                Element(symbol='Rb'),
                Element(symbol='Re'),
                Element(symbol='Sb'),
                Element(symbol='Ta'),
                Element(symbol='Tl'),
                Element(symbol='V'),
                Element(symbol='Be'),
                Element(symbol='O'),
                Element(symbol='F'),
                Element(symbol='Na'),
                Element(symbol='Al'),
                Element(symbol='P'),
                Element(symbol='Sc'),
                Element(symbol='Mn'),
                Element(symbol='Co'),
                Element(symbol='As'),
                Element(symbol='Y'),
                Element(symbol='Nb'),
                Element(symbol='Rh'),
                Element(symbol='I'),
                Element(symbol='Cs'),
                Element(symbol='Pr'),
                Element(symbol='Tb'),
                Element(symbol='Ho'),
                Element(symbol='Tm'),
                Element(symbol='Au'),
                Element(symbol='Bi'),
                Element(symbol='Th'),
                Element(symbol='Pa')
                ]        

class Element(Isotope):
    def __init__(self,*args,**kwargs):

        if len(args)==1:
            protons_or_symbol=args[0]

        self.classname = self.__class__.__name__

        self.symbol = kwargs.get('symbol')

        self.protons = kwargs.get('protons')

        if self.protons == None and self.symbol == None:
            if isinstance(protons_or_symbol,int):
                self.protons=protons_or_symbol

            elif isinstance(protons_or_symbol,str):
                self.symbol = protons_or_symbol

        if self.symbol ==None:
            self.symbol = self.find_symbol_from_protons(self.protons)
        if self.protons ==None:
            self.protons = self.find_protons_from_symbol(self.symbol)

        self.isotopes = kwargs.get('enriched_isotopes')
        if self.isotopes == None :
            self.isotopes = self.find_natural_isotopes_in_element_from_symbol(self.symbol)#looks at natural abundances
        else:
            self.isotopes = self.check_enriched_isotopes_in_element()

        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.material_card_name = kwargs.get('material_card_name')
        if self.material_card_name == None:

            self.material_card_name = self.find_element_name(self.symbol)

        self.molar_mass_g = self.find_molar_mass_g()

        self.color = kwargs.get('color')

    def check_enriched_isotopes_in_element(self):
        cumlative_abundance = 0
        for isotope in self.isotopes:

            cumlative_abundance = cumlative_abundance + isotope.abundance
            if isotope.symbol != self.symbol:
                raise ValueError(
                    'When creating and Element and specifying Isotopes present they must be isotops of that element')
        if cumlative_abundance != 1.0:
            raise ValueError(
                'When creating and Element and specifying Isotopes present within an Element their abundance must sum to 1.0')
        return self.isotopes

    def find_natural_isotopes_in_element_from_symbol(self,symbol):
        
        if symbol == 'Sn': return [Isotope(symbol=symbol , atomic_number = 112), 
                                   Isotope(symbol=symbol , atomic_number = 114), 
                                   Isotope(symbol=symbol , atomic_number = 115),
                                   Isotope(symbol=symbol , atomic_number = 116), 
                                   Isotope(symbol=symbol , atomic_number = 117),
                                   Isotope(symbol=symbol , atomic_number = 118), 
                                   Isotope(symbol=symbol , atomic_number = 119), 
                                   Isotope(symbol=symbol , atomic_number = 120),
                                   Isotope(symbol=symbol , atomic_number = 122), 
                                   Isotope(symbol=symbol , atomic_number = 124)]
        if symbol == 'Xe': return [Isotope(symbol=symbol , atomic_number = 124), 
                                   Isotope(symbol=symbol , atomic_number = 126), 
                                   Isotope(symbol=symbol , atomic_number = 128),
                                   Isotope(symbol=symbol , atomic_number = 129), 
                                   Isotope(symbol=symbol , atomic_number = 130),
                                   Isotope(symbol=symbol , atomic_number = 131), 
                                   Isotope(symbol=symbol , atomic_number = 132), 
                                   Isotope(symbol=symbol , atomic_number = 134),
                                   Isotope(symbol=symbol , atomic_number = 136)]
        if symbol == 'Cd': return [Isotope(symbol=symbol , atomic_number = 106), 
                                   Isotope(symbol=symbol , atomic_number = 108), 
                                   Isotope(symbol=symbol , atomic_number = 110),
                                   Isotope(symbol=symbol , atomic_number = 111), 
                                   Isotope(symbol=symbol , atomic_number = 112),
                                   Isotope(symbol=symbol , atomic_number = 113),
                                   Isotope(symbol=symbol , atomic_number = 114), 
                                   Isotope(symbol=symbol , atomic_number = 116)]
        if symbol == 'Te': return [Isotope(symbol=symbol , atomic_number = 120), 
                                   Isotope(symbol=symbol , atomic_number = 122), 
                                   Isotope(symbol=symbol , atomic_number = 123),
                                        Isotope(symbol=symbol , atomic_number = 124), 
                                        Isotope(symbol=symbol , atomic_number = 125), 
                                        Isotope(symbol=symbol , atomic_number = 126),
                                        Isotope(symbol=symbol , atomic_number = 128), 
                                        Isotope(symbol=symbol , atomic_number = 130)]
        if symbol == 'Ba': return [Isotope(symbol=symbol , atomic_number = 130), 
                                   Isotope(symbol=symbol , atomic_number = 132), 
                                   Isotope(symbol=symbol , atomic_number = 134),
                                        Isotope(symbol=symbol , atomic_number = 135), 
                                        Isotope(symbol=symbol , atomic_number = 136), 
                                        Isotope(symbol=symbol , atomic_number = 137),
                                        Isotope(symbol=symbol , atomic_number = 138)]
        if symbol == 'Dy': return [Isotope(symbol=symbol , atomic_number = 156), 
                                   Isotope(symbol=symbol , atomic_number = 158), 
                                   Isotope(symbol=symbol , atomic_number = 160),
                                        Isotope(symbol=symbol , atomic_number = 161), 
                                        Isotope(symbol=symbol , atomic_number = 162), 
                                        Isotope(symbol=symbol , atomic_number = 163),
                                        Isotope(symbol=symbol , atomic_number = 164)]
        if symbol == 'Gd': return [Isotope(symbol=symbol , atomic_number = 152), 
                                   Isotope(symbol=symbol , atomic_number = 154), 
                                   Isotope(symbol=symbol , atomic_number = 155),
                                        Isotope(symbol=symbol , atomic_number = 156), 
                                        Isotope(symbol=symbol , atomic_number = 157), 
                                        Isotope(symbol=symbol , atomic_number = 158),
                                        Isotope(symbol=symbol , atomic_number = 160)]
        if symbol == 'Hg': return [Isotope(symbol=symbol , atomic_number = 196), 
                                   Isotope(symbol=symbol , atomic_number = 198), 
                                        Isotope(symbol=symbol , atomic_number = 199),
                                        Isotope(symbol=symbol , atomic_number = 200), 
                                        Isotope(symbol=symbol , atomic_number = 201), 
                                        Isotope(symbol=symbol , atomic_number = 202),
                                        Isotope(symbol=symbol , atomic_number = 204)]
        if symbol == 'Mo': return [Isotope(symbol=symbol , atomic_number = 92), Isotope(symbol=symbol , atomic_number = 94), Isotope(symbol=symbol , atomic_number = 95),
                                        Isotope(symbol=symbol , atomic_number = 96), Isotope(symbol=symbol , atomic_number = 97), Isotope(symbol=symbol , atomic_number = 98),
                                        Isotope(symbol=symbol , atomic_number = 100)]
        if symbol == 'Nd': return [Isotope(symbol=symbol , atomic_number = 142), Isotope(symbol=symbol , atomic_number = 143), Isotope(symbol=symbol , atomic_number = 144),
                                        Isotope(symbol=symbol , atomic_number = 145), Isotope(symbol=symbol , atomic_number = 146), Isotope(symbol=symbol , atomic_number = 148),
                                        Isotope(symbol=symbol , atomic_number = 150)]
        if symbol == 'Os': return [Isotope(symbol=symbol , atomic_number = 184), Isotope(symbol=symbol , atomic_number = 186), Isotope(symbol=symbol , atomic_number = 187),
                                        Isotope(symbol=symbol , atomic_number = 188), Isotope(symbol=symbol , atomic_number = 189), Isotope(symbol=symbol , atomic_number = 190),
                                        Isotope(symbol=symbol , atomic_number = 192)]
        if symbol == 'Ru': return [Isotope(symbol=symbol , atomic_number = 96), Isotope(symbol=symbol , atomic_number = 98), Isotope(symbol=symbol , atomic_number = 99),
                                        Isotope(symbol=symbol , atomic_number = 100), Isotope(symbol=symbol , atomic_number = 101),
                                        Isotope(symbol=symbol , atomic_number = 102), Isotope(symbol=symbol , atomic_number = 104)]
        if symbol == 'Sm': return [Isotope(symbol=symbol , atomic_number = 144), Isotope(symbol=symbol , atomic_number = 147), Isotope(symbol=symbol , atomic_number = 148),
                                        Isotope(symbol=symbol , atomic_number = 149), Isotope(symbol=symbol , atomic_number = 150),
                                        Isotope(symbol=symbol , atomic_number = 152), Isotope(symbol=symbol , atomic_number = 154)]
        if symbol == 'Yb': return [Isotope(symbol=symbol , atomic_number = 168), Isotope(symbol=symbol , atomic_number = 170), Isotope(symbol=symbol , atomic_number = 171),
                                        Isotope(symbol=symbol , atomic_number = 172), Isotope(symbol=symbol , atomic_number = 173),
                                        Isotope(symbol=symbol , atomic_number = 174), Isotope(symbol=symbol , atomic_number = 176)]
        if symbol == 'Ca': return [Isotope(symbol=symbol , atomic_number = 40), Isotope(symbol=symbol , atomic_number = 42), Isotope(symbol=symbol , atomic_number = 43),
                                        Isotope(symbol=symbol , atomic_number = 44), Isotope(symbol=symbol , atomic_number = 46), Isotope(symbol=symbol , atomic_number = 48)]
        if symbol == 'Er': return [Isotope(symbol=symbol , atomic_number = 162), Isotope(symbol=symbol , atomic_number = 164), Isotope(symbol=symbol , atomic_number = 166),
                                        Isotope(symbol=symbol , atomic_number = 167), Isotope(symbol=symbol , atomic_number = 168), Isotope(symbol=symbol , atomic_number = 170)]
        if symbol == 'Hf': return [Isotope(symbol=symbol , atomic_number = 174), Isotope(symbol=symbol , atomic_number = 176), Isotope(symbol=symbol , atomic_number = 177),
                                        Isotope(symbol=symbol , atomic_number = 178), Isotope(symbol=symbol , atomic_number = 179), Isotope(symbol=symbol , atomic_number = 180)]
        if symbol == 'Kr': return [Isotope(symbol=symbol , atomic_number = 78), Isotope(symbol=symbol , atomic_number = 80), Isotope(symbol=symbol , atomic_number = 82),
                                        Isotope(symbol=symbol , atomic_number = 83), Isotope(symbol=symbol , atomic_number = 84), Isotope(symbol=symbol , atomic_number = 86)]
        if symbol == 'Pd': return [Isotope(symbol=symbol , atomic_number = 102), Isotope(symbol=symbol , atomic_number = 104), Isotope(symbol=symbol , atomic_number = 105),
                                        Isotope(symbol=symbol , atomic_number = 106), Isotope(symbol=symbol , atomic_number = 108), Isotope(symbol=symbol , atomic_number = 110)]
        if symbol == 'Pt': return [Isotope(symbol=symbol , atomic_number = 190), Isotope(symbol=symbol , atomic_number = 192), Isotope(symbol=symbol , atomic_number = 194),
                                        Isotope(symbol=symbol , atomic_number = 195), Isotope(symbol=symbol , atomic_number = 196), Isotope(symbol=symbol , atomic_number = 198)]
        if symbol == 'Se': return [Isotope(symbol=symbol , atomic_number = 74), Isotope(symbol=symbol , atomic_number = 76), Isotope(symbol=symbol , atomic_number = 77),
                                        Isotope(symbol=symbol , atomic_number = 78), Isotope(symbol=symbol , atomic_number = 80), Isotope(symbol=symbol , atomic_number = 82)]
        if symbol == 'Ge': return [Isotope(symbol=symbol , atomic_number = 70), Isotope(symbol=symbol , atomic_number = 72), Isotope(symbol=symbol , atomic_number = 73),
                                        Isotope(symbol=symbol , atomic_number = 74), Isotope(symbol=symbol , atomic_number = 76)]
        if symbol == 'Ni': return [Isotope(symbol=symbol , atomic_number = 58), Isotope(symbol=symbol , atomic_number = 60), Isotope(symbol=symbol , atomic_number = 61),
                                        Isotope(symbol=symbol , atomic_number = 62), Isotope(symbol=symbol , atomic_number = 64)]
        if symbol == 'Ti': return [Isotope(symbol=symbol , atomic_number = 46), Isotope(symbol=symbol , atomic_number = 47), Isotope(symbol=symbol , atomic_number = 48),
                                        Isotope(symbol=symbol , atomic_number = 49), Isotope(symbol=symbol , atomic_number = 50)]
        if symbol == 'W': return [Isotope(symbol=symbol , atomic_number = 180), Isotope(symbol=symbol , atomic_number = 182), Isotope(symbol=symbol , atomic_number = 183),
                                       Isotope(symbol=symbol , atomic_number = 184), Isotope(symbol=symbol , atomic_number = 186)]
        if symbol == 'Zn': return [Isotope(symbol=symbol , atomic_number = 64), Isotope(symbol=symbol , atomic_number = 66), Isotope(symbol=symbol , atomic_number = 67),
                                        Isotope(symbol=symbol , atomic_number = 68), Isotope(symbol=symbol , atomic_number = 70)]
        if symbol == 'Zr': return [Isotope(symbol=symbol , atomic_number = 90), Isotope(symbol=symbol , atomic_number = 91), Isotope(symbol=symbol , atomic_number = 92),
                                        Isotope(symbol=symbol , atomic_number = 94), Isotope(symbol=symbol , atomic_number = 96)]
        if symbol == 'Ce': return [Isotope(symbol=symbol , atomic_number = 136), Isotope(symbol=symbol , atomic_number = 138), Isotope(symbol=symbol , atomic_number = 140),
                                        Isotope(symbol=symbol , atomic_number = 142)]
        if symbol == 'Cr': return [Isotope(symbol=symbol , atomic_number = 50), Isotope(symbol=symbol , atomic_number = 52), Isotope(symbol=symbol , atomic_number = 53),
                                        Isotope(symbol=symbol , atomic_number = 54)]
        if symbol == 'Fe': return [Isotope(symbol=symbol , atomic_number = 54), Isotope(symbol=symbol , atomic_number = 56), Isotope(symbol=symbol , atomic_number = 57),
                                        Isotope(symbol=symbol , atomic_number = 58)]
        if symbol == 'Pb': return [Isotope(symbol=symbol , atomic_number = 204), Isotope(symbol=symbol , atomic_number = 206), Isotope(symbol=symbol , atomic_number = 207),
                                        Isotope(symbol=symbol , atomic_number = 208)]
        if symbol == 'S': return [Isotope(symbol=symbol , atomic_number = 32), Isotope(symbol=symbol , atomic_number = 33), Isotope(symbol=symbol , atomic_number = 34),
                                       Isotope(symbol=symbol , atomic_number = 36)]
        if symbol == 'Sr': return [Isotope(symbol=symbol , atomic_number = 84), Isotope(symbol=symbol , atomic_number = 86), Isotope(symbol=symbol , atomic_number = 87),
                                        Isotope(symbol=symbol , atomic_number = 88)]
        if symbol == 'Ar': return [Isotope(symbol=symbol , atomic_number = 36), Isotope(symbol=symbol , atomic_number = 38), Isotope(symbol=symbol , atomic_number = 40)]
        if symbol == 'C': return [Isotope(symbol=symbol , atomic_number = 12), Isotope(symbol=symbol , atomic_number = 13)]#, Isotope(symbol=symbol , atomic_number = 14)]
        if symbol == 'K': return [Isotope(symbol=symbol , atomic_number = 39), Isotope(symbol=symbol , atomic_number = 40), Isotope(symbol=symbol , atomic_number = 41)]
        if symbol == 'Mg': return [Isotope(symbol=symbol , atomic_number = 24), Isotope(symbol=symbol , atomic_number = 25), Isotope(symbol=symbol , atomic_number = 26)]
        if symbol == 'Ne': return [Isotope(symbol=symbol , atomic_number = 20), Isotope(symbol=symbol , atomic_number = 21), Isotope(symbol=symbol , atomic_number = 22)]
        if symbol == 'Si': return [Isotope(symbol=symbol , atomic_number = 28), Isotope(symbol=symbol , atomic_number = 29), Isotope(symbol=symbol , atomic_number = 30)]
        if symbol == 'U': return [Isotope(symbol=symbol , atomic_number = 234), Isotope(symbol=symbol , atomic_number = 235), Isotope(symbol=symbol , atomic_number = 238)]
        if symbol == 'Ag': return [Isotope(symbol=symbol , atomic_number = 107), Isotope(symbol=symbol , atomic_number = 109)]
        if symbol == 'B': return [Isotope(symbol=symbol , atomic_number = 10), Isotope(symbol=symbol , atomic_number = 11)]
        if symbol == 'Br': return [Isotope(symbol=symbol , atomic_number = 79), Isotope(symbol=symbol , atomic_number = 81)]
        if symbol == 'Cl': return [Isotope(symbol=symbol , atomic_number = 35), Isotope(symbol=symbol , atomic_number = 37)]
        if symbol == 'Cu': return [Isotope(symbol=symbol , atomic_number = 63), Isotope(symbol=symbol , atomic_number = 65)]
        if symbol == 'Eu': return [Isotope(symbol=symbol , atomic_number = 151), Isotope(symbol=symbol , atomic_number = 153)]
        if symbol == 'Ga': return [Isotope(symbol=symbol , atomic_number = 69), Isotope(symbol=symbol , atomic_number = 71)]
        if symbol == 'H':  return [Isotope(symbol=symbol , atomic_number = 1), Isotope(symbol=symbol , atomic_number = 2)]
        if symbol == 'He': return [Isotope(symbol=symbol , atomic_number = 3), Isotope(symbol=symbol , atomic_number = 4)]
        if symbol == 'In': return [Isotope(symbol=symbol , atomic_number = 113), Isotope(symbol=symbol , atomic_number = 115)]
        if symbol == 'Ir': return [Isotope(symbol=symbol , atomic_number = 191), Isotope(symbol=symbol , atomic_number = 193)]
        if symbol == 'La': return [Isotope(symbol=symbol , atomic_number = 138), Isotope(symbol=symbol , atomic_number = 139)]
        if symbol == 'Li': return [Isotope(symbol=symbol , atomic_number = 6), Isotope(symbol=symbol , atomic_number = 7)]
        if symbol == 'Lu': return [Isotope(symbol=symbol , atomic_number = 175), Isotope(symbol=symbol , atomic_number = 176)]
        if symbol == 'N':  return [Isotope(symbol=symbol , atomic_number = 14), Isotope(symbol=symbol , atomic_number = 15)]
        if symbol == 'Rb': return [Isotope(symbol=symbol , atomic_number = 85), Isotope(symbol=symbol , atomic_number = 87)]
        if symbol == 'Re': return [Isotope(symbol=symbol , atomic_number = 185), Isotope(symbol=symbol , atomic_number = 187)]
        if symbol == 'Sb': return [Isotope(symbol=symbol , atomic_number = 121), Isotope(symbol=symbol , atomic_number = 123)]
        if symbol == 'Ta': return [Isotope(symbol=symbol , atomic_number = 180), Isotope(symbol=symbol , atomic_number = 181)]
        if symbol == 'Tl': return [Isotope(symbol=symbol , atomic_number = 203), Isotope(symbol=symbol , atomic_number = 205)]
        if symbol == 'V':  return [Isotope(symbol=symbol , atomic_number = 50), Isotope(symbol=symbol , atomic_number = 51)]
        if symbol == 'Be': return [Isotope(symbol=symbol , atomic_number = 9)]
        if symbol == 'O':  return [Isotope(symbol=symbol , atomic_number = 16),Isotope(symbol=symbol , atomic_number = 17),Isotope(symbol=symbol , atomic_number = 18)]
        if symbol == 'F':  return [Isotope(symbol=symbol , atomic_number = 19)]
        if symbol == 'Na': return [Isotope(symbol=symbol , atomic_number = 23)]
        if symbol == 'Al': return [Isotope(symbol=symbol , atomic_number =27)]
        if symbol == 'P':  return [Isotope(symbol=symbol , atomic_number = 31)]
        if symbol == 'Sc': return [Isotope(symbol=symbol , atomic_number = 45)]
        if symbol == 'Mn': return [Isotope(symbol=symbol , atomic_number = 55)]
        if symbol == 'Co': return [Isotope(symbol=symbol , atomic_number = 59)]
        if symbol == 'As': return [Isotope(symbol=symbol , atomic_number = 75)]
        if symbol == 'Y':  return [Isotope(symbol=symbol , atomic_number = 89)]
        if symbol == 'Nb': return [Isotope(symbol=symbol , atomic_number = 93)]
        if symbol == 'Rh': return [Isotope(symbol=symbol , atomic_number = 103)]
        if symbol == 'I':  return [Isotope(symbol=symbol , atomic_number = 127)]
        if symbol == 'Cs': return [Isotope(symbol=symbol , atomic_number = 133)]
        if symbol == 'Pr': return [Isotope(symbol=symbol , atomic_number = 141)]
        if symbol == 'Tb': return [Isotope(symbol=symbol , atomic_number = 159)]
        if symbol == 'Ho': return [Isotope(symbol=symbol , atomic_number = 165)]
        if symbol == 'Tm': return [Isotope(symbol=symbol , atomic_number = 169)]
        if symbol == 'Au': return [Isotope(symbol=symbol , atomic_number = 197)]
        if symbol == 'Bi': return [Isotope(symbol=symbol , atomic_number = 209)]
        if symbol == 'Th': return [Isotope(symbol=symbol , atomic_number = 232)]
        if symbol == 'Pa': return [Isotope(symbol=symbol , atomic_number = 231)]

        else:
            raise ValueError('natural composition of isotope not found for ', symbol)

    def find_molar_mass_g(self):
        element_mass = 0
        for isotope in self.isotopes:
            element_mass = element_mass + isotope.abundance * isotope.mass_amu
        return element_mass

    def serpent_material_card(self):

        if self.density_g_per_cm3 == None and self.density_atoms_per_barn_per_cm == None:

            raise ValueError("To produce a serpent material card the density_g_per_cm3 or density_atoms_per_barn_per_cm must be provided")

        if self.density_g_per_cm3 == None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  ' + str(self.density_g_per_cm3*self.packing_fraction)

        if self.color == None:

            color=''

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")
            
        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)]) 

        mat_card = 'mat ' +self.material_card_name  + density +color +' \n'

        for isotope in self.isotopes:

            mat_card = mat_card+ '   '+(isotope.zaid + isotope.nuclear_library).ljust(11)+ ' '+ str(isotope.abundance).ljust(22)+' % ' +isotope.material_card_name +'\n'

        return mat_card

class Material():
    def __init__(self,**kwargs):
        self.classname = self.__class__.__name__
        self.elements = kwargs.get('elements')
        self.atom_fractions = kwargs.get('atom_fractions')
        self.mass_fractions = kwargs.get('mass_fractions')
        self.description = kwargs.get('description')

        self.material_card_name = kwargs.get('material_card_name',self.description)

        if self.elements == None:
            print('A list of elements present within the material must be specified')
            sys.exit()

        if self.atom_fractions == None and self.mass_fractions == None:
            print('To make a material either atom_fractions or mass_fractions must be provided')
            sys.exit()

        if self.atom_fractions == None:
            self.atom_fractions  = self.find_atom_fractions_from_mass_fractions()
                
        if self.mass_fractions == None:
            self.mass_fractions = self.find_mass_fractions_from_atom_fractions()

        if len(self.elements)!=len(self.atom_fractions):
            print('When making a material please provide the same number of elements and atom/mass fractions')
            sys.exit()

        #if self.isotopes == None:
        self.isotopes = []
        for element in self.elements:
            for isotope in element.isotopes:
                self.isotopes.append(isotope)

        self.isotope_fractions =[]
        for element, atom_fraction in zip(self.elements,self.atom_fractions):
            for isotope in element.isotopes:
                self.isotope_fractions.append(atom_fraction*isotope.abundance)


        self.packing_fraction=kwargs.get('packing_fraction',1.0)

        self.density_g_per_cm3 = kwargs.get('density_g_per_cm3')
        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        self.color = kwargs.get('color')

    def find_atom_fractions_from_mass_fractions(self):
        list_of_atom_fractions =[]
        for mass_fraction, element in zip(self.mass_fractions,self.elements):
            list_of_atom_fractions.append(mass_fraction/element.molar_mass_g )
        return list_of_atom_fractions

    def find_mass_fractions_from_atom_fractions(self):
        list_of_mass_fractions =[]
        for atom_fraction, element in zip(self.atom_fractions,self.elements):
            list_of_mass_fractions.append(atom_fraction*element.molar_mass_g )
        return list_of_mass_fractions

    def serpent_material_card(self):
        if self.material_card_name == None:
            print('material_card_name must be provided when making a serpent_material_card from a material')
            sys.exit()

        if self.density_g_per_cm3 == None and self.density_atoms_per_barn_per_cm == None:

            raise ValueError("To produce a serpent material card the density_g_per_cm3 or density_atoms_per_barn_per_cm must be provided")

        if self.density_g_per_cm3 == None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  ' + str(self.density_g_per_cm3*self.packing_fraction)

        if self.color == None:

            mat_card = 'mat ' +self.material_card_name  + ' -' +str(self.density_g_per_cm3) +' \n'

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")
            
        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)]) 

            mat_card = 'mat ' +self.material_card_name  + density +color +' \n'

        for isotope, isotope_fraction in zip(self.isotopes, self.isotope_fractions):
            #mat_card = mat_card+ isotope.zaid +' ' +str(isotope_fraction)+'\n'
            mat_card = mat_card+ '   '+(isotope.zaid + isotope.nuclear_library).ljust(11)+ ' '+ str(isotope_fraction).ljust(22)+' % ' +isotope.name +'\n'
        return mat_card

class Compound():
    def __init__(self,chemical_equation,**kwargs):
        self.classname = self.__class__.__name__

        self.chemical_equation = chemical_equation

        self.fractions_coefficients= self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)

        self.enriched_isotopes=kwargs.get('enriched_isotopes')

        self.elements = self.find_elements_in_chemical_equation(chemical_equation)

        self.atom_fractions = self.get_atom_fractions_from_chemical_equations(chemical_equation)

        self.isotopes= self.find_isotopes_in_chemical_equation()

        self.isotope_fractions = self.find_isotope_fractions_in_chemical_equation()

        self.state_of_matter=kwargs.get('state_of_matter','solid')

        self.molar_mass = self.find_molar_mass()

        self.average_atom_mass = self.find_average_atom_mass()

        self.volume_of_unit_cell_cm3=kwargs.get('volume_of_unit_cell_cm3')

        self.atoms_per_unit_cell = kwargs.get('atoms_per_unit_cell')

        self.temperature_K=kwargs.get('temperature_K')

        self.pressure_Pa=kwargs.get('pressure_Pa')

        self.density_g_per_cm3=kwargs.get('density_g_per_cm3')

        self.density_atoms_per_barn_per_cm = kwargs.get('density_atoms_per_barn_per_cm')

        if self.density_g_per_cm3 == None:
            self.density_g_per_cm3 = self.find_density_g_per_cm3()

        if self.density_atoms_per_barn_per_cm == None:
            self.density_atoms_per_barn_per_cm = self.find_density_atoms_per_barn_per_cm()


        self.packing_fraction=kwargs.get('packing_fraction',1.0)

        self.color = kwargs.get('color')

        self.material_card_name = kwargs.get('material_card_name',self.chemical_equation)

    def find_isotope_fractions_in_chemical_equation(self):
        isotope_fractions=[]
        for element, atom_fraction in zip(self.elements,self.atom_fractions):
            for isotope in element.isotopes:
                isotope_fractions.append(atom_fraction*isotope.abundance)
        return isotope_fractions

    def find_isotopes_in_chemical_equation(self):
        isotopes=[]
        for element in self.elements:
            for isotope in element.isotopes:
                isotopes.append(isotope)
        return isotopes

    def serpent_material_card(self):

        comment = '%   '

        if self.density_g_per_cm3 == None and self.density_atoms_per_barn_per_cm == None:
            raise ValueError(
                "To produce a serpent material card the volume_of_unit_cell_cm3 and the atoms_per_unit_cell \n or provide the density with either the density_g_per_cm3 or density_atoms_per_barn_per_cm keyword")

        if self.density_g_per_cm3 == None:
            density = '  ' + str(self.density_atoms_per_barn_per_cm*self.packing_fraction)
        else:
            density = '  ' + str(self.density_g_per_cm3*self.packing_fraction)

        if self.color == None:

            color = ''

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")

        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)])

        mat_card = 'mat ' + self.material_card_name + density + color + ' \n'

        for isotope, isotope_fraction in zip(self.isotopes, self.isotope_fractions):
            #mat_card = mat_card+ isotope.zaid +' ' +str(isotope_fraction)+'\n'
            mat_card = mat_card+ '   '+(isotope.zaid + isotope.nuclear_library).ljust(11)+ ' '+ str(isotope_fraction).ljust(22)+' % ' +isotope.material_card_name+'\n'

        return mat_card

    def find_average_atom_mass(self):
        masses = []
        for element,number_of_element_atoms in zip(self.elements,self.fractions_coefficients):
            element_mass = 0
            for isotope in element.isotopes:
                element_mass = element_mass + isotope.abundance * isotope.mass_amu
            masses.append(element_mass*number_of_element_atoms)
        return (sum(masses)/sum(self.fractions_coefficients) )*1.66054e-24

    def find_elements_in_chemical_equation(self,chemical_equation):
        chemical_equation_chopped_up = [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]

        list_elements = []
        enriched_element_symbol=''
        if self.enriched_isotopes!=None:
            enriched_element_symbol = self.enriched_isotopes[0].symbol
            for isotope in self.enriched_isotopes:
                if isotope.symbol != enriched_element_symbol:
                    raise ValueError('Enriched isotope must all be from the same element')


        for counter in range(0, len(chemical_equation_chopped_up)):
            # print(list[counter])
            if not is_number(chemical_equation_chopped_up[counter]):
                element_symbol =chemical_equation_chopped_up[counter]
                if element_symbol==enriched_element_symbol:
                    list_elements.append(Element(symbol=element_symbol,enriched_isotopes=self.enriched_isotopes))
                else:
                    list_elements.append(Element(symbol=element_symbol))


        return list_elements

    def get_atom_fractions_from_chemical_equations(self,chemical_equation):
        list_of_fractions = []
        chemical_equation_chopped_up = [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                try:
                    if is_number(chemical_equation_chopped_up[counter + 1]):
                        list_of_fractions.append(float(chemical_equation_chopped_up[counter + 1]))
                    else:
                        list_of_fractions.append(1)
                except:
                    list_of_fractions.append(1)


        a = sum(list_of_fractions)
        b = 1.0

        rtol = 1e-6

        if not abs(a - b) <= rtol * max(abs(a), abs(b)):

            normalised_list_of_fractions = []
            normalisation_factor = 1.0 / sum(list_of_fractions)
            for fraction in list_of_fractions:
                normalised_list_of_fractions.append(normalisation_factor * fraction)

            return normalised_list_of_fractions

        return list_of_fractions

    def find_fractions_coefficients_in_chemical_equation(self,chemical_equation):
        chemical_equation_chopped_up = [a for a in re.split(r'([A-Z][a-z]*)', chemical_equation) if a]
        list_fraction = []
        for counter in range(0, len(chemical_equation_chopped_up)):
            if not is_number(chemical_equation_chopped_up[counter]):
                try:
                    if is_number(chemical_equation_chopped_up[counter + 1]):
                        list_fraction.append(float(chemical_equation_chopped_up[counter + 1]))
                    else:
                        list_fraction.append(1.0)
                except:
                    list_fraction.append(1.0)
        return list_fraction        

    def find_molar_mass(self):
        masses = []
        for element in self.elements:
            element_mass = 0
            for isotope in element.isotopes:
                element_mass = element_mass + isotope.abundance * isotope.mass_amu
            masses.append(element_mass)

        cumlative_molar_mass = 0
        for mass, fraction in zip(masses, self.find_fractions_coefficients_in_chemical_equation(self.chemical_equation)):
            cumlative_molar_mass = cumlative_molar_mass + (mass * float(fraction))

        return cumlative_molar_mass

    def density_g_per_cm3_idea_gas(self):

        density_kg_m3 = (self.pressure_Pa / (8.31 * self.temperature_K)) * self.molar_mass * 6.023e23 * 1.66054e-27
        density_g_cm3 = density_kg_m3 / 1000.0
        return density_g_cm3

    def density_g_per_cm3_liquid(self):
        from thermo.chemical import Chemical
        hot_pressurized_liquid = Chemical(self.chemical_equation, T=self.temperature_K, P=self.pressure_Pa)
        return hot_pressurized_liquid.rho * 0.001

    def find_density_g_per_cm3(self):

        if self.state_of_matter == 'solid' and self.volume_of_unit_cell_cm3 != None and self.atoms_per_unit_cell !=None:
            return (self.molar_mass*1.66054e-24*self.atoms_per_unit_cell / self.volume_of_unit_cell_cm3)

        if self.density_atoms_per_barn_per_cm != None:
            return (self.density_atoms_per_barn_per_cm / 1e-24) * self.average_atom_mass

        if self.state_of_matter == 'gas' and self.pressure_Pa != None and self.temperature_K != None:
            return self.density_g_per_cm3_idea_gas()

        if self.state_of_matter == 'liquid' and self.pressure_Pa != None and self.temperature_K != None:
            return self.density_g_per_cm3_liquid()

        return None

    def find_density_atoms_per_barn_per_cm(self):

        if self.atoms_per_unit_cell != None and self.volume_of_unit_cell_cm3 != None:

            return (self.atoms_per_unit_cell / self.volume_of_unit_cell_cm3) * 1e-24

        if self.density_g_per_cm3 != None and self.volume_of_unit_cell_cm3 != None:

            return (self.density_g_per_cm3 / self.molar_mass) * 6.023e23 * 1e-24

        return None

class Homogenised_mixture():
    def __init__(self,mixtures,**kwargs):

        self.classname = self.__class__.__name__
        self.mixtures=mixtures

        self.mass_fractions=kwargs.get('mass_fractions')

        self.volume_fractions=kwargs.get('volume_fractions')

        if self.volume_fractions == None and self.mass_fractions == None:
            print('volume_fractions or mass_fractions must be provided')
            sys.exit()

        if self.volume_fractions == None:
            self.volume_fractions = self.find_volume_fractions_from_mass_fractions()
            self.material_card_name = self.find_material_card_name_with_mass_fractions()

        if self.mass_fractions == None:
            self.mass_fractions = self.find_mass_fractions_from_volume_fractions()
            self.material_card_name = self.find_material_card_name_with_volume_fractions()

        self.density_g_per_cm3= self.find_density_g_per_cm3(self.mixtures,self.volume_fractions)

        self.color = kwargs.get('color')
        
    def find_volume_fractions_from_mass_fractions(self):
        if sum(self.mass_fractions) > 1.0:
            print('provided mass fractions should sum to 1 not ', sum(self.volume_fractions))
            sys.exit()

        list_of_non_normalised_volume_fractions = []
        cumlative_vol_fraction=0
        for mix,mass_fraction in zip(self.mixtures,self.mass_fractions):
            non_normalised_volume_fractions = mass_fraction/mix.density_g_per_cm3
            list_of_non_normalised_volume_fractions.append(non_normalised_volume_fractions)
            cumlative_vol_fraction = cumlative_vol_fraction+ non_normalised_volume_fractions
        factor = 1.0/cumlative_vol_fraction

        normalised_volume_fractions=[]
        for non_normalised_volume_fractions in list_of_non_normalised_volume_fractions:
            normalised_volume_fractions.append(non_normalised_volume_fractions*factor)
        return normalised_volume_fractions
        
    def find_mass_fractions_from_volume_fractions(self):
        if sum(self.volume_fractions) > 1.0:
            print('provided volume fractions should sum to 1 not ',sum(self.volume_fractions))
            sys.exit()

        list_of_non_normalised_mass_fractions = []
        cumlative_mass_fraction = 0
        for mix, vol_fraction in zip(self.mixtures, self.volume_fractions):
            non_normalised_mass_fractions = vol_fraction * mix.density_g_per_cm3
            list_of_non_normalised_mass_fractions.append(non_normalised_mass_fractions)
            cumlative_mass_fraction = cumlative_mass_fraction + non_normalised_mass_fractions
        factor = 1.0 / cumlative_mass_fraction

        normalised_mass_fractions = []
        for non_normalised_mass_fractions in list_of_non_normalised_mass_fractions:
            normalised_mass_fractions.append(non_normalised_mass_fractions * factor)
        return normalised_mass_fractions

    def find_density_g_per_cm3(self,mixtures,volume_fractions):
        cumlative_density = 0
        for mixture, volume in zip(mixtures,volume_fractions):
            cumlative_density = cumlative_density + (mixture.density_g_per_cm3 * volume)
        # todo allow density combinations involving atom_per_barn_cm2
        return cumlative_density

    def find_material_card_name_with_volume_fractions(self):
        description_to_return = ''
        for item, vol_frac in zip(self.mixtures,self.volume_fractions):
            description_to_return = description_to_return +item.material_card_name+'_vf_'+str(vol_frac)+'_'
        return  description_to_return[:-1]

    def find_material_card_name_with_mass_fractions(self):
        description_to_return = ''
        for item, frac in zip(self.mixtures, self.mass_fractions):
            description_to_return = description_to_return + item.material_card_name + '_mf_' + str(frac)+'_'
        return description_to_return[:-1]

    def serpent_material_card(self):
        comment = '%  '

        density = ' -' + str(self.density_g_per_cm3)

        if self.color == None:

            color = ''

        elif type(self.color) not in (tuple, list, np.ndarray) or len(self.color) != 3:

            raise ValueError("3-length RGB color tuple please.")

        else:

            color = ' rgb ' + ' '.join([str(i) for i in np.array(self.color).clip(0, 255)])

        mat_card = 'mat ' + self.material_card_name + density + color + ' \n'

        for item, volume_fraction, mass_fraction in zip(self.mixtures, self.volume_fractions, self.mass_fractions):

            if item.isotopes==[]:
                mat_card = mat_card + comment + '\n' + comment + item.material_card_name + ' with a density of ' + str(item.density_g_per_cm3) + ' g per cm3 \n'
                mat_card = mat_card + comment + 'volume fraction of ' + str(volume_fraction) + ' \n'
                # makes no sense to have a void mass fraction material_card = material_card + comment + 'mass fraction of ' + str(mass_fraction) + ' \n'
            else:
                average_mass_of_one_atom = 0.0
                for isotope, atom_fraction in zip(item.isotopes, item.isotope_fractions):
                    #print('    isotope.mass_amu * atom_fraction',isotope.mass_amu , atom_fraction)
                    average_mass_of_one_atom = average_mass_of_one_atom + isotope.mass_amu * atom_fraction
                number_of_atoms_per_cm3_of_item = item.density_g_per_cm3 / (average_mass_of_one_atom * 1.66054e-24)

                #print('    number_of_atoms_per_cm3_of_item',number_of_atoms_per_cm3_of_item)
                number_of_atoms_per_cm3_of_mix = number_of_atoms_per_cm3_of_item*volume_fraction/7.66e22
                #print('    number_of_atoms_per_cm3_of_mix',number_of_atoms_per_cm3_of_mix)

                mat_card = mat_card + comment+'\n'+comment + item.material_card_name + ' with a density of '+ str(item.density_g_per_cm3) +' g per cm3 \n'
                mat_card = mat_card + comment+ 'volume fraction of ' + str(volume_fraction) + ' \n'
                mat_card = mat_card + comment+ 'mass fraction of ' + str(mass_fraction) + ' \n'

                for isotope, isotopes_atom_fraction in zip(item.isotopes, item.isotope_fractions):

                    if isotopes_atom_fraction > 0:
                        mat_card = mat_card + '   ' + (isotope.zaid + isotope.nuclear_library).ljust(11) + ' ' + str(isotopes_atom_fraction*number_of_atoms_per_cm3_of_mix).ljust(22) + ' % ' + isotope.name + '\n'

        return mat_card

