import nose
from nose.tools import *
import pypol
import pypol.funcs as funcs


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

    def testQuadratic(self):
        pass

    def testNewton(self):
        pass

    def testRuffini(self):
        pass

    def testBisection(self):
        pass

    def testPolyder(self):
        pass

    def testPolyint(self):
        pass

    def testFib_poly(self):
        pass

    def testFib_poly_r(self):
        pass

    def testHermite_prob(self):
        pass

    def testHermite_prob_r(self):
        pass

    def testHermite_phys(self):
        pass

    def testHermite_phys_r(self):
        pass

    def testChebyshev_t(self):
        pass

    def testChebyshev_u(self):
        pass

    def testAbel(self):
        pass


if __name__ == '__main__':
    nose.runmodule()