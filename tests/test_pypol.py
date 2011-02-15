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

import copy
import operator

import py
import pypol

class TestPolynomial(object):
    def setup_method(self, method):
        self.a = pypol.polynomial('x^3 - 2x^2 + x -5')
        self.b = pypol.polynomial('a^3 - 2x^2 - b + 3')
        self.c = pypol.polynomial('-x + 1')
        self.d = pypol.polynomial('a')

    def testAdd(self):
        assert pypol.polynomial('x^3 + x + a^3 - 4x^2 - b - 2') == self.a + self.b
        assert pypol.polynomial('x^3 - 2x^2 + x - 6') == self.a + -1
        assert pypol.polynomial('x^3 - 2x^2 + x - 5 + y^2') == self.a + 'y^2'

    def testSub(self):
        assert pypol.ONE - pypol.x == self.c
        assert 1 - pypol.x == self.c
        assert pypol.polynomial('x^3 - a^3  + x + b - 8') == self.a - self.b
        assert pypol.polynomial('x^3 - 2x^2 + x - 7') == self.a - 2
        assert pypol.polynomial('x^3 - 2x^2 + x - 5 - y^2') == self.a - 'y^2'

    def testMul(self):
        assert pypol.polynomial('x^3a - 2x^2a + xa - 5a') == self.a * self.d
        assert pypol.polynomial('x^3a^3 - 2x^5 - x^3b - 2x^2a^3 + 4x^4 + 2x^2b + xa^3 + x^3 - xb + 3x - 5a^3 + 4x^2 + 5b - 15') == self.a * self.b

    def testDivmod(self):
        assert (pypol.polynomial('- x^2 + x'), pypol.polynomial('- 5')) == divmod(self.a, self.c)

    def testDiv(self):
        assert (2 * pypol.x + 1) / 2 == pypol.polynomial('x + 1/2')
        assert pypol.polynomial('- x^2 + x') == self.a / self.c

    def testMod(self):
        p = pypol.polynomial('x^2 + 3')
        assert pypol.polynomial('4') == p % self.c

    def testTruediv(self):
        pass

    def testDegree(self):
        assert self.a.degree == 3
        assert self.b.degree == 3
        assert self.c.degree == 1
        assert self.d.degree == 1
        assert pypol.NULL.degree == float('-inf')
        assert pypol.ONE.degree == 0

    def testPow(self):
        assert pypol.polynomial('x^2 -2x + 1') == self.c ** 2

    def testOrderedMonomials(self):
        assert [(-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})] == \
                        self.b.ordered_monomials(key=self.b._key('x'), reverse=True)

    def testSort(self):
        self.b.sort(key=self.b._key('x'), reverse=True)
        assert ((-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})) == self.b.monomials

    def testGcd(self):
        assert pypol.polynomial('3x^4 - 9x').gcd() in (pypol.polynomial('3x'), pypol.polynomial('-3x'))

    def testLcm(self):
        assert pypol.polynomial('3x^4 - 9x').lcm() in (pypol.polynomial('9x^4'), pypol.polynomial('-9x^4'))

    def testIsSquareDiff(self):
        assert pypol.polynomial('a6 - 9').is_square_diff()
        assert pypol.polynomial('a2 - 9').is_square_diff()
        assert not pypol.polynomial('a').is_square_diff()
        assert not pypol.polynomial('a2').is_square_diff()
        assert not pypol.polynomial('a2 - 3').is_square_diff()
        assert not pypol.polynomial('a2 + 9').is_square_diff()
        assert not pypol.polynomial('a6 + 9').is_square_diff()
        assert not pypol.polynomial('a6 - 6').is_square_diff()
        assert not self.a.is_square_diff()

    def testDivAll(self):
        assert pypol.polynomial('2x^3 + 4xy - 16').div_all(-2) == pypol.polynomial('- x^3 - 2xy + 8')

    def testLetters(self):
        assert ('a', 'b', 'x') == self.b.letters
        assert () == pypol.polynomial().letters

    def testJointLetters(self):
        assert ('a',) == self.d.joint_letters
        assert () == self.a.joint_letters

    def testEvalForm(self):
        assert '2*y**5*x**3-4*x**2+2' == pypol.polynomial('2x^3y^5 - 4x^2 +2').eval_form

    @ py.test.mark.skipif('__import__("pypol").__version__ >= (0, 4)')
    def testZeros(self):  ## DEPRECATED
        assert (1,) == self.c.zeros
        assert () == self.a.zeros
        assert NotImplemented == self.b.zeros

    def testRawPowers(self):
        assert [3, 0, 0, 0] == self.b.raw_powers('a')
        assert [0, 2, 0, 0] == self.b.raw_powers('x')
        assert [0, 0, 1, 0] == self.b.raw_powers('b')
        assert {'a': [3, 0, 0, 0], 'x': [0, 2, 0, 0], 'b': [0, 0, 1, 0]} == self.b.raw_powers()
        self.b.append('-3x^3')
        assert {'a': [3, 0, 0, 0, 0], 'x': [0, 3, 2, 0, 0], 'b': [0, 0, 0, 1, 0]} == self.b.raw_powers()
        del self.b[-1]
        assert {'a': [3, 0, 0, 0], 'x': [0, 3, 2, 0], 'b': [0, 0, 0, 1]} == self.b.raw_powers()

    def testPowers(self):
        assert [3, 0] == self.b.powers('a')
        assert [2, 0] == self.b.powers('x')
        assert [1, 0] == self.b.powers('b')
        self.b.append('-3x^3')
        assert {'a': [3, 0], 'x': [3, 2, 0], 'b': [1, 0]} == self.b.powers()
        del self.b[-1]
        assert {'a': [3, 0], 'x': [3, 2, 0], 'b': [1]} == self.b.powers()

    def testLinear(self):
        assert not self.a.islinear()
        assert self.c.islinear()

    def testOrdered(self):
        assert pypol.polynomial('4a3+6a2+4a+5').isordered()
        assert pypol.polynomial('4a3+6a2+4a+5').isordered('a')
        assert not pypol.polynomial('a3+b3+c+ab ').isordered()
        assert not pypol.polynomial('a3+b3+c+ab ').isordered('a')
        assert not pypol.polynomial('a3+b3+c+ab ').isordered('b')

    def testComplete(self):
        assert self.c.iscomplete('x')
        assert not self.b.iscomplete('x')

    def testFromRoots(self):
        p = pypol.Polynomial.from_roots([1, -3, 44, 45245, -2332])
        assert map(p, [1, -3, 44, 45245, -2332]) == [0, 0, 0, 0, 0]
        assert pypol.Polynomial.from_roots([1, -2, 3], 'o').letters == ('o',)

    def testUpdate(self):
        self.d.update('3x - y + 2')
        assert pypol.polynomial('3x - y + 2') == self.d

    def testEq(self):
        assert pypol.polynomial('x^3 - 2x^2 + x - 5') == self.a

    def testNe(self):
        assert self.a != self.b
        assert not self.c != self.c

    def testPos(self):
        assert self.a == +self.a

    def testNeg(self):
        assert pypol.polynomial('x - 1') == -self.c

    def testLen(self):
        assert 4 == len(self.a)
        assert 1 == len(self.d)
        assert 0 == len(pypol.NULL)

    def testNonzero(self):
        p = pypol.polynomial()
        assert self.a
        assert not p

    def testContains(self):
        assert (1, {'x': 3}) in self.a
        assert not (1, {'x': 5}) in self.a

    def testGetitem(self):
        assert (1, {'a': 1}) == pypol.polynomial('a')[0]
        py.test.raises(IndexError, lambda: pypol.polynomial('a')[2])

    def testSetitem(self):
        self.a[2] = (3, {'x': 3, 'y': 4})
        assert pypol.polynomial('x^3 + 3x3y4 - 2x^2 -5') == self.a

    def testDelitem(self):
        del self.a[1:3]
        assert pypol.polynomial('x^3 - 5') == self.a


class TestFunctions(object):
    def testPolynomial(self):
        assert type(pypol.polynomial()) == pypol.Polynomial

    def testParsePolynomial(self):
        assert [(2, {'x': 3}), (-3, {'x': 1}), (2, {})] == pypol.parse_polynomial('2x^3 -3x + 2')

    def testMonomial(self):
        vars = {'a': 3, 'b': 4}
        m = pypol.monomial(5, **vars)
        assert type(pypol.monomial()) == pypol.Polynomial
        assert ('a', 'b') == m.letters
        assert [5] == m.coefficients

    def testAreSimilar(self):
        assert pypol.are_similar((3, {'x': 2}), (4, {'x': 2}))
        assert not pypol.are_similar((2, {'y': 3}), (2, {'y': 2}))

    def testGcd(self):
        x = pypol.x
        assert pypol.gcd(3*x, 6*x**2) == 3*x

    def testLcm(self):
        x = pypol.x
        assert pypol.lcm(3*x, 6*x**2) == 6*x**2

if __name__ == '__main__':
    import sys
    import os.path
    py.test.main(args=[os.path.abspath(__file__)] + sys.argv[1:])