#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials and algebraic fractions.

Author: Michele Lacchia <michelelacchia@gmail.com>
Copyright: 2010-2011 Michele Lacchia
License: GNU GPL

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

Copyright (C) 2010-2011 Michele Lacchia
'''

from __future__ import division
import random
import functools
import fractions
import operator
import copy
import re


__author__ = 'Michele Lacchia'
__version__ = (0, 5)
__version_str__ = '0.5'

__all__ = ['polynomial', 'algebraic_fraction', 'monomial','poly1d', 'poly1d_2',
           'coerce_poly', 'coerce_frac', 'gcd', 'lcm', 'are_similar', 'parse_polynomial',
           'Polynomial', 'AlgebraicFraction', '__author__', '__version__', '__version_str__']

def polynomial(string=None, simplify=True):
    '''
    Returns a :class:`Polynomial` object.

    :param string: a string that represent a polynomial, default is None.
    :param simplify: if True, the polynomial will be simplified on __init__ and on update.
    :type string: string or None
    :type simplify: bool
    :rtype: :class:`Polynomial`

    .. warning::
        With this function you cannot make polynomials with negative powers. In case you want to use negative powers, use :func:`poly1d_2` instead.


        **Examples**

        We want to make the polynomial :math:`2x^{-1} + 2`::

            >>> polynomial('2x^-1 + 2')
            + 2x + 1 ## Wrong!
            >>> k = poly1d_2([[2, -1], [2, 0]])
            >>> k
            + 2x^-1 + 2
            >>> k.sort(key=k._key('x'))
            >>> k
            + 2x^-1 + 2
