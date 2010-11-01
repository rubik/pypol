# -*- coding: utf-8 -*-

'''
This file is part of the pypol project.
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
        .. math:: \int p(x)dx

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

def fibonacci(n):
    '''
    Returns the *n-th* Fibonacci polynomial.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> fibonacci(0)
        
        >>> fibonacci(1)
        + 1
        >>> fibonacci(2)
        + x
        >>> fibonacci(3)
        + x^2 + 1
        >>> fibonacci(4)
        + x^3 + 2x
        >>> fibonacci(5)
        + x^4 + 3x^2 + 1
        >>> fibonacci(6)
        + x^5 + 4x^3 + 3x
        >>> fibonacci(23)
        + x^22 + 21x^20 + 190x^18 + 969x^16 + 3060x^14 + 6188x^12 + 8008x^10 + 6435x^8 + 3003x^6 + 715x^4 + 66x^2 + 1
        >>> fibonacci(100)
        + x^99 + 98x^97 + 4656x^95 + 142880x^93 ... + 197548686920970x^17 + 22057981462440x^15 + 1889912732400x^13 + 119653565850x^11 + 5317936260x^9 + 154143080x^7 + 2598960x^5 + 20825x^3 + 50x
        >>> fibonacci(200)
        + x^199 + 198x^197 + ... + 15913388077274800x^13 + 249145778809200x^11 + 2747472247520x^9 + 19813501785x^7 + 83291670x^5 + 166650x^3 + 100x
        >>> len(fibonacci(300))
        150
        >>> len(str(fibonacci(300)))
        8309

    .. versionadded:: 0.3
    '''

    if n <= 0:
        raise ValueError('Fibonacci polynomials only defined for n > 0')
    elif n == 1:
        return ONE
    elif n == 2:
        return monomial(x=1)
    p = [ONE, monomial(x=1)]
    for x in xrange(n - 2):
        p.append(polynomial('x') * p[-1] + p[-2])
    return p[-1]

def hermite_prob(n):
    '''
    Returns the *n-th* probabilistic Hermite polynomial, that is a polynomial of degree *n*.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Hermite polynomials (probabilistic) only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return x
    p = [x]
    for _ in xrange(n - 1):
        p.append(p[-1] * x - polyder(p[-1]))
    return p[-1]

def hermite_phys(n):
    '''
    Returns the *n-th* Hermite polynomial (physicist).

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Hermite polynomials (physicist) only defined for n >= 0')
    if n == 0:
        return ONE
    p = [ONE]
    for _ in xrange(n):
        p.append((p[-1] * x * 2) - polyder(p[-1]))
    return p[-1]

def chebyshev_t(n):
    '''
    Returns the *n-th* Chebyshev polynomial of the first kind in ``x``.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Chebyshev polynomials of the first kind only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return x
    return chebyshev_t(n - 1) * '2x' - chebyshev_t(n - 2)

def chebyshev_u(n):
    '''
    Returns the *n-th* Chebyshev polynomial of the second kind in ``x``.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Chebyshev polynomials of the second kind only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return poly1d([2, 0])
    return chebyshev_u(n - 1) * '2x' - chebyshev_u(n - 2)

def abel(n, variable='a'):
    '''
    Returns the *n-th* Abel polynomial in ``x`` and *variable*.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Abel polynomials only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return x
    p = poly1d([n])
    return x * (x - p*variable) ** (n - 1)

def spread(n): ## Should work but it doesn't
    '''
    Returns the *n-th* Spread polynomial in ``x``.
    
    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`
    '''

    if n < 0:
        raise ValueError('Spread polynomials only defined for n >= 0')
    if n == 0:
        return NULL
    if n == 1:
        return x
    p = [NULL, x]
    for _ in xrange(n - 2):
        p.append(2*x - p[-2] + (2 - 4*x) * p[-1])
    return p[-1]

