#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials (and monomials too)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
- Python 2.6 (or 2.7)
'''

from __future__ import division       ## STATS ##
import copy                        ## used 6 times
import fractions                   ## used 6 times
import operator                    ## used 6 times
import random                      ## used 7 times
import re                          ## 2 used times


__author__ = 'Michele Lacchia'
__version__ = (0, 2)
__version_str__ = '0.2'

__all__ = ['polynomial', 'algebraic_fraction', 'monomial', 'gcd', 'lcm', 'gcd_p', 'lcm_p', 'are_similar', 'make_polynomial', 'parse_polynomial', 'random_poly', 'root', 'Polynomial', 'AlgebraicFraction',]


def polynomial(string=None, simplify=True):
    '''
    Returns a :class:`Polynomial` object.

    :param string: a string that represent a polynomial, default is None.
    :param simplify: if True, the polynomial will be simplified on __init__ and on update.
    :type string: string or None
    :type simplify: bool
    :rtype: :class:`Polynomial`
    '''

    if not string:
        return Polynomial()
    return make_polynomial(parse_polynomial(string), simplify)

def algebraic_fraction(s1, s2='1', simplify=True):
    '''
    Wrapper function that returns an :class:`AlgebraicFraction` object.

    :parameters s1, s2: two strings that represent a polynomial

    ::

        >>> algebraic_fraction('3x^2 - 4xy', 'x + y')
        AlgebraicFraction(+ 3x² - 4xy, + x + y)
        >>> algebraic_fraction('3x^2 - 4xy', 'x + y').terms
        (+ 3x^2 - 4xy, + x + y)

    .. seealso::
        :class:`AlgebraicFraction`
    '''

    return AlgebraicFraction(polynomial(s1), polynomial(s2), simplify)

def monomial(c=1, **vars):
    '''
    Simple function that returns a :class:`Polynomial` object.

    :param c: the coefficient of the polynomial
    :key \*\*vars: the monomial's letters

    ::

        >>> monomial(5, a=3, b=4)
        + 5a^3b^4
        >>> m = monomial(5, a=3, b=4)
        >>> m
        + 5a^3b^4
        >>> type(m)
        <class 'pypol.src.pypol.Polynomial'>
        >>> m.monomials
        ((5, {'a': 3, 'b': 4}),)

    This function is useful when you need a monomial. If there isn't this function you should do::

       >>> Polynomial(((5, {'a': 3, 'b': 4}),))
       + 5a^3b^4

    Either *c* or *\*\*vars* is optional::

        >>> monomial()
        + 1
        >>> monomial(1)
        + 1


    Equivalent to::

        def monomial(c=1, **vars):
            return Polynomial(((c, vars),))

    .. versionadded:: 0.2
    '''

    return Polynomial(((c, vars),))

def make_polynomial(monomials, simplify=True):
    '''
    Make a polynomial from a list of tuples.

    :param monomials: list of monomials
    :param simplify: if True, it simplifies the monomial on __init__ and :meth:`Polynomial.update`
    :type monomials: list of tuples
    :type simplify: bool

    For example::

        >>> make_polynomial(parse_polynomial('2x + 3y - 4'))
        2x + 3y - 4
        >>> make_polynomial(((2, {'x': 1}), (3, {'y': 1}), (-4, {})))
        2x + 3y - 4
    '''

    return Polynomial(monomials, simplify)

def are_similar(a, b):
    '''
    Returns True whether the two monomials *a* and *b* are similar, i.e. they have the same literal part, False otherwise.
    An example::

        >>> are_similar((-2, {'x': 2, 'y': 2}), (-2, {'x': 3}))
        False
        >>> are_similar((3, {'y': 4}), (4, {'y': 4}))
        True
    '''

    return a[1] == b[1]

def gcd(a, b):
    '''
    Returns the Greatest Common Divisor between the two polynomials::

       >>> gcd(polynomial('3x'), polynomial('6x^2'))
       + 3x

    .. seealso::
        :func:`gcd_p`, :func:`lcm`, :func:`lcm_p`. 
    '''

    coefficient = fractions.gcd(a.coeff_gcd, b.coeff_gcd)
    letters = set(a.letters).intersection(b.letters)
    return monomial(coefficient, **_get_letters_powers(a, b, letters))

def gcd_p(*polynomials):
    '''
    Like :func:`gcd`, but accepts many arguments::

        >>> gcd_p(polynomial('3x'), polynomial('6x^2'), polynomial('8x^3'))
        + x

    Equivalent to::

        def gcd_p(*polynomials):
            return reduce(gcd, polynomials)

    .. seealso::
        :func:`gcd`, :func:`lcm`, :func:`lcm_p`. 
    '''

    return reduce(gcd, polynomials)

def lcm(a, b):
    '''
    Returns the Least Common Multiple of the two polynomials::

        >>> lcm(p('3x'), p('6x^2'))
        + 6x^2

    .. seealso::
        :func:`gcd`, :func:`gcd_p`, :func:`lcm_p`.
    '''

    coefficient = (operator.truediv(a.coeff_lcm*b.coeff_lcm, fractions.gcd(a.coeff_lcm, b.coeff_lcm)))
    if coefficient == int(coefficient):
        coefficient = int(coefficient)
    else:
        coefficient = fractions.Fraction(str(coefficient))
    letters = set(a.letters).intersection(b.letters)
    return monomial(coefficient, **_get_letters_powers(a, b, letters, False))

def lcm_p(*polynomials):
    '''
    Like :func:`lcm`, but accepts many arguments::

        >>> lcm_p(polynomial('3x'), polynomial('6x^2'), polynomial('8x^3'))
        + 24x^3

    Equivalent to::

        def lcm_p(*polynomials):
            return reduce(lcm, polynomials)

    .. seealso::
        :func:`gcd`, :func:`gcd_p`, :func:`lcm`.
    '''

    return reduce(lcm, polynomials)

def parse_polynomial(string, max_length=None):
    '''
    Parses a string that represent a polynomial.
    It can parse integer coefficients, float coefficient and fractional coefficient.

    :param string: a string that represent a polynomial
    :param max_length: represents the maximum length that the polynomial can have.
    :type max_length: integer or None

    An example::

        >>> parse_polynomial('2x^3 - 3y + 2')
        [(2, {'x': 3}), (-3, {'y': 1}), (2, {})]
        >>> parse_polynomial('x3 - 3y2 + 2')
        [(1, {'x': 3}), (-3, {'y': 2}), (2, {})]

    .. seealso::
        :ref:`syntax-rules`
    '''

    monomials = []
    regex = re.compile(r'([-+]?\s*\d*[\./]?\d*)((?:\w?\^?\d*)*)')

    for c, l in regex.findall(string):
        if max_length and len(monomials) == max_length:
            return monomials

        c, l = c.strip(), l.strip()
        if not c and not l:
            continue
        c, l = _parse_coeff(c), _parse_letters(l)
        monomials.append((c, l))

    return monomials

def random_poly(coeff_range=xrange(-10, 11), len_=None, letters='xyz', max_letters=3, unique=False, exp_range=xrange(1, 6), right_hand_side=None):
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

        .. versionadded:: 0.2

    :param exp_range: the range of the exponents.

    :param right_hand_side: if True, the polynomial will have a right-hand side. Default is None, that means the right-hand side will be chosen randomly.

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
    '''

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

    return Polynomial(monomials)

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

    if all(coeff > 0 for coeff in poly.coefficients) and all(exp & 1 == 0 for exp in poly.powers(poly.letters[0])):
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
        print 'Errore!'
        return NotImplemented

    return int(media)