'''

    if not string:
        return Polynomial()
    return Polynomial(parse_polynomial(string), simplify)

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

def monomial(coeff=1, **vars):
    '''
    Simple function that returns a :class:`Polynomial` object.

    :param coeff: the coefficient of the polynomial
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

    This function is useful when you need a monomial. Without it you should do::

       >>> Polynomial(((5, {'a': 3, 'b': 4}),))
       + 5a^3b^4

    Either *coeff* or *\*\*vars* is optional::

        >>> monomial()
        + 1
        >>> monomial(1)
        + 1


    Equivalent to::

        def monomial(coeff=1, **vars):
            return Polynomial(((coeff, vars),))

    .. versionadded:: 0.2
    .. versionadded:: 0.4
        The *\*var* parameter
    '''

    assert all(len(v) == 1 for v in vars), 'Cannot set a letter with length > 1'
    return Polynomial(((coeff, vars),))

def poly1d(coeffs, variable='x', right_hand_side=True):
    '''
    Make a 1 dimension polynomial from a list of coefficients.

    :param list coeffs: the list of the polynomial coefficients
    :param string variable: the letter of the polynomial, default ``x``
    :param right_hand_side: if True, the last term of *coeffs* will be the right hand-side of the polynomial
    :type right_hand_side: bool or None

    **Examples**

    We create the polynomials :math:`3x^3 - 2x^2 + 4x - 2`, :math:`2x^3 - 2` and :math:`3x`.
    ::

        >>> poly1d([3, -2, 4, -2])
        + 3x^3 - 2x^2 + 4x - 2
        >>> poly1d([2, 0, 0, -2])
        + 2x^3   - 2

    pay attention here::

        >>> poly1d([3], right_hand_side=False)
        + 3x

    because if you don't do this::

        >>> poly1d([3])
        + 3

    ``3`` will be interpreted as the right_hand_side of the polynomial.

    An alternative solution may be::

        >>> poly1d([3, 0])
        + 3x
    '''

    if right_hand_side:
        poly = Polynomial([(c, {variable: i+1}) for i, c in enumerate(reversed(coeffs[:-1]))])
        if coeffs[-1]:
            poly.append(coeffs[-1])
        return poly
    return Polynomial([(c, {variable: i+1}) for i, c in enumerate(reversed(coeffs))])

def poly1d_2(monomials, variable='x'):
    '''
    Make a 1 dimension polynomial from a list of lists.

    :param list monomials: a list of lists that represents the polynomial's monomial; evary sub-list has the coefficient and the power of the variable
    :param string variable: the letter of the polynomial (default ``x``)
    :rtype: :class:`Polynomial`

    **Examples**

    We want to create these two polynomials: :math:`2x^3 - 2x^2 + x` and :math:`x`::

        >>> poly1d_2([[-1, 7], [2, 3], [-2, 2], [1, 1]])
        - x^7 + 2x^3 - 2x^2 + x
        >>> poly1d_2([[1, 1]])
        + x

    This function is very useful when you need a polynomial with negative powers or with spread powers::

        >>> poly1d_2([[1, -1], [2, -3], [3, 5]])
        + 3x^5 + x^-1 + 2x^-3

    or::

        >>> poly1d_2([[2, 9], [1, 2]])
        + 2x^9 + x^2

    in this case, if you want to use :func:`poly1d` or :func:`polynomial` you can do this::

        >>> poly1d([2, 0, 0, 0, 0, 0, 0, 1, 0, 0])
        + 2x^9 + x^2
        >>> poly1d([2, 0, 0, 0, 0, 0, 0, 1, 0], right_hand_side=False)
        + 2x^9 + x^2
        >>> polynomial('2x^9 + x^2')
        + 2x^9 + x^2
        >>> polynomial('2x9 x2')
        + 2x^9 + x^2
    '''

    return Polynomial([(c, {variable: exp}) for (c, exp) in monomials])

def gcd(a, b):
    '''
    Returns the Greatest Common Divisor between two polynomials::

       >>> gcd(polynomial('3x'), polynomial('6x^2'))
       + 3x
    '''

    def _gcd(x, y):
        if not y:
            return x
        while True:
            r = x % y
            if not r:
                return y
            x, y = y, r

    try:
        return _gcd(a, b)
    except ValueError:
        return _gcd(b, a)

def lcm(a, b):
    '''
    Returns the Least Common Multiple between two polynomials::

        >>> lcm(polynomial('3x'), polynomial('6x^2'))
        + 6x^2
    '''

    k = operator.truediv(a, gcd(a, b)) * b
    try:
        if int(k) == k:
            return int(k)
    except TypeError:
        return k
    return k

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

def coerce_poly(wrapped):
    '''
    If the second term is not a polynomial, it is coerced.
    '''
    @ functools.wraps(wrapped)
    def wrapper(self, other):
        if isinstance(other, int) or isinstance(other, long):
            other = monomial(other)
        elif isinstance(other, str):
            other =  polynomial(other)
        elif isinstance(other, tuple):
            other =  Polynomial(other)
        elif isinstance(other, float):
            other = monomial(fractions.Fraction.from_float(other))
        elif isinstance(other, fractions.Fraction):
            other = monomial(other)
        return wrapped(self, other)
    return wrapper

def coerce_frac(wrapped):
    '''
    If the second term is not an algebraic fractions, it is coerced.
    '''
    def wrapper(self, other):
        if isinstance(other, Polynomial):
            other = AlgebraicFraction(other)
        elif isinstance(other, str):
            other = AlgebraicFraction(polynomial(other))
        elif isinstance(other, int):
            other = AlgebraicFraction(poly1d([other]))
        elif isinstance(other, tuple):
            other = AlgebraicFraction(polynomial([0]), polynomial(other[1]))
        return wrapped(self, other)
    return wrapper



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

    if not string:
        return []

    for c, l in regex.findall(string):
        if max_length and len(monomials) == max_length:
            return monomials

        c, l = c.strip(), l.strip()
        if not c and not l:
            continue
        c, l = _parse_coeff(c), _parse_letters(l)
        monomials.append((c, l))

    return monomials


def _parse_coeff(c):
    if not c:
        return 1
    elif c == '+':
        return 1
    elif c == '-':
        return -1
    elif '.' in c or '/' in c:
        return fractions.Fraction(c.replace(' ', ''))
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

class Polynomial(object):
    '''
    The class :class:`Polynomial` is an object that represents a Polynomial.
    It accepts two arguments: *monomials* and *simplify*.

    *monomials* is a tuple of tuples that represents all the polynomial's monomials.

    If *simplify* is True, then the polynomial will be simplified on __init__ and on :meth:`update`.

    .. seealso::
        :meth:`simplify`

    **Examples**

    ::
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
        self._monomials = tuple(monomials)
        self.sort(key=self._key(), reverse=True)
        self._simplify = simplify
        if self._simplify:
            self.simplify()

    @ property
    def monomials(self):
        '''
        Returns the polynomial's monomials.
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
        self._monomials = list(values)
        self.sort(key=self._key(), reverse=True)

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
            >>> k.sort(key=k._key('x'), reverse=True)
            >>> k
            + x^2 + xy - y^2

        .. versionadded:: 0.2
        .. versionchanged:: 0.4
            Now the *key* parameter is for default to ``self._key(self.max_letter())``
        '''

        if len(self) != 1:
            if not key:
                key = self._key(self.max_letter())
            self._monomials = tuple(self.ordered_monomials(cmp, key, reverse))

    @ property
    def coefficients(self):
        '''
        Returns the polynomial's coefficients::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 5')).coefficients
            [2, 4, -5]
        '''

        return [monomial[0] for monomial in self._monomials]

    def gcd(self):
        '''
        Returns the Greatest Common Divisor of the polynomial's monomials::

            >>> Polynomial(parse_polynomial('3x^4 - 9x')).gcd()
            - 3x

        .. versionadded:: 0.2
        .. versionchanged:: 0.4
            Become a method
        '''

        vars = {} ## Change for Py2.7
        for letter in self.joint_letters:
            vars[letter] = self.min_power(letter)
        return monomial(reduce(fractions.gcd, self.coefficients), **vars)

    def lcm(self):
        '''
        Returns the Least Common Multiple of the polynomial's monomials::

            >>> Polynomial(parse_polynomial('3x^4 - 9x')).lcm()
            + 9x^4

        .. versionadded:: 0.2
        .. versionchanged:: 0.4
            Become a method
        '''

        vars = {} ## Change for Py2.7
        for letter in self.letters:
            vars[letter] = self.max_power(letter)
        l = reduce(lambda a, b: operator.truediv(a, fractions.gcd(a, b)) * b, self.coefficients)
        if int(l) == l:
            l = int(l)
        return monomial(l, **vars)

    @ property
    def degree(self):
        '''
        Returns the degree of the polynomial, i.e. the maximum degree of its monomials.
        An example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).degree
            3
            >>> Polynomial(parse_polynomial('')).degree
            -inf
        '''

        if not self:
            return float('-inf')
        return max(sum(monomial[1].values(), 0) for monomial in self._monomials)

    @ property
    def eval_form(self):
        '''
        Returns a string form of the polynomial that can be used with eval::

            >>> e = Polynomial(parse_polynomial('2x^2 - 4x + 4')).eval_form
            >>> e
            '2*x**2-4*x+4'
            >>> eval(e, {'x': 3})
            10
            >>> Polynomial(parse_polynomial('2x^2y^4 - 4xabc + 4z^2y^5')).eval_form
            '4*y**5*z**2+2*y**4*x**2-4*a*x*c*b'
        '''

        ## We could replace the following code with this:
        #return '+'.join(['%s*%s' % (str(c), '*'.join(['%s**%s' % (letter, exp) for letter, exp in vars.iteritems()])) for c, vars in (self._monomials[:-1] if self.right_hand_side else self._monomials)]).replace('+-', '-').replace('**1', '') + (str((self.right_hand_side if self.right_hand_side < 0 else '+' + str(self.right_hand_side))) if self.right_hand_side else '')

        tmp = []
        for c, vars in self._monomials:
            ll = []
            if not vars:
                tmp.append(str(c))
            else:
                for letter, exp in vars.iteritems():
                    ll.append('%s**%s' % (letter, exp))
                tmp.append('%s*%s' % (str(c), '*'.join(ll)))

        evallable = '+'.join(tmp).replace('+-', '-') \
                                 .replace('-1*', '-')
        return evallable

    @ property
    def letters(self):
        '''
        Returns a tuple of all the letters that appear in the polynomial.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).letters
            ('x', 'y')
        '''

        return tuple(sorted(reduce(operator.or_, [set(m[1].keys()) \
                                    for m in self._monomials if m[1]], set())))

    @ property
    def joint_letters(self):
        '''
        Returns a tuple of the letters that appear in all the polynomial's monomials::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16')).joint_letters
            ()
            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 16ax')).joint_letters
            ('x',)

        .. versionadded:: 0.2
        '''

        if len(self) == 1:
            return self.letters
        try:
            return tuple(reduce(operator.and_, [set(monomial[1].keys()) \
                                        for monomial in self.monomials]))
        except TypeError:
            return ()

    def max_letter(self, alphabetically=True):
        '''
        Returns the letter with the maximum power in the polynomial.

        :param bool alphabetically: if True and if there is more than one letter with the same exponent, will be chosen the first letter in alphabetical order, the last otherwise (when ``alphabetically=False``).
        :rtype: string or False, when :attr:`letters` is an empty tuple

        Some examples::

            >>> polynomial('2x^3 + 4xy - 16').max_letter()
            'x'
            >>> polynomial('2x^3 + 4x2y2 - 16').max_letter()
            'x'
            >>> polynomial('2x^3 + 4x2y3 - 16').max_letter(False)
            'y'
            >>> polynomial('2x^3 + 4x2y3 - 16').max_letter()
            'x'
            >>> polynomial('2x^3 + 4x2y4 - 16').max_letter()
            'y'
            >>> polynomial('2x^3 + 4x2y3 - 16').max_letter(False)
            'y'

        .. versionadded:: 0.2
        '''

        if alphabetically:
            cmp_ = operator.lt
        else:
            cmp_ = operator.gt

        if not self.letters:
            return False
        if len(self.letters) == 1:
            return self.letters[0]

        max_ = self.max_power(self.letters[0])
        letter_ = self.letters[0]

        for letter in self.letters[1:]:
            power = self.max_power(letter)
            if power > max_:
                max_ = power
                letter_ = letter
            elif power == max_:
                if cmp_(letter, letter_) == 1:
                    max_ = power
                    letter_ = letter

        return letter_

    @ property
    def right_hand_side(self):
        '''
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
    def rhs(self):
        '''
        A shorthand for :attr:`right_hand_side`.

        .. versionadded:: 0.5
        '''

        return self.right_hand_side

    # DEPRECATED since 0.3
    #@ property
    #def zeros(self):
    #    '''
    #    Returns a tuple containing all the polynomial's zeros, based on the right-hand side.
    #
    #    :rtype: :exc:`NotImplemented` when:
    #
    #    * there is more than one letter
    #    * there isn't the right-hand side and there is more than one letter or the sum of the polynomial's coefficients is not 0
    #
    #    For example::
    #
    #        >>> Polynomial(parse_polynomial('2x - 4')).zeros
    #        (2,)
    #        >>> Polynomial(parse_polynomial('2x')).zeros
    #        NotImplemented
    #        >>> Polynomial(parse_polynomial('2xy')).zeros
    #        NotImplemented
    #
    #    .. deprecated:: 0.4
    #        Use :func:`pypol.funcs.ruffini` instead.
    #    '''
    #
    #    raise DeprecationWarning('This method is deprecated and will be removed in pypol 0.4. Use pypol.funcs.ruffini instead')
    #    if len(self.letters) - 1: ## Polynomial has more than one letter or none
    #        if len(self) == 1 and self.right_hand_side: ## For example polynomial('-4'), i.e. no letters
    #            return -self.right_hand_side
    #        return NotImplemented
    #
    #    if not self.right_hand_side:
    #        if len(self.letters) == 1:
    #            if not sum(self.coefficients):
    #                return 1
    #        return NotImplemented
    #
    #    divisors = lambda n: ([1] if n != 1 else []) + \
    #                    [x for x in xrange(2, n//2 +1) if not n % x] + [n]
    #
    #    divs = divisors((-self.right_hand_side if self.right_hand_side < 0 \
    #                                           else self.right_hand_side))
    #    negdivs = map(operator.neg, divs)
    #    return tuple([x for x in divs + negdivs if not self(x)])

    def get(self, power, letter=None):
        '''
        Returns the coefficients of the term ``letter^power``.

        :param integer power: the power of the term
        :param string letter: the variable (default to ``x``)
        :rtype: integer, float, or :class:`fractions.Fraction`

        **Examples**

        ::

            >>> p = x**3 - y**3*x**4 -.4*z**5*y**5
            >>> p
            - 2/5y^5z^5 - x^4y^3 + x^3
            >>> p.get(1)
            0
            >>> p.get(3)
            1
            >>> p.get(3, 'y')
            -1
            >>> p.get(5, 'y')
            Fraction(-2, 5)
            >>> p.get(5, 'z')
            Fraction(-2, 5)
            >>> p.get(5, 'x')
            0
            >>> p.get(6, 'y')
            0
        '''

        if not letter:
            letter = self.letters[0]
        if power == 0:
            return self.right_hand_side or 0
        plist = self.to_plist(letter)
        c = [None] + plist[::-1]
        try: ## Fast way
            if c[power][1] == power:
                return c[power][0]
        except IndexError:
            for t in plist:
                if t[1] == power:
                    return t[0]
        return 0

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
        '''

        if not letter:
            d = {}  # change for Py2.7
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
              File "core.py", line 316, in max_power
                raise KeyError('letter not in polynomial')
            KeyError: 'letter not in polynomial'

        It raises KeyError if the letter is not in the polynomial.
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
              File "core.py", line 325, in min_power
                raise KeyError('letter not in polynomial')
            KeyError: 'letter not in polynomial'

        It raises KeyError if the letter is not in the polynomial.
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
        '''

        if not letter:
            d = {}  # change for Py2.7
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

        .. versionadded:: 0.2
        '''

        def is_p_square(n):
            '''
            Internal function used to check if a power is divisible by 2
            '''
            return n & 1 == 0 ## n % 2
        def is_perfect_square(n):
            '''
            Internal function to check if an integer is a perfect square
            '''
            return int(n ** 0.5) ** 2 == n
        def _check(a):
            '''
            Check if a monomial is a square
            '''
            first = self[a][1]
            power = first[first.keys()[0]]
            if len(first) == 1 and is_p_square(power):
                if a == 1:
                    return self[a][0] < 0
                if is_perfect_square(self[a][0]):
                    return True
            return False

        if len(self) != 2:
            return False
        if self.right_hand_side:
            if self.right_hand_side < 0 and \
                                       is_perfect_square(-self.right_hand_side):
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

    def to_plist(self, letter='x'):
        '''
        Returns the polynomial formatted into a list of lists.
        '''

        return [[m[0], m[1].get(letter, 0)] for m in self._monomials]

    def invert(self, v=1):
        '''
        Returns an :class:`AlgebraicFraction` object with *v* as :meth:`AlgebraicFraction.numerator` and the polynomial as :meth:`AlgebraicFraction.denominator`::

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

    @ coerce_poly
    def update(self, pol_or_monomials, simplify=None):
        '''
        Updates the polynomial with another polynomial.
        This does not create a new instance, but replaces :attr:`monomials` with others monomials, then it simplifies.

        *pol_or_monomials* can be:
            * a polynomial
            * a tuple of monomials
            * a string that will be passed to :func:`parse_polynomial`
            * an integer

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

        If *simplify*, the polynomial will be simplified. Default is None, in this case *simplify* will be equal to :attr:`self._simplify`.

        This method returns the instance, so we can use it::

            >>> p.update('2c - 4a').raw_powers()
            {'a': [0, 1], 'c': [1, 0]}
            >>> p
            + 2c - 4a
            >>> p.update('3x^2 - x + 5').iscomplete()
            True
            >>> p
            + 3x^2 - x + 5
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

    @ coerce_poly
    def append(self, pol_or_monomials):
        '''
        Appends the given monomials to :attr:`monomials`, then simplifies.

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
        '''

        self._monomials = tuple(list(pol_or_monomials._monomials) + list(self._monomials))
        self.simplify()

    def div_all(self, poly, int=False):
        '''
        Divide all polynomial's monomials by *poly*::

            >>> a = Polynomial(parse_polynomial('3x^4 - 9x'))
            >>> a.gcd
            - 3x
            >>> a.div_all(a.gcd)
            - x^3 + 3

        :param poly: the polynomial or the integer
        :param bool int: when True, the *poly* parameter will be interpreted as an integer, and the division will be between each coefficient and *poly*
        :type poly: :class:`Polynomial` or integer
        :rtype: :class:`Polynomial`

        .. versionadded:: 0.2
        .. versionadded:: 0.4
            The *int* parameter
        '''

        if int: # the poly parameter is an integer
            return poly1d([c / poly for c in self.coefficients])
        return sum((Polynomial((monomial,)) / poly for monomial in self._monomials), Polynomial())

    def isnum(self):
        '''
        Returns True whether the polynomial represents a number, False otherwise::

            >>> from pypol import *
            >>> x.isnum()
            False
            >>> (x + 1).isnum()
            False
            >>> ONE.isnum()
            True
            >>> NULL.isnum()
            True

        .. versionadded:: 0.5
        '''
        if self == Polynomial():
            return True
        return self.right_hand_side and len(self) == 1

    def filter(self):
        '''
        Returns a new Polynomial instance, with :attr:`monomials` filtered, i.e. with no null term (with 0 coefficient).

        **Examples**

        >>> m = parse_polynomial('0x3 + 0x2 - 1x - 4') ## pypol.parse_polynomial
        >>> m
        [(0, {'x': 3}), (0, {'x': 2}), (-1, {'x': 1}), (-4, {})]
        >>> p = Polynomial(m)
        >>> p
        - x - 4
        >>> p.monomials
        ((0, {'x': 3}), (0, {'x': 2}), (-1, {'x': 1}), (-4, {}))
        >>> q = p.filter() ## Polynomial object is immutable
        >>> q
        - x - 4
        >>> q == p
        True
        >>> p.monomials
        ((0, {'x': 3}), (0, {'x': 2}), (-1, {'x': 1}), (-4, {}))
        >>> q.monomials
        ((-1, {'x': 1}), (-4, {}))

        .. versionadded:: 0.4
        '''

        return Polynomial(self._filter())

    @ classmethod
    def from_roots(cls, roots, var='x'):
        '''
        This classmethod constructs a :class:`~pypol.Polynomial` from its roots.

        :param roots: the roots of the polynomial to be constructed
        :param string var: the polynomial's letter (default to :math:`x`)
        :rtype: :class:`~pypol.Polynomial`

        It does exactly the same as :func:`pypol.funcs.from_roots`::

            >>> from pypol import *
            >>> from pypol import funcs
            >>> 
            >>> p = Polynomial.from_roots([4, -23, 42424, 2])
            >>> p
            + x^4 - 42407x^3 - 721338x^2 + 5515304x - 7806016
            >>> map(p, (4, 2, -23, 42424))
            [0, 0, 0, 0L]
            >>> p = Polynomial.from_roots([14, -3, 42, -22], 'y')
            >>> p
            + y^4 - 31y^3 - 746y^2 + 11004y + 38808
            >>> p(14)
            0
            >>> p(-3)
            0
            >>> funcs.from_roots([2, -3, 42])
            + x^3 - 41x^2 - 48x + 252

        You can call :meth:`from_roots` from any polynomial::

            >>> x.from_roots([1, -1, 2, -2])
            + x^4 - 5x^2 + 4
            >>> NULL.from_roots([1, -2, 2442, 2])
            + x^4 - 2443x^3 + 2438x^2 + 9772x - 9768
            >>> ONE.from_roots([1, -23])
            + x^2 + 22x - 23
            >>> (x - 2 + y**2).from_roots([1, -2])
            + x^2 + x - 2

        .. versionadded:: 0.5
        '''

        x = monomial(**{var: 1})
        return reduce(operator.mul, (x - (fractions.Fraction.from_float(r) if isinstance(r, float) else r) for r in roots))

    def to_float(self):
        '''
        Converts the polynomial coefficients into floats and creates a new polynomial::

            >>> p = polynomial('3/2x^2 - 3x + 1/2')
            >>> p
            + 3/2x^2 - 3x + 1/2
            >>> p.to_float()
            + 1.5x^2 - 3.0x + 0.5

        `p` has not changed::

            >>> p
            + 3/2x^2 - 3x + 1/2
            >>> p.update(p.to_float())
            + 1.5x^2 - 3.0x + 0.5
            >>> p
            + 1.5x^2 - 3.0x + 0.5

        .. versionadded:: 0.5
        '''

        tmp = list(copy.deepcopy(self._monomials))
        tmp_ = copy.deepcopy(tmp)
        for i, m in enumerate(tmp_):
            tmp[i] = list(tmp[i])
            tmp[i][0] = float(m[0])

        return Polynomial(tmp)

    def simplify(self):
        '''
        Simplifies the polynomial. This is done automatically on the __init__ and on the :meth:`update` methods if :attr:`self._simplify` is True.
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

            if not monomial[0] and (not monomial[1] or all(not x for x in monomial[1].values())):
                simplified[index] = None

        self._monomials = tuple(sorted(filter(lambda i: i is not None, simplified), key=self._key(), reverse=True))

    def _key(self, letter=None):
        '''
        Comparator function used to sort the polynomial's monomials. You should neither change it nor overload it.

        .. versionadded:: 0.2
        '''

        if not letter:
            letter = self.max_letter()

        return lambda item: item[1].get(letter, 0)

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

    def _filter(self):
        return [copy.deepcopy(m) for m in self._monomials if m[0]]

    def _format(self):
        '''
        Format the polynomial for __repr__.
        '''

        return ' '.join(filter(None, [self._m_format(monomial).replace('-', '- ') if monomial[0] < 0 \
                                      else ('+ ' + self._m_format(monomial) if self._m_format(monomial) \
                                                                            else '') \
                                    for monomial in self._monomials])).strip()

    def _m_format(self, monomial):
        '''
        Format a single monomial.
        '''

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

        #if print_format: ## Older versions
        #    return tmp_coefficient + ''.join(var_list).replace('^', '') \
        #        .replace('0', unichr(8304)).replace('1', unichr(8305)) \
        #        .replace('2', unichr(178)).replace('3', unichr(179)) \
        #        .replace('4', unichr(8308)).replace('5', unichr(8309)) \
        #        .replace('6', unichr(8310)).replace('7', unichr(8311)) \
        #        .replace('8', unichr(8312)).replace('9', unichr(8313)) \
        #        .encode('utf-8')
        return tmp_coefficient + ''.join(var_list)

    def __repr__(self):
        return self._format()

    #def __str__(self): ## Older versions
    #    raise NotImplementedError('Use Polynomial.__repr__')

    @ coerce_poly
    def __eq__(self, other):
        try:
            if not len(self) and not len(other):
                return True

            return sorted(self._filter()) == sorted(other._filter())
        except (AttributeError, TypeError):
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self._filter())

    def __pos__(self):
        return copy.copy(self)

    def __neg__(self):
        return self * -1

    def __nonzero__(self):
        if not len(self):
            return False
        if all(not m[0] for m in self._monomials):
            return False
        return True

    def __contains__(self, other):
        return other in self._monomials

    def __copy__(self):
        return Polynomial(self._monomials)

    def __deepcopy__(self, p):
        return Polynomial(self._monomials, self._simplify)

    def __getitem__(self, p):
        return self._monomials[p]

    def __setitem__(self, p, v):
        tmp_monomials = list(self._monomials)
        tmp_monomials[p] = v
        self._monomials = tuple(tmp_monomials)

    def __delitem__(self, p):
        tmp_monomials = list(self._monomials)
        del tmp_monomials[p]
        self._monomials = tuple(tmp_monomials)

    def __call__(self, *args, **kwargs):
        '''
        It's also possible to call the polynomial.
        You can pass the arguments in two ways:

            * positional way, using *args*
            * keyword way, using *kwargs*

        :raises: :exc:`NameError` if you do not pass any argument.

        ::

            >>> Polynomial(parse_polynomial('x^3 - 4x^2 + 3'))()

            Traceback (most recent call last):
              File "<pyshell#3>", line 1, in <module>
                Polynomial(parse_polynomial('x^3 - 4x^2 + 3'))()
              File "core.py", line 1466, in __call__
                return eval(self.eval_form, letters)
              File "<string>", line 1, in <module>
            NameError: name 'x' is not defined
            >>> Polynomial(parse_polynomial('x^3 - 4x^2 + 3'))(2)
            -5
            >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(2, 3)  ## Positional way, x=2, y=3
            18
            >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(y=2, x=3)  ## Keyword way: y=2, x=3
            23

        When you use *args*, the dictionary is built in this way::

            dict(zip(self.letters[:len(args)], args))

        *args* has a major priority of *kwargs*, so if you try them both at the same time you will see::

            >>> Polynomial(parse_polynomial('3xy + x^2 - 4'))(2, 3, y=5, x=78) # args is predominant
            18

        If no argument is supplied, set automatically all the letters to 1, with::

            dict(zip(self.letters, [1]*len(self.letters)))

        so::

            >>> p = poly1d([3, -2, 4, .53, -2, 5, .3])
            >>> q = poly1d([4, -2, 4, .4], 'y')
            >>> p
            + 3x^6 - 2x^5 + 4x^4 + 0.53x^3 - 2x^2 + 5x + 3/10
            >>> q
            + 4y^3 - 2y^2 + 4y + 2/5
            >>> k = p*q
            >>> k
            + 12x^6y^3 - 6x^6y^2 + 12x^6y + 6/5x^6 - 8x^5y^3 + 4x^5y^2 - 8x^5y - 4/5x^5 + 16x^4y^3 - 8x^4y^2 + 16x^4y + 8/5x^4 + 2.12x^3y^3 - 1.06x^3y^2 + 2.12x^3y + 0.212x^3 - 8x^2y^3 + 4x^2y^2 - 8x^2y - 4/5x^2 + 20xy^3 - 10xy^2 + 20xy + 2x + 6/5y^3 - 3/5y^2 + 6/5y + 3/25
            >>> k()
            56.512
            >>> k() == k(1, 1)
            True
            >>> k() == k(x=1, y=1)
            True
            >>> k() == k(y=1, x=1)
            True

        .. versionchanged:: 0.2
            Added the support for positional and keyword arguments.
        .. versionchanged:: 0.4
            Added the support for no arguments
        '''

        if not self:
            return 0
        if args:
            letters = dict(zip(self.letters[:len(args)], args))
        elif kwargs:
            letters = kwargs
        else:
            letters = dict(zip(self.letters, [1]*len(self.letters)))
        if len(letters) < len(self.letters):
            for l in self.letters:
                if l not in letters:
                    letters[l] = monomial(**{l: 1})
        return eval(self.eval_form, {'__builtins__': None}, letters)

    @ coerce_poly
    def __add__(self, other):
        try:
            if not other:
                return self
            return Polynomial(self._monomials + other._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    def __radd__(self, other):
        return self + other

    @ coerce_poly
    def __sub__(self, other):
        try:
            if not other:
                return self
            return Polynomial(self._monomials + (-other)._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    @ coerce_poly
    def __rsub__(self, other):
        return Polynomial((-self)._monomials + other._monomials)

    @ coerce_poly
    def __mul__(self, other):
        def _mul(a, b):
            new_coeff = a[0] * b[0]
            if not a[1] and not b[1]:
                return (new_coeff, {})
       ## The following code can be replaced with this (only for Py2.7):
       #new_vars = {letter: (a[1].get(letter, 0) + b[1].get(letter, 0)) \
       #for letter in set(a[1].keys()).union(b[1].keys())} # uncomment for Py2.7

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

    @ coerce_poly
    def __divmod__(self, other):
        def _div(a, b):
            new_coefficient = fractions.Fraction(str(a[0] / b[0]))
            new_vars = copy.copy(a[1])
            for letter, exp in b[1].iteritems():
                if exp == 0:
                    continue
                new_vars[letter] = a[1][letter] - exp

            return monomial(new_coefficient, **new_vars)

        if not other:
            raise ZeroDivisionError('polynomial division or modulo by zero')
        if other == monomial():
            return (self, Polynomial())
        if other == monomial(-1):
            return (-self, Polynomial())

        A = Polynomial(copy.deepcopy(self._monomials))
        B = Polynomial(copy.deepcopy(other._monomials))
        Q = Polynomial()

        if A.degree < B.degree:
            raise ValueError('The polynomials are not divisible')

        letter = B.max_letter()
        while A.degree >= B.degree:
            if not A:
                return Q, Polynomial()
            if A.isnum() and B.isnum():
                Q.append(A.right_hand_side / B.right_hand_side)
                return Q, Polynomial()

            A.sort(key=self._key(letter), reverse=True)
            try:
                quotient = _div(A[0], B[0])
            except KeyError:
                raise ValueError('The polynomials are not divisible')
            del A[0]
            Q.append(quotient)

            if len(B) == 1:
                continue
            m = Polynomial(B[1:])
            if not m:
                return Q, Polynomial()
            A += (-quotient * m)
            if not A:
                return Q, Polynomial()

        return Q, A.filter()

    @ coerce_poly
    def __div__(self, other):
        return divmod(self, other)[0]

    @ coerce_poly
    def __truediv__(self, other):
        try:
            quotient, remainder = divmod(self, other)
        except ValueError:
            return AlgebraicFraction(self, other)
        if remainder:
            return AlgebraicFraction(self, other)
        return quotient

    @ coerce_poly
    def __mod__(self, other):
        return divmod(self, other)[1]

    def __rmod__(self, other):
        return self % other

    def __pow__(self, exp):
        if exp == 0:
            return monomial()
        elif exp < 0:
            return AlgebraicFraction(monomial(1), self ** abs(exp))
        elif len(self) == 1:
            c = self.filter()
            for m in c._monomials:
                for l in m[1]:
                    m[1][l] *= exp
            return c
        else:
            try:
                return reduce(operator.mul, [self]*exp)
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
        #if self._simplify:
            #self.simplify()

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

    @ coerce_frac
    def update(self, pol_or_string):
        '''
        Updates the algebraic fraction with *pol_or_string*.
        *pol_or_string* can be:

            * a string
            * a polynomial
            * 2-length tuple

        **Examples**

        ::

            
        '''

        self._numerator, self._denominator = pol_or_string.terms
        return self

    def simplify(self):
        '''
        Simplifies the algebraic fraction. This is done automatically on the __init__ and on the :meth:`update` methods if :attr:`self._simplify` is True.
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

        common_poly = gcd(self._numerator, self._denominator)
        self._numerator = self._numerator.div_all(common_poly)
        self._denominator = self._denominator.div_all(common_poly)
        return self

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

    def __deepcopy__(self, a):
        return AlgebraicFraction(self._numerator,
                                 self._denominator,
                                 self._simplify)

    @ coerce_frac
    def __add__(self, other):
        least_multiple = lcm(self._denominator.lcm, other._denominator.lcm)
        num = least_multiple / self._numerator
        den = least_multiple / self._denominator
        return AlgebraicFraction(self._numerator * num, self._denominator * den)

    def __radd__(self, other):
        return self + other

    @ coerce_frac
    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return self - other

    @ coerce_frac
    def __mul__(self, other):
        return AlgebraicFraction(self._numerator * other._numerator,
                                self._denominator * other._denominator)

    def __rmul__(self, other):
        return self * other

    @ coerce_frac
    def __div__(self, other):
        return self * other.invert()