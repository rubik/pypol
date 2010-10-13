# -*- coding: utf-8 -*-

'''
This file is part of the pypol project.
(C) Copyright 2010 Michele Lacchia
'''

from __future__ import division
import random
import operator
import fractions
import math

from core import Polynomial, poly1d, poly1d_2, polynomial, monomial

NULL = Polynomial()
ONE = monomial()
TWO = monomial(2)
x = poly1d([1, 0])

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
            return NULL
        try:
            variable = poly.letters[0]
        except IndexError:
            variable = 'x'

        return poly1d_2([_single_der(t) for t in poly.to_plist()], variable)

    if m < 0:
        raise ValueError('order of derivative must be positive (see polyint)')
    if m == 0:
        return poly
    if m == 1:
        return _der(poly)
    p_d = _der(poly)
    for _ in xrange(m - 1):
        if not p_d:
            return NULL
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

    Let's calculate the indefinite integrals of the polynomials: |p6| and |p7|::

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
            j = fractions.Fraction(var[0], n)
            if int(j) == j:
                j = int(j)
            return [j, n]

        p = poly1d_2([_single_int(t) for t in p.to_plist()])
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
    :rtype: integer or float

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
        return (-1) ** k
    if n == k:
        return 1
    if n < k:
        raise ValueError('k cannot be greater than n')

    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def fib_poly(n):
    '''
    Returns the *nth* Fibonacci polynomial. This is the iterative version, and it is extremely faster than the recursive one.

    **Examples**

    ::

        >>> fib_poly(0)
        
        >>> fib_poly(1)
        + 1
        >>> fib_poly(2)
        + x
        >>> fib_poly(3)
        + x^2 + 1
        >>> fib_poly(4)
        + x^3 + 2x
        >>> fib_poly(5)
        + x^4 + 3x^2 + 1
        >>> fib_poly(6)
        + x^5 + 4x^3 + 3x
        >>> fib_poly(23)
        + x^22 + 21x^20 + 190x^18 + 969x^16 + 3060x^14 + 6188x^12 + 8008x^10 + 6435x^8 + 3003x^6 + 715x^4 + 66x^2 + 1
        >>> fib_poly(100)
        + x^99 + 98x^97 + 4656x^95 + 142880x^93 .. cut .. + 197548686920970x^17 + 22057981462440x^15 + 1889912732400x^13 + 119653565850x^11 + 5317936260x^9 + 154143080x^7 + 2598960x^5 + 20825x^3 + 50x
        >>> fib_poly(200)
        + x^199 + 198x^197 + .. cut .. + 15913388077274800x^13 + 249145778809200x^11 + 2747472247520x^9 + 19813501785x^7 + 83291670x^5 + 166650x^3 + 100x
        >>> len(fib_poly(300))
        150
        >>> len(str(fib_poly(300)))
        8309

    .. versionadded:: 0.3
    '''

    if n <= 0:
        return NULL
    elif n == 1:
        return ONE
    elif n == 2:
        return poly1d([1], right_hand_side=False)
    p = [ONE, poly1d([1], right_hand_side=False)]
    for x in xrange(n - 2):
        p.append(polynomial('x') * p[-1] + p[-2])
    return p[-1]

def fib_poly_r(n):
    '''
    Returns the *nth* Fibonacci polynomial in *x* (recursive version)::

        >>> fib_poly(1)
        + 1
        >>> fib_poly(2)
        + x
        >>> fib_poly(3)
        + x^2 + 1
        >>> fib_poly(4)
        + x^3 + 2x
        >>> fib_poly(5)
        + x^4 + 3x^2 + 1
        >>> fib_poly(6)
        + x^5 + 4x^3 + 3x
        >>> fib_poly(12)
        + x^11 + 10x^9 + 36x^7 + 56x^5 + 35x^3 + 6x
        >>> fib_poly(20)
        + x^19 + 18x^17 + 136x^15 + 560x^13 + 1365x^11 + 2002x^9 + 1716x^7 + 792x^5 + 165x^3 + 10x
        >>> fib_poly(25)
        + x^24 + 23x^22 + 231x^20 + 1330x^18 + 4845x^16 + 11628x^14 + 18564x^12 + 19448x^10 + 12870x^8 + 5005x^6 + 1001x^4 + 78x^2 + 1

    .. versionadded:: 0.3
    '''

    if n <= 0:
        return NULL
    elif n == 1:
        return ONE
    elif n == 2:
        return poly1d([1], right_hand_side=False)
    elif n > 2:
        return polynomial('x')*fib_poly(n - 1) + fib_poly(n - 2)

