import re
import sys
import numpy as np

from pandas import DataFrame

list_of_element_dicts=[]
list_of_element_dicts.append({'symbol':'Sn','name':'Tin','natural_atomic_number':[112, 114, 115, 116, 117, 118, 119, 120, 122, 124],'natural_adundance':[0.0097, 0.0066, 0.0034, 0.1454, 0.0768, 0.2422, 0.0859, 0.3258, 0.0463, 0.0579],'protons':50})
list_of_element_dicts.append({'symbol':'Xe','name':'Xenon','natural_atomic_number':[124, 126, 128, 129, 130, 131, 132, 134, 136],'natural_adundance':[0.000952, 0.00089, 0.019102, 0.264006, 0.04071, 0.212324, 0.269086, 0.104357, 0.088573],'protons':54})
list_of_element_dicts.append({'symbol':'Cd','name':'Cadmium','natural_atomic_number':[106, 108, 110, 111, 112, 113, 114, 116],'natural_adundance':[0.0125, 0.0089, 0.1249, 0.128, 0.2413, 0.1222, 0.2873, 0.0749],'protons':48})
list_of_element_dicts.append({'symbol':'Te','name':'Tellurium','natural_atomic_number':[120, 122, 123, 124, 125, 126, 128, 130],'natural_adundance':[0.0009, 0.0255, 0.0089, 0.0474, 0.0707, 0.1884, 0.3174, 0.3408],'protons':52})
list_of_element_dicts.append({'symbol':'Ba','name':'Barium','natural_atomic_number':[130, 132, 134, 135, 136, 137, 138],'natural_adundance':[0.00106, 0.00101, 0.02417, 0.06592, 0.07854, 0.11232, 0.71698],'protons':56})
list_of_element_dicts.append({'symbol':'Dy','name':'Dysprosium','natural_atomic_number':[156, 158, 160, 161, 162, 163, 164],'natural_adundance':[0.00056, 0.00095, 0.02329, 0.18889, 0.25475, 0.24896, 0.2826],'protons':66})
list_of_element_dicts.append({'symbol':'Gd','name':'Gadolinium','natural_atomic_number':[152, 154, 155, 156, 157, 158, 160],'natural_adundance':[0.002, 0.0218, 0.148, 0.2047, 0.1565, 0.2484, 0.2186],'protons':64})
list_of_element_dicts.append({'symbol':'Hg','name':'Mercury','natural_atomic_number':[196, 198, 199, 200, 201, 202, 204],'natural_adundance':[0.0015, 0.0997, 0.1687, 0.231, 0.1318, 0.2986, 0.0687],'protons':80})
list_of_element_dicts.append({'symbol':'Mo','name':'Molybdenum','natural_atomic_number':[92, 94, 95, 96, 97, 98, 100],'natural_adundance':[0.1453, 0.0915, 0.1584, 0.1667, 0.096, 0.2439, 0.0982],'protons':42})
list_of_element_dicts.append({'symbol':'Nd','name':'Neodymium','natural_atomic_number':[142, 143, 144, 145, 146, 148, 150],'natural_adundance':[0.27152, 0.12174, 0.23798, 0.08293, 0.17189, 0.05756, 0.05638],'protons':60})
list_of_element_dicts.append({'symbol':'Os','name':'Osmium','natural_atomic_number':[184, 186, 187, 188, 189, 190, 192],'natural_adundance':[0.0002, 0.0159, 0.0196, 0.1324, 0.1615, 0.2626, 0.4078],'protons':76})
list_of_element_dicts.append({'symbol':'Ru','name':'Ruthenium','natural_atomic_number':[96, 98, 99, 100, 101, 102, 104],'natural_adundance':[0.0554, 0.0187, 0.1276, 0.126, 0.1706, 0.3155, 0.1862],'protons':44})
list_of_element_dicts.append({'symbol':'Sm','name':'Samarium','natural_atomic_number':[144, 147, 148, 149, 150, 152, 154],'natural_adundance':[0.0307, 0.1499, 0.1124, 0.1382, 0.0738, 0.2675, 0.2275],'protons':62})
list_of_element_dicts.append({'symbol':'Yb','name':'Ytterbium','natural_atomic_number':[168, 170, 171, 172, 173, 174, 176],'natural_adundance':[0.00123, 0.02982, 0.1409, 0.2168, 0.16103, 0.32026, 0.12996],'protons':70})
list_of_element_dicts.append({'symbol':'Ca','name':'Calcium','natural_atomic_number':[40, 42, 43, 44, 46, 48],'natural_adundance':[0.96941, 0.00647, 0.00135, 0.02086, 4e-05, 0.00187],'protons':20})
list_of_element_dicts.append({'symbol':'Er','name':'Erbium','natural_atomic_number':[162, 164, 166, 167, 168, 170],'natural_adundance':[0.00139, 0.01601, 0.33503, 0.22869, 0.26978, 0.1491],'protons':68})
list_of_element_dicts.append({'symbol':'Hf','name':'Hafnium','natural_atomic_number':[174, 176, 177, 178, 179, 180],'natural_adundance':[0.0016, 0.0526, 0.186, 0.2728, 0.1362, 0.3508],'protons':72})
list_of_element_dicts.append({'symbol':'Kr','name':'Krypton','natural_atomic_number':[78, 80, 82, 83, 84, 86],'natural_adundance':[0.00355, 0.02286, 0.11593, 0.115, 0.56987, 0.17279],'protons':36})
list_of_element_dicts.append({'symbol':'Pd','name':'Palladium','natural_atomic_number':[102, 104, 105, 106, 108, 110],'natural_adundance':[0.0102, 0.1114, 0.2233, 0.2733, 0.2646, 0.1172],'protons':46})
list_of_element_dicts.append({'symbol':'Pt','name':'Platinum','natural_atomic_number':[190, 192, 194, 195, 196, 198],'natural_adundance':[0.00012, 0.00782, 0.3286, 0.3378, 0.2521, 0.07356],'protons':78})
list_of_element_dicts.append({'symbol':'Se','name':'Selenium','natural_atomic_number':[74, 76, 77, 78, 80, 82],'natural_adundance':[0.0089, 0.0937, 0.0763, 0.2377, 0.4961, 0.0873],'protons':34})
list_of_element_dicts.append({'symbol':'Ge','name':'Germanium','natural_atomic_number':[70, 72, 73, 74, 76],'natural_adundance':[0.2057, 0.2745, 0.0775, 0.365, 0.0773],'protons':32})
list_of_element_dicts.append({'symbol':'Ni','name':'Nickel','natural_atomic_number':[58, 60, 61, 62, 64],'natural_adundance':[0.68077, 0.26223, 0.011399, 0.036346, 0.009255],'protons':28})
list_of_element_dicts.append({'symbol':'Ti','name':'Titanium','natural_atomic_number':[46, 47, 48, 49, 50],'natural_adundance':[0.0825, 0.0744, 0.7372, 0.0541, 0.0518],'protons':22})
list_of_element_dicts.append({'symbol':'W','name':'Tungsten','natural_atomic_number':[180, 182, 183, 184, 186],'natural_adundance':[0.0012, 0.265, 0.1431, 0.3064, 0.2843],'protons':74})
list_of_element_dicts.append({'symbol':'Zn','name':'Zinc','natural_atomic_number':[64, 66, 67, 68, 70],'natural_adundance':[0.4917, 0.2773, 0.0404, 0.1845, 0.0061],'protons':30})
list_of_element_dicts.append({'symbol':'Zr','name':'Zirconium','natural_atomic_number':[90, 91, 92, 94, 96],'natural_adundance':[0.5145, 0.1122, 0.1715, 0.1738, 0.028],'protons':40})
list_of_element_dicts.append({'symbol':'Ce','name':'Cerium','natural_atomic_number':[136, 138, 140, 142],'natural_adundance':[0.00185, 0.00251, 0.8845, 0.11114],'protons':58})
list_of_element_dicts.append({'symbol':'Cr','name':'Chromium','natural_atomic_number':[50, 52, 53, 54],'natural_adundance':[0.04345, 0.83789, 0.09501, 0.02365],'protons':24})
list_of_element_dicts.append({'symbol':'Fe','name':'Iron','natural_atomic_number':[54, 56, 57, 58],'natural_adundance':[0.05845, 0.91754, 0.02119, 0.00282],'protons':26})
list_of_element_dicts.append({'symbol':'Pb','name':'Lead','natural_atomic_number':[204, 206, 207, 208],'natural_adundance':[0.014, 0.241, 0.221, 0.524],'protons':82})
list_of_element_dicts.append({'symbol':'S','name':'Sulfur','natural_atomic_number':[32, 33, 34, 36],'natural_adundance':[0.9499, 0.0075, 0.0425, 0.0001],'protons':16})
list_of_element_dicts.append({'symbol':'Sr','name':'Strontium','natural_atomic_number':[84, 86, 87, 88],'natural_adundance':[0.0056, 0.0986, 0.07, 0.8258],'protons':38})
list_of_element_dicts.append({'symbol':'Ar','name':'Argon','natural_atomic_number':[36, 38, 40],'natural_adundance':[0.003336, 0.000629, 0.996035],'protons':18})
list_of_element_dicts.append({'symbol':'C','name':'Carbon','natural_atomic_number':[12, 13],'natural_adundance':[0.9893, 0.0107],'protons':6})
list_of_element_dicts.append({'symbol':'K','name':'Potassium','natural_atomic_number':[39, 40, 41],'natural_adundance':[0.932581, 0.000117, 0.067302],'protons':19})
list_of_element_dicts.append({'symbol':'Mg','name':'Magnesium','natural_atomic_number':[24, 25, 26],'natural_adundance':[0.7899, 0.1, 0.1101],'protons':12})
list_of_element_dicts.append({'symbol':'Ne','name':'Neon','natural_atomic_number':[20, 21, 22],'natural_adundance':[0.9048, 0.0027, 0.0925],'protons':10})
list_of_element_dicts.append({'symbol':'Si','name':'Silicon','natural_atomic_number':[28, 29, 30],'natural_adundance':[0.92223, 0.04685, 0.03092],'protons':14})
list_of_element_dicts.append({'symbol':'U','name':'Uranium','natural_atomic_number':[234, 235, 238],'natural_adundance':[5.4e-05, 0.007204, 0.992742],'protons':92})
list_of_element_dicts.append({'symbol':'Ag','name':'Silver','natural_atomic_number':[107, 109],'natural_adundance':[0.51839, 0.48161],'protons':47})
list_of_element_dicts.append({'symbol':'B','name':'Boron','natural_atomic_number':[10, 11],'natural_adundance':[0.199, 0.801],'protons':5})
list_of_element_dicts.append({'symbol':'Br','name':'Bromine','natural_atomic_number':[79, 81],'natural_adundance':[0.5069, 0.4931],'protons':35})
list_of_element_dicts.append({'symbol':'Cl','name':'Chlorine','natural_atomic_number':[35, 37],'natural_adundance':[0.7576, 0.2424],'protons':17})
list_of_element_dicts.append({'symbol':'Cu','name':'Copper','natural_atomic_number':[63, 65],'natural_adundance':[0.6915, 0.3085],'protons':29})
list_of_element_dicts.append({'symbol':'Eu','name':'Europium','natural_atomic_number':[151, 153],'natural_adundance':[0.4781, 0.5219],'protons':63})
list_of_element_dicts.append({'symbol':'Ga','name':'Gallium','natural_atomic_number':[69, 71],'natural_adundance':[0.60108, 0.39892],'protons':31})
list_of_element_dicts.append({'symbol':'H','name':'Hydrogen','natural_atomic_number':[1, 2],'natural_adundance':[0.999885, 0.000115],'protons':1})
list_of_element_dicts.append({'symbol':'He','name':'Helium','natural_atomic_number':[3, 4],'natural_adundance':[1.34e-06, 0.99999866],'protons':2})
list_of_element_dicts.append({'symbol':'In','name':'Indium','natural_atomic_number':[113, 115],'natural_adundance':[0.0429, 0.9571],'protons':49})
list_of_element_dicts.append({'symbol':'Ir','name':'Iridium','natural_atomic_number':[191, 193],'natural_adundance':[0.373, 0.627],'protons':77})
list_of_element_dicts.append({'symbol':'La','name':'Lanthanum','natural_atomic_number':[138, 139],'natural_adundance':[0.0008881, 0.9991119],'protons':57})
list_of_element_dicts.append({'symbol':'Li','name':'Lithium','natural_atomic_number':[6, 7],'natural_adundance':[0.0759, 0.9241],'protons':3})
list_of_element_dicts.append({'symbol':'Lu','name':'Lutetium','natural_atomic_number':[175, 176],'natural_adundance':[0.97401, 0.02599],'protons':71})
list_of_element_dicts.append({'symbol':'N','name':'Nitrogen','natural_atomic_number':[14, 15],'natural_adundance':[0.99636, 0.00364],'protons':7})
list_of_element_dicts.append({'symbol':'Rb','name':'Rubidium','natural_atomic_number':[85, 87],'natural_adundance':[0.7217, 0.2783],'protons':37})
list_of_element_dicts.append({'symbol':'Re','name':'Rhenium','natural_atomic_number':[185, 187],'natural_adundance':[0.374, 0.626],'protons':75})
list_of_element_dicts.append({'symbol':'Sb','name':'Antimony','natural_atomic_number':[121, 123],'natural_adundance':[0.5721, 0.4279],'protons':51})
list_of_element_dicts.append({'symbol':'Ta','name':'Tantalum','natural_atomic_number':[180, 181],'natural_adundance':[0.0001201, 0.9998799],'protons':73})
list_of_element_dicts.append({'symbol':'Tl','name':'Thallium','natural_atomic_number':[203, 205],'natural_adundance':[0.2952, 0.7048],'protons':81})
list_of_element_dicts.append({'symbol':'V','name':'Vanadium','natural_atomic_number':[50, 51],'natural_adundance':[0.0025, 0.9975],'protons':23})
list_of_element_dicts.append({'symbol':'Be','name':'Beryllium','natural_atomic_number':[9],'natural_adundance':[1],'protons':4})
list_of_element_dicts.append({'symbol':'O','name':'Oxygen','natural_atomic_number':[16, 17, 18],'natural_adundance':[0.99757, 0.00038, 0.00205],'protons':8})
list_of_element_dicts.append({'symbol':'F','name':'Fluorine','natural_atomic_number':[19],'natural_adundance':[1],'protons':9})
list_of_element_dicts.append({'symbol':'Na','name':'Sodium','natural_atomic_number':[23],'natural_adundance':[1],'protons':11})
list_of_element_dicts.append({'symbol':'Al','name':'Aluminum','natural_atomic_number':[27],'natural_adundance':[1],'protons':13})
list_of_element_dicts.append({'symbol':'P','name':'Phosphorus','natural_atomic_number':[31],'natural_adundance':[1],'protons':15})
list_of_element_dicts.append({'symbol':'Sc','name':'Scandium','natural_atomic_number':[45],'natural_adundance':[1],'protons':21})
list_of_element_dicts.append({'symbol':'Mn','name':'Manganese','natural_atomic_number':[55],'natural_adundance':[1.0],'protons':25})
list_of_element_dicts.append({'symbol':'Co','name':'Cobalt','natural_atomic_number':[59],'natural_adundance':[1.0],'protons':27})
list_of_element_dicts.append({'symbol':'As','name':'Arsenic','natural_atomic_number':[75],'natural_adundance':[1],'protons':33})
list_of_element_dicts.append({'symbol':'Y','name':'Yttrium','natural_atomic_number':[89],'natural_adundance':[1],'protons':39})
list_of_element_dicts.append({'symbol':'Nb','name':'Niobium','natural_atomic_number':[93],'natural_adundance':[1],'protons':41})
list_of_element_dicts.append({'symbol':'Rh','name':'Rhodium','natural_atomic_number':[103],'natural_adundance':[1],'protons':45})
list_of_element_dicts.append({'symbol':'I','name':'Iodine','natural_atomic_number':[127],'natural_adundance':[1],'protons':53})
list_of_element_dicts.append({'symbol':'Cs','name':'Cesium','natural_atomic_number':[133],'natural_adundance':[1],'protons':55})
list_of_element_dicts.append({'symbol':'Pr','name':'Praseodymium','natural_atomic_number':[141],'natural_adundance':[1],'protons':59})
list_of_element_dicts.append({'symbol':'Tb','name':'Terbium','natural_atomic_number':[159],'natural_adundance':[1],'protons':65})
list_of_element_dicts.append({'symbol':'Ho','name':'Holmium','natural_atomic_number':[165],'natural_adundance':[1],'protons':67})
list_of_element_dicts.append({'symbol':'Tm','name':'Thulium','natural_atomic_number':[169],'natural_adundance':[1],'protons':69})
list_of_element_dicts.append({'symbol':'Au','name':'Gold','natural_atomic_number':[197],'natural_adundance':[1],'protons':79})
list_of_element_dicts.append({'symbol':'Bi','name':'Bismuth','natural_atomic_number':[209],'natural_adundance':[1],'protons':83})
list_of_element_dicts.append({'symbol':'Th','name':'Thorium','natural_atomic_number':[232],'natural_adundance':[1],'protons':90})
list_of_element_dicts.append({'symbol':'Pa','name':'Protactinium','natural_atomic_number':[231],'natural_adundance':[1],'protons':91})

