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

def quadratic(poly):
    '''
    Returns the two roots of the polynomial *poly* solving the quadratic equation:
        |p1|
    where the polynomial is |p2|.

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

def newton(poly, x=1, epsilon=float('-inf')):
    '''
    Returns one root of the polynomial *poly*.

    :param integer x: the start value for evaluate ``poly(x)``.
    :param integer epsilon: the precision of the calculus (default to ``float('-inf')``).
    :rtype: integer of float

    **Examples**

    ::

        >>> k = poly1d([2, 5, 3])
        >>> k
        + 2x^2 + 5x + 3

    the roots (real) of this polynomial are ``-1`` and ``-1.5``.
    We start with 10::

        >>> newton(k, 10)
        -1.0000000000000002

    so we try ``-1``::

        >>> newton(k, -1)
        -1
        >>> k(-1)
        0

    We have one root! We continue::

        >>> newton(k, -2)
        -1.5
        >>> k(-1.5)
        0.0

    But this function cannot find complex roots::

        >>> k = poly1d([1, -3, 6])
        >>> k
        + x^2 - 3x + 6
        >>> quadratic(k) ## quadratic works for polynomial with degree 2 only
        ((1.5+1.9364916731037085j), (1.5-1.9364916731037085j))
        >>> newton(k)
        
        Traceback (most recent call last):
          File "<pyshell#157>", line 1, in <module>
            newton(k)
          File "funcs.py", line 261, in newton
            poly_d = polyder(poly)
          File "core.py", line 1308, in __call__
            letters = dict(zip(self.letters[:len(args)], args))
          File "core.py", line 552, in letters
            for m in self._monomials if m[1]], set())))
        KeyboardInterrupt
        >>> newton(k, -1)
        
        Traceback (most recent call last):
          File "<pyshell#158>", line 1, in <module>
            newton(k, -1)
          File "funcs.py", line 261, in newton
            poly_d = polyder(poly)
          File "core.py", line 1311, in __call__
            return eval(self.eval_form, letters)
          File "core.py", line 522, in eval_form
            for c, vars in self._monomials:
        KeyboardInterrupt

    We must interrupt!

    .. versionadded:: 0.3
    '''

    poly_d = polyder(poly)

    while True:
        p_s = poly(x)
        if not p_s:
            break
        x_n = x - p_s / poly_d(x)
        if x == x_n or abs(x - x_n) <= epsilon:
            break
        x = x_n

    return x

def ruffini(poly):
    '''
    Returns the zeros of the polynomial basing on the right-hand side. If the polynomial has not the right-hand side, returns an empty list.

    **Examples**

    ::

        >>> p = poly1d([1, 5, 5, -5, -6])
        >>> p
        + x^4 + 5x^3 + 5x^2 - 5x - 6
        >>> ruffini(p)
        [-1, 1]
        >>> p(-1), p(1)
        (0, 0)

    and we can go on::

        >>> p2, p3 = p / (x - 1), p / (x + 1)
        >>> p2, p3
        (+ x^3 + 6x^2 + 11x + 6, + x^3 + 4x^2 + x - 6)
        >>> ruffini(p2), ruffini(p3)
        ([-1, -2, -3], [1])
        >>> p2(-1), p2(-2), p2(-3)
        (0, 0, 0)
        >>> p3(1)
        0
        >>> p4, p5, p6 = p2 / (x - 1), p2 / (x - 2), p / (x - 3)
        >>> p4, p5, p6
        (+ x^2 + 7x + 18, + x^2 + 8x + 27, + x^3 + 8x^2 + 29x + 82)
        >>> ruffini(p4), ruffini(p5), ruffini(p6)
        ([], [], [])

    there are no more real roots, but if we try :func:`quadratic`::

        >>> quadratic(p4), quadratic(p5)
        (((-3.5+2.3979157616563596j), (-3.5-2.3979157616563596j)), ((-4+3.3166247903553998j), (-4-3.3166247903553998j)))
    '''

    def _divs(n):
        d = [1] + [x for x in xrange(2, n // 2 + 1)] + [n]
        return map(operator.neg, d) + d

    p = poly.right_hand_side
    if not p:
        return []
    return [x for x in _divs(p) if not poly(x)]

def bisection(poly, k=0.5, epsilon=10**-8):
    '''
    Finds the root of the polynomial *poly* using the *bisection method*.
    When it finds the root, it checks if ``-root`` is a root too. If so, it returns a two-length tuple, else a tuple
    with one root.

    :param float k: the increment of the two extreme point. The increment is calculated with the formula ``a + ak``.

    So, if *a* is 50, after the increment ``50 + 50*0.5`` *a* will be 75.
    *epsilon* sets the precision of the calculation. Smaller it is, greater is the precision.

    .. warning:: If *epsilon* is bigger than 5 or *k* is negative, :exc:`ValueError` is raised.
    .. warning:: NotImplemented is returned if:

            * *poly* has more than one letter
            * or the root is a complex number

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bisection_method>`_

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
    '''

    def _single_der(var):
        return [var[0]*var[1], var[1] - 1]

    try:
        variable = p.letters[0]
    except IndexError:
        variable = 'x'

    return poly1d_2([_single_der(t) for t in p.to_plist()], variable)

def polyint(p, C=None):
    '''
    Returns the indefinite integral of the polynomial *p*:
        |p5|

    :param Polynomial p: the polynomial
    :param integer C: the costant that will be added to the polynomial
    :rtype: :class:`pypol.Polynomial`

    **Examples**

    Calculate the integrals of the polynomials: |p6| and |p7|::

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

    p = poly1d_2([_single_int(t) for t in p.to_plist()])
    if C:
        p += C
    return p

def polyint_(poly, a, b):
    '''
    Returns the definite integral of the polynomial *poly*, with upper and lower limits:
        |p8|

    :param integer a: the lower limit
    :param integer b: the upper limit
    :rtype: :class:`pypol.Polynomial`
    '''

    F = polyint(poly)
    return F(a) - F(b)

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

def spread(n):
    '''
    Returns the *nth* Spread polynomial in ``x``.
    '''

    if n < 0:
        return Polynomial()
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
        return Polynomial()
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
        return Polynomial()
    if n == 0:
        return ONE
    if n == 1:
        return a + ONE - x

    a = monomial(**{a: 1})
    l1, ll = Polynomial(), ONE
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

def durand_kerner(poly, start=complex(.4, .9)):
    roots = []
    deg = poly.degree
    for e in xrange(deg):
        roots.append(start ** e)
    while True:
        pass