def touchard(n):
    '''
    Returns the *n-th* Touchard polynomial in ``x``.

    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> touchard(0)
        + 1
        >>> touchard(1)
        + x
        >>> touchard(2)
        + x^2 + x
        >>> touchard(12)
        + x^12 + 66x^11 + 7498669301432319/4398046511104x^10 + 22275x^9 + 159027x^8 + 627396x^7 + 1323652x^6 + 1379400x^5 + 611501x^4 + 86526x^3 + 2047x^2 + x

    The Touchard polynomials also satisfy:
        |p15|

    where |p16| is the *n-th* Bell number (:func:`bell_num`)::

        >>> long(touchard(19)(1)) == long(bell_num(19))
        True

    The more *n* become greater, the more it loses precision::

        >>> long(touchard(23)(1)) == long(bell_num(23))
        False
        >>> abs(long(touchard(23)(1)) - long(bell_num(23)))
        8L
        >>> long(touchard(45)(1)) == long(bell_num(45))
        False
        >>> abs(long(touchard(45)(1)) - long(bell_num(45)))
        19342813113834066795298816L
        >>> long(touchard(123)(1)) == long(bell_num(123))
        False
        >>> abs(long(touchard(123)(1)) - long(bell_num(123)))
        429106803807439187983719223678319701219747465049443431177466446916319867062128867811451292833717675081551803755143128885524389827706879L
    '''

    if n < 0:
        return NULL
    if n == 0:
        return ONE    
    return sum(stirling_2(n, k) * x ** k for k in xrange(n + 1))

def lucas(n):
    '''
    Returns the *n-th* Lucas polynomial.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> lucas(0)
        + 2
        >>> lucas(1)
        + x
        >>> lucas(2)
        + x^2 + 2
        >>> lucas(3)
        + x^3 + 3x
        >>> lucas(4)
        + x^4 + 4x^2 + 2
        >>> lucas(14)
        + x^14 + 14x^12 + 77x^10 + 210x^8 + 294x^6 + 196x^4 + 49x^2 + 2

    .. note::
        The Lucas polynomials are obtained setting ``p = x`` and ``q = 1`` in the Lucas polynomial sequence (see :func:`lucas_seq`).
        You can generate them with this small piece of code::

            >>> from pypol import x, ONE, TWO
            >>> from pypol.funcs import lucas_seq
            >>> 
            >>> def lucas_poly(n):
                return lucas_seq(n, x, ONE, TWO, x)
            
            >>> lucas_poly(0)
            + 2
            >>> lucas_poly(1)
            + x
            >>> lucas_poly(2)
            + x^2 + 2
            >>> lucas_poly(5)
            + x^5 + 5x^3 + 5x
            >>> lucas_poly(15)
            + x^15 + 15x^13 + 90x^11 + 275x^9 + 450x^7 + 378x^5 + 140x^3 + 15x


    **References**

    `MathWorld <http://mathworld.wolfram.com/LucasPolynomial.html>`_
    '''

    if n < 0:
        raise ValueError('Lucas polynomials only defined for n >= 0')
    if n == 0:
        return TWO
    if n == 1:
        return x
    p = [TWO, x]
    for _ in xrange(n - 1):
        p.append(x * p[-1] + p[-2])
    return p[-1]

def pell(n):
    '''
    Returns the *n-th* Pell polynomial.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> pell(0) # A null polynomial
        
        >>> pell(1)
        + 1
        >>> pell(2)
        + 2x
        >>> pell(3)
        + 4x^2 + 1
        >>> pell(4)
        + 8x^3 + 4x
        >>> pell(14)
        + 8192x^13 + 24576x^11 + 28160x^9 + 15360x^7 + 4032x^5 + 448x^3 + 14x

    .. note::

        The Pell polynomials are obtained setting ``p = 2x`` and ``q = 1`` in the Lucas sequence (see :func:`lucas_seq`).
        You can easily generate them::

            >>> from pypol import x, ONE
            >>> from pypol.funcs import lucas_seq
            >>> 
            >>> def pell_poly(n):
                return lucas_seq(n, 2*x, ONE)
            
            >>> pell_poly(0)
            
            >>> pell_poly(1)
            + 1
            >>> pell_poly(3)
            + 4x^2 + 1
            >>> pell_poly(9)
            + 256x^8 + 448x^6 + 240x^4 + 40x^2 + 1

    **References**

    `MathWorld <http://mathworld.wolfram.com/PellPolynomial.html>`_
    '''

    if n < 0:
        raise ValueError('Pell polynomials only defined for n >= 0')
    if n == 0:
        return NULL
    if n == 1:
        return ONE
    p = [NULL, ONE]
    for _ in xrange(n- 1):
        p.append(2*x * p[-1] + p[-2])
    return p[-1]

def pell_lucas(n):
    '''
    '''

    if n < 0:
        raise ValueError('Pell-Lucas polynomials only defined for n >= 0')
    if n == 0:
        return TWO
    if n == 1:
        return 2*x
    p = [TWO, 2*x]
    for _ in xrange(n- 1):
        p.append(2*x * p[-1] + 1 * p[-2])
    return p[-1]

