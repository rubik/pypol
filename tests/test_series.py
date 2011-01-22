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
import pypol.series as series

x = pypol.monomial(x=1)
a = pypol.monomial(a=1)
NULL = pypol.Polynomial()
ONE = pypol.monomial()
TWO = pypol.monomial(2)

class TestSeries(object):
    def testFibonacci(self):
        assert series.fibonacci(1) == ONE
        assert series.fibonacci(2) == x
        assert series.fibonacci(3) == x**2 + 1
        assert series.fibonacci(4) == x**3 + 2*x
        assert series.fibonacci(5) == x**4 + 3 * x**2 + 1

    def testLucasSequence(self):
        l = series.LucasSeq(x, ONE)
        l1 = series.LucasSeq(x, ONE, 'w')
        l2 = series.LucasSeq(2*x, ONE)
        l3 = series.LucasSeq(2*x, ONE, 'w')
        l4 = series.LucasSeq(ONE, 2*x)
        l5 = series.LucasSeq(ONE, 2*x, 'w')
        l6 = series.LucasSeq(3*x, -TWO)
        l7 = series.LucasSeq(3*x, -TWO, 'w')
        for n in xrange(10):
            if n > 0:
                l(n) == series.fibonacci(n)
            assert l1(n) == series.lucas(n)
            assert l2(n) == series.pell(n)
            assert l3(n) == series.pell_lucas(n)
            assert l4(n) == series.jacobsthal(n)
            assert l5(n) == series.jacob_lucas(n)
            assert l6(n) == series.fermat(n)
            assert l7(n) == series.fermat_lucas(n)

    def testLucas(self):
        assert series.lucas(0) == 2
        assert series.lucas(1) == x
        assert series.lucas(2) == x**2 + 2
        assert series.lucas(3) == x**3 + 3*x
        assert series.lucas(4) == x**4 + 4*x**2 + 2
        assert series.lucas(5) == x**5 + 5*x**3 + 5*x

    def testPell(self):
        assert series.pell(0) == NULL
        assert series.pell(1) == ONE
        assert series.pell(2) == 2*x
        assert series.pell(3) == 4*x**2 + 1
        assert series.pell(4) == 8*x**3 + 4*x
        assert series.pell(5) == 16*x**4 + 12*x**2 + 1

    def testPellLucas(self):
        assert series.pell_lucas(0) == TWO
        assert series.pell_lucas(1) == 2*x
        assert series.pell_lucas(2) == 4*x**2 + 2
        assert series.pell_lucas(3) == 8*x**3 + 6*x
        assert series.pell_lucas(4) == 16*x**4 + 16*x**2 + 2
        assert series.pell_lucas(5) == 32*x**5 + 40*x**3 + 10*x

    def testJacobsthal(self):
        assert series.jacobsthal(0) == NULL
        assert series.jacobsthal(1) == ONE
        assert series.jacobsthal(2) == ONE
        assert series.jacobsthal(3) == 2*x + 1
        assert series.jacobsthal(4) == 4*x + 1
        assert series.jacobsthal(5) == 4*x**2 + 6*x + 1

    def testJacobsthalLucas(self):
        assert series.jacob_lucas(0) == TWO
        assert series.jacob_lucas(1) == ONE
        assert series.jacob_lucas(2) == 4*x + 1
        assert series.jacob_lucas(3) == 6*x + 1
        assert series.jacob_lucas(4) == 8*x**2 + 8*x + 1
        assert series.jacob_lucas(5) == 20*x**2 + 10*x + 1

    def testFermat(self):
        assert series.fermat(0) == NULL
        assert series.fermat(1) == ONE
        assert series.fermat(2) == 3*x
        assert series.fermat(3) == 9*x**2 - 2
        assert series.fermat(4) == 27*x**3 - 12*x
        assert series.fermat(5) == 81*x**4 - 54*x**2 + 4

    def testFermatLucas(self):
        assert series.fermat_lucas(0) == TWO
        assert series.fermat_lucas(1) == 3*x
        assert series.fermat_lucas(2) == 9*x**2 - 4
        assert series.fermat_lucas(3) == 27*x**3 - 18*x
        assert series.fermat_lucas(4) == 81*x**4 - 72*x**2 + 8
        assert series.fermat_lucas(5) == 243*x**5 - 270*x**3 + 60*x

    def testHermite_prob(self):
        assert series.hermite_prob(1) == x
        assert series.hermite_prob(2) == x**2 - 1
        assert series.hermite_prob(3) == x**3 - 3*x
        assert series.hermite_prob(4) == x**4 - 6*x**2 + 3

    def testHermite_phys(self):
        assert series.hermite_phys(0) == 1
        assert series.hermite_phys(1) == 2*x
        assert series.hermite_phys(2) == 4*x**2 - 2
        assert series.hermite_phys(3) == 8*x**3 - 12*x
        assert series.hermite_phys(4) == 16*x**4 - 48*x**2 + 12

    def testChebyshev_t(self):
        assert series.chebyshev_t(0) == 1
        assert series.chebyshev_t(1) == x
        assert series.chebyshev_t(2) == 2*x**2 - 1
        assert series.chebyshev_t(3) == 4*x**3 - 3*x
        assert series.chebyshev_t(4) == 8*x**4 - 8*x**2 + 1
        assert series.chebyshev_t(5) == 16*x**5 - 20*x**3 + 5*x

    def testChebyshev_u(self):
        assert series.chebyshev_u(0) == 1
        assert series.chebyshev_u(1) == 2*x
        assert series.chebyshev_u(2) == 4*x**2 - 1
        assert series.chebyshev_u(3) == 8*x**3 - 4*x
        assert series.chebyshev_u(4) == 16*x**4 - 12*x**2 + 1
        assert series.chebyshev_u(5) == 32*x**5 - 32*x**3 + 6*x

    def testAbel(self):
        assert series.abel(0) == 1
        assert series.abel(1) == x
        assert series.abel(2) == x**2 - 2*a*x
        assert series.abel(3) == x**3 - 6*a*x**2 + 9*a**2*x
        assert series.abel(4) == x**4 - 12*a*x**3 + 48*a**2*x**2 - 64*a**3*x

    def testTouchard(self):
        assert series.touchard(0) == ONE
        assert series.touchard(1) == x
        assert series.touchard(2) == x**2 + x
        assert series.touchard(3) == x**3 + 3*x**2 + x
        assert series.touchard(4) == x**4 + 6*x**3 + 7*x**2 + x
        assert series.touchard(5) == x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x

    def testBell(self):
        py.test.raises(ValueError, series.bell, -1)
        assert series.bell(0) == ONE
        assert series.bell(1) == x
        assert series.bell(2) == x**2 + x
        assert series.bell(3) == x**3 + 3*x**2 + x
        assert series.bell(4) == x**4 + 6*x**3 + 7*x**2 + x
        assert series.bell(5) == x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x
        assert series.bell(6) == x**6 + 15*x**5 + 65*x**4 + 90*x**3 + 31*x**2 + x

    def testGegenbauer(self):
        assert series.gegenbauer(0) == ONE
        assert series.gegenbauer(1) == 2*a*x
        assert series.gegenbauer(2) == -a + 2*a * (1 + a) * x**2
        assert series.gegenbauer(3) == -2*a * (1 + a)*x + fractions.Fraction(4, 3)*a * (1 + a) * (2 + a) * x**3

    def testLaguerre(self):
        assert series.laguerre(0) == ONE
        assert series.laguerre(1) == ONE - x
        assert series.laguerre(2) == fractions.Fraction(1, 2) * (x ** 2 - 4*x + 2)
        assert series.laguerre(3) == fractions.Fraction(1, 6) * (-x**3 + 9*x**2 - 18*x + 6)

    def testGeneralizedLaguerre(self):
        assert series.laguerre_g(0) == ONE
        assert series.laguerre_g(1) == -x + a + 1
        assert series.laguerre_g(2) == fractions.Fraction(1, 2) * (x ** 2 - 2*(a + 2)*x + (a + 1) * (a + 2))
        assert series.laguerre_g(3) == fractions.Fraction(1, 6) * (-x**3 + 3*(a + 3)*x**2 - 3*(a + 2) * (a + 3)*x + (a + 1) * (a + 2) * (a + 3))

    def testBernoulli(self):
        py.test.raises(ValueError, series.bernoulli, -1)
        assert series.bernoulli(0) == ONE
        assert series.bernoulli(1) == x - fractions.Fraction(1, 2)
        assert series.bernoulli(2) == x**2 - x + fractions.Fraction(1, 6)
        assert series.bernoulli(3) == x**3 - fractions.Fraction(3, 2)*x**2 + fractions.Fraction(1, 2)*x
        assert series.bernoulli(4) == x**4 - 2*x**3 + x**2 - fractions.Fraction(1, 30)
        assert series.bernoulli(5) == x**5 - fractions.Fraction(5, 2)*x**4 + fractions.Fraction(5, 3)*x**3 - fractions.Fraction(1, 6)*x
        assert series.bernoulli(6) == x**6 - 3*x**5 + fractions.Fraction(5, 2)*x**4 - fractions.Fraction(1, 2)*x**2 + fractions.Fraction(1, 42)

    def testBernoulliNumbers(self):
        py.test.raises(ValueError, series.bern_num, -1)
        assert not series.bern_num(3)
        assert series.bern_num(0) == 1
        assert series.bern_num(1) == fractions.Fraction(-1, 2)
        assert series.bern_num(2) == fractions.Fraction(1, 6)
        assert series.bern_num(4) == fractions.Fraction(-1, 30)
        assert series.bern_num(6) == fractions.Fraction(1, 42)
        assert series.bern_num(8) == fractions.Fraction(-1, 30)
        assert series.bern_num(10) == fractions.Fraction(5, 66)
        assert series.bern_num(12) == fractions.Fraction(-691, 2730)
        assert series.bern_num(14) == fractions.Fraction(7, 6)
        assert series.bern_num(16) == fractions.Fraction(-3617, 510)
        assert series.bern_num(18) == fractions.Fraction(43867, 798)

    def testEuler(self):
        py.test.raises(ValueError, series.euler, -1)
        assert series.euler(0) == ONE
        assert series.euler(1) == x - .5
        assert series.euler(2) == x**2 - x
        assert series.euler(3) == x**3 - fractions.Fraction(3, 2)*x**2 + .25
        assert series.euler(4) == x**4 - 2*x**3 + x

    def testEulerNumbers(self):
        py.test.raises(ValueError, series.euler_num, -1)
        assert series.euler_num(0) == 1
        assert series.euler_num(1) == 0
        assert series.euler_num(2) == -1
        assert series.euler_num(4) == 5
        assert series.euler_num(6) == -61
        assert series.euler_num(8) == 1385
        assert series.euler_num(10) == -50521

    def testGenocchi(self):
        py.test.raises(ValueError, series.genocchi, -1)
        assert series.genocchi(0) == 0
        assert series.genocchi(1) == 1
        assert series.genocchi(2) == -1
        assert series.genocchi(4) == 1
        assert series.genocchi(6) == -3
        assert series.genocchi(8) == 17

if __name__ == '__main__':
    import sys
    import os.path
    py.test.main(args=[os.path.abspath(__file__)] + sys.argv[1:])