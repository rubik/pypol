#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
import operator
import copy
import pypol

class PolynomialTestCase(unittest.TestCase):
    def setUp(self):
        self.a = pypol.polynomial('x^3 - 2x^2 + x -5')
        self.b = pypol.polynomial('a^3 - 2x^2 - b + 3')
        self.c = pypol.polynomial('-x + 1')
        self.d = pypol.polynomial('a')

    def testAdd(self):
        self.assertEqual(pypol.polynomial('x^3 + x + a^3 - 4x^2 - b - 2'), self.a + self.b)
        self.assertEqual(pypol.polynomial('x^3 - 2x^2 + x - 6'), self.a + -1)
        self.assertEqual(pypol.polynomial('x^3 - 2x^2 + x - 5 + y^2'), self.a + 'y^2')
        self.assertRaises(TypeError, operator.add, self.a, [])

    def testSub(self):
        self.assertEqual(pypol.polynomial('x^3 - a^3  + x + b - 8'), self.a - self.b)
        self.assertEqual(pypol.polynomial('x^3 - 2x^2 + x - 7'), self.a - 2)
        self.assertEqual(pypol.polynomial('x^3 - 2x^2 + x - 5 - y^2'), self.a - 'y^2')
        self.assertRaises(TypeError, operator.sub, self.a, [])

    def testMul(self):
        self.assertEqual(pypol.polynomial('x^3a - 2x^2a + xa - 5a'), self.a * self.d)
        self.assertEqual(pypol.polynomial('x^3a^3 - 2x^5 - x^3b - 2x^2a^3 + 4x^4 + 2x^2b + xa^3 + x^3 - xb + 3x - 5a^3 + 4x^2 + 5b - 15'), self.a * self.b)
        self.assertRaises(TypeError, operator.mul, self.d, [])

    def testDivmod(self):
        self.assertEqual((pypol.polynomial('- x^2 + x'), pypol.polynomial('- 5')), divmod(self.a, self.c))

    def testDiv(self):
        self.assertEqual(pypol.polynomial('- x^2 + x'), self.a / self.c)

    def testMod(self):
        p = pypol.polynomial('x^2 + 3')
        self.assertEqual(pypol.polynomial('4'), p % self.c)

    def testTruediv(self):
        pass

    def testPow(self):
        self.assertEqual(pypol.polynomial('x^2 -2x + 1'), self.c ** 2)

    def testOrderedMonomials(self):
        self.assertEqual([(-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})], \
                        self.b.ordered_monomials(key=self.b._key('x'), reverse=True))

    def testSort(self):
        self.b.sort(key=self.b._key('x'), reverse=True)
        self.assertEqual(((-2, {'x': 2}), (1, {'a': 3}), (-1, {'b': 1}), (3, {})), self.b.monomials)

    def testGcd(self):
        pass

    def testLcm(self):
        pass

    def testCoeffGcd(self):
        pass

    def testCoeffLcm(self):
        pass

    def testIsSquareDiff(self):
        self.assertTrue(pypol.polynomial('a6 - 9').is_square_diff())
        self.assertTrue(pypol.polynomial('a2 - 9').is_square_diff())
        self.assertFalse(pypol.polynomial('a').is_square_diff())
        self.assertFalse(pypol.polynomial('a2').is_square_diff())
        self.assertFalse(pypol.polynomial('a2 - 3').is_square_diff())
        self.assertFalse(pypol.polynomial('a2 + 9').is_square_diff())
        self.assertFalse(pypol.polynomial('a6 + 9').is_square_diff())
        self.assertFalse(pypol.polynomial('a6 - 6').is_square_diff())
        self.assertFalse(self.a.is_square_diff())

    def testDivAll(self):
        self.assertEqual(pypol.polynomial('2x^3 + 4xy - 16').div_all(-2), pypol.polynomial('- x^3 - 2xy + 8'))

    def testLetters(self):
        self.assertEqual(('a', 'b', 'x'), self.b.letters)
        self.assertEqual((), pypol.polynomial().letters)

    def testJointLetters(self):
        self.assertEqual(('a',), self.d.joint_letters)
        self.assertEqual((), self.a.joint_letters)

    def testEvalForm(self):
        self.assertEqual('2*y**5*x**3-4*x**2+2', pypol.polynomial('2x^3y^5 - 4x^2 +2').eval_form)

    def testZeros(self):
        self.assertEqual((1,), self.c.zeros)
        self.assertEqual((), self.a.zeros)
        self.assertEqual(NotImplemented, self.b.zeros)

    def testRawPowers(self):
        self.assertEqual([3, 0, 0, 0], self.b.raw_powers('a'))

    def testPowers(self):
        self.assertEqual([3, 0], self.b.powers('a'))

    def testLinear(self):
        self.assertFalse(self.a.islinear())
        self.assertTrue(self.c.islinear())

    def testOrdered(self):
        self.assertTrue(pypol.polynomial('4a3+6a2+4a+5').isordered())
        self.assertTrue(pypol.polynomial('4a3+6a2+4a+5').isordered('a'))
        self.assertFalse(pypol.polynomial('a3+b3+c+ab ').isordered())
        self.assertFalse(pypol.polynomial('a3+b3+c+ab ').isordered('a'))
        self.assertFalse(pypol.polynomial('a3+b3+c+ab ').isordered('b'))

    def testComplete(self):
        self.assertTrue(self.c.iscomplete('x'))
        self.assertFalse(self.b.iscomplete('x'))

    def testUpdate(self):
        self.d.update('3x - y + 2')
        self.assertEqual(pypol.polynomial('3x - y + 2'), self.d)

    def testEq(self):
        self.assertTrue(pypol.polynomial('x^3 - 2x^2 + x - 5') == self.a)

    def testNe(self):
        self.assertTrue(self.a != self.b)
        self.assertFalse(self.c != self.c)

    def testPos(self):
        self.assertEqual(self.a, +self.a)

    def testNeg(self):
        self.assertEqual(pypol.polynomial('x - 1'), -self.c)

    def testLen(self):
        self.assertEqual(4, len(self.a))
        self.assertEqual(1, len(self.d))

    def testNonzero(self):
        p = pypol.polynomial()
        self.assertTrue(self.a)
        self.assertFalse(p)

    def testContains(self):
        self.assertTrue((1, {'x': 3}) in self.a)
        self.assertFalse((1, {'x': 5}) in self.a)

    def testGetitem(self):
        self.assertEqual((1, {'a': 1}), self.d[0])
        self.assertRaises(IndexError, lambda x: self.d[x], 2)

    def testSetitem(self):
        self.a[2] = (3, {'x': 3, 'y': 4})
        self.assertEqual(pypol.polynomial('x^3 + 3x3y4 - 2x^2 -5'), self.a)

    def testDelitem(self):
        del self.a[1:3]
        self.assertEqual(pypol.polynomial('x^3 - 5'), self.a)


class FunctionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def testPolynomial(self):
        self.assertTrue(type(pypol.polynomial()) == pypol.Polynomial)

    def testMakePolynomial(self):
        self.assertEqual(pypol.make_polynomial(((2, {'x': 3}), (-3, {'x': 1, 'y': 1}), (-2, {}))), pypol.polynomial('2x^3 -3xy - 2'))

    def testParsePolynomial(self):
        self.assertEqual([(2, {'x': 3}), (-3, {'x': 1}), (2, {})], pypol.parse_polynomial('2x^3 -3x + 2'))

    def testMonomial(self):
        vars = {'a': 3, 'b': 4}
        m = pypol.monomial(5, **vars)
        self.assertTrue(type(pypol.monomial()) == pypol.Polynomial)
        self.assertEqual(('a', 'b'), m.letters)
        self.assertEqual([5], m.coefficients)

    def testAreSimilar(self):
        self.assertTrue(pypol.are_similar((3, {'x': 2}), (4, {'x': 2})))
        self.assertFalse(pypol.are_similar((2, {'y': 3}), (2, {'y': 2})))

    def testGcd(self):
        pass

    def testLcm(self):
        pass

    def testRandomPoly(self):
        for _ in xrange(100):
            self.assertEqual(pypol.Polynomial, type(pypol.random_poly()))
        self.assertEqual(('x',), pypol.random_poly(letters='x').letters)
        try:
            self.assertTrue(pypol.random_poly(unique=True).letters[0] in ('x', 'y', 'z'))
        except IndexError:  ## random_poly is an empty polynomial
            pass
        self.assertTrue(all(-10 <= c < 11 for c in pypol.random_poly().coefficients))

    def testRoot(self):
        pass


def run():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_cases = [PolynomialTestCase,
                  FunctionsTestCase]
    for cls in test_cases:
        suite.addTest(loader.loadTestsFromTestCase(cls))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
