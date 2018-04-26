#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:16:19 2018

@author: mc2056
"""

from nmm import Material, Element, is_number
import unittest
import numpy as np
from functools import wraps  # TODO: Improve wrapper syntax. Looks ugly
from scipy.interpolate import interp1d


def list_array(list_):
    '''
    Always returns a numpy array
    Can handle int, float, list, np.ndarray
    '''
    if isinstance(list_, list):
        return np.array(list_)
    elif is_number(list_):
        return np.array([list_])
    elif isinstance(list_, np.ndarray):
        return list_


def value_array(value):
    if is_number(value):
        return value
    else:
        return list_array(value)


def matproperty(Tmin, Tmax):
    '''
    Material property decorator object
    Checks that input T vector is within bounds
    Handles floats and arrays
    '''
    def decorator(f):
        def wrapper(*args, **kwargs):
            T = list_array(args[0])
            if not (T <= Tmax).all():
                raise ValueError('Material property not valid outside of tempe'
                                 f'rature range: {T} > Tmax = {Tmax}')
            if not (T >= Tmin).all():
                raise ValueError('Material property not valid outside of tempe'
                                 f'rature range: {T} < Tmin = {Tmin}')
            return f(T, **kwargs)
        return wrapper
    return decorator


def CtoK(T):
    return list_array(T)+273.15


def KtoC(T):
    return list_array(T)-273.15


def interp_1D(t, prop, T):
    if is_number(T):
        return interp1d(t, prop)(T)[0]
    else:
        return interp1d(t, prop)(T)


class MfMaterial(Material):
    def __init__(self):
        super().__init__(material_card_name=self.name,
                         density_g_per_cm3=self.rho,
                         density_atoms_per_barn_per_cm=self.brho,
                         elements=[Element(e) for e in self.mf.keys()],
                         mass_fractions=self.mf.values())

    def k(T):
        '''
        Thermal conductivity in W.m/K
        '''
        raise NotImplementedError

    def E(T):
        '''
        Young's modulus in GPa
        '''
        raise NotImplementedError

    def Cp(T):
        '''
        Specific heat in J/kg/K
        '''
        raise NotImplementedError

    def CTE(T):
        '''
        Mean coefficient of thermal expansion in 10**-6/T
        '''
        raise NotImplementedError

    def rho(T):
        '''
        Mass density in kg/m**3
        '''
        raise NotImplementedError
        
    def Sy(T):
        '''
        Minimum yield stress in MPa
        '''
        raise NotImplementedError


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
    rho = 7.87  # g/cm^3
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
    rho = 7.93
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
        return interp_1D(CtoK(t), rho, T)

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
    rho = 19.0
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


class test_property(unittest.TestCase):
    E = EUROfer()
    W = Tungsten()
    S = SS316LN()

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
            
    def test_interp(self):
        self.S.rho([300])
        self.S.rho(300)
        self.assertTrue(self.S.rho(CtoK(20)) == 7930)
        self.assertTrue(self.S.rho(CtoK(300)) == 7815)
        a = self.S.rho([300, 400, 500])
        b = self.S.rho(np.array([300, 400, 500]))
        self.assertTrue((a-b).all() == 0)
        
    def test_values(self):
        self.assertTrue(np.isclose(self.S.Sy(CtoK(100)), 172))



if __name__ is '__main__':
    unittest.main()
    W = Tungsten()
    S = SS316LN()
    #EUROfer.Cp(400)
    #EUROfer.Cp(490)
    #EUROfer.Cp(4000)
    pass
    