def hermite_prob(n):
    '''
    Returns the *nth* probabilistic Hermite polynomial, that is a polynomial of degree *n*.

    **Examples**

    ::

        >>> hermite_prob(0)
         + 1
        >>> hermite_prob(1)
         + x
        >>> hermite_prob(2)
         + x^2 - 1
        >>> hermite_prob(4)
         + x^4 - 6x^2 + 3
        >>> hermite_prob(45)
         + x^45 - 990x^43 + .. cut .. + 390756386568644372393927184375x^5 - 186074469794592558282822468750x^3 + 25373791335626257947657609375x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return x
    p = [x]
    for _ in xrange(n - 1):
        p.append(p[-1] * x - polyder(p[-1]))
    return p[-1]

def hermite_prob_r(n):
    '''
    Returns the *nth* Hermite probabilistic polynomial (recursive version).

    **Examples**

    ::

        >>> hermite_prob_r(0)
         + 1
        >>> hermite_prob_r(1)
         + x
        >>> hermite_prob_r(2)
         + x^2 - 1
        >>> hermite_prob_r(3)
         + x^3 - 3x
        >>> hermite_prob_r(4)
         + x^4 - 6x^2 + 3
        >>> hermite_prob_r(42)
         + x^42 - 861x^40 + 335790x^38 .. cut .. - 747445016088215350396115625x^8 + 1162692247248334989505068750x^6 - 917914932038159202240843750x^4 + 275374479611447760672253125x^2 - 13113070457687988603440625

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return x
    return hermite_prob(n - 1) * x - polyder(hermite_prob(n - 1))

def hermite_phys(n):
    '''
    Returns the *nth* Hermite polynomial (physicist).

    **Examples**

    ::

        >>> hermite_phys(0)
         + 1
        >>> hermite_phys(1)
         + 2x
        >>> hermite_phys(2)
         + 4x^2 - 2
        >>> hermite_phys(3)
         + 8x^3 - 12x
        >>> hermite_phys(4)
         + 16x^4 - 48x^2 + 12
        >>> hermite_phys(9)
         + 512x^9 - 9216x^7 + 48384x^5 - 80640x^3 + 30240x
        >>> hermite_phys(11)
         + 2048x^11 - 56320x^9 + 506880x^7 - 1774080x^5 + 2217600x^3 - 665280x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    p = [ONE]
    for _ in xrange(n):
        p.append((p[-1] * x * 2) - polyder(p[-1]))
    return p[-1]

def hermite_phys_r(n):
    '''
    Returns the *nth* Hermite polynomial (physicist and recursive version).

    **Examples**

    ::

        >>> hermite_phys_r(0)
        + 1
        >>> hermite_phys_r(1)
         + 2x
        >>> hermite_phys_r(2)
         + 4x^2 - 2
        >>> hermite_phys_r(3)
         + 8x^3 - 12x
        >>> hermite_phys_r(6)
         + 64x^6 - 480x^4 + 720x^2 - 120
        >>> hermite_phys_r(9)
         + 512x^9 - 9216x^7 + 48384x^5 - 80640x^3 + 30240x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    return (hermite_phys(n - 1) * x * 2) - polyder(hermite_phys(n - 1))