elements_df = DataFrame(list_of_element_dicts, index=None)


NAT_ELEMENT_SYMBOLS =  ['Sn', 'Xe', 'Cd', 'Te', 'Ba', 'Dy', 'Gd', 'Hg', 'Mo', 'Nd', 'Os', 'Ru', 'Sm', 'Yb', 'Ca', 'Er', 'Hf',
                        'Kr', 'Pd', 'Pt', 'Se', 'Ge', 'Ni', 'Ti', 'W', 'Zn', 'Zr', 'Ce', 'Cr', 'Fe', 'Pb', 'S', 'Sr', 'Ar', 'C',
                        'K', 'Mg', 'Ne', 'Si', 'U', 'Ag', 'B', 'Br', 'Cl', 'Cu', 'Eu', 'Ga', 'H', 'He', 'In', 'Ir', 'La', 'Li',
                        'Lu', 'N', 'Rb', 'Re', 'Sb', 'Ta', 'Tl', 'V', 'Be', 'O', 'F', 'Na', 'Al', 'P', 'Sc', 'Mn', 'Co', 'As',
                        'Y', 'Nb', 'Rh', 'I', 'Cs', 'Pr', 'Tb', 'Ho', 'Tm', 'Au', 'Bi', 'Th', 'Pa']


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

        nat_abun = elements_df.loc[elements_df['symbol']==symbol]['natural_adundance']
        nat_atom =elements_df.loc[elements_df['symbol']==symbol]['natural_atomic_number']
        nat_atom= list(nat_atom.values)[0]
        if atomic_number in nat_atom:
            index = nat_atom.index(atomic_number)
            nat_abun = list(nat_abun.values)[0]

            return nat_abun[index]
        else:
            return 0.0

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
        raise ValueError('proton number ' + str(protons) + ' not found')

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
        raise ValueError('element symbol not found', symbol)
        

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
        try:
            xsdir_contents = open(xsdir, "r").readlines()
            for line in xsdir_contents:
                choped_up_line = line.split()[0].split('.')
                if choped_up_line[0] == zaid:
                    return '.'+choped_up_line[1]
            return ''
        except:
            return ''

    def find_prefered_library_file(self,zaid,xsdir):
        try:
            xsdir_contents = open(xsdir, "r").readlines()
            for line in xsdir_contents:
                choped_up_line = line.split()

                if choped_up_line[0].split('.')[0] == zaid:
                    #print('line = ',choped_up_line[-1])
                    return choped_up_line[-1]
            return ''
        except:
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

        self.all_natural_element_symbols = self.find_all_natural_element_symbols()


    def find_all_natural_element_symbols(self):
        return NAT_ELEMENT_SYMBOLS

    def find_all_natural_elements(self):
        return [Element(e) for e in NAT_ELEMENT_SYMBOLS]

