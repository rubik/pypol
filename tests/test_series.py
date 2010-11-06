import nose
from nose.tools import *

import fractions

import pypol
import pypol.series as series

x = pypol.monomial(x=1)
a = pypol.monomial(a=1)
NULL = pypol.Polynomial()
ONE = pypol.monomial()
TWO = pypol.monomial(2)

class TestSeries(object):
    def setUp(self):
        pass

    def testFibonacci(self):
        assert_raises(ValueError, series.fibonacci, 0)
        assert_equal(series.fibonacci(1), ONE)
        assert_equal(series.fibonacci(2), x)
        assert_equal(series.fibonacci(3), x**2 + 1)
        assert_equal(series.fibonacci(4), x**3 + 2*x)
        assert_equal(series.fibonacci(5), x**4 + 3 * x**2 + 1)

    def testLucasSequence(self):
        for n in xrange(10):
            if n > 0:
                assert_equal(series.lucas_seq(n, x, ONE), series.fibonacci(n))
            assert_equal(series.lucas_seq(n, x, ONE, TWO, x), series.lucas(n))
            assert_equal(series.lucas_seq(n, 2*x, ONE), series.pell(n))
            assert_equal(series.lucas_seq(n, 2*x, ONE, TWO, 2*x), series.pell_lucas(n))
            assert_equal(series.lucas_seq(n, ONE, 2*x), series.jacobsthal(n))
            assert_equal(series.lucas_seq(n, ONE, 2*x, TWO, ONE), series.jacob_lucas(n))
            assert_equal(series.lucas_seq(n, 3*x, -TWO), series.fermat(n))
            assert_equal(series.lucas_seq(n, 3*x, -TWO, TWO, 3*x), series.fermat_lucas(n))

    def testLucas(self):
        assert_equal(series.lucas(0), 2)
        assert_equal(series.lucas(1), x)
        assert_equal(series.lucas(2), x**2 + 2)
        assert_equal(series.lucas(3), x**3 + 3*x)
        assert_equal(series.lucas(4), x**4 + 4*x**2 + 2)
        assert_equal(series.lucas(5), x**5 + 5*x**3 + 5*x)

    def testPell(self):
        assert_equal(series.pell(0), NULL)
        assert_equal(series.pell(1), ONE)
        assert_equal(series.pell(2), 2*x)
        assert_equal(series.pell(3), 4*x**2 + 1)
        assert_equal(series.pell(4), 8*x**3 + 4*x)
        assert_equal(series.pell(5), 16*x**4 + 12*x**2 + 1)

    def testPellLucas(self):
        assert_equal(series.pell_lucas(0), TWO)
        assert_equal(series.pell_lucas(1), 2*x)
        assert_equal(series.pell_lucas(2), 4*x**2 + 2)
        assert_equal(series.pell_lucas(3), 8*x**3 + 6*x)
        assert_equal(series.pell_lucas(4), 16*x**4 + 16*x**2 + 2)
        assert_equal(series.pell_lucas(5), 32*x**5 + 40*x**3 + 10*x)

    def testJacobsthal(self):
        assert_equal(series.jacobsthal(0), NULL)
        assert_equal(series.jacobsthal(1), ONE)
        assert_equal(series.jacobsthal(2), ONE)
        assert_equal(series.jacobsthal(3), 2*x + 1)
        assert_equal(series.jacobsthal(4), 4*x + 1)
        assert_equal(series.jacobsthal(5), 4*x**2 + 6*x + 1)

    def testJacobsthalLucas(self):
        assert_equal(series.jacob_lucas(0), TWO)
        assert_equal(series.jacob_lucas(1), ONE)
        assert_equal(series.jacob_lucas(2), 4*x + 1)
        assert_equal(series.jacob_lucas(3), 6*x + 1)
        assert_equal(series.jacob_lucas(4), 8*x**2 + 8*x + 1)
        assert_equal(series.jacob_lucas(5), 20*x**2 + 10*x + 1)

    def testFermat(self):
        assert_equal(series.fermat(0), NULL)
        assert_equal(series.fermat(1), ONE)
        assert_equal(series.fermat(2), 3*x)
        assert_equal(series.fermat(3), 9*x**2 - 2)
        assert_equal(series.fermat(4), 27*x**3 - 12*x)
        assert_equal(series.fermat(5), 81*x**4 - 54*x**2 + 4)

    def testFermatLucas(self):
        assert_equal(series.fermat_lucas(0), TWO)
        assert_equal(series.fermat_lucas(1), 3*x)
        assert_equal(series.fermat_lucas(2), 9*x**2 - 4)
        assert_equal(series.fermat_lucas(3), 27*x**3 - 18*x)
        assert_equal(series.fermat_lucas(4), 81*x**4 - 72*x**2 + 8)
        assert_equal(series.fermat_lucas(5), 243*x**5 - 270*x**3 + 60*x)

    def testHermite_prob(self):
        assert_equal(series.hermite_prob(1), x)
        assert_equal(series.hermite_prob(2), x**2 - 1)
        assert_equal(series.hermite_prob(3), x**3 - 3*x)
        assert_equal(series.hermite_prob(4), x**4 - 6*x**2 + 3)

    def testHermite_phys(self):
        assert_equal(series.hermite_phys(0), 1)
        assert_equal(series.hermite_phys(1), 2*x)
        assert_equal(series.hermite_phys(2), 4*x**2 - 2)
        assert_equal(series.hermite_phys(3), 8*x**3 - 12*x)
        assert_equal(series.hermite_phys(4), 16*x**4 - 48*x**2 + 12)

    def testChebyshev_t(self):
        assert_equal(series.chebyshev_t(0), 1)
        assert_equal(series.chebyshev_t(1), x)
        assert_equal(series.chebyshev_t(2), 2*x**2 - 1)
        assert_equal(series.chebyshev_t(3), 4*x**3 - 3*x)
        assert_equal(series.chebyshev_t(4), 8*x**4 - 8*x**2 + 1)
        assert_equal(series.chebyshev_t(5), 16*x**5 - 20*x**3 + 5*x)

    def testChebyshev_u(self):
        assert_equal(series.chebyshev_u(0), 1)
        assert_equal(series.chebyshev_u(1), 2*x)
        assert_equal(series.chebyshev_u(2), 4*x**2 - 1)
        assert_equal(series.chebyshev_u(3), 8*x**3 - 4*x)
        assert_equal(series.chebyshev_u(4), 16*x**4 - 12*x**2 + 1)
        assert_equal(series.chebyshev_u(5), 32*x**5 - 32*x**3 + 6*x)

    def testAbel(self):
        assert_equal(series.abel(0), 1)
        assert_equal(series.abel(1), x)
        assert_equal(series.abel(2), x**2 - 2*a*x)
        assert_equal(series.abel(3), x**3 - 6*a*x**2 + 9*a**2*x)
        assert_equal(series.abel(4), x**4 - 12*a*x**3 + 48*a**2*x**2 - 64*a**3*x)

    def testTouchard(self):
        pass

    def testBell(self):
        assert_raises(ValueError, series.bell, -1)
        assert_equal(series.bell(0), ONE)
        assert_equal(series.bell(1), x)
        assert_equal(series.bell(2), x**2 + x)
        assert_equal(series.bell(3), x**3 + 3*x**2 + x)
        assert_equal(series.bell(4), x**4 + 6*x**3 + 7*x**2 + x)
        assert_equal(series.bell(5), x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x)
        assert_equal(series.bell(6), x**6 + 15*x**5 + 65*x**4 + 90*x**3 + 31*x**2 + x)

    def testGegenbauer(self):
        assert_equal(series.gegenbauer(0), ONE)
        assert_equal(series.gegenbauer(1), 2*a*x)
        assert_equal(series.gegenbauer(2), -a + 2*a * (1 + a) * x**2)
        assert_equal(series.gegenbauer(3), -2*a * (1 + a)*x + fractions.Fraction(4, 3)*a * (1 + a) * (2 + a) * x**3)

    def testLaguerre(self):
        assert_equal(series.laguerre(0), ONE)
        assert_equal(series.laguerre(1), ONE - x)
        assert_equal(series.laguerre(2), fractions.Fraction(1, 2) * (x ** 2 - 4*x + 2))
        assert_equal(series.laguerre(3), fractions.Fraction(1, 6) * (-x**3 + 9*x**2 - 18*x + 6))

    def testGeneralizedLaguerre(self):
        assert_equal(series.laguerre_g(0), ONE)
        assert_equal(series.laguerre_g(1), -x + a + 1)
        assert_equal(series.laguerre_g(2), fractions.Fraction(1, 2) * (x ** 2 - 2*(a + 2)*x + (a + 1) * (a + 2)))
        assert_equal(series.laguerre_g(3), fractions.Fraction(1, 6) * (-x**3 + 3*(a + 3)*x**2 - 3*(a + 2) * (a + 3)*x + (a + 1) * (a + 2) * (a + 3)))

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