def chebyshev_t(n):
    '''
    Returns the *nth* Chebyshev polynomial of the first kind in ``x``.

    **Examples**

    ::

        >>> chebyshev_t(0)
         + 1
        >>> chebyshev_t(1)
         + x
        >>> chebyshev_t(2)
         + 2x^2 - 1
        >>> chebyshev_t(4)
         + 8x^4 - 8x^2 + 1
        >>> chebyshev_t(5)
         + 16x^5 - 20x^3 + 5x
        >>> chebyshev_t(9)
         + 256x^9 - 576x^7 + 432x^5 - 120x^3 + 9x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return x
    return chebyshev_t(n - 1) * '2x' - chebyshev_t(n - 2)

def chebyshev_u(n):
    '''
    Returns the *nth* Chebyshev polynomial of the second kind in ``x``.

    **Examples**

    ::

        >>> chebyshev_u(0)
         + 1
        >>> chebyshev_u(1)
         + 2x
        >>> chebyshev_u(2)
         + 4x^2 - 1
        >>> chebyshev_u(4)
         + 16x^4 - 12x^2 + 1
        >>> chebyshev_u(6)
         + 64x^6 - 80x^4 + 24x^2 - 1
        >>> chebyshev_u(8)
         + 256x^8 - 448x^6 + 240x^4 - 40x^2 + 1
        >>> chebyshev_u(11)
         + 2048x^11 - 5120x^9 + 4608x^7 - 1792x^5 + 280x^3 - 12x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return poly1d([2, 0])
    return chebyshev_u(n - 1) * '2x' - chebyshev_u(n - 2)

def abel(n, variable='a'):
    '''
    Returns the *nth* Abel polynomial in ``x`` and *variable*.

    **Examples**

    ::

        >>> abel(0)
         + 1
        >>> abel(1)
         + x
        >>> abel(2)
         + x^2 - 2ax
        >>> abel(5)
         + x^5 - 20ax^4 + 150a^2x^3 - 500a^3x^2 + 625a^4x
        >>> abel(9)
         + x^9 - 72ax^8 + 2268a^2x^7 - 40824a^3x^6 + 459270a^4x^5 - 3306744a^5x^4 + 14880348a^6x^3 - 38263752a^7x^2 + 43046721a^8x

    .. versionadded:: 0.3
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return x
    p = poly1d([n])
    return x * (x - p*variable) ** (n - 1)

def spread(n):
    '''
    Returns the *nth* Spread polynomial in ``x``.
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return x
    return 2*x - spread(n - 2) + (2 - 4*x) * spread(n - 1)

def gegenbauer_r(n, a='a'):
    '''
    Returns the *nth* Gegenbauer polynomial in ``x``.

    **Examples**

    ::

        >>> gegenbauer_r(0)
        + 1
        >>> gegenbauer_r(1)
        + 2ax
        >>> gegenbauer_r(2)
        + 2a^2x^2 + 2ax^2 - a
        >>> 
        >>> 
        >>> gegenbauer_r(4)
        + 2/3a^4x^4 + 4a^3x^4 - 2a^3x^2 + 22/3a^2x^4 + 1/2a^2 - 6a^2x^2 + 4ax^4 - 4ax^2 + 1/2a

    **References**

    +-----------------------------------------------------------------------+
    | `Wikipedia <http://en.wikipedia.org/wiki/Gegenbauer_polynomials>`_    |
    +-----------------------------------------------------------------------+
    | `MathWorld <http://mathworld.wolfram.com/GegenbauerPolynomial.html>`_ |
    +-----------------------------------------------------------------------+

    .. versionadded:: 0.4
    '''

    a = monomial(**{a: 1})
    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return 2*a*x
    return fractions.Fraction(1, n) * ((2*x * (n + a - ONE) * gegenbauer_r(n - 1) \
                                    - (n + 2*a - 2) * gegenbauer_r(n - 2)))

