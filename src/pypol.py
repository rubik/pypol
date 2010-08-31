#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials (and monomails too)

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
- Python 2.6 (or greater)
'''

from __future__ import division
import copy ## used 6 times
import fractions ## used 2 times
import operator ## used 4 times
import random ## used 7 times
import re ## 2 used times


__author__ = 'Michele Lacchia'
__version__ = (0, 1)
__version_str__ = '0.1'

__all__ = ['polynomial', 'algebraic_fraction', 'gcd', 'lcm', 'gcd_p', 'lcm_p', 'are_similar', 'make_polynomial', 'parse_polynomial', 'random_poly', 'Polynomial', 'AlgebraicFraction',]


def polynomial(string=None, simplify=True):
    '''
    Function that returns a Polynomial object.
    string is a string that represent a polynomial, default is None.
    If simplify, then the Polynomial will be simplified on __init__ and on update.

    ## Syntax rules
        Powers can be expressed using the `^` symbol. If a digit follows a letter then it is interpreted as an exponent. So the following expressions are be equal:

            >>> polynomial('2x^3y^2 + 1') == polynomial('2x3y2 + 1')
            True

          but if there is a white space after the letter then the digit is interpreted as a positive coefficient.
          So this:

            >>> polynomial('2x3y 2 + 1')

          represents this polynomial:

            2x^3y + 3
    '''

    if not string:
        return Polynomial()
    return make_polynomial(parse_polynomial(string), simplify)

def algebraic_fraction(s1, s2='1', simplify=True):
    '''
    Wrapper function that returns an :class:AlgebraicFraction object.
        s1 and s2 are two strings that represent a polynomial::

            >>> algebraic_fraction('3x^2 - 4xy', 'x + y')
            AlgebraicFraction(+ 3x² - 4xy, + x + y)
            >>> algebraic_fraction('3x^2 - 4xy', 'x + y').terms
            (+ 3x^2 - 4xy, + x + y)
    '''

    return AlgebraicFraction(polynomial(s1), polynomial(s2), simplify)

def make_polynomial(monomials, simplify=True):
    '''
    Make a polynomial from a list of tuples.
    For example:

        >>> make_polynomial(parse_polynomial('2x + 3y - 4'))
        2x + 3y - 4
    '''

    return Polynomial(monomials, simplify)

def are_similar(a, b):
    '''
    Returns True whether the two monomials are similar,
    i.e. if they have the same literal part, False otherwise.
    '''

    return a[1] == b[1]

def gcd(a, b):
    '''
    Calculates the Greatest Common Divisor of the two polynomials.
    '''

    coefficient = fractions.gcd(a.coeff_gcd, b.coeff_gcd)
    letters = set(a.letters).intersection(b.letters)
    vars = {} ## Change for Py2.7
    for letter in letters:
        vars[letter] = min(a.min_power(letter), b.min_power(letter))
    return Polynomial(((coefficient, vars),))

def gcd_p(*polynomials):
    return reduce(gcd, polynomials)

def lcm(a, b):
    '''
    Calculates the Least Common Divisor of two polynomials.
    '''

    coefficient = (a.coeff_lcm*b.coeff_lcm, fractions.gcd(a.coeff_lcm, b.coeff_lcm))
    letters = set(a.letters).intersection(b.letters)
    for letter in letters:
        vars[letter] = max(a.max_power(letter), b.max_power(letter))
    return Polynomial(((coefficient, vars),))

def lcm_p(*polynomials):
    return reduce(lcm, polynomials)

def parse_polynomial(string, max_length=None):
    '''
    Parses a string that represent a polynomial.
    It can parse integer coefficients, float coefficient and fractional coefficient.

    See polynomial's syntax rules.
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

def random_poly(coeff_range=xrange(-10, 11), len_=None, letters='xyz', max_letters=3, exp_range=xrange(1, 6), right_hand_side=None):
    '''
    Returns a polynomial generated randomly.

    coeff_range is the range of the polynomial's coefficients, default is ``xrange(-10, 11)``.
    len_ is the len of the polynomial. Default is None, in this case len_ will be a random number chosen in coeff_range.
    letters are the letters that appear in the polynomial.
    max_letter is the maximum number of letter for every monomial.
    exp_range is the range of the exponents.
    if right_hand_side is True the polynomial will have a right_hand_side. Default is None, that means the right_hand_side will be chosen randomly.
    '''
    if not len_:
        len_ = random.choice(coeff_range)
    if len_ < 0:
        len_ = -len_
    monomials = []
    for _ in xrange((len_ - 1 if right_hand_side else len_)):
        vars = {} ## Change on Py2.7
        for __ in xrange(random.randint(1, max_letters)):
            vars[random.choice(letters)] = random.choice(exp_range)
        monomials.append((random.choice(coeff_range), vars))
    if not right_hand_side:
        right_hand_side = random.choice((True, False,))
    if right_hand_side:
        monomials.append((random.choice(coeff_range), {}))
    return Polynomial(monomials)

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

