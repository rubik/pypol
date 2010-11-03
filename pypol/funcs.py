# -*- coding: utf-8 -*-

'''
This module offer some utility functions like polyder, polyint or some generator functions
(C) Copyright 2010 Michele Lacchia
'''

from __future__ import division
import copy
import random
import operator
import fractions
import math

from core import Polynomial, AlgebraicFraction, poly1d, poly1d_2, polynomial, monomial

NULL = Polynomial()
ONE = monomial()
TWO = monomial(2)
x = monomial(x=1)

def divisible(a, b):
    '''
    Returns True whether *a* and *b* are divisible, i.e. ``a % b == 0``

    :params a: the first polynomial
    :params b: the second polynomial
    :rtype: bool

    **Examples**
    ::

        >>> a, b = poly1d([1, 7, 6]), poly1d([1, -5, -6])
        >>> a, b
        (+ x^2 + 7x + 6, + x^2 - 5x - 6)
        >>> c = gcd(a, b)
        >>> c
        + 12x + 12
        >>> divisible(a, c)
        True
        >>> divisible(b, c)
        True

    .. versionadded:: 0.3
    '''

    if a.degree < b.degree:
        return False

    return a % b == polynomial()

def from_roots(roots):
    '''
    Make a polynomial from its roots. These can be integer, float or :class:`fractions.Fraction` objects but the **complex** type is not supported.

    **Examples**

    ::

        >>> p = from_roots([4, -2, 153, -52])
        >>> p
        + x^4 - 103x^3 - 7762x^2 + 16720x + 63648
        >>> p(4)
        0
        >>> p(-2)
        0
        >>> p(153)
        0
        >>> p(-52)
        0
        >>> roots.newton(p, 1000)
        153.0
        >>> roots.newton(p, 100)
        -2.0
        >>> roots.newton(p, 10)
        4.0
        >>> roots.newton(p, -10000)
        -52.0
    '''

    return reduce(operator.mul, ((x - (fractions.Fraction.from_float(r) if isinstance(r, float) else r)) for r in roots))

def random_poly(coeff_range=xrange(-10, 11), len_=None, len_range=xrange(-10, 11),
                letters='xyz', max_letters=3, unique=False, exp_range=xrange(1, 6),
                right_hand_side=None, not_null=None):
    '''
    Returns a polynomial generated randomly.

    :param coeff_range: the range of the polynomial's coefficients, default is ``xrange(-10, 11)``.
    :param len\_: the len of the polynomial. Default is None, in this case len\_ will be a random number chosen in coeff_range. If *len\_* is negative it will be coerced to be positive: ``len_ = -len_``.
    :param letters: the letters that appear in the polynomial.
    :param max_letter: is the maximum number of letter for every monomial.
    :param unique: if True, all the polynomial's monomials will have the same letter (chosen randomly).
        For example, if you want to generate a polynomial with a letter only, you can do::

            >>> random_poly(letters='x')
            + 3x^5 - 10x^4 - 4x^3 + x - 9
            >>> random_poly(letters='x')
            - 12x^4 - 6x^2
            >>> random_poly(letters='z')
            + 8z^5 - 7z^3 + 10z^2 + 10
            >>> random_poly(letters='y')
            - 12y^5 - 15y^4 - y^3 + 9y^2 + 4y

        or::

            >>> random_poly(unique=True)
            + 6z^5 - 8z^4 + 6z^3 + 7z^2 + 2z
            >>> random_poly(unique=True)
            - 2z^5 + 3
            >>> random_poly(unique=True)
            - 19y^5 - y^4 - 8y^3 - 5y^2 - 4y
            >>> random_poly(unique=True)
            - 2x^4 - 10x^3 + 2x^2 + 3

    :param exp_range: the range of the exponents.
    :param right_hand_side: if True, the polynomial will have a right-hand side. Default is None, that means the right-hand side will be chosen randomly.
    :param not_null: if True, the polynomial will not be an empty polynomial

    :rtype: :class:`pypol.Polynomial`

    Some examples::

        >>> random_poly()
         + 2x^4y^5 + 3y^5 + 5xy^5 + 10x^2y^3z^3 - 5z
        >>> random_poly()
         + 7xy^5 - 3z^4 - 2
        >>> random_poly(len_=3, letters='ab')
         + 9a^5 + 7a^2b^4 - 8ab^2
        >>> random_poly(letters='abcdef', max_letters=1)
        - 9
        >>> random_poly(letters='abcdef', max_letters=1)
        - 5e^5 + 2f^4 + 5a^2
        >>> random_poly(letters='abcdef', max_letters=2)
        - 9f^5 - d - 10
        >>> random_poly(letters='abcdef', max_letters=2)
        - 9de^5 - 4a^3d^5 - 5d^5 + 4af^3 + 2e^2f - 3f^2
        >>> random_poly(letters='abcdef', max_letters=2, exp_range=xrange(0, 20, 5))
        - 7e^15 + 5d^15 - 10c^15 - 9b^10 - 12e^5 - 12c^5 - 2f^5

    .. versionadded:: 0.2
        The *unique* parameter.

    .. versionadded:: 0.3
        The *not_null* parameter.
    '''

    kwargs = locals() ## For not_null
    if not len_:
        len_ = random.choice(coeff_range)
    if right_hand_side is None:
        right_hand_side = random.choice((True, False,))
    if len_ < 0:
        len_ = -len_

    if unique:
        letter = random.choice(letters)

    monomials = []
    for _ in xrange((len_ - 1 if right_hand_side else len_)):
        vars = {}
        if unique:
            vars[letter] = random.choice(exp_range)
        else:
            for __ in xrange(random.randint(1, max_letters)):
                vars[random.choice(letters)] = random.choice(exp_range)

        monomials.append((random.choice(coeff_range), vars))

    if right_hand_side:
        monomials.append((random.choice(coeff_range), {}))

    poly = Polynomial(monomials)
    if not_null and not poly:
        poly = random_poly(**kwargs)

    return poly

