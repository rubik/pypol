#import nose
#from nose.tools import *

import fractions

import pypol
import pypol.funcs as funcs
from pypol import ONE, x

a = pypol.monomial(a=1)

class TestFuncs(object):
    def setUp(self):
        pass

    def testDivisible(self):
        p = pypol.poly1d([2, 6, -4, 8])*x
        assert_true(funcs.divisible(p, p.gcd))

    def testRandomPoly(self):
        for _ in xrange(1000):
            assert_equal(type(funcs.random_poly()), pypol.Polynomial)

        poly1, poly2, poly3 = funcs.random_poly(letters='x', right_hand_side=False, not_null=True), \
                              funcs.random_poly(unique=True, right_hand_side=False, not_null=True), \
                              funcs.random_poly(not_null=True)

        assert poly1
        assert poly2
        assert poly3
        assert_equal(('x',), poly1.letters)
        assert_true(poly2.letters[0] in ('x', 'y', 'z'))
        assert_true(all(-10 <= c < 11 for c in poly3.coefficients))
        pass

    def testPolyder(self):
        p = pypol.poly1d([1]*4)
        assert_equal(pypol.poly1d([3, 2, 1]), funcs.polyder(p))
        assert_equal(pypol.poly1d([6, 2]), funcs.polyder(p, 2))
        assert_equal(pypol.poly1d([6]), funcs.polyder(p, 3))

    def testPolyint(self):
        pass

    def testInterpolation(self):
        pass

    def testBinCoeff(self):
        pass

    def testHarmonic(self):
        assert_raises(ValueError, funcs.harmonic, -1)
        assert_raises(ValueError, funcs.harmonic, 0)
        assert_equal(funcs.harmonic(1), fractions.Fraction(1, 1))
        assert_equal(funcs.harmonic(2), fractions.Fraction(3, 2))
        assert_equal(funcs.harmonic(3), fractions.Fraction(11, 6))
        assert_equal(funcs.harmonic(4), fractions.Fraction(25, 12))
        assert_equal(funcs.harmonic(5), fractions.Fraction(137, 60))
        assert_equal(funcs.harmonic(6), fractions.Fraction(49, 20))
        assert_equal(funcs.harmonic(7), fractions.Fraction(363, 140))
        assert_equal(funcs.harmonic(8), fractions.Fraction(761, 280))
        assert_equal(funcs.harmonic(9), fractions.Fraction(7129, 2520))
        assert_equal(funcs.harmonic(10), fractions.Fraction(7381, 2520))

    def testGeneralizedHarmonic(self):
        pass

    def testStirling(self):
        pass

    def testStirling2(self):
        pass

    def testPochammer(self):
        assert_equal(funcs.pochammer(0), ONE)
        assert_equal(funcs.pochammer(1), x)
        assert_equal(funcs.pochammer(2), x**2 + x)
        assert_equal(funcs.pochammer(3), x**3 + 3*x**2 + 2*x)
        assert_equal(funcs.pochammer(4), x**4 + 6*x**3 + 11*x**2 + 6*x)

    def testFactorialPower(self):
        assert_equal(funcs.factorial_power(0), ONE)
        assert_equal(funcs.factorial_power(1), x)
        assert_equal(funcs.factorial_power(2), x**2 - x)
        assert_equal(funcs.factorial_power(3), x**3 - 3*x**2 + 2*x)
        assert_equal(funcs.factorial_power(4), x**4 - 6*x**3 + 11*x**2 - 6*x)


if __name__ == '__main__':
    nose.runmodule()