def jacobsthal(n):
    if n < 0:
        raise ValueError('Jacobsthal polynomials only defined for n >= 0')
    if n == 0:
        return NULL
    if n == 1:
        return ONE
    p = [NULL, ONE]
    for _ in xrange(n- 1):
        p.append(1 * p[-1] + 2*x * p[-2])
    return p[-1]

def jacob_lucas(n):
    if n < 0:
        raise ValueError('Jacobsthal-Lucas polynomials only defined for n >= 0')
    if n == 0:
        return TWO
    if n == 1:
        return ONE
    p = [TWO, ONE]
    for _ in xrange(n- 1):
        p.append(1 * p[-1] + 2*x * p[-2])
    return p[-1]

def fermat(n):
    if n < 0:
        raise ValueError('Fermat polynomials only defined for n >= 0')
    if n == 0:
        return NULL
    if n == 1:
        return ONE
    p = [NULL, ONE]
    for _ in xrange(n- 1):
        p.append(3*x * p[-1] -2 * p[-2])
    return p[-1]

def fermat_lucas(n):
    if n < 0:
        raise ValueError('Fermat-Lucas polynomials only defined for n >= 0')
    if n == 0:
        return TWO
    if n == 1:
        return 3*x
    p = [TWO, 3*x]
    for _ in xrange(n- 1):
        p.append(3*x * p[-1] -2 * p[-2])
    return p[-1]

def lucas_seq(n, p, q, zero=NULL, one=ONE):
    '''
    "The Lucas polynomial sequence is a pair of generalized polynomials which generalize the Lucas sequence to polynomials ..." [MathWorld]_

    :param integer n: the *n-th* element of the sequence
    :param p: The *p* parameter
    :param q: The *q* parameter
    :param zero: The first element of the sequence (at index 0)
    :type zero: :class:`pypol.Polynomial`
    :param one: The second element of the sequence (at index 1)
    :type one: :class:`pypol.Polynomial`
    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    Setting different values for *p* and *q* we obtain some polynomial sequences, for every *p* and *q* pair there are two polynomials sequences, |p17| and |p18|:

    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | **p**  | **q**  |    **W(x)**                                                           |   **w(x)**                                                          |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | x      | 1      |  Fibonacci polynomials (:func:`fibonacci`)                            | Lucas polynomials (:func:`lucas`)                                   |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | 2x     | 1      |  Pell polynomials (:func:`pell`)                                      | Pell-Lucas polynomials (:func:`pell_lucas`)                         |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | 1      | 2x     |  Jacobsthal polynomials (:func:`jacobsthal`)                          | Jacobsthal-Lucas polynomials (:func:`jacob_lucas`)                  |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | 3x     | -2     |  Fermat polynomials (:func:`fermat`)                                  | Fermat-Lucas polynomials (:func:`fermat_lucas`)                     |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+
    | 2x     | -1     |  Chebyshev polynomials of the second kind |p19| (:func:`chebyshev_u`) | Chebyshev polynomials of the first kind |p20| (:func:`chebyshev_t`) |
    +--------+--------+-----------------------------------------------------------------------+---------------------------------------------------------------------+


    .. [MathWorld]: `Weisstein, Eric W. <http://mathworld.wolfram.com/about/author.html>`_ "Lucas Polynomial Sequence." From `MathWorld <http://mathworld.wolfram.com/>`_--A Wolfram Web Resource.
    '''

    if n < 0:
        raise ValueError('Lucas sequence only defined for n >= 0')
    o = [zero, one]
    if n in (0, 1):
        return o[n]
    for _ in xrange(n - 1):
        o.append(p * o[-1] + q * o[-2])
    return o[-1]