def polyder(poly, m=1):
    '''
    Returns the derivative of the polynomial *poly*.

    :param integer m: order of differentiation (default 1)
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    Let's calculate the derivative of the polynomials |p3| and |p4|::

        >>> p1 = poly1d([1, 0, 0]) ## or poly1d([1, 0], right_hand_side=False)
        >>> p1
         + x^2
        >>> polyder(p1)
         + 2x
        >>> p2 = poly1d([2, -4, 0, 1])
        >>> p2
         + 2x^3 - 4x^2  + 1
        >>> polyder(p2)
         + 6x^2 - 8x

    .. versionadded:: 0.3
    .. versionadded:: 0.4
        The *m* parameter.
    '''
    def _der(poly):
        def _single_der(var):
            return [var[0]*var[1], var[1] - 1]

        if not poly:
            return Polynomial()
        try:
            variable = poly.letters[0]
        except IndexError:
            variable = 'x'

        return poly1d_2([_single_der(t) for t in poly.to_plist()], variable)

    if m < 0:
        raise ValueError('order of derivative must be positive (see polyint)')
    if m == 0:
        return poly
    elif m == 1:
        return _der(poly)
    p_d = _der(poly)
    for _ in xrange(m - 1):
        if not p_d:
            return Polynomial()
        p_d = _der(p_d)

    return p_d

