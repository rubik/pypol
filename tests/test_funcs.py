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

    def testFibonacci(self):
        assert not funcs.fibonacci(0)
        assert_equal(funcs.fibonacci(1), 1)
        assert_equal(funcs.fibonacci(2), x)
        assert_equal(funcs.fibonacci(3), x**2 + 1)
        assert_equal(funcs.fibonacci(4), x**3 + 2*x)
        assert_equal(funcs.fibonacci(5), x**4 + 3 * x**2 + 1)

    def testHermite_prob(self):
        assert_equal(funcs.hermite_prob(1), x)
        assert_equal(funcs.hermite_prob(2), x**2 - 1)
        assert_equal(funcs.hermite_prob(3), x**3 - 3*x)
        assert_equal(funcs.hermite_prob(4), x**4 - 6*x**2 + 3)

    def testHermite_phys(self):
        assert_equal(funcs.hermite_phys(0), 1)
        assert_equal(funcs.hermite_phys(1), 2*x)
        assert_equal(funcs.hermite_phys(2), 4*x**2 - 2)
        assert_equal(funcs.hermite_phys(3), 8*x**3 - 12*x)
        assert_equal(funcs.hermite_phys(4), 16*x**4 - 48*x**2 + 12)

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

    def testLaguerreG(self):
        pass

    def testBernoulli(self):
        pass

    def testBernoulliNumbers(self):
        pass

    def testEuler(self):
        pass

    def testEulerNumbers(self):
        pass

    def testGenocchi(self):
        pass


if __name__ == '__main__':
    nose.runmodule()