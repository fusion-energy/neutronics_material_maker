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
                                                matproperty, _Void)
from neutronics_material_maker.refmaterials import (EUROfer, Tungsten, SS316LN,
                                                     PureCopper, CuCrZr, Beryllium,
                                                     Nb3Sn, Nb3Sn_2, NbTi, H2O)
from neutronics_material_maker.nmm import Material, Element, Isotope
import unittest
import numpy as np
from scipy.interpolate import interp1d


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
        T = self.E.Cp(np.array([400, 500, 550]))
        Tl = self.E.Cp([400, 500, 550])
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
            self.Be.material_card(material_card_name='Be', color=(0, 1, 2))
        self.Be.T = 300
        self.assertTrue(hasattr(self.Be, 'density'))
        self.assertTrue(is_number(self.Be.density))
        self.assertTrue(type(self.Be.density) == float)
        s = self.Be.material_card(material_card_name='Be', color=(0, 1, 2))
        s = s.splitlines()[2]
        # Check serpent header updated with correct density
        self.assertTrue(float(s.split(' ')[2][1:]) == self.Be.density_g_per_cm3)

    def test_T_tmp(self):
        s = self.S.material_card()
        self.assertTrue(' tmp 293.15 ' in s.splitlines()[2])
        s = self.S.material_card(temperature_K=400)
        self.assertTrue(' tmp 400 ' in s.splitlines()[2])

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
        s = self.H.material_card(material_card_name='H2O', color=(0, 1, 2))
        s = s.splitlines()[2]
        self.assertTrue(float(s.split(' ')[2][1:]) == self.H.density_g_per_cm3)