def polyint(poly, m=1, C=[]):
    '''
    Returns the indefinite integral of the polynomial *poly*:
        |p5|

    :param Polynomial poly: the polynomial
    :param integer m: the order of the antiderivative (default 1)
    :param C: integration costants. They are given in order of integration: those corresponding to highest-order terms come first.
    :type C: list of integers or integer - if *m* = 1
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    Let's calculate the indefinite integrals of the polynomials: :math:`-x` and :math:`x^3 - 7x + 5`::

        >>> p1, p2 = poly1d([-1, 0]), poly1d([1, 0, -7, 5])
        >>> p1, p2
        (- x, + x^3 - 7x + 5)
        >>> polyint(p1)
        - 1/2x^2
        >>> polyint(p2)
        + 1/4x^4 - 7/2x^2 + 5x
        >>> polyder(polyint(p2))
        + x^3 - 7x + 5
        >>> polyder(polyint(p1))
        - x

    The integration costants default to zero, but can be specified::

        >>> polyder(p2)
        + 3x^2 - 7
        >>> polyint(polyder(p2))
        + x^3 - 7x ## + 5 is missing!
        >>> polyint(polyder(p2), [5])
        + x^3 - 7x + 5
        >>> p = poly1d([1]*3)
        >>> p
        + x^2 + x + 1
        >>> P = polyint(p, 3, [6, 5, 3])
        >>> P
        + 1/60x^5 + 1/24x^4 + 1/6x^3 + 3x^2 + 5x + 3
        >>> polyint(p, 3, [6, 5, 3]) == polyint(polyint(polyint(p, C=[6]), C=[5]), C=[3])
        True
        >>> polyint(poly1d([1, 2, 3]))
        + 1/3x^3 + x^2 + 3x
        >>> polyint(poly1d([1, 2, 3]), C=[2])
        + 1/3x^3 + x^2 + 3x + 2
        >>> polyint(poly1d([1, 2, 3]), C=2)
        + 1/3x^3 + x^2 + 3x + 2
        >>> polyint(poly1d([1, 2, 3]), 2, [4, 2])
        + 1/12x^4 + 1/3x^3 + 3/2x^2 + 4x + 2
        >>> polyint(poly1d([1]*4), 3, [3, 2, 1])
        + 1/120x^6 + 1/60x^5 + 1/24x^4 + 1/6x^3 + 3/2x^2 + 2x + 1
        >>> polyint(poly1d([1]*4), 3, [3, 2, 1, 5]) ## Take only the first 3
        + 1/120x^6 + 1/60x^5 + 1/24x^4 + 1/6x^3 + 3/2x^2 + 2x + 1

    **References**

    +---------------------------------------------------------------------+
    | `MathWorld <http://mathworld.wolfram.com/IndefiniteIntegral.html>`_ |
    +---------------------------------------------------------------------+

    .. versionadded:: 0.3
    '''

    def _int(p, c=None):
        def _single_int(var):
            n = var[1] + 1
            if not n:
                return [0, 0]
            j = fractions.Fraction(str(var[0])) / fractions.Fraction(str(n))
            jint = int(j)
            if jint == j:
                return [jint, n]
            return [j, n]

        p = poly1d_2([_single_int(t) for t in p.to_float().to_plist()])
        if c:
            p += c
        return p

    if m < 0:
        raise ValueError('order of antiderivative must be positive (see polyder)')
    if m == 0:
        return poly
    if m == 1:
        if C:
            try:
                return _int(poly, C[0])
            except TypeError:
                return _int(poly, C)
        return _int(poly)

    if C:
        p_i = _int(poly, C[0])
        for i in xrange(1, m):
            p_i = _int(p_i, C[i])
    else:
        p_i = _int(poly)
        for _ in xrange(m - 1):
            p_i = _int(p_i)

    return p_i

def polyint_(poly, a, b):
    '''
    Returns the definite integral of the polynomial *poly*, with upper and lower limits:
        |p8|

    :param integer a: the lower limit
    :param integer b: the upper limit
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> p = poly1d([1, -3, -9, 1])
        >>> p
        + x^3 - 3x^2 - 9x + 1
        >>> q = (x - 4) * (x + 1) ** 3
        >>> q
        + x^4 - x^3 - 9x^2 - 11x - 4
        >>> polyint_(p, 2, 5)
        56.25
        >>> polyint_(p, 2, -3)
        -23.75
        >>> polyint_(q, -2, 5)
        63.350000000000001
        >>> polyint_(q, -2, -5)
        523.35000000000002
        >>> polyint_(q, -2, -2)
        0.0
        >>> polyint_(q, -2, 2)
        51.200000000000003

    **References**

    +-------------------------------------------------------------------+
    | `Wikipedia <http://en.wikipedia.org/wiki/Integral>`_              |
    +-------------------------------------------------------------------+
    | `MathWorld <http://mathworld.wolfram.com/DefiniteIntegral.html>`_ |
    +-------------------------------------------------------------------+
    '''

    F = polyint(poly)
    return F(a) - F(b)