class Element(Isotope):
    def __init__(self,*args,**kwargs):

        if len(args)==1:
            protons_or_symbol=args[0]

        self.elements_df = elements_df

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
        isotopes_to_return = []
        for i in self.elements_df.loc[self.elements_df['symbol']==symbol]['natural_atomic_number']:
            for an in i:
                isotopes_to_return.append(Isotope(symbol=symbol, atomic_number=an))
        if len(isotopes_to_return)==0:
            raise ValueError('natural composition of isotope not found for ', symbol)

        return isotopes_to_return
 
            
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
            raise ValueError('A list of elements present within the material must be specified')

        if self.atom_fractions == None and self.mass_fractions == None:
            raise ValueError('To make a material either atom_fractions or mass_fractions must be provided')

        if self.atom_fractions == None:
            self.atom_fractions  = self.find_atom_fractions_from_mass_fractions()
                
        if self.mass_fractions == None:
            self.mass_fractions = self.find_mass_fractions_from_atom_fractions()

        if len(self.elements)!=len(self.atom_fractions):
            raise ValueError('When making a material please provide the same number of elements and atom/mass fractions')

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
            raise ValueError('material_card_name must be provided when making a serpent_material_card from a material')

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

        self.enriched_isotopes=kwargs.get('enriched_isotopes',None)

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
            raise ValueError('volume_fractions or mass_fractions must be provided')

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
            raise ValueError('provided mass fractions should sum to 1 not ', sum(self.volume_fractions))

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
            raise ValueError('provided volume fractions should sum to 1 not ',sum(self.volume_fractions))

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