def _get_letters_powers(p, l, min=True):
    d = {} ## Change for Py2.7
    for letter in l:
        if min:
            d[letter] = p.min_power(letter)
        else:
            d[letter] = p.max_power(letter)
    return d


class Polynomial(object):
    '''
    Base class that represent a polynomial
    Polynomial([monomials[, simplify]])

    monomials is a tuple of tuples like this:

      -3xy + 4x^2y^4       ->

        ((-3, {'x': 1, 'y': 1}), (4, {'x': 2, 'y': 4}))

    if simplify, if simplifies monomials on __init__ and update
    '''

    __slots__ = ('_monomials', '_simplify',)

    def __init__(self, monomials=(), simplify=True):
        self._monomials = tuple(sorted(monomials, cmp=self._cmp, reverse=True))
        self._simplify = simplify
        if self._simplify:
            self.simplify()

    @ property
    def monomials(self):
        return self._monomials

    @ monomials.setter
    def monomials(self, values):
        self._monomials = sorted(values, cmp=self._cmp, reverse=True)

    def ordered_monomials(self, cmp=None, key=None, reverse=False):
        '''
        Return a sorted tuple of monomials applying sorted() to self.monomials.
        '''

        return sorted(self._monomials, cmp, key, reverse)

    @ property
    def coefficients(self):
        return [monomial[0] for monomial in self._monomials]

    @ property
    def coeff_gcd(self):
        return reduce(fractions.gcd, self.coefficients)

    @ property
    def coeff_lcm(self):
        return reduce(lambda a, b: operator.truediv(a*b, fractions.gcd(a, b)), self.coefficients)

    @ property
    def gcd(self):
        vars = {} ## Change for Py2.7
        for letter in self.joint_letters:
            vars[letter] = self.min_power(letter)
        return Polynomial(((self.coeff_gcd, vars),))

    @ property
    def lcm(self):
        vars = {} ## Change for Py2.7
        for letter in self.joint_letters:
            vars[letter] = self.max_power(letter)
        return Polynomial(((self.coeff_gcd, vars),))

    @ property
    def degree(self):
        '''
        Return the degree of the polynomial, i.e. the maximum
        degree of its monomials.
        '''

        try:
            return max([sum(monomial[1].values()) for monomial in self._monomials])
        except ValueError:
            return 0

    @ property
    def eval_form(self):
        '''
        Returns a string form that can be used with eval()
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

        evallable = '+'.join(tmp).replace('+-', '-').replace('**1', '').replace('1*', '')
        return evallable

    @ property
    def letters(self):
        '''
        Returns a tuple of all the letters that appear in the polynomial.
        '''

        return tuple(sorted(reduce(operator.or_, [set(m[1].keys()) for m in self._monomials if m[1]], set())))

    @ property
    def joint_letters(self):
        '''
        Returns a tuple of the letters that appear in all the polynomial's monomials
        '''

        if len(self) == 1:
            return self.letters
        return tuple(reduce(operator.and_, [set(monomial[1].keys()) for monomial in self.monomials]))

    @ property
    def right_hand_side(self):
        '''
        Returns, if there is, the right hand-side term, False otherwise.
        '''

        if not self._monomials[-1][1]:
            return self._monomials[-1]
        return False

    @ property
    def zeros(self):
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
        Returns all the degrees of a letter.
        '''

        if not letter:
            d={}  # change for Py2.7
            for l in self.letters:
                d[l] = self.raw_powers(l)
            return d

        return [monomial[1].get(letter, 0) for monomial in self._monomials]

    def max_power(self, letter):
        '''
        Returns the maximum degree of a letter.
        '''

        if letter not in self.letters:
            raise KeyError('letter not in polynomial')
        return max(self.raw_powers(letter))

    def min_power(self, letter):
        '''
        Returns the minimum degree of a letter.
        '''

        if letter not in self.letters:
            raise KeyError('letter not in polynomial')
        if self.right_hand_side:
            return 0
        return min(self.raw_powers(letter))

    def powers(self, letter=None):
        '''
        Returns all the degrees of a letter and eliminates
        all the zeros except the trailing one.
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
        Returns True if the polynomial is linear, False otherwise.
        '''

        return self.degree <= 1

    def isordered(self, letter=None):
        '''
        Returns True whether the polynomial is ordered, False otherwise.
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
        '''

        if not letter:
            return all(self.iscomplete(l) for l in self.letters)

        if self.max_power(letter) == 1:
            return True
        return self.powers(letter) == range(self.max_power(letter), -1, -1)

    def invert(self, v=1):
        return AlgebraicFraction(Polynomial(((v, {}),)), self)

    def check_other(wrapped):
        def wrapper(self, other):
            if isinstance(other, int):
                other = Polynomial(((other, {}),))
            elif isinstance(other, str):
                other =  polynomial(other)
            elif isinstance(other, tuple):
                other =  Polynomial(other)
            return wrapped(self, other)
        return wrapper

    @ check_other
    def update(self, pol_or_monomials=None):
        '''
        Updates the polynomial with another polynomial.
        This does not create a new instance, but replaces self.monomials with others monomials, then simplify.

        pol_or_monomials can be:
          - a polynomial
          - a tuple of monomials
          - a string that will be passed to parse_polynomial
          - an integer

        default is None. In this case self.monomials will be updated with an empty tuple.
        '''

        if not pol_or_monomials:
            self._monomials = ()
            if self._simplify:
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
        Appends the given monomials to self.monomials,
        then simplify.

        pol_or_monomials can be:
          - a polynomial
          - a string
          - a tuple of monomials
          - an integer
        '''

        self._monomials = tuple(sorted(pol_or_monomials._monomials + self._monomials, cmp=self._cmp, reverse=True))
        self.simplify()

    def div_all(self, poly):
        '''
        Divide all polynomial's monomials by *poly*
        '''

        return sum([Polynomial((monomial,)) / poly for monomial in self._monomials])

    def simplify(self):
        '''
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

    def _cmp(self, a, b):
        '''
        Comparator function used to sort the monomials.
        '''

        ma = max(a[1].values() + [0])
        mb = max(b[1].values() + [0])
        if ma > mb:
            return 1
        elif ma == mb:
            return 0
        else:
            return -1

    def _make_complete(self, letter):
        '''
        If the polynomial is already complete returns False, otherwise makes it complete and returns True.
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
                .replace('0', unichr(8304)).replace('1', unichr(185)) \
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
        self._monomials = tuple(sorted(tmp_monomials, cmp=self._cmp, reverse=True))

    def __delitem__(self, b):
        tmp_monomials = list(self._monomials)
        del tmp_monomials[b]
        self._monomials = tuple(tmp_monomials)

    def __call__(self, *args, **kwargs):
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

            return Polynomial(((new_coefficient, new_vars),))

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

    def __pow__(self, exp):
        '''
        '''

        if exp == 0:
            return Polynomial()
        elif exp < 0:
            return AlgebraicFraction(Polynomial(((1, {}),)), self ** abs(exp))
        else:
            try:
                return reduce(operator.mul, [self]*exp)
            except (AttributeError, TypeError):
                return NotImplemented


class AlgebraicFraction(object):

    __slots__ = ('_numerator', '_denominator', '_simplify',)

    def __init__(self, numerator, denominator=1, simplify=True):
        if not denominator:
            raise ZeroDivisionError('Denominator cannot be 0')
        if isinstance(numerator, AlgebraicFraction) or isinstance(denominator, AlgebraicFraction):
            return NotImplemented
        self._numerator = numerator
        self._denominator = denominator
        self._simplify = simplify
        if self._simplify:
            self.simplify()

    @ property
    def numerator(self):
        '''
        Returns the numerator of the AlgebraicFraction.
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
        Returns the denominator of the algebraic fraction.
        '''

        return self._denominator

    @ denominator.setter
    def denominator(self, val):
        '''
        Sets the denominator of the algebraic fraction
        '''

        self._denominator = val

    @ property
    def terms(self):
        '''
        Returns both the numerator and the denominator.
        '''

        return (self._numerator, self._denominator)

    def invert(self):
        return AlgebraicFraction(self._denominator, self._numerator)

    def simplify(self):
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
        a, b = str(self._numerator), str(self._denominator)
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
        return NotImplemented

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