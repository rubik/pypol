#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
import operator
import pypol

class PypolTestCase(unittest.TestCase):
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

    def testDiv(self):
        self.assertEqual((pypol.polynomial('- x^2 + x'), pypol.polynomial('- 5')), divmod(self.a, self.c))
        self.assertEqual(pypol.polynomial('- x^2 + x'), self.a / self.c)

    def testMod(self):
        pass

    def testTruediv(self):
        pass

    def testPow(self):
        pass

    def testLetters(self):
        pass

    def testRawPowers(self):
        pass

    def testPowers(self):
        pass

    def testLinear(self):
        pass

    def testOrdered(self):
        pass

    def testComplete(self):
        pass

    def testUpdate(self):
        pass

    def testEq(self):
        pass

    def testNe(self):
        pass

    def testPos(self):
        pass

    def testNeg(self):
        pass

    def testLen(self):
        pass

    def testNonzero(self):
        pass

    def testContains(self):
        pass

    def testGetitem(self):
        pass

    def testSetitem(self):
        pass

    def testDelitem(self):
        pass


if __name__ == '__main__':
    unittest.main()