def factors(poly):
    '''
    
    '''

    r = root(poly)
    if r in (0, NotImplemented):
        return (poly,)

    p = polynomial(poly.letters[0]) - r
    return (poly / p, p)

def _parse_coeff(c):
    if not c:
        return 1
    elif c == '+':
        return 1
    elif c == '-':
        return -1
    elif '.' in c or '/' in c:
        return fractions.Fraction(c)
    else:
        return int(c)

def _parse_letters(l):
    d = {}
    r = re.compile(r'(\w?)\^?(\d*)')
    for letter, exp in r.findall(l):
        letter, exp = letter.strip(), exp.strip()
        if not letter and not exp:
            continue
        if not exp:
            exp = 1
        d[letter] = int(exp)
    return d

def _get_letters_powers(a, b, l, min_=True):
    d = {} ## Change for Py2.7
    for letter in l:
        if min_:
            d[letter] = min(a.min_power(letter), b.min_power(letter))
        else:
            d[letter] = max(a.max_power(letter), b.max_power(letter))
    return d


class Polynomial(object):
    '''
    A :class:`Polynomial` is an object that represents a Polynomial.
    It accepts two arguments: *monomials* and *simplify*.

    *monomials* is a tuple of tuples that represents all the polynomial's monomials.

    If *simplify* is True, then the polynomial will be simplified on __init__ and on :meth:`update`.

    .. seealso::
        :meth:`simplify`

    An example::

        >>> monomials = ((2, {'x': 3}), (4, {'x': 1, 'y': 1}))
        >>> p = Polynomial(monomials)
        >>> p
        + 2x^3 + 4xy
        >>> Polynomial(((2, {}),)) ## Remember the comma!
        + 2
        >>> parse_polynomial('2x^3 + 4xy')
        [(2, {'x': 3}), (4, {'y': 1, 'x': 1})]
        >>> p = Polynomial(parse_polynomial('2x^3 + 4xy'))
        >>> p
        + 2x^3 + 4xy
        >>> p = Polynomial(parse_polynomial('2x^3 + 4xy - 2xy + 4 - 3'), simplify=False)
        >>> p
        + 2x^3 + 4xy - 2xy + 4 - 3
        >>> p.simplify()
        >>> p
        + 2x^3 + 2xy + 1

    We can use the :func:`parse_polynomial` function too.
    '''

    __slots__ = ('_monomials', '_simplify',)

    def __init__(self, monomials=(), simplify=True):
        self._monomials = monomials
        self.sort(key=self._key, reverse=True)
        self._simplify = simplify
        if self._simplify:
            self.simplify()

    @ property
    def monomials(self):
        '''
        **property**

        monomials is a property that returns the polynomial's monomials.
        Example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).monomials
            ((2, {'x': 3}), (4, {'y': 1, 'x': 1}))

        You can also set the monomials::

            >>> p = Polynomial(parse_polynomial('2x^3 + 4xy'))
            >>> p.monomials = ((2, {}),) # The comma!
            >>> p
            + 2
        '''

        return self._monomials

    @ monomials.setter
    def monomials(self, values):
        self.sort(values, key=self._key, reverse=True)

    def ordered_monomials(self, cmp=None, key=None, reverse=False):
        '''
        Applies :func:`sorted` to the polynomial's monomials, with *cmp*, *key* and *reverse* arguments.
        '''

        return sorted(self._monomials, cmp, key, reverse)

    def sort(self, cmp=None, key=None, reverse=False):
        '''
        Sort the polynomial's monomials in-place::

            >>> k = Polynomial(parse_polynomial('x2 -y2 xy'))
            >>> k.sort()
            >>> k
            - y^2 + x^2 + xy
            >>> k.sort(key=k._key, reverse=True) ## 
            >>> k
            + x^2 + xy - y^2
        '''

        self._monomials = tuple(self.ordered_monomials(cmp, key, reverse))

    @ property
    def coefficients(self):
        '''
        **property**

        Returns the polynomial's coefficients::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 5')).coefficients
            [2, 4, -5]
        '''

        return [monomial[0] for monomial in self._monomials]

    @ property
    def coeff_gcd(self):
        '''
        **property**

        Returns the Greatest Common Divisor of the polynomial coefficients::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16')).coeff_gcd
            -2

        Equivalent to::

            >>> import fractions
            >>> reduce(fractions.gcd, Polynomial(parse_polynomial('2x^3 + 4xy - 16')).coefficients)
            -2

        .. seealso::
            :meth:`coeff_lcm`
        '''

        return reduce(fractions.gcd, self.coefficients)

    @ property
    def coeff_lcm(self):
        '''
        **property**

        Returns the Least Common Multiple of the polynomial coefficients::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16')).coeff_lcm
            16.0

        Equivalent to::

            >>> import fractions
            >>> import operator
            >>> reduce(lambda a, b: operator.truediv(a*b, fractions.gcd(a, b), Polynomial(parse_polynomial('2x^3 + 4xy - 16')).coefficients)
            16.0

        .. seealso::
            :meth:`coeff_gcd`
        '''

        c_lcm = reduce(lambda a, b: operator.truediv(a*b, fractions.gcd(a, b)), self.coefficients)
        if c_lcm == int(c_lcm):
            c_lcm = int(c_lcm)
        else:
            c_lcm = fractions.Fraction(str(c_lcm))
        return c_lcm

    @ property
    def gcd(self):
        '''
        **property**

        Returns the Greatest Common Divisor of the polynomial::

            >>> Polynomial(parse_polynomial('3x^4 - 9x')).gcd
            - 3x
        '''

        vars = {} ## Change for Py2.7
        for letter in self.joint_letters:
            vars[letter] = self.min_power(letter)
        return monomial(self.coeff_gcd, **vars)

    @ property
    def lcm(self):
        '''
        **property**

        Returns the Least Common Multiple of the polynomial::

            >>> Polynomial(parse_polynomial('3x^4 - 9x')).lcm
            + 9x^4
        '''

        vars = {} ## Change for Py2.7
        for letter in self.joint_letters:
            vars[letter] = self.max_power(letter)
        return monomial(self.coeff_lcm, **vars)

    @ property
    def degree(self):
        '''
        **property**

        Returns the degree of the polynomial, i.e. the maximum degree of its monomials.
        An example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).degree
            3
        '''

        return max([sum(monomial[1].values()) for monomial in self._monomials] + [0])

    @ property
    def eval_form(self):
        '''
        **property**

        Returns a string form of the polynomial that can be used with eval::

            >>> e = Polynomial(parse_polynomial('2x^2 - 4x + 4')).eval_form
            >>> e
            '2*x**2-4*x+4'
            >>> eval(e, {'x': 3})
            10
            >>> Polynomial(parse_polynomial('2x^2y^4 - 4xabc + 4z^2y^5')).eval_form
            '4*y**5*z**2+2*y**4*x**2-4*a*x*c*b'
        '''

        ## We can replace the code below with this:
        #return '+'.join(['%s*%s' % (str(c), '*'.join(['%s**%s' % (letter, exp) for letter, exp in vars.iteritems()]))
                        #for c, vars in (self._monomials[:-1] if self.right_hand_side else self._monomials)]) \
                    #.replace('+-', '-').replace('**1', '') + (str((self.right_hand_side if self.right_hand_side < 0 \
                                            #else '+' + str(self.right_hand_side))) if self.right_hand_side else '')
        tmp = []
        for c, vars in self._monomials:
            ll = []
            if not vars:
                tmp.append(str(c))
            else:
                for letter, exp in vars.iteritems():
                    ll.append('%s**%s' % (letter, exp))
                tmp.append('%s*%s' % (str(c), '*'.join(ll)))

        evallable = '+'.join(tmp).replace('+-', '-').replace('**1', '').replace('-1*', '-')
        return evallable

    @ property
    def letters(self):
        '''
        **property**

        Returns a tuple of all the letters that appear in the polynomial.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).letters
            ('x', 'y')

        .. seealso::
            :meth:`join_letters`.
        '''

        return tuple(sorted(reduce(operator.or_, [set(m[1].keys()) for m in self._monomials if m[1]], set())))

    @ property
    def joint_letters(self):
        '''
        **property**

        Returns a tuple of the letters that appear in all the polynomial's monomials::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16')).joint_letters
            ()
            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16ax')).joint_letters
            ('x',)

        .. seealso::
            :meth:`letters`.
        '''

        if len(self) == 1:
            return self.letters
        return tuple(reduce(operator.and_, [set(monomial[1].keys()) for monomial in self.monomials]))

    def max_letter(self, alphabetically=True):
        '''
        Returns the letter with the maximum power in the polynomial.

        :param bool alphabetically: if True and if there is more than one letter with the same exponent, will be chosen the first letter in alphabetical order, the last otherwise (when ``alphabetically=False``).
        :rtype: string

        Some examples::

            
        '''

        if alphabetically:
            cmp = operator.lt
        else:
            cmp = operator.gt

        if not self.letters:
            max_, letter_ = float('-inf'), chr(255)
        else:
            max_ = self.max_power(self.letters[0])
            letter_ = self.letters[0]

        for letter in self.letters[1:]:
            power = self.max_power(letter)
            if power > max_:
                max_ = power
                letter_ = letter
            elif power == max_:
                if cmp(letter, letter_):
                    max_ = power
                    letter_ = letter

        return letter_

    @ property
    def right_hand_side(self):
        '''
        **property**

        Returns the right-hand side, if it exist, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).right_hand_side
            False
            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 3')).right_hand_side
            -3
        '''

        if not self._monomials[-1][1]:
            return self._monomials[-1][0]
        return False

    @ property
    def zeros(self):
        '''
        **property**

        Returns a tuple containing all the polynomial's zeros, based on the right-hand side.

        .. warning::
            Returns NotImplemented when:

            * there is more than one letter
            * there isn't the right-hand side and there is more than one letter or the sum of the polynomial's
                coefficients is not 0

        For example::

            >>> Polynomial(parse_polynomial('2x - 4')).zeros
            (2,)
            >>> Polynomial(parse_polynomial('2x')).zeros
            NotImplemented
            >>> Polynomial(parse_polynomial('2xy')).zeros
            NotImplemented
            >>> 
        '''

        if len(self.letters) - 1: ## Polynomial has more than one letter or none
            if len(self) == 1 and self.right_hand_side: ## For example polynomial('-4'), i.e. no letters
                return -self.right_hand_side
            return NotImplemented

        if not self.right_hand_side:
            if len(self.letters) == 1:
                if not sum(self.coefficients):
                    return 1
            return NotImplemented

        divisors = lambda n: ([1] if n != 1 else []) + [x for x in xrange(2, n//2 +1) if not n % x] + [n]

        divs = divisors((-self.right_hand_side if self.right_hand_side < 0 else self.right_hand_side))
        negdivs = map(operator.neg, divs)
        return tuple([x for x in divs + negdivs if not self(x)])

    def raw_powers(self, letter=None):
        '''
        Returns a list with the same length of the polynomial with all the degrees of *letter*.
        Example::

            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).raw_powers('x')
            [3, 0, 1, 0] ## In -2a^2 and -2 there isn't the letter `x`, so there are two zeros
            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).raw_powers('q')
            [0, 0, 0, 0]

        If letter is None, it returns a dictionary with all the degrees of all the letters in the polynomial::

            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).raw_powers()
            {'a': [0, 2, 0, 0],
             'x': [3, 0, 1, 0],
             }

        .. seealso::
            :meth:`powers`.
        '''

        if not letter:
            d={}  # change for Py2.7
            for l in self.letters:
                d[l] = self.raw_powers(l)
            return d

        return [monomial[1].get(letter, 0) for monomial in self._monomials]

    def max_power(self, letter):
        '''
        Returns the maximum degree of a letter::

            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).max_power('a')
            2
            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).max_power('x')
            3
            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).max_power('q')
            
            Traceback (most recent call last):
              File "<pyshell#7>", line 1, in <module>
                Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).max_power('q')
              File "/home/miki/pypol/src/pypol.py", line 316, in max_power
                raise KeyError('letter not in polynomial')
            KeyError: 'letter not in polynomial'

        It raises KeyError if the letter is not in the polynomial.
        .. seealso::
            :meth:`min_power`.
        '''

        if letter not in self.letters:
            raise KeyError('letter not in polynomial')
        return max(self.raw_powers(letter))

    def min_power(self, letter):
        '''
        Returns the maximum degree of a letter::

            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).min_power('a')
            0
            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).min_power('x')
            0
            >>> Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).min_power('q')
            
            Traceback (most recent call last):
              File "<pyshell#3>", line 1, in <module>
                Polynomial(parse_polynomial('3x^3 - 2a^2 + x - 2')).min_power('q')
              File "/home/miki/pypol/src/pypol.py", line 325, in min_power
                raise KeyError('letter not in polynomial')
            KeyError: 'letter not in polynomial'

        It raises KeyError if the letter is not in the polynomial.
        .. seealso::
            :meth:`max_power`.
        '''

        if letter not in self.letters:
            raise KeyError('letter not in polynomial')
        if self.right_hand_side:
            return 0
        return min(self.raw_powers(letter))

    def powers(self, letter=None):
        '''
        Like :meth:`raw_powers`, but eliminates all the zeros except the trailing one.
        If *letter* is None, it returns a dictionary::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).powers('x')
            [3, 1, 0]
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).powers('a')
            [2, 0]
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).powers()
            {'a': [2, 0],
            'x': [3, 1, 0],
            }

        .. seealso::
            :meth:`raw_powers`.
        '''

        if not letter:
            d={}  # change for Py2.7
            for l in self.letters:
                d[l] = self.powers(l)
            return d

        raw = self.raw_powers(letter)
        try:
            return filter(None, raw[:-1]) + [raw[-1]]
        except IndexError:
            return []

    def islinear(self):
        '''
        Returns True if the polynomial is linear, i.e. all the expoenents are <= 1, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).islinear()
            False
            >>> Polynomial(parse_polynomial('-5')).islinear()
            True
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).powers('q')
            [0]
            >>> Polynomial(parse_polynomial('')).powers('q')
            []
        '''

        return self.degree <= 1

    def is_square_diff(self):
        '''
        Returns True whether the polynomial is a difference of two squares, False otherwise::

            >>> Polynomial(parse_polynomial('2x^4 - 6')).is_square_diff()
            False
            >>> Polynomial(parse_polynomial('2x^4 + 9')).is_square_diff()
            False
            >>> Polynomial(parse_polynomial('2x^4 - 9')).is_square_diff()
            False
            >>> Polynomial(parse_polynomial('x^4 - 9')).is_square_diff()
            True
            >>> Polynomial(parse_polynomial('25x^4 - 9')).is_square_diff()
            True
        '''

        def is_square(n):
            return n & 1 == 0 ## n % 2
        def is_perfect_square(n):
            return int(n ** 0.5) ** 2 == n
        def _check(a):
            first = self[a][1]
            power = first[first.keys()[0]]
            if len(first) == 1 and is_square(power):
                if a == 1:
                    return self[a][0] < 0
                if is_perfect_square(self[a][0]):
                    return True
            return False

        if len(self) != 2:
            return False
        if self.right_hand_side:
            if self.right_hand_side < 0 and is_perfect_square(-self.right_hand_side):
                return _check(0)
            else:
                return False
        else:
            return _check(0) and _check(1)

    def isordered(self, letter=None):
        '''
        Returns True whether the polynomial is ordered, False otherwise.
        If letter is None, it checks for all letters; if the polynomial is ordered for all letters, it returns True, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).isordered('x')
            False
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).isordered('a')
            True

        .. seealso::
            :meth:`iscomplete`.
        '''

        if not letter:
            return all(self.isordered(l) for l in self.letters)
        if self.iscomplete():
            return True

        return self.powers(letter) in (range(self.min_power(letter), self.max_power(letter)+1),
                                       range(self.max_power(letter), self.min_power(letter)-1, -1))

    def iscomplete(self, letter=None):
        '''
        Returns True whether the polynomial is complete, False otherwise.
        If letter is None it checks for all the letters of the polynomial.
        ::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete('a')
            True
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete('x')
            False
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete()
            False

        .. seealso::
            :meth:`isordered`.
        '''

        if not letter:
            return all(self.iscomplete(l) for l in self.letters)

        if self.max_power(letter) == 1:
            return True
        return self.powers(letter) == range(self.max_power(letter), -1, -1)

    def invert(self, v=1):
        '''
        Returns an :class:`AlgebraicFraction` object with *v* as :meth:`AlgebraicFraction.numerator` and this polynomial as :meth:`AlgebraicFraction.denominator`::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).invert()
            AlgebraicFraction(+ 1, + 3x³ - a² + a - 5)
            >>> print Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).invert(3)
                    + 3         
            −−−−−−−−−−−−−−−−−−−−
            + 3x³ - a² + a - 5

        .. seealso::
            :meth:`AlgebraicFraction.invert`
        '''

        return AlgebraicFraction(monomial(v), self)

    def check_other(wrapped):
        def wrapper(self, other):
            if isinstance(other, int):
                other = monomial(other)
            elif isinstance(other, str):
                other =  polynomial(other)
            elif isinstance(other, tuple):
                other =  Polynomial(other)
            return wrapped(self, other)
        return wrapper

    @ check_other
    def update(self, pol_or_monomials=None, simplify=None):
        '''
        Updates the polynomial with another polynomial.
        This does not create a new instance, but replaces self.monomials with others monomials, then it simplifies.

        pol_or_monomials can be:
          * a polynomial
          * a tuple of monomials
          * a string that will be passed to :func:`parse_polynomial`
          * an integer

        default is None. In this case self.monomials will be updated with an empty tuple.
        ::

            >>> p = Polynomial(parse_polynomial('3x^3 - a^2 + a - 5'))
            >>> p
            + 3x^3 - a^2 + a - 5
            >>> p.update(Polynomial(parse_polynomial('3x^2 - 2')))
            + 3x^2 - 2
            >>> p
            + 3x^2 - 2
            >>> p.update(((3, {'x': 1}), (-5, {})))
            + 3x - 5
            >>> p
            + 3x - 5
            >>> p.update('30j + q - y')
            + 30j + q - y
            >>> p
            + 30j + q - y
            >>> p.update(3)
            + 3
            >>> p
            + 3

        This method returns the instance, so we can use it::

            >>> p.update('2c - 4a').raw_powers()
            {'a': [0, 1], 'c': [1, 0]}
            >>> p
            + 2c - 4a
            >>> p.update('3x^2 - x + 5').iscomplete()
            True
            >>> p
            + 3x^2 - x + 5

        .. seealso::
            :meth:`append`.
        '''

        if simplify is None:
            simplify = self._simplify

        if not pol_or_monomials:
            self._monomials = ()
            if simplify:
                self.simplify()
            return self

        try:
            self._monomials = pol_or_monomials._monomials
        except AttributeError:
            return NotImplemented

        if self._simplify:
            self.simplify()
        return self

    @ check_other
    def append(self, pol_or_monomials):
        '''
        Appends the given monomials to self.monomials, then simplifies.

        pol_or_monomials can be:
          * a polynomial
          * a string
          * a tuple of monomials
          * an integer

        ::

            >>> p = Polynomial(parse_polynomial('3x^2 - ax + 5'))
            >>> p
            + 3x^2 - ax + 5
            >>> p.append('x^3')
            >>> p
            + x^3 + 3x^2 - ax + 5
            >>> p.append(-4)
            >>> p
            + x^3 + 3x^2 - ax + 1
            >>> p.append(((-1, {'a': 1, 'x': 1}),)) ## The comma!
            >>> p
            + x^3 + 3x^2 - 2ax + 1
            >>> p.append(Polynomial(parse_polynomial('-x^3 + ax + 4')))
            >>> p
            + 3x^2 - ax + 5

        .. seealso::
            :meth:`update`.
        '''

        self.sort(pol_or_monomials._monomials + self._monomials, key=self._key, reverse=True)
        self.simplify()

    def div_all(self, poly):
        '''
        Divide all polynomial's monomials by *poly*::

            >>> a = Polynomial(parse_polynomial('3x^4 - 9x'))
            >>> a.gcd
            - 3x
            >>> a.div_all(a.gcd)
            - x^3 + 3
        '''

        return sum([Polynomial((monomial,)) / poly for monomial in self._monomials])

    def simplify(self):
        '''
        Simplifies the polynomial. This is done automatically on the __init__ and on the :meth:`update` methods if self._simplify is True.
        ::

            >>> p = Polynomial(parse_polynomial('3x^2 - ax + 5 - 4 + 4ax'))
            >>> p
            + 3x^2 + 3ax + 1
            >>> p = Polynomial(parse_polynomial('3x^2 - ax + 5 - 4 + 4ax'), simplify=False)
            >>> p
            + 3x^2 - ax + 4ax + 5 - 4
            >>> p.simplify()
            >>> p
            + 3x^2 + 3ax + 1
        '''

        simplified = []
        for monomial in self._monomials:
            for other in simplified:
                if are_similar(monomial, other):
                    simplified.append((monomial[0] + other[0], monomial[1]))
                    simplified.remove(other)
                    break
            else:
                simplified.append(monomial)

        simplified2 = copy.deepcopy(simplified)
        for index, monomial in enumerate(simplified2):
            for letter, exp in monomial[1].iteritems():
                if exp == 0:
                    del simplified[index][1][letter]

            if not monomial[0] and not monomial[1]:
                del simplified[index]

        self._monomials = tuple(simplified)

    def insert(self, index, monomial):
        '''
        Deprecated method
        '''
        raise DeprecationWarning('This method is deprecated, use append instead')
        tmp_monomials = list(self._monomials)
        tmp_monomials.insert(index, monomial)
        self._monomials = tuple(tmp_monomials)
        self.simplify()

    def _key(self, letter=None):
        '''
        Comparator function used to sort the polynomial's monomials. You should not change it nor call it.
            See (NotImplemented)
        '''

        if not letter:
            letter = self.max_letter()

        return (lambda item: item[1].get(letter, 0))

    def _make_complete(self, letter):
        '''
        If the polynomial is already complete for the letter *letter* returns False, otherwise makes it complete and returns True.
        ::

            >>> p = Polynomial(parse_polynomial('3x^2 + 2'))
            >>> p
            + 3x^2 + 2
            >>> p.monomials
            ((3, {'x': 2}), (2, {}))
            >>> p.iscomplete('x')
            False
            >>> p._make_complete('x')
            True
            >>> p.iscomplete('x')
            True
            >>> p.monomials
            ((3, {'x': 2}), (0, {'x': 1}), (2, {}))
        '''

        if self.iscomplete(letter):
            return False
        for exp in xrange(1, self.max_power(letter)+1):
            self.append(((0, {letter:exp}),))
        return True

    def _format(self, print_format=False):
        return ' '.join([self._m_format(monomial, print_format).replace('-', '- ') if monomial[0] < 0 \
                    else ('+ ' + self._m_format(monomial, print_format) if self._m_format(monomial, print_format) \
                    else '') for monomial in self._monomials]).strip()

    def _m_format(self, monomial, print_format):
        tmp_coefficient = monomial[0]
        if tmp_coefficient == 0:
            return ''
        elif tmp_coefficient == 1 and monomial[1]:
            tmp_coefficient = ''
        elif tmp_coefficient == -1 and monomial[1]:
            tmp_coefficient = '-'
        else:
            tmp_coefficient = str(tmp_coefficient)

        var_list = []
        for var, exp in sorted(monomial[1].items(), key=lambda i: i[0]):
            if exp == 0:
                continue
            elif exp == 1:
                var_list.append(var)
            else:
                var_list.append('%s^%s' % (var, exp))

        if print_format:
            return tmp_coefficient + ''.join(var_list).replace('^', '') \
                .replace('0', unichr(8304)).replace('1', unichr(8305)) \
                .replace('2', unichr(178)).replace('3', unichr(179)) \
                .replace('4', unichr(8308)).replace('5', unichr(8309)) \
                .replace('6', unichr(8310)).replace('7', unichr(8311)) \
                .replace('8', unichr(8312)).replace('9', unichr(8313)).encode('utf-8')
        return tmp_coefficient + ''.join(var_list)

    def __repr__(self):
        return self._format()

    def __str__(self):
        return self._format(True)

    def __eq__(self, other):
        def _filter(mons):
            tmp_mons = []
            for m in mons:
                if m[0]:
                    tmp_mons.append(m)
            return tmp_mons

        if len(self) == 0 and len(other) == 0:
            return True
        try:
            return sorted(_filter(self._monomials)) == sorted(_filter(other._monomials))
        except (AttributeError, TypeError):
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self._monomials)

    def __pos__(self):
        return copy.copy(self)

    def __neg__(self):
        return self * -1

    def __nonzero__(self):
        return bool(len(self))

    def __contains__(self, other):
        return other in self._monomials

    def __copy__(self):
        return Polynomial(self._monomials)

    def __deepcopy__(self, p):
        return Polynomial(self._monomials)

    def __getitem__(self, b):
        return self._monomials[b]

    def __setitem__(self, b, v):
        tmp_monomials = list(self._monomials)
        tmp_monomials[b] = v
        self.sort(tmp_monomials, key=self._key, reverse=True)

    def __delitem__(self, b):
        tmp_monomials = list(self._monomials)
        del tmp_monomials[b]
        self._monomials = tuple(tmp_monomials)

    def __call__(self, *args, **kwargs):
        '''
        It's also possible to call the polynomial.
           You can pass the arguments in two ways:

              * positional way, using *args*
                * keyword way, using *kwargs*

            ::

                >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(2, 3)  ## Positional way, x=2, y=3
                18
                >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(y=2, x=3)  ## Keyword way: y=2, x=3
                23

            When you use *args*, the dictionary is built in this way::

                dict(zip(self.letters[:len(args)], args))

            *args* has a major priority of *kwargs*, so if you try them both at the same time::

                >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(2, 3, y=5, x=78)
                18

            *args* is predominant.
        '''

        if args:
            letters = dict(zip(self.letters[:len(args)], args))
        elif kwargs:
            letters = kwargs
        return eval(self.eval_form, letters)

    @ check_other
    def __add__(self, other):
        try:
            return Polynomial(self._monomials + other._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    def __radd__(self, other):
        return self + other

    @ check_other
    def __sub__(self, other):
        try:
            return Polynomial(self._monomials + (-other)._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    def __rsub__(self, other):
        return self - other

    @ check_other
    def __mul__(self, other):
        def _mul(a, b):
            new_coeff = a[0] * b[0]
            if not a[1] and not b[1]:
                return (new_coeff, {})
            #new_vars = {letter: (a[1].get(letter, 0) + b[1].get(letter, 0)) \
                       #for letter in set(a[1].keys()).union(b[1].keys())} # uncomment later for Py2.7

            new_vars = {}
            for letter in set(a[1].keys()).union(b[1].keys()): ## by Bakuriu
                new_vars[letter] = a[1].get(letter, 0) + b[1].get(letter, 0)

            return (new_coeff, new_vars)

        try:
            return Polynomial([_mul(monomial, other_monomial) for monomial in \
                        self._monomials for other_monomial in other._monomials])
        except (AttributeError, TypeError):
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    @ check_other
    def __divmod__(self, other):
        def _set_up(pol):
            if not pol.letters:
                #for letter in set(self.letters).union(other.letters):
                    #pol._make_complete(letter)
                return
            for m in pol._monomials:
                for var in self.letters:
                    if var not in m[1]:
                        m[1][var] = 0
            #for letter in set(self.letters).union(other.letters):
                #pol._make_complete(letter)

        def _div(a, b):
            new_coefficient = fractions.Fraction(str(a[0] / b[0]))
            new_vars = copy.copy(a[1])
            for letter, exp in b[1].iteritems():
                if exp == 0:
                    continue
                new_vars[letter] = a[1][letter] - exp

            return monomial(new_coefficient, **new_vars)

        A = Polynomial(copy.deepcopy(self._monomials))
        B = Polynomial(copy.deepcopy(other._monomials))
        Q = Polynomial()

        if A.degree < B.degree:
            raise ValueError('The polynomials are not divisible')

        _set_up(A); _set_up(B)
        while A.degree >= B.degree:
            quotient = _div(A._monomials[0], B._monomials[0])
            Q.append(quotient)
            del A[0]

            m = Polynomial(B[1:])
            if not m:
                return Q, A
            A += (-quotient * m)

        return Q, A

    def __div__(self, other):
        quotient, remainder = divmod(self, other)
        return quotient

    def __truediv__(self, other):
        quotient, remainder = divmod(self, other)
        if remainder:
            return AlgebraicFraction(quotient, remainder)
        return quotient

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __pow__(self, exp, mod=None):
        '''
        '''

        if exp == 0:
            return Polynomial()
        elif exp < 0:
            return AlgebraicFraction(monomial(1), self ** abs(exp))
        else:
            try:
                pow = reduce(operator.mul, [self]*exp)
                if mod:
                    return pow % mod
                return pow
            except (AttributeError, TypeError):
                return NotImplemented


class AlgebraicFraction(object):
    '''
    This class represent an algebraic fraction.
    It accepts two arguments: *numerator* and *denominator*.
    *numerator* is the numerator of the algebraic fraction, and *denominator* its denominator. Both the terms have to be two polynomials.
    ::

        >>> AlgebraicFraction(a, b)
        AlgebraicFraction(+ 3x - 5, + 2a)

    .. seealso::
        :func:`algebraic_fraction`
    '''

    __slots__ = ('_numerator', '_denominator', '_simplify',)

    def __init__(self, numerator, denominator=1, simplify=True):
        if not denominator:
            raise ZeroDivisionError('Denominator cannot be 0')
        if isinstance(numerator, AlgebraicFraction):
            self = self._numerator * AlgebraicFraction(1, self._denominator)
        elif isinstance(denominator, AlgebraicFraction):
            self = AlgebraicFraction(self._numerator) * self._denominator.invert()
        self._numerator = numerator
        self._denominator = denominator
        self._simplify = simplify
        if self._simplify:
            self.simplify()

    @ property
    def numerator(self):
        '''
        **property**

        Returns the numerator of the :class:`AlgebraicFraction`.
        ::

            >>> AlgebraicFraction(a, b).numerator
            + 3x - 5
        '''

        return self._numerator

    @ numerator.setter
    def numerator(self, val):
        '''
        Sets the numerator of the AlgebraicFraction
        '''

        self._numerator = val

    @ property
    def denominator(self):
        '''
        **property**

        Returns the denominator of the :class:`AlgebraicFraction`.
        ::

            >>> AlgebraicFraction(a, b).denominator
            + 2a
        '''

        return self._denominator

    @ denominator.setter
    def denominator(self, val):
        '''
        Sets the denominator of the AlgebraicFraction
        '''

        self._denominator = val

    @ property
    def terms(self):
        '''
        **property**

        Returns both the :meth:`numerator` and the :meth:`denominator`::

            >>> AlgebraicFraction(a, b).terms
            (+ 3x - 5, + 2a)
        '''

        return (self._numerator, self._denominator)

    def invert(self):
        '''
        Returns a new :class:`AlgebraicFraction` object with the numerator and the denominator swapped::

            >>> c = AlgebraicFraction(a, b)
            >>> c
            AlgebraicFraction(+ 3x - 5, + 2a)
            >>> d = c.swap()
            >>> d
            AlgebraicFraction(+ 2a, + 3x - 5)
            >>> c.swap() == AlgebraicFraction(b, a)
            True

        .. seealso::
            :meth:`Polynomial.invert`
        '''

        return AlgebraicFraction(self._denominator, self._numerator)

    def simplify(self):
        '''
        Simplifies the algebraic fraction. This is done automatically on the __init__ and on the :meth:`update` methods if self._simplify is True.
        Actually we can simplify some algebraic fractions only.
        ::

            >>> c, d = polynomial('12a - 6a^3'), polynomial('2a - 4a^2')
            >>> f = AlgebraicFraction(c, d)
            >>> f
            AlgebraicFraction(- 3a² + 6, - 2a + 1)
            >>> f = AlgebraicFraction(c, d, simplify=False)
            >>> f
            AlgebraicFraction(- 6a³ + 12a, - 4a² + 2a)
            >>> f.simplify()
            AlgebraicFraction(- 3a² + 6, - 2a + 1)
        '''

        common_poly = gcd(self._numerator.gcd, self._denominator.gcd)
        self._numerator = self._numerator.div_all(common_poly)
        self._denominator = self._denominator.div_all(common_poly)
        return self

    def check_other(wrapped):
        def wrapper(self, other):
            if isinstance(other, Polynomial):
                other = AlgebraicFraction(other)
            elif isinstance(other, str):
                other = AlgebraicFraction(polynomial(other))
            return wrapped(self, other)
        return wrapper

    def __repr__(self):
        return 'AlgebraicFraction({0[0]}, {0[1]})'.format(self.terms)

    def __str__(self):
        a, b = map(str, self.terms)
        la, lb = len(a), len(b)
        n = max(la, lb)
        sep = n*u'\u2212'.encode('utf-8')
        return '\n'.join([a.center(n), sep, b.center(n)])

    def __eq__(self, other):
        return self._numerator == other._numerator and \
               self._denominator == other._denominator
    
    def __ne__(self, other):
        return not self == other

    def __pos__(self):
        return copy.copy(self)

    def __neg__(self):
        return AlgebraicFraction(-self._numerator, self._denominator)

    def __copy__(self):
        return AlgebraicFraction(self._numerator, self._denominator)

    def __deepcopy__(self, algebraicfraction):
        return AlgebraicFraction(self._numerator, self._denominator)

    def __add__(self, other):
        least_multiple = lcm(self._denominator.lcm, other._denominator.lcm)
        num = least_multiple / self._numerator
        den = least_multiple / self._denominator
        return AlgebraicFraction(self._numerator * num, self._denominator * den)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return self - other

    @ check_other
    def __mul__(self, other):
        return AlgebraicFraction(self._numerator * other._numerator,
                                self._denominator * other._denominator)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        return self * other.invert()