def gegenbauer(n, a='a'):
    '''
    Returns the *n-th* Gegenbauer polynomial in ``x``.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> gegenbauer(0)
        + 1
        >>> gegenbauer(1)
        + 2ax
        >>> gegenbauer(2)
        + 2a^2x^2 + 2ax^2 - a
        >>> 
        >>> 
        >>> gegenbauer(4)
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
        raise ValueError('Gegenbauer polynomials only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return 2*a*x
    return fractions.Fraction(1, n) * ((2*x * (n + a - ONE) * gegenbauer(n - 1) \
                                    - (n + 2*a - 2) * gegenbauer(n - 2)))

def laguerre(n):
    '''
    Returns the *n-th* Laguerre polynomial in ``x``.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> laguerre(0)
        + 1
        >>> laguerre(1)
        - x + 1
        >>> laguerre(2)
        + 1/2x^2 - 2x + 1
        >>> laguerre(3)
        - 1/6x^3 + 3/2x^2 - 3x + 1
        >>> laguerre(4)
        + 1/24x^4 - 2/3x^3 + 3x^2 - 4x + 1
        >>> laguerre(14)
        + 1/87178291200x^14 - 1/444787200x^13 + 13/68428800x^12 - 13/1425600x^11 + 143/518400x^10 - 143/25920x^9 + 143/1920x^8 - 143/210x^7 + 1001/240x^6 - 1001/60x^5 + 1001/24x^4 - 182/3x^3 + 91/2x^2 - 14x + 1

    Should be approximatively like a generalized Laguerre polynomial with ``a = 0`` (:func:`laguerre_g`)::

        >>> laguerre(5), laguerre_g(5)(a=0)
        (- 1/120x^5 + 5/24x^4 - 5/3x^3 + 5x^2 - 5x + 1, - 833333333333/100000000000000x^5 + 208333333333/1000000000000x^4 - 166666666667/100000000000x^3 + 5x^2 - 5x + 1)

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Laguerre_polynomials>`_ | `MathWorld <http://mathworld.wolfram.com/LaguerrePolynomial.html>`_
    '''

    if n < 0:
        raise ValueError('Laguerre polynomials only defined for n >= 0')
    if n == 0:
        return ONE
    if n == 1:
        return ONE - x

    l1, ll = NULL, ONE
    for i in xrange(1, n + 1):
        l0, l1 = l1, ll
        ll = ((2*i - 1 - x) * l1 - (i - 1) * l0) / monomial(i)

    if n & 1: ## little hack for odd n
        return -ll
    return ll

def laguerre_g(n, a='a'):
    '''
    Returns the *n-th* generalized Laguerre polynomial in ``x``.

    :raises: :exc:`ValueError` if *n* is negative
    :rtype: :class:`pypol.Polynomial`

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
        raise ValueError('Generalized Laguerre polynomials only defined for n >= 0')
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

def bernoulli(m):
    '''
    Returns the *m-th* Bernoulli polynomial.

    :raises: :exc:`ValueError` if *m* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> bernoulli(0)
        + 1
        >>> bernoulli(1)
        + x - 1/2
        >>> bernoulli(2)
        + x^2 - x + 1/6
        >>> bernoulli(3)
        + x^3 - 3/2x^2 + 1/2x
        >>> bernoulli(4)
        + x^4 - 2x^3 + x^2 - 1/30
        >>> bernoulli(5)
        + x^5 - 5/2x^4 + 5/3x^3 - 1/6x
        >>> bernoulli(6)
        + x^6 - 3x^5 + 5/2x^4 - 1/2x^2 + 1/42
        >>> bernoulli(16)
        + x^16 - 8x^15 + 20x^14 - 182/3x^12 + 572/3x^10 - 429x^8 + 1820/3x^6 - 1382/3x^4 + 140x^2 - 3617/510
        >>> bernoulli(36)
        + x^36 - 18x^35 + 105x^34 - 3927/2x^32 + 46376x^30 - 1008678x^28 + 19256580x^26 - 316816590x^24 + 4429013400x^22 - 51828575337x^20 + 498870877450x^18 - 3866772293937x^16 + 23507139922200x^14 - 108370572082590x^12 + 362347726769028x^10 - 826053753510678x^8 + 1171754413536680x^6 - 1780853160521127/2x^4 + 270657225128535x^2 - 26315271553053477373/1919190

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bernoulli_polynomials>`_ | `MathWorld <http://mathworld.wolfram.com/BernoulliPolynomial.html>`_
    '''

    def _sum(n):
        return sum([(-1) ** k * bin_coeff(n, k) * (x + k) ** m for k in xrange(0, n + 1)])
    if m < 0:
        raise ValueError('Bernoulli polynomials only defined for m >= 0')
    if m == 0:
        return ONE
    return x ** m + sum([fractions.Fraction(1, n + 1) * _sum(n) for n in xrange(1, m + 1)])

