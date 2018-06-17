#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:16:19 2018

@author: mc2056
"""

from neutronics_material_maker.utilities import (CtoK, KtoC, is_number,
                                                 kgm3togcm3)
from neutronics_material_maker.material import (MfMaterial, NbSnSuperconductor,
                                                NbTiSuperconductor, Liquid,
                                                matproperty)
from neutronics_material_maker.nmm import Material, Element, Isotope
import unittest
import numpy as np
from scipy.interpolate import interp1d


class DTPlasma(Material):
    name = 'DT Plasma'
    def __init__(self, rho_barns_cm2=1e20):
        #TODO: Determine what this number is... not Na
        amu = (0.5*2+0.5*3)
        rho = rho_barns_cm2*1.66054e-24*amu
        # TODO FIX HOOK
        super().__init__(material_card_name=self.name, 
                         density_g_per_cm3=.000001,
                         elements=[Element('H',
                                           enriched_isotopes=[Isotope('H', 2,
                                                                      abundance=0.5),
                                                              Isotope('H', 3,
                                                                      abundance=0.5)])
                                  ], atom_fractions= [1.])


class DDPlasma(Material):
    name = 'DD Plasma'
    def __init__(self, rho_barns_cm2=1e20):
        super().__init__(material_card_name=self.name, 
                         density_atoms_per_barn_per_cm=rho_barns_cm2,
                         elements=[Isotope('H', 2)], atom_fractions= [1.])


class NbTi(NbTiSuperconductor):
    mf = {'Al': 1}
    name = 'NbTi'
    density = None
    brho = None
    # Superconducting parameterisation
    C_0 = 168512
    Bc_20 = 14.61
    Tc_0 = 9.03
    alpha = 1
    beta = 1.54
    gamma = 2.1

    @staticmethod
    def rho(T: 'Kelvin'):
        return 6538


class Nb3Sn(NbSnSuperconductor):
    name = 'Nb3Sn - WST'
    mf = {'Al': 1}
    density = 8910
    brho = None
    # WST strand
    C_a1 = 50.06
    C_a2 = 0
    eps_0a = 0.312
    eps_m = -0.059
    B_c20m = 33.24
    T_c0max = 16.34
    C = 83075
    p = .593
    q = 2.156

    @staticmethod
    def rho(T: 'Kelvin'):
        return 8910


class Nb3Sn_2(NbSnSuperconductor):
    name = 'Nb3Sn - EUTF4'
    mf = {'Al': 1}
    density = 8910
    brho = None
    # EUTF4 strand
    C_a1 = 45.74
    C_a2 = 0
    eps_0a = 0.256
    eps_m = -0.110
    B_c20m = 32.97
    T_c0max = 16.06
    C = 76189
    p = .63
    q = 2.1

    @staticmethod
    def rho(T: 'Kelvin'):
        return 8910


class Void(MfMaterial):
    #TODO: FIX DUMMY VOID not writing serpent card
    name = ' Void'
    density = 0
    mf = {}
    brho = None


class Bronze(MfMaterial):
    name = 'Bronze'
    density = 8877.5
    mf = {'Cu': 0.95,
          'Sn': 0.05}
    brho = None


class EpoxyResin(MfMaterial):
    name = 'Epoxy resin'
    mf = {'Al': 0.0007074,
          'C': 0.0034056,
          'H': 0.0038934,
          'Mg': 0.0002142004,
          'N': 0.0003708,
          'O': 0.0048708,
          'S': 9.179996e-05,
          'Si': 0.0058552000000000005}
    density = 1207


class EUROfer(MfMaterial):
    name = 'EUROfer'
    mf = {'Fe': 0.88821,
          'B': 1e-05,
          'C': 0.00105,
          'N': 0.0004,
          'O': 1e-05,
          'Al': 4e-05,
          'Si': 0.00026,
          'P': 2e-05,
          'S': 3e-05,
          'Ti': 1e-05,
          'V': 0.0002,
          'Cr': 0.09,
          'Mn': 0.0055,
          'Co': 5e-05,
          'Ni': 0.0001,
          'Cu': 3e-05,
          'Nb': 5e-05,
          'Mo': 3e-05,
          'Ta': 0.0012,
          'W': 0.011}
    density = 7870
    brho = 8.43211E-02  # barn/cm

    @staticmethod
    @matproperty(Tmin=0, Tmax=5000)  # TODO: Check actual limits
    def Cp(T: 'Kelvin'):
        '''
        K. Mergia, N. Boukos,
        Structural, thermal, electrical and magnetic properties of Eurofer 97
        steel,
        Journal of Nuclear Materials,
        Volume 373, Issues 1–3,
        2008,
        Pages 1-8,
        ISSN 0022-3115,
        https://doi.org/10.1016/j.jnucmat.2007.03.267.
        (http://www.sciencedirect.com/science/article/pii/S0022311507006642)
        '''
        return 2.696*T-0.004962*T**2+3.335e-6*T**3


class SS316LN(MfMaterial):
    name = 'SS316-LN'
    mf = {'B': 1e-05,
          'C': 0.0003,
          'Co': 0.0005,
          'Cr': 0.18,
          'Cu': 0.003,
          'Fe': 0.63684,
          'Mn': 0.02,
          'Mo': 0.027,
          'N': 0.0008,
          'Nb': 0.0001,
          'Ni': 0.125,
          'P': 0.00025,
          'S': 0.0001,
          'Si': 0.005,
          'Ta': 0.0001}
    density = 7930
    brho = 8.58294E-02

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def CTE(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 40
        T_ref = 293 K
        '''
        T = KtoC(T)
        return 15.13+7.93e-3*T-3.33e-6*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def E(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 41
        '''
        T = KtoC(T)
        return 0.001*(201660-84.8*T)

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def rho(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Table A.S03.2.4-1
        '''
        rho = [7930, 7919, 7899, 7879, 7858, 7837, 7815, 7793, 7770, 7747,
               7724, 7701, 7677, 7654, 7630, 7606, 7582]
        t = [20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600,
             650, 700, 750, 800]
        p = interp1d(CtoK(t), rho)(T)
        if is_number(T):
            return p[0]
        else:
            return p

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def k(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 42
        '''
        T = KtoC(T)
        return 13.98+1.502e-2*T

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def Cp(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 43
        '''
        T = KtoC(T)
        return 462.69+0.520265*T-1.7117e-3*T**2+3.3658e-6*T**3-2.1958e-9*T**4

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def Sy(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 44
        '''
        T = KtoC(T)
        return (225.75-0.73683*T+2.5036e-3*T**2-5.4546e-6*T**3 +
                6.4366e-9*T**4-3.029e-12*T**5)

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def Syavg(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 44
        '''
        T = KtoC(T)
        return 1.28*(225.75-0.73683*T+2.5036e-3*T**2-5.4546e-6*T**3 +
                     6.4366e-9*T**4-3.029e-12*T**5)

    @staticmethod
    @matproperty(Tmin=CtoK(50), Tmax=CtoK(650))
    def Su(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 47
        '''
        T = KtoC(T)
        return (529.75-0.95180*T+2.5732e-3*T**2-2.3316e-6*T**3-4.3944e-10*T**4
                + 3.4942e-13*T**5)

    @staticmethod
    @matproperty(Tmin=CtoK(50), Tmax=CtoK(650))
    def Suavg(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 47
        '''
        T = KtoC(T)
        return (529.75-0.95180*T+2.5732e-3*T**2-2.3316e-6*T**3-4.3944e-10*T**4
                + 3.4942e-13*T**5)*1.112


class PureCopper(MfMaterial):
    '''
    Pure Copper as per ITER materials.
    '''
    name = 'Pure Cu'
    mf = {'Cu': 0.9999075,
          'Sb': 4e-6,
          'As': 5e-6,
          'Bi': 1e-6,
          'Cd': 1e-6,
          'Fe': 10e-6,
          'Pb': 5e-6,
          'Mn': 0.5e-6,
          'Ni': 10e-6,
          'O': 5e-6,
          'P': 3e-6,
          'Se': 3e-6,
          'Ag': 25e-6,
          'S': 15e-6,
          'Te': 2e-6,
          'Sn': 2e-6,
          'Zn': 1e-6}
    density = 8940
    brho = None

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(900))
    def CTE(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 83
        '''
        T = KtoC(T)
        return 16.73+5.26e-3*T-5.53e-6*T**2+4.2e-9*T**3

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(400))
    def E(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 84
        '''
        T = KtoC(T)
        return 117-2.17e-2*T-6.29e-5*T**2

    @staticmethod
    def mu(T): return 0.33

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(900))
    def rho(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 85
        '''
        T = KtoC(T)
        return 8940*(1-3e-6*(T-20)*(-2.49e-9*T**3+8.18e-6*T**2+3.16e-3*T+16.8))

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def k(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 86
        '''
        T = KtoC(T)
        return 402+2.46e-6*T**2-7.08e-2*T

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def Cp(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 87
        '''
        T = KtoC(T)
        return 387+4.36e-5*T**2+6.35e-2*T

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(950))
    def Sy(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 91
        '''
        T = KtoC(T)
        return 584-5.04e-2*T-5e-6*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(950))
    def Su(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 92
        '''
        T = KtoC(T)
        return 212-2.94e-1*T+8.17e-5*T**2


class CuCrZr(MfMaterial):
    '''
    Copper-Chrome-Zirconium alloy - ITER-grade
    '''
    name = 'CuCrZr'
    mf = {'Cu': 0.8,  # TODO: TOTAL GUESS - SEEMS TO BE NO STANDARD???
          'Cr': 0.1,
          'Zr': 0.1}
    brho = None
    density = 8900

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def E(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 96
        '''
        T = KtoC(T)
        return 128-2.59e-2*T-4.87e-5*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(600))
    def CTE(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Table A.S31.2.1-1
        '''
        T = KtoC(T)
        t = [20, 50, 100, 150, 200, 250, 300, 400, 450, 500, 550, 600]
        a = [16.7, 17, 17.3, 17.5, 17.7, 17.8, 18, 18.1, 18.2, 18.4, 18.5,
             18.6]
        return interp1d(CtoK(t), a)(T)

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def rho(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 97
        '''
        T = KtoC(T)
        return 8900*(1-3e-6*(T-20)*(7.2e-9*T**3-9.05e-6*T**2+6.24e-3*T+16.6))

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(700))
    def k(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 98
        '''
        T = KtoC(T)
        return 2.11e-7*T**3-2.83e-4*T**2-1.38e-1*T+323


class Tungsten(MfMaterial):
    name = 'Tungsten'
    mf = {'Ag': 1e-05,
          'Al': 1.5e-05,
          'As': 5e-06,
          'Ba': 5e-06,
          'C': 3e-05,
          'Ca': 5e-06,
          'Cd': 5e-06,
          'Co': 1e-05,
          'Cr': 2e-05,
          'Cu': 1e-05,
          'Fe': 3e-05,
          'H': 5e-06,
          'K': 1e-05,
          'Mg': 5e-06,
          'Mn': 5e-06,
          'Mo': 0.0001,
          'N': 5e-06,
          'Na': 1e-05,
          'Nb': 1e-05,
          'Ni': 5e-06,
          'O': 2e-05,
          'P': 2e-05,
          'Pb': 5e-06,
          'S': 5e-06,
          'Si': 2e-05,
          'Ta': 2e-05,
          'Ti': 5e-06,
          'W': 0.999595,
          'Zn': 5e-06,
          'Zr': 5e-06}
    density = 19000
    brho = None

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1200))
    def CTE(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 135
        '''
        T = KtoC(T)
        return 3.9225+5.8352e-4*T+5.7054e-11*T**2-2.0463e-14*T**3

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def E(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 136
        '''
        T = KtoC(T)
        return 397.903-2.3066e-3*T-2.7162e-5*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1200))
    def rho(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 137
        '''
        T = KtoC(T)
        return 1000*(19.3027-2.3786e-4*T-2.2448e-8*T**2)

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def k(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 138
        '''
        T = KtoC(T)
        return 174.9274-0.1067*T+5.0067e-5*T**2-7.8349e-9*T**3

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def Cp(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 139
        '''
        T = KtoC(T)
        return 128.308+3.2797e-2*T-3.4097e-6*T**2


class Beryllium(MfMaterial):
    '''
    Properties and composition taken from ITER_D_222RLN v3.3
    '''
    name = 'Be'
    mf = {'Be': 0.99637,
          'Al': 0.06e-2,
          'C': 0.1e-2,
          'Fe': 0.08e-2,
          'Mg': 0.06e-2,
          'Si': 0.06e-2,
          'U': 0.003e-2}
    density = None  # Random number
    brho = None

    @staticmethod
    def mu(T):
        '''
        Poisson's ratio
        '''
        return 0.1

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(1000))
    def CTE(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 127
        '''
        T = KtoC(T)
        return 4.1e-9*T**3-1.2e-5*T**2+1.33e-2*T+11.3

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def E(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 128
        '''
        T = KtoC(T)
        return 306.78-2.9281e-2*T-4.5069e-5*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def rho(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 129
        '''
        T = KtoC(T)
        return 1830*(1-3e-6*(4.1e-9*T**3-1.2e-5*T**2+1.33E-2*T+11.3)*(T-20))

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(800))
    def k(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 130
        '''
        T = KtoC(T)
        return 209-4.8e-1*T+9.38E-4*T**2-9.37e-7*T**3+3.34e-10*T**4

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(500))
    def Cp(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Table A.A01.2.6-1
        '''
        T = KtoC(T)
        t = [20, 100, 200, 300, 400, 500, 600, 700, 800]
        cp = [1807, 2046, 2295, 2497, 2660, 2791, 2998, 2989, 3071]
        return interp1d(t, cp)(T)

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(650))
    def Sy(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 131
        '''
        T = KtoC(T)
        return 252.2-1.524e-1*T-1.45E-4*T**2

    @staticmethod
    @matproperty(Tmin=CtoK(20), Tmax=CtoK(950))
    def Su(T: 'Kelvin'):
        '''
        ITER_D_222RLN v3.3 Equation 132
        '''
        T = KtoC(T)
        return 392.8-3.023e-1*T-2.011e-4*T**2


class H2O(Liquid):
    symbol = 'H2O'


class Helium(Liquid):
    symbol = 'He'
    T0 = 4.5
    P0 = 6e5


class test_property(unittest.TestCase):
    E = EUROfer()
    W = Tungsten()
    S = SS316LN()
    C = PureCopper()
    CCZ = CuCrZr()

    def test_property(self):
        with self.assertRaises(ValueError):
            self.E.Cp(-200)
        with self.assertRaises(ValueError):
            self.E.Cp([-200])
        with self.assertRaises(ValueError):
            self.E.Cp(20000)
        with self.assertRaises(ValueError):
            self.E.Cp([20000])
        self.E.Cp(400)
        self.E.Cp([400])

    def test_array(self):
        T = self.E.Cp(np.array([20, 30, 40]))
        Tl = self.E.Cp([20, 30, 40])
        self.assertTrue((T-Tl).all() == 0)

    def test_array_limits(self):
        a = self.W.k(CtoK([20, 30, 400, 1000, 1000]))
        with self.assertRaises(ValueError):
            a = self.W.k(CtoK([20, 30, 400, 1000, 1001]))
        with self.assertRaises(ValueError):
            a = self.W.k(CtoK([19, 30, 400, 1000, 1000]))
        with self.assertRaises(ValueError):
            a = self.W.k(CtoK([19, 30, 400, 1000, 1001]))
        del a

    def test_interp(self):
        self.S.rho([300])
        self.S.rho(300)
        self.assertTrue(self.S.rho(CtoK(20)) == 7930)
        self.assertTrue(self.S.rho(CtoK(300)) == 7815)
        a = self.S.rho([300, 400, 500])
        b = self.S.rho(np.array([300, 400, 500]))
        self.assertTrue((a-b).all() == 0)

    def test_Curho(self):
        self.assertEqual(self.C.rho(CtoK(20)), 8940)  # Eq check

    def test_CuCrZrrho(self):
        self.assertEqual(self.CCZ.rho(CtoK(20)), 8900)  # Eq check


class test_materials(unittest.TestCase):
    Be = Beryllium()
    W = Tungsten()
    S = SS316LN()
    N = Nb3Sn()
    N_2 = Nb3Sn_2()
    NT = NbTi()
    plot = False

    def test_density_load(self):
        self.Be.density_g_per_cm3 = None  # Force raise
        self.Be.density_atoms_per_barn_per_cm = None
        with self.assertRaises(ValueError):
            self.Be.material_card_header('Be', (0, 1, 2), 'serpent', None)
        self.Be.T = 300
        self.assertTrue(hasattr(self.Be, 'density'))
        self.assertTrue(is_number(self.Be.density))
        self.assertTrue(type(self.Be.density) == float)
        
        s = self.Be.material_card_header('Be', (0, 1, 2), 'serpent', None)
        s = s[-1]
        # Check serpent header updated with correct density
        self.assertTrue(float(s.split(' ')[2][1:]) == self.Be.density_g_per_cm3)

    def test_default(self):

        class Dummy(MfMaterial):
            name = 'test'
            density = None
            mf = {'Al': 1}
            brho = None

            @staticmethod
            def rho(T):
                return T*300-100
        D = Dummy()
        self.assertTrue(D.T == 293.15)
        self.assertTrue(D.density == D.T*300-100)
        self.assertTrue(D.density_g_per_cm3 == kgm3togcm3(D.density))

        class Dummy(MfMaterial):
            name = 'test'
            density = None
            mf = {'Al': 1}
            brho = None
            T0 = 500

            @staticmethod
            def rho(T):
                return T*300-100
        D = Dummy()
        self.assertTrue(D.T == 500)
        self.assertTrue(D.density == D.T*300-100)
        self.assertTrue(D.density_g_per_cm3 == kgm3togcm3(D.density))

    def test_SC_plot(self):
        if self.plot:
            Bmin, Bmax = 3, 16
            Tmin, Tmax = 2, 6
            eps = -.66
            self.N.plot_SC(Bmin, Bmax, Tmin, Tmax, eps)
            self.N_2.plot_SC(Bmin, Bmax, Tmin, Tmax, eps)
            self.NT.plot_SC(Bmin, Bmax, Tmin, Tmax)


class test_liquids(unittest.TestCase):
    H = H2O()

    def test_TP(self):
        self.assertTrue(self.H.T == 293.15)
        self.assertTrue(self.H.P == 101325)
        self.assertTrue(self.H.density == 998.987347802)
        self.H.T, self.H.P = 500, 200000
        s = self.H.material_card_header('H2O', (0, 1, 2), 'serpent', None)
        s = s[-1]
        self.assertTrue(float(s.split(' ')[2][1:]) == self.H.density_g_per_cm3)


if __name__ is '__main__':
    unittest.main()
