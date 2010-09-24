#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import nose
from nose.tools import *
import operator
import copy
import pypol

class TestPolynomial(object):
    def setUp(self):
        self.a = pypol.polynomial('x^3 - 2x^2 + x -5')
        self.b = pypol.polynomial('a^3 - 2x^2 - b + 3')
        self.c = pypol.polynomial('-x + 1')
        self.d = pypol.polynomial('a')

    def testAdd(self):
        assert_equal(pypol.polynomial('x^3 + x + a^3 - 4x^2 - b - 2'), self.a + self.b)
        assert_equal(pypol.polynomial('x^3 - 2x^2 + x - 6'), self.a + -1)
        assert_equal(pypol.polynomial('x^3 - 2x^2 + x - 5 + y^2'), self.a + 'y^2')
        assert_raises(TypeError, operator.add, self.a, [])

    def testSub(self):
        assert_equal(pypol.polynomial('x^3 - a^3  + x + b - 8'), self.a - self.b)
        assert_equal(pypol.polynomial('x^3 - 2x^2 + x - 7'), self.a - 2)
        assert_equal(pypol.polynomial('x^3 - 2x^2 + x - 5 - y^2'), self.a - 'y^2')
        assert_raises(TypeError, operator.sub, self.a, [])

    def testMul(self):
        assert_equal(pypol.polynomial('x^3a - 2x^2a + xa - 5a'), self.a * self.d)
        assert_equal(pypol.polynomial('x^3a^3 - 2x^5 - x^3b - 2x^2a^3 + 4x^4 + 2x^2b + xa^3 + x^3 - xb + 3x - 5a^3 + 4x^2 + 5b - 15'), self.a * self.b)
        assert_raises(TypeError, operator.mul, self.d, [])

    def testDivmod(self):
        assert_equal((pypol.polynomial('- x^2 + x'), pypol.polynomial('- 5')), divmod(self.a, self.c))

    def testDiv(self):
        assert_equal(pypol.polynomial('- x^2 + x'), self.a / self.c)

    def testMod(self):
        p = pypol.polynomial('x^2 + 3')
        assert_equal(pypol.polynomial('4'), p % self.c)

    def testTruediv(self):
        pass

    def testPow(self):
        assert_equal(pypol.polynomial('x^2 -2x + 1'), self.c ** 2)

    def testOrderedMonomials(self):
        assert_equal([(-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})], \
                        self.b.ordered_monomials(key=self.b._key('x'), reverse=True))

    def testSort(self):
        self.b.sort(key=self.b._key('x'), reverse=True)
        assert_equal(((-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})), self.b.monomials)

    def testGcd(self):
        pass

    def testLcm(self):
        pass

    def testCoeffGcd(self):
        pass

    def testCoeffLcm(self):
        pass

    def testIsSquareDiff(self):
        assert_true(pypol.polynomial('a6 - 9').is_square_diff())
        assert_true(pypol.polynomial('a2 - 9').is_square_diff())
        assert_false(pypol.polynomial('a').is_square_diff())
        assert_false(pypol.polynomial('a2').is_square_diff())
        assert_false(pypol.polynomial('a2 - 3').is_square_diff())
        assert_false(pypol.polynomial('a2 + 9').is_square_diff())
        assert_false(pypol.polynomial('a6 + 9').is_square_diff())
        assert_false(pypol.polynomial('a6 - 6').is_square_diff())
        assert_false(self.a.is_square_diff())

    def testDivAll(self):
        assert_equal(pypol.polynomial('2x^3 + 4xy - 16').div_all(-2), pypol.polynomial('- x^3 - 2xy + 8'))

    def testLetters(self):
        assert_equal(('a', 'b', 'x'), self.b.letters)
        assert_equal((), pypol.polynomial().letters)

    def testJointLetters(self):
        assert_equal(('a',), self.d.joint_letters)
        assert_equal((), self.a.joint_letters)

    def testEvalForm(self):
        assert_equal('2*y**5*x**3-4*x**2+2', pypol.polynomial('2x^3y^5 - 4x^2 +2').eval_form)

    def testZeros(self):
        assert_equal((1,), self.c.zeros)
        assert_equal((), self.a.zeros)
        assert_equal(NotImplemented, self.b.zeros)

    def testRawPowers(self):
        assert_equal([3, 0, 0, 0], self.b.raw_powers('a'))

    def testPowers(self):
        assert_equal([3, 0], self.b.powers('a'))

    def testLinear(self):
        assert_false(self.a.islinear())
        assert_true(self.c.islinear())

    def testOrdered(self):
        assert_true(pypol.polynomial('4a3+6a2+4a+5').isordered())
        assert_true(pypol.polynomial('4a3+6a2+4a+5').isordered('a'))
        assert_false(pypol.polynomial('a3+b3+c+ab ').isordered())
        assert_false(pypol.polynomial('a3+b3+c+ab ').isordered('a'))
        assert_false(pypol.polynomial('a3+b3+c+ab ').isordered('b'))

    def testComplete(self):
        assert_true(self.c.iscomplete('x'))
        assert_false(self.b.iscomplete('x'))

    def testUpdate(self):
        self.d.update('3x - y + 2')
        assert_equal(pypol.polynomial('3x - y + 2'), self.d)

    def testEq(self):
        assert_true(pypol.polynomial('x^3 - 2x^2 + x - 5') == self.a)

    def testNe(self):
        assert_true(self.a != self.b)
        assert_false(self.c != self.c)

    def testPos(self):
        assert_equal(self.a, +self.a)

    def testNeg(self):
        assert_equal(pypol.polynomial('x - 1'), -self.c)

    def testLen(self):
        assert_equal(4, len(self.a))
        assert_equal(1, len(self.d))

    def testNonzero(self):
        p = pypol.polynomial()
        assert_true(self.a)
        assert_false(p)

    def testContains(self):
        assert_true((1, {'x': 3}) in self.a)
        assert_false((1, {'x': 5}) in self.a)

    def testGetitem(self):
        assert_equal((1, {'a': 1}), self.d[0])
        assert_raises(IndexError, lambda x: self.d[x], 2)

    def testSetitem(self):
        self.a[2] = (3, {'x': 3, 'y': 4})
        assert_equal(pypol.polynomial('x^3 + 3x3y4 - 2x^2 -5'), self.a)

    def testDelitem(self):
        del self.a[1:3]
        assert_equal(pypol.polynomial('x^3 - 5'), self.a)