def bern_num(m):
    '''
    Returns the *m-th* Bernoulli number.

    :raises: :exc:`ValueError` if *m* is negative
    :rtype: :class:`fractions.Fraction`

    .. note::
        If *m* is odd, the result is always 0.

    **Examples**

    ::

        >>> bern_num(0)
        + 1
        >>> bern_num(1)
        - 1/2
        >>> bern_num(2)
        Fraction(1, 6)
        >>> bern_num(3)
        0
        >>> bern_num(4)
        Fraction(-1, 30)
        >>> bern_num(6)
        Fraction(1, 42)
        >>> bern_num(8)
        Fraction(-1, 30)
        >>> bern_num(10)
        Fraction(5, 66)

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bernoulli_numbers>`_ | `MathWorld <http://mathworld.wolfram.com/BernoulliNumber.html>`_
    '''

    def _sum(k):
        return sum([(-1) ** v * fractions.Fraction.from_float(bin_coeff(k, v)) * fractions.Fraction(v ** m, k + 1) for v in xrange(k + 1)])
    if m < 0:
        raise ValueError('Bernoulli numbers only defined for m >= 0')
    if m == 0:
        return 0
    if m == 1:
        return fractions.Fraction(-1, 2)
    if m & 1:
        return 0
    #return bernoulli(n).right_hand_side
    return sum([_sum(k) for k in xrange(m + 1)])

def euler(m):
    '''
    Returns the *m-th* Bernoulli polynomial.

    :raises: :exc:`ValueError` if *m* is negative
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    ::

        >>> euler(0)
        + 1
        >>> euler(1)
        + x - 1/2
        >>> euler(2)
        + x^2 - x
        >>> euler(3)
        + x^3 - 3/2x^2 + 1/4
        >>> euler(4)
        + x^4 - 2x^3 + x
        >>> euler(5)
        + x^5 - 5/2x^4 + 5/2x^2 - 1/2
        >>> euler(15)
        + x^15 - 15/2x^14 + 455/4x^12 - 3003/2x^10 + 109395/8x^8 - 155155/2x^6 + 943215/4x^4 - 573405/2x^2 + 929569/16

    **References**

    `MathWorld <http://mathworld.wolfram.com/EulerPolynomial.html>`_
    '''

    def _sum(n):
        return sum([(- 1) ** k * bin_coeff(n, k) * (x + k) ** m for k in xrange(n + 1)])
    if m < 0:
        raise ValueError('Euler polynomials only defined for m >= 0')
    if m == 0:
        return ONE
    return x ** m + sum([fractions.Fraction(1, 2 ** n) * _sum(n) for n in xrange(1, m + 1)])

def eu2(m):
    def _sum(n):
        return sum([(- 1) ** k * bin_coeff(n, k) * (x + k) ** m for k in xrange(n + 1)])
    if m == 0:
        return ONE
    return sum([_sum(n) * fractions.Fraction(1, 2 ** n) for n in xrange(m + 1)])

def euler_num(m): ## Still in development
    '''
    Returns the *m-th* Euler number.

    :raises: :exc:`ValueError` if *m* is negative
    :rtype: Integer

    .. note::
        If *m* is odd, the result is always 0.

    **Examples**

    ::

        

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bernoulli_numbers>`_ | `MathWorld <http://mathworld.wolfram.com/BernoulliNumber.html>`_
    '''

    if m < 0:
        raise ValueError('Euler numbers only defined for m >= 0')
    if m == 0:
        return ONE
    if m & 1:
        return 0
    return int(2 ** m * euler(m)(.5))

def e2(m):
    def _sum(k):
        return sum([bin_coeff(k, i) * (((-1) ** i * (k - 2*i) ** (m + 1)) / (2 ** k * c ** k * k)) for i in xrange(k + 1)])
    if m == 0:
        return ONE
    if m & 1:
        return 0
    c = 1j
    return math.ceil((c * sum([_sum(k) for k in xrange(1, m + 2)])).real)

def genocchi(n):
    '''
    Returns the *n-th* Genocchi number.

    :rtype: integer or :class:`fractions.Fraction`

    .. note::
        If *n* is odd, the result is always 0.

    **Examples**

    ::

        >>> genocchi(0)
        0
        >>> genocchi(2)
        -1
        >>> genocchi(8)
        17
        >>> genocchi(17)
        0
        >>> genocchi(34)
        -14761446733784164001387L

    Should be quite fast::

        >>> from timeit import timeit
        >>> timeit('(genocchi(i) for i in xrange(1000))', 'from pypol.funcs import genocchi', number=1000000)
        1.8470048904418945
    '''

    if not n:
        return 0
    if n == 1:
        return 1

    r = 2 * (1 - 2 ** n) * bern_num(n)
    if not r:
        return 0
    try:
        rint = int(r)
    except TypeError:
        return r

    if rint == r:
        return rint
    return r


################################################################################
##                            Still in development                            ##
################################################################################

def bernstein(v, n): ## Still in development
    if not v and not n:
        return ONE
    if v == n:
        return x ** v
    return bin_coeff(n, v) * (x**v) * (1 - x) ** (n - v)

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