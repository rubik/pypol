import nose
from nose.tools import *

import pypol
import pypol.funcs as funcs

x = pypol.monomial(x=1)
a = pypol.monomial(a=1)

class TestFuncs(object):
    def setUp(self):
        pass

    def testDivisible(self):
        pass

    def testRandomPoly(self):
        for _ in xrange(1000):
            assert_equal(pypol.Polynomial, type(pypol.funcs.random_poly()))

        poly1, poly2, poly3 = pypol.funcs.random_poly(letters='x', right_hand_side=False, not_null=True), \
                              pypol.funcs.random_poly(unique=True, right_hand_side=False, not_null=True), \
                              pypol.funcs.random_poly(not_null=True)

        assert poly1
        assert poly2
        assert poly3
        assert_equal(('x',), poly1.letters)
        assert_true(poly2.letters[0] in ('x', 'y', 'z'))
        assert_true(all(-10 <= c < 11 for c in poly3.coefficients))
        pass

    def testPolyder(self):
        pass

    def testPolyint(self):
        pass

    def testFib_poly(self):
        assert not funcs.fib_poly(0)
        assert_equal(funcs.fib_poly(1), 1)
        assert_equal(funcs.fib_poly(2), x)
        assert_equal(funcs.fib_poly(3), x**2 + 1)
        assert_equal(funcs.fib_poly(4), x**3 + 2*x)
        assert_equal(funcs.fib_poly(5), x**4 + 3 * x**2 + 1)

    def testFib_poly_r(self):
        assert not funcs.fib_poly_r(0)
        assert_equal(funcs.fib_poly_r(1), 1)
        assert_equal(funcs.fib_poly_r(2), x)
        assert_equal(funcs.fib_poly_r(3), x**2 + 1)
        assert_equal(funcs.fib_poly_r(4), x**3 + 2*x)
        assert_equal(funcs.fib_poly_r(5), x**4 + 3 * x**2 + 1)
        assert_equal(funcs.fib_poly(11), funcs.fib_poly_r(11))

    def testHermite_prob(self):
        assert_equal(funcs.hermite_prob(1), x)
        assert_equal(funcs.hermite_prob(2), x**2 - 1)
        assert_equal(funcs.hermite_prob(3), x**3 - 3*x)
        assert_equal(funcs.hermite_prob(4), x**4 - 6*x**2 + 3)

    def testHermite_prob_r(self):
        assert_equal(funcs.hermite_prob_r(1), x)
        assert_equal(funcs.hermite_prob_r(2), x**2 - 1)
        assert_equal(funcs.hermite_prob_r(3), x**3 - 3*x)
        assert_equal(funcs.hermite_prob_r(4), x**4 - 6*x**2 + 3)
        assert_equal(funcs.hermite_prob(13), funcs.hermite_prob_r(13))

    def testHermite_phys(self):
        assert_equal(funcs.hermite_phys(0), 1)
        assert_equal(funcs.hermite_phys(1), 2*x)
        assert_equal(funcs.hermite_phys(2), 4*x**2 - 2)
        assert_equal(funcs.hermite_phys(3), 8*x**3 - 12*x)
        assert_equal(funcs.hermite_phys(4), 16*x**4 - 48*x**2 + 12)

    def testHermite_phys_r(self):
        assert_equal(funcs.hermite_phys_r(0), 1)
        assert_equal(funcs.hermite_phys_r(1), 2*x)
        assert_equal(funcs.hermite_phys_r(2), 4*x**2 - 2)
        assert_equal(funcs.hermite_phys_r(3), 8*x**3 - 12*x)
        assert_equal(funcs.hermite_phys_r(4), 16*x**4 - 48*x**2 + 12)
        assert_equal(funcs.hermite_phys(12), funcs.hermite_phys_r(12))

    def testChebyshev_t(self):
        assert_equal(funcs.chebyshev_t(0), 1)
        assert_equal(funcs.chebyshev_t(1), x)
        assert_equal(funcs.chebyshev_t(2), 2*x**2 - 1)
        assert_equal(funcs.chebyshev_t(3), 4*x**3 - 3*x)
        assert_equal(funcs.chebyshev_t(4), 8*x**4 - 8*x**2 + 1)
        assert_equal(funcs.chebyshev_t(5), 16*x**5 - 20*x**3 + 5*x)

    def testChebyshev_u(self):
        assert_equal(funcs.chebyshev_u(0), 1)
        assert_equal(funcs.chebyshev_u(1), 2*x)
        assert_equal(funcs.chebyshev_u(2), 4*x**2 - 1)
        assert_equal(funcs.chebyshev_u(3), 8*x**3 - 4*x)
        assert_equal(funcs.chebyshev_u(4), 16*x**4 - 12*x**2 + 1)
        assert_equal(funcs.chebyshev_u(5), 32*x**5 - 32*x**3 + 6*x)

    def testAbel(self):
        assert_equal(funcs.abel(0), 1)
        assert_equal(funcs.abel(1), x)
        assert_equal(funcs.abel(2), x**2 - 2*a*x)
        assert_equal(funcs.abel(3), x**3 - 6*a*x**2 + 9*a**2*x)
        assert_equal(funcs.abel(4), x**4 - 12*a*x**3 + 48*a**2*x**2 - 64*a**3*x)

    def testGegenbauer(self):
        pass

    def testLaguerre(self):
        pass


if __name__ == '__main__':
    nose.runmodule()