def bin_coeff(n, k):
    '''
    Returns the binomial coefficient |p11|, i.e. the coefficient of the |p12| term of the binomial power |p13|.

    :param integer n: the power of the binomial. If ``n == 1`` the result will be |p14|
    :param integer k: the power of the term
    :rtype: float

    **Examples**

    ::

        >>> bin_coeff(1, 4)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "funcs.py", line 367, in bin_coeff
            
        ValueError: k cannot be greater than n
        >>> bin_coeff(6, 4)
        15.0
        >>> bin_coeff(16, 9)
        11440.0
        >>> bin_coeff(-1, 9)
        -1
        >>> bin_coeff(-1, 8)
        1
        >>> bin_coeff(124, 98)
        3.9616705576337044e+26

    It is the same as::

        >>> def bin_coeff_2(n, k):
            if n < k:
                raise ValueError('k cannot be greater than n')
            return ((1 + x) ** n).get(k)
        
        >>> bin_coeff(5, 4)
        5.0
        >>> bin_coeff_2(5, 4)
        5
        >>> bin_coeff_2(3, 4)
        Traceback (most recent call last):
          File "<pyshell#18>", line 1, in <module>
            bin_coeff_2(3, 4)
          File "<pyshell#15>", line 3, in bin_coeff_2
            raise ValueError('k cannot be greater than n')
        ValueError: k cannot be greater than n
        >>> bin_coeff(3, 4)
        Traceback (most recent call last):
          File "<pyshell#19>", line 1, in <module>
            bin_coeff(3, 4)
          File "funcs.py", line 388, in bin_coeff
            raise ValueError('k cannot be greater than n')
        ValueError: k cannot be greater than n
        >>> bin_coeff(56, 54)
        1540.0
        >>> bin_coeff_2(56, 54)
        1540
        >>> bin_coeff(123, 54)
        3.0748160713247975e+35
        >>> bin_coeff_2(123, 54)
        307481607132479763736986522890815830L

    but :func:`bin_coeff` is faster.

    **References**

    +-------------------------------------------------------------------+
    | `Wikipedia <http://en.wikipedia.org/wiki/Binomial_coefficient>`_  |
    +-------------------------------------------------------------------+
    '''

    if n == -1:
        return float((-1) ** k)
    if n == k:
        return 1.
    if n < k:
        raise ValueError('k cannot be greater than n')

    return float(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))

def harmonic(n):
    return sum(fractions.Fraction(1, k) for k in xrange(1, n + 1))

def harmonic_g(n, m):
    return sum(fractions.Fraction(1, k ** m) for k in xrange(1, n + 1))

def stirling(n, k):
    if n == k:
        return 1.
    if n > 0 and k == 0:
        return 0.
    if k > n:
        return 0.
    if k == 1:
        return math.factorial(n - 1)
    if k == 2:
        return math.factorial(n - 1) * harmonic(n - 1)
    if k == 3:
        return fractions.Fraction(1, 2) * math.factorial(n - 1) * (harmonic(n - 1) ** 2 - harmonic_g(n - 1, 2))
    if k == (n - 1):
        return bin_coeff(n, 2)
    if k == (n - 2):
        return fractions.Fraction(1, 4) * (3*n - 1) * bin_coeff(n, 3)
    if k == (n - 3):
        return bin_coeff(n, 2) * bin_coeff(n, 4)
    return stirling(n - 1, k - 1) - (n - 1) * stirling(n - 1, k)

def stirling_2(n, k):
    return fractions.Fraction(1, math.factorial(k)) * sum((-1) ** (k - j) * bin_coeff(k, j) * j ** n for j in xrange(k + 1))

def bell_num(n):
    if n == 0:
        return 1.
    if n == 1:
        return 1.
    return sum(stirling_2(n, k) for k in xrange(n + 1))


################################################################################
##                            Still in development                            ##
################################################################################

def interpolate(x_values, y_values): ## Still in development
    '''
    Interpolate with the Lagrange method.

    :param list x_values: the list of the *abscissas*
    :param list y_values: the list of the *ordinates*
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        
    '''

    def _basis(j):
        p = [(x - x_values[m])/(x_values[j] - x_values[m]) for m in xrange(k + 1) if m != j]
        return reduce(operator.mul, p)

    assert len(x_values) != 0 and (len(x_values) == len(y_values)), 'x and y cannot be empty and must have the same length'

    k = len(x_values) - 1
    r = [_basis(j) for j in xrange(k)]
    c = copy.deepcopy(r)
    for i, v in enumerate(c):
        if isinstance(v, AlgebraicFraction):
            q = divmod(*v.terms)
            if len(q) > 1:
                r[i] = q[0] + q[1]
            else:
                r[i] = q
    return sum(r)