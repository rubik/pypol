'''
This file is part of the pypol project.
(C) Copyright 2010 Michele Lacchia
'''

from __future__ import division
import random
import operator
import fractions

from core import Polynomial, poly1d, poly1d_2, polynomial


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

def remove_multiple_roots(poly):
    '''
    Removes multiple roots, speeding up root-finding.
    '''

    return poly / gcd(poly, polyder(poly))

def quadratic(poly):
    '''
    Returns the two roots of the polynomial *poly* solving the quadratic equation:
        .. image:: quad_eq.gif

    where the polynomial is: ``ax^2 + bx + c``.

    .. warning::
        The polynomial must be of the second degree.

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

    assert poly.degree == 2
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

def newton(poly, start=1, epsilon=10**-8): ## Still in development
    poly_d = polyder(poly)

    while True:
        if poly(start) == 0:
            break
        if poly(start) <= epsilon:
            break
        n = start - poly(start) / poly_d(start)
        if start == n:
            break
        start = n

    return start

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

    if len(poly.letters) != 1:
        return NotImplemented

    if all(coeff > 0 for coeff in poly.coefficients) and \
        all(exp & 1 == 0 for exp in poly.powers(poly.letters[0])): #complex root
        return NotImplemented

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
    '''

    if n <= 0:
        return Polynomial()
    elif n == 1:
        return poly1d([1])
    elif n == 2:
        return poly1d([1], right_hand_side=False)
    p = [poly1d([1]), poly1d([1], right_hand_side=False)]
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
    '''

    if n <= 0:
        return Polynomial()
    elif n == 1:
        return poly1d([1])
    elif n == 2:
        return poly1d([1], right_hand_side=False)
    elif n > 2:
        return polynomial('x')*fib_poly(n - 1) + fib_poly(n - 2)

def hermite_prob(n):
    '''
    '''

    x = poly1d([1, 0])
    if n < 0:
        return Polynomial()
    if n == 0:
        return poly1d([1])
    if n == 1:
        return x
    p = [x]
    for _ in xrange(n - 1):
        p.append(p[-1] * x - polyder(p[-1]))
    return p[-1]

def hermite_prob_r(n):
    '''
    '''

    x = poly1d([1, 0])
    if n < 0:
        return Polynomial()
    if n == 0:
        return poly1d([1])
    if n == 1:
        return x
    return hermite_prob(n - 1) * x - polyder(hermite_prob(n - 1))

def hermite_phys(n):
    '''
    '''

    if n < 0:
        return Polynomial()
    if n == 0:
        return poly1d([1])
    x = poly1d([1, 0])
    p = [poly1d([1])]
    for _ in xrange(n):
        p.append((p[-1] * x * 2) - polyder(p[-1]))
    return p[-1]

def hermite_phys_r(n):
    '''
    '''

    if n < 0:
        return Polynomial()
    if n == 0:
        return poly1d([1])
    x = poly1d([1, 0])
    return (hermite_phys(n - 1) * x * 2) - polyder(hermite_phys(n - 1))