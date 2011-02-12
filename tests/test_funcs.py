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
from pypol import ONE, TWO, x

a = pypol.monomial(a=1)

class TestFuncs(object):
    def testDivisible(self):
        p = pypol.poly1d([2, 6, -4, 8]) * x
        assert funcs.divisible(p, p.gcd())

    def testFromRoots(self):
        p = funcs.from_roots([1, -3, 44, 45245, -2332])
        assert map(p, [1, -3, 44, 45245, -2332]) == [0, 0, 0, 0, 0]
        assert funcs.from_roots([1, -2, 3], 'o').letters == ('o',)

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
        p = pypol.poly1d([4, -3, 4, 1])
        py.test.raises(ValueError, lambda: funcs.polyint(ONE, -1))
        assert funcs.polyint(ONE) == x
        assert funcs.polyint(TWO) == 2*x
        assert funcs.polyint(p) == pypol.poly1d([1, -1, 2, 1, 0])
        assert funcs.polyint(p, 2) == funcs.polyint(funcs.polyint(p)) \
                                   == pypol.polynomial('+ 1/5x^5 - 1/4x^4 + 2/3x^3 + 1/2x^2')

    def testPolyint_(self):
        assert funcs.polyint_(ONE, 1, 1) == 0.0
        assert funcs.polyint_(3*x - 4, 2, 12) == 170.0
        assert funcs.polyint_(-TWO*2, 7, -2) == 36.0
        import random
        for i in xrange(20):
            r = random.randint(1, 100)
            r2 = random.randint(1, 100)
            assert funcs.polyint_(ONE, r, r2) == r2 - r ## More generally: polyint_(p, r1, r2) with p integer = (r2 - r1) * p

    def testInterpolation(self):
        pass

    def testBinCoeff(self):
        py.test.raises(ValueError, lambda: funcs.bin_coeff(1, 2))
        assert funcs.bin_coeff(2, 1) == 2
        assert funcs.bin_coeff(4, 3) == 4
        assert funcs.bin_coeff(12, 11) == 12
        assert funcs.bin_coeff(10, 3) == 120
        assert funcs.bin_coeff(20, 15) == 15504
        assert funcs.bin_coeff(49, 8) == 450978066

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
        py.test.raises(ValueError, funcs.harmonic_g, -1, 1)
        py.test.raises(ValueError, funcs.harmonic_g, 0, 1)
        assert funcs.harmonic_g(10, 1) == funcs.harmonic(10)
        assert funcs.harmonic_g(2, 1) == fractions.Fraction(3, 2)
        assert funcs.harmonic_g(3, 2) == fractions.Fraction(49, 36)
        assert funcs.harmonic_g(4, 4) == fractions.Fraction(22369, 20736)
        assert funcs.harmonic_g(2, 3) == fractions.Fraction(9, 8)
        assert funcs.harmonic_g(4, 2) == fractions.Fraction(205, 144)
        assert funcs.harmonic_g(4, 4) == fractions.Fraction(22369, 20736)

    def testStirling(self):
        py.test.raises(ValueError, lambda: funcs.stirling(-1, -2))
        assert funcs.stirling(0, 0) == 1
        assert funcs.stirling(1, 1) == 1
        assert funcs.stirling(2, 1) == -1
        assert funcs.stirling(3, 1) == 2
        assert funcs.stirling(4, 3) == -6
        assert funcs.stirling(9, 4) == -67284

    def testStirling2(self):
        py.test.raises(ValueError, lambda: funcs.stirling2(1, -1))
        assert funcs.stirling2(0, 0) == 1
        assert funcs.stirling2(2, 1) == 1
        assert funcs.stirling2(12, 3) == 86526
        assert funcs.stirling2(13, 13) == 1
        assert funcs.stirling2(13, 12) == 78

    def testBellNumbers(self):
        assert funcs.bell_num(-1) == 0
        assert funcs.bell_num(0) == 1
        assert funcs.bell_num(1) == 1
        assert funcs.bell_num(2) == 2
        assert funcs.bell_num(3) == 5
        assert funcs.bell_num(4) == 15
        assert funcs.bell_num(5) == 52

if __name__ == '__main__':
    import sys
    import os.path
    py.test.main(args=[os.path.abspath(__file__)] + sys.argv[1:])