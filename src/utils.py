'''
This file is part of the pypol project.
(C) Copyright 2010 Michele Lacchia
'''

import random
import operator
import fractions

from core import Polynomial, poly1d, poly1d_2, polynomial


def divisible(a, b):
    '''
    Returns True whether a and b are divisible, i.e. ``a % b == 0``

    :params a: the first polynomial
    :params b: the second polynomial
    :rtype: bool

    Example::

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

def make_polynomial(monomials, simplify=True):
    '''
    Make a polynomial from a list of tuples.

    :param monomials: list of monomials
    :param bool simplify: if True, it simplifies the polynomial on __init__ and :meth:`Polynomial.update`
    :type monomials: list of tuples

    For example::

        >>> make_polynomial(parse_polynomial('2x + 3y - 4'))
        2x + 3y - 4
        >>> make_polynomial(((2, {'x': 1}), (3, {'y': 1}), (-4, {})))
        2x + 3y - 4
    '''

    return Polynomial(monomials, simplify)

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
        return operator.truediv(a, gcd(a, b)) * b
    except ValueError:
        return operator.truediv(b, gcd(b, a)) * a

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
    if not right_hand_side:
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

def root(poly, k=0.5, epsilon=10**-8):
    '''
    Finds the root of the polynomial *poly* using the *bisection method* [#f1]_.
    Before trying to find the root, it tries ``poly.zeros``.
    When it finds the root, it checks if -root is a root too. If so, it returns a two-length tuple, else a tuple
    with one root.
    *k* is the increment of the two extreme point. The increment is calculated with the following formula::

        a + ak

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

    if poly.zeros and poly.zeros != NotImplemented:
        return poly.zeros

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
    def _single_der(var):
        return [var[0]*var[1], var[1] - 1]

    return poly1d_2([_single_der(t) for t in p.to_plist()])

def polyint(p, letter='x'):
    def _single_int(monomial):
        n = monomial[1].get()
        return fractions.Fraction(1, )
    pass

def fib_poly(n):
    '''
    Returns the *nth* Fibonacci polynomial in *x*::

        
    '''

    if n <= 0:
        return Polynomial()
    elif n == 1:
        return poly1d([1])
    elif n == 2:
        return poly1d([1], right_hand_side=False)
    elif n > 2:
        return polynomial('x')*fib_poly(n - 1) + fib_poly(n - 2)