class TestFunctions(object):
    def setUp(self):
        pass

    def testPolynomial(self):
        assert_true(type(pypol.polynomial()) == pypol.Polynomial)

    def testMakePolynomial(self):
        assert_equal(pypol.make_polynomial(((2, {'x': 3}), (-3, {'x': 1, 'y': 1}), (-2, {}))), pypol.polynomial('2x^3 -3xy - 2'))

    def testParsePolynomial(self):
        assert_equal([(2, {'x': 3}), (-3, {'x': 1}), (2, {})], pypol.parse_polynomial('2x^3 -3x + 2'))

    def testMonomial(self):
        vars = {'a': 3, 'b': 4}
        m = pypol.monomial(5, **vars)
        assert_true(type(pypol.monomial()) == pypol.Polynomial)
        assert_equal(('a', 'b'), m.letters)
        assert_equal([5], m.coefficients)

    def testAreSimilar(self):
        assert_true(pypol.are_similar((3, {'x': 2}), (4, {'x': 2})))
        assert_false(pypol.are_similar((2, {'y': 3}), (2, {'y': 2})))

    def testGcd(self):
        pass

    def testLcm(self):
        pass

    def testRandomPoly(self):
        for _ in xrange(1000):
            assert_equal(pypol.Polynomial, type(pypol.utils.random_poly()))

        poly1, poly2, poly3 = random_poly(letters='x', not_null=True), \
                              random_poly(unique=True, not_null=True), \
                              random_poly(not_null=True)

        assert poly1
        assert poly2
        assert poly3
        assert_equal(('x',), poly1.letters)
        assert_true(poly2.letters[0] in ('x', 'y', 'z'))
        assert_true(all(-10 <= c < 11 for c in poly3.coefficients))

    def testRoot(self):
        pass


def run():
    nose.run()

if __name__ == '__main__':
    run()
