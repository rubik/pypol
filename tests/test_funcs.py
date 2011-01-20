#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials and algebraic fractions.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
- Python 2.6 (or 2.7)
'''

import fractions

import py
import pypol
import pypol.funcs as funcs
from pypol import ONE, x

a = pypol.monomial(a=1)

class TestFuncs(object):
    def testDivisible(self):
        p = pypol.poly1d([2, 6, -4, 8]) * x
        assert funcs.divisible(p, p.gcd())

    def testRandomPoly(self):
        for _ in xrange(1000):
            assert type(funcs.random_poly()) == pypol.Polynomial

        poly1, poly2, poly3 = funcs.random_poly(letters='x', right_hand_side=False, not_null=True), \
                              funcs.random_poly(unique=True, right_hand_side=False, not_null=True), \
                              funcs.random_poly(not_null=True)

        assert poly1
        assert poly2
        assert poly3
        assert ('x',) == poly1.letters
        assert poly2.letters[0] in ('x', 'y', 'z')
        assert all(-10 <= c < 11 for c in poly3.coefficients)

    def testPolyder(self):
        p = pypol.poly1d([1]*4)
        assert pypol.poly1d([3, 2, 1]) == funcs.polyder(p)
        assert pypol.poly1d([6, 2]) == funcs.polyder(p, 2)
        assert pypol.poly1d([6]) == funcs.polyder(p, 3)

    def testPolyint(self):
        pass

    def testPolyint_(self):
        pass

    def testInterpolation(self):
        pass

    def testBinCoeff(self):
        pass

    def testHarmonic(self):
        py.test.raises(ValueError, funcs.harmonic, -1)
        py.test.raises(ValueError, funcs.harmonic, 0)
        assert funcs.harmonic(1) == fractions.Fraction(1, 1)
        assert funcs.harmonic(2) == fractions.Fraction(3, 2)
        assert funcs.harmonic(3) == fractions.Fraction(11, 6)
        assert funcs.harmonic(4) == fractions.Fraction(25, 12)
        assert funcs.harmonic(5) == fractions.Fraction(137, 60)
        assert funcs.harmonic(6) == fractions.Fraction(49, 20)
        assert funcs.harmonic(7) == fractions.Fraction(363, 140)
        assert funcs.harmonic(8) == fractions.Fraction(761, 280)
        assert funcs.harmonic(9) == fractions.Fraction(7129, 2520)
        assert funcs.harmonic(10) == fractions.Fraction(7381, 2520)

    def testGeneralizedHarmonic(self):
        pass

    def testStirling(self):
        pass

    def testStirling2(self):
        pass