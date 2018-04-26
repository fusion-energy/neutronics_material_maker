#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:16:19 2018

@author: mc2056
"""

from nmm import Material, Element
import unittest
import numpy as np
from functools import wraps  # TODO: Improve wrapper syntax. Looks ugly


def matproperty(Tmin, Tmax):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if args[0] > Tmax:
                raise ValueError('Material property not valid outside of tempe'
                                 f'rature range: {args[0]} > Tmax = {Tmax}')
            elif args[0] < Tmin:
                raise ValueError('Material property not valid outside of tempe'
                                 f'rature range: {args[0]} < Tmin = {Tmin}')
            return f(*args, **kwargs)
        return wrapper
    return decorator
        


class MfMaterial(Material):
    def __init__(self):
        super().__init__(material_card_name=self.name,
                         density_g_per_cm3=self.rho,
                         density_atoms_per_barn_per_cm=self.brho,
                         elements=[Element(e) for e in self.mf.keys()],
                         mass_fractions=self.mf.values())
        

    def k(self, T):
        '''
        Thermal conductivity in W.m/K
        '''
        raise NotImplementedError
        
    def E(self, T):
        '''
        Young's modulus in GPa
        '''
        raise NotImplementedError

    def Cp(T):
        '''
        Specific heat in J/kg/K
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
    @matproperty(Tmin=300, Tmax=1000)
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
        return 2.696*T-0.004962*T**2+3.335*10**-6*T**3


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


mat_Eurofer = Material(material_card_name='Eurofer',
                    density_g_per_cm3=7.87,
                    density_atoms_per_barn_per_cm=8.43211E-02,
                    elements=[Element('Fe'),
                              Element('B'),
                              Element('C'),
                              Element('N'),
                              Element('O'),
                              Element('Al'),
                              Element('Si'),
                              Element('P'),
                              Element('S'),
                              Element('Ti'),
                              Element('V'),
                              Element('Cr'),
                              Element('Mn'),
                              Element('Co'),
                              Element('Ni'),
                              Element('Cu'),
                              Element('Nb'),
                              Element('Mo'),
                              Element('Ta'),
                              Element('W')
                              ],
                    mass_fractions=[0.88821,
                                    0.00001,
                                    0.00105,
                                    0.00040,
                                    0.00001,
                                    0.00004,
                                    0.00026,
                                    0.00002,
                                    0.00003,
                                    0.00001,
                                    0.00020,
                                    0.09000,
                                    0.00550,
                                    0.00005,
                                    0.00010,
                                    0.00003,
                                    0.00005,
                                    0.00003,
                                    0.00120,
                                    0.01100
                                    ])


class test_monkeypatch(unittest.TestCase):

    def test_EtoE(self):
        jse = mat_Eurofer.serpent_material_card().splitlines()[1:]
        E = EUROfer()
        mce = E.serpent_material_card().splitlines()[1:]
        self.assertTrue(jse==mce)



if __name__ is '__main__':
    #unittest.main()
    EUROfer = EUROfer()
    a = EUROfer.serpent_material_card(name='test', color=np.random.rand(3)*255)
    EUROfer.Cp(400)
    EUROfer.Cp(40)
    EUROfer.Cp(4000)
    
    