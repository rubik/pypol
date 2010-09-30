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

ONE = monomial()
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

    .. versionadded:: 0.2
    '''

    return a % b == polynomial()

def gcd(a, b):
    '''
    Returns the Greatest Common Divisor between the two polynomials::

       >>> gcd(polynomial('3x'), polynomial('6x^2'))
       + 3x

    .. seealso::
        :func:`lcm`. 
    '''

    if not b:
        return a
    while True:
        r = a % b
        if not r:
            return b
        a, b = b, r

def lcm(a, b):
    '''
    Returns the Least Common Multiple of the two polynomials::

        >>> lcm(polynomial('3x'), polynomial('6x^2'))
        + 6x^2

    .. seealso::
        :func:`gcd`.
    '''

    try:
        k = operator.truediv(a, gcd(a, b)) * b
    except ValueError:
        k = operator.truediv(b, gcd(b, a)) * a

    if int(k) == k:
        return int(k)
    return k

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

    :rtype: :class:`Polynomial`

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

def quadratic(poly):
    '''
    Returns the two roots of the polynomial *poly* solving the quadratic equation:
        .. image:: quad_eq.gif

    where the polynomial is: ``ax^2 + bx + c``.

    :raises: :exc:`AssertionError` if the polynomial's degree is not 2.
    :rtype: 2 length tuple

    **Examples**

    ::

        >>> p = poly1d([1, 0, -4])
        >>> p
        + x^2 - 4
        >>> quadratic(p)
        (2.0, -2.0)
        >>> p(2)
        0
        >>> p(-2)
        0
        >>> p = poly1d([2, 3, 1])
        >>> p
        + 2x^2 + 3x + 1
        >>> quadratic(p)
        (-0.5, -1.0)
        >>> p(-0.5)
        0.0
        >>> p(-1.0)
        0.0

    this functions can return complex numbers too::

        >>> p = poly1d([-4, 5, -3])
        >>> p
        - 4x^2 + 5x - 3
        >>> quadratic(p)
        ((0.625-0.59947894041408989j), (0.625+0.59947894041408989j))

    but the precision is lower::

        >>> p = poly1d([-4, 5, -3])
        >>> p
        - 4x^2 + 5x - 3
        >>> quadratic(p)
        ((0.625-0.59947894041408989j), (0.625+0.59947894041408989j))
        >>> r1 = (0.625-0.59947894041408989j)
        >>> p(r1)
        (-4.4408920985006262e-16+0j)
        >>> r2 = (0.625+0.59947894041408989j)
        >>> p(r2)
        (-4.4408920985006262e-16+0j)

    .. versionadded:: 0.3
    '''

    def _get(power):
        if power == 0:
            return poly.right_hand_side or 0
        plist = poly.to_plist()
        c = [None] + plist[::-1]
        if c[power][1] == power:
            return c[power][0]
        else:
            for t in plist:
                if t[1] == power:
                    return t[0]
            return 0

    assert poly.degree == 2, 'The polynomial\'s degree must be 2'
    if len(poly.coefficients) == 3:
        a, b, c = poly.coefficients
    else:
        a, b, c = map(_get, [2, 1, 0])
    r = b ** 2 - 4*a*c
    if r < 0:
        r = complex(imag=(-r) ** 0.5)
    else:
        r = r ** 0.5
    return ((-b + r) / (2*a), (-b - r) / (2*a))

def newton(poly, start=1, c=100):
    '''
    Returns one root of the polynomial *poly*.

    :param integer start: the start value for evaluate ``poly(x)``.
    :param integer c: the number of cycles to perform.
    :rtype: integer of float

    **Examples**

    ::

        >>> k = poly1d([2, 5, 3])
        >>> k
        + 2x^2 + 5x + 3
        >>> funcs.newton(k, -1)
        -1
        >>> k(-1)
        0
        >>> funcs.newton(k, 1)
        -1.0000000000000004
        >>> r = funcs.newton(k, 1)
        >>> r
        -1.0000000000000004
        >>> k(r)
        0.0
        >>> funcs.newton(k, -900) ## If the starting value is too far from the root, the precision is lower
        -1.4999999999999996

    .. versionadded:: 0.3
    '''

    poly_d = polyder(poly)

    for _ in xrange(c):
        p_s = poly(start)
        if not p_s:
            return start
        x_n = start - p_s / poly_d(start)
        if start == x_n:
            break
        start = x_n

    return start

def ruffini(poly):
    '''
    
    '''

    def _divs(n):
        d = [1] + [x for x in xrange(2, n // 2 + 1)] + [n]
        return map(lambda i: i * -1, d) + d

    p = poly.right_hand_side
    if not p:
        return []
    return [x for x in _divs(p) if not poly(x)]

def bisection(poly, k=0.5, epsilon=10**-8):
    '''
    Finds the root of the polynomial *poly* using the *bisection method* [#f1]_.
    When it finds the root, it checks if ``-root`` is a root too. If so, it returns a two-length tuple, else a tuple
    with one root.

    :param float k: the increment of the two extreme point. The increment is calculated with the formula ``a + ak``.

    So, if *a* is 50, after the increment ``50 + 50*0.5`` *a* will be 75.
    *epsilon* sets the precision of the calculation. Smaller it is, greater is the precision.

    .. warning:: If *epsilon* is bigger than 5 or *k* is negative, :exc:`ValueError` is raised.
    .. warning:: NotImplemented is returned if:

            * *poly* has more than one letter
            * or the root is a complex number

    .. versionadded:: 0.2
    '''

    if k < 0:
        raise ValueError('k value cannot be negative')

    if epsilon > 5:
        raise ValueError('epsilon cannot be greater than 5')

    assert len(poly.letters) == 1

    assert  not all(coeff > 0 for coeff in poly.coefficients) and \
            not all(exp & 1 == 0 for exp in poly.powers(poly.letters[0])), \
            'The root of the polynomial is a complex number'

    _d = lambda a, b: a * b < 0 # Check if discordant
    a, b = -50, 45

    try:
        while abs(a - b) > 2*epsilon:
            media = (a + b) / 2 # Midpoint
            if _d(poly(a), poly(media)):
                b = media
            elif _d(poly(b), poly(media)):
                a = media
            else: # Not discordant
                a, b = a + a*k, b + b*k
    except OverflowError:
        return NotImplemented

    return int(media)

def polyder(p):
    '''
    Returns the derivative of the polynomial *p*.

    :param Polynomial poly: the polynomial
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    Calculate the derivative of the polynomials ``x^2`` and ``2x^3 - 4x^2 + 1``::

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
    '''

    def _single_der(var):
        return [var[0]*var[1], var[1] - 1]

    try:
        variable = p.letters[0]
    except IndexError:
        variable = 'x'

    return poly1d_2([_single_der(t) for t in p.to_plist()], variable)

def polyint(p):
    '''
    Returns the integral of the polynomial *p*

    :param Polynomial p: the polynomial
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    Calculate the integrals of the polynomials ``-x`` and ``x^3 - 7x + 5``
    ::

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

    .. versionadded:: 0.3
    '''

    def _single_int(var):
        n = var[1] + 1
        if not n:
            return [0, 0]
        j = fractions.Fraction(var[0], n)
        if int(j) == j:
            j = int(j)
        return [j, n]

    return poly1d_2([_single_int(t) for t in p.to_plist()])

def interpolate(poly, x_values, y_values):
    '''
    Interpolate the polynomial *poly* with the Newton method.

    :param Polynomial poly: the polynomial to interpolate
    :param list x_values: the list of the *abscissas*
    :param list y_values: the list of the *ordinates*
    :rtype: Polynomial

    **Examples**

    ::

        
    '''

    assert len(x_values) != 0 and (len(x_values) == len(y_values)), 'x and y cannot be empty and must have the same length'
    b0 = y[0]

    coeffs = []
    for i, x in enumerate(x_values):
        return NotImplemented

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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
    if n == 0:
        return ONE
    if n == 1:
        return x
    p = poly1d([n])
    return x * (x - p*variable) ** (n - 1)

def bernstein(v, n): ## Still in development
    def _bin_coeff(n, k):
        return math.factorial(n)/(math.factorial(k)*math.factorial(n - k))

    if not v and not n:
        return ONE
    return _bin_coeff(n, v) * (x**v) * poly1d([-1, 1]) ** (n - v)

def laguerre(n): ## Still in development
    if n < 0:
        return Polynomial()
    if n == 0:
        return ONE
    if n == 1:
        return ONE - x
    return (1 / (n + 1))*((2 * n + 1 - x) * laguerre(n - 1) - n * laguerre(n - 2))