def laguerre(n, a='a'):
    '''
    Returns the *nth* generalized Laguerre polynomial in ``x``.

    **Examples**

    ::

        >>> l(0)
        + 1
        >>> l(1)
        + a + 1 - x
        >>> l(2)
        + 1/2a^2 + 3/2a - ax + 1 - 2x + 1/2x^2
        >>> l(3)
        + 1/6a^3 + a^2 - 1/2a^2x + 11/6a - 5/2ax + 1/2ax^2 + 1 - 3x - 1/6x^3 + 3/2x^2
        >>> l(2, 'k')
        + 1/2k^2 + 3/2k - kx + 1 - 2x + 1/2x^2
        >>> l(2, 'z')
        + 1/2x^2 - 2x - xz + 1 + 3/2z + 1/2z^2
        >>> l(5, 'z')
        - 1/120x^5 + 5/24x^4 + 1/24x^4z - 5/3x^3 - 3/4x^3z - 1/12x^3z^2 + 5x^2 + 47/12x^2z + x^2z^2 + 1/12x^2z^3 - 5x - 77/12xz - 71/24xz^2 - 7/12xz^3 - 1/24xz^4 + 1 + 137/60z + 15/8z^2 + 17/24z^3 + 1/8z^4 + 1/120z^5
        >>> l(5)
        + 1/120a^5 + 1/8a^4 - 1/24a^4x + 17/24a^3 - 7/12a^3x + 1/12a^3x^2 - 71/24a^2x + 15/8a^2 + a^2x^2 - 1/12a^2x^3 + 47/12ax^2 - 77/12ax + 137/60a - 3/4ax^3 + 1/24ax^4 + 5x^2 - 5/3x^3 - 5x + 1 - 1/120x^5 + 5/24x^4
        >>> l(6)
        + 1/720a^6 + 7/240a^5 - 1/120a^5x + 35/144a^4 - 1/6a^4x + 1/48a^4x^2 - 31/24a^3x + 49/48a^3 + 3/8a^3x^2 - 1/36a^3x^3 + 119/48a^2x^2 - 29/6a^2x + 203/90a^2 - 5/12a^2x^3 + 1/48a^2x^4 - 37/18ax^3 + 57/8ax^2 + 49/20a - 87/10ax + 11/48ax^4 - 1/120ax^5 + 5/8x^4 - 10/3x^3 + 1 - 6x + 15/2x^2 - 1/20x^5 + 1/720x^6


    **References**

    +---------------------------------------------------------------------+
    | `Wikipedia <http://en.wikipedia.org/wiki/Laguerre_polynomials>`_    |
    +---------------------------------------------------------------------+
    | `MathWorld <http://mathworld.wolfram.com/LaguerrePolynomial.html>`_ |
    +---------------------------------------------------------------------+

    .. versionadded:: 0.4
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE
    if n == 1:
        return a + ONE - x

    a = monomial(**{a: 1})
    l1, ll = NULL, ONE
    for i in xrange(1, n + 1):
        l0, l1 = l1, ll
        ll = ((2*i - 1 + a - x) * l1 - (i - 1 + a) * l0) / monomial(i)
    return ll

################################################################################
##                            Still in development                            ##
################################################################################

def bernstein(i, n): ## Still in development
    def _bin_coeff(n, k):
        return math.factorial(n)/(math.factorial(k)*math.factorial(n - k))

    if not i and not n:
        return ONE
    return _bin_coeff(n, i) * (x**i) * (1 - x) ** (n - i)

def interpolate(x_values, y_values): ## Still in development
    '''
    Interpolate with the Lagrange method.

    :param list x_values: the list of the *abscissas*
    :param list y_values: the list of the *ordinates*
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        
    '''

    def _product(i):
        p = [(x - x_values[k])/(x_values[i] - x_values[k]) for k in xrange(n) if k != i] + [y_values[i]]
        return reduce(operator.mul, p)

    assert len(x_values) != 0 and (len(x_values) == len(y_values)), 'x and y cannot be empty and must have the same length'

    n = len(x_values)
    return sum(_product(j) for j in xrange(n))