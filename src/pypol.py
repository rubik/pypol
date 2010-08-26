# -*- coding: utf-8 -*-

from __future__ import division
import copy ## 6 times used
import fractions ## 2 times used
import operator ## 4 times used
import random ## 7 times used
import re ## 2 times used


__author__ = 'Michele Lacchia'
__version__ = (0, 0)
__version_str__ = '0.0'

__all__ = ['polynomial', 'gcd', 'lcm', 'are_similar', 'make_polynomial', 'parse_polynomial', 'random_poly', 'Polynomial', 'AlgebraicFraction',]


def polynomial(string=None, simplify=True, print_format=True):
    '''
    Function that returns a Polynomial instance.
    string is a string that represent a polynomial, default is None.

    ## Syntax rules
        Powers can be expressed using the `^` symbol. If a digit follows a letter then it is interpreted as an exponent. So the following expressions are be equal:

             polynomial('2x^3y^2 + 1'); polynomial('2x3y2 + 1')

          but if there is a white space after the letter then the digit is interpreted as a positive coefficient.
          So this:

             polynomial('2x3y 2 + 1')

          represents this polynomial:

             2x^3y + 3
    '''

    if not string:
        return Polynomial()
    return make_polynomial(parse_polynomial(string), simplify, print_format)

def make_polynomial(monomials, simplify=True, print_format=True):
    '''
    Make a polynomial from a list of tuples.
    For example:

        make_polynomial(parse_polynomial('2x + 3y - 4'))
        2x + 3y - 4
    '''

    return Polynomial(monomials, simplify, print_format)

def are_similar(a, b):
    '''
    Returns True whether the two monomials are similar,
    i.e. if they have the same literal part, False otherwise
    '''

    return a[1] == b[1]

def gcd(*args): # Still in development
    '''
    Calculate the Greatest Common Divisor of args.
    '''
    def _internal_gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    return reduce(_internal_gcd, args)

def lcm(*args): # Still in development
    '''
    Calculate the Least Common Divisor of args.
    '''
    def _internal_lcm(a, b):
        return operator.truediv(a*b, gcd(a, b))

    return reduce(_internal_lcm, args)

def parse_polynomial(string, max_length=None):
    '''
    Parse a string that represent a polynomial.
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


class Polynomial(object):
    '''
    Base class that represent a polynomial
    Polynomial([monomials[, simplify[, print_format]]])

    monomials is a tuple of tuples like this:

      -3xy + 4x^2y^4       ->

        ((-3, {'x': 1, 'y': 1}), (4, {'x': 2, 'y': 4}))

    if simplify, if simplifies monomials on __init__ and update
    if print_format it will print literal exponents instead of ^ on __repr__
    '''

    def __init__(self, monomials=(), simplify=True, print_format=True):
        self._monomials = tuple(sorted(monomials, cmp=self._cmp, reverse=True))
        self.simplify = simplify
        self._print_format = print_format
        if self.simplify:
            self._simplify()

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
    def letters(self):
        '''
        Returns a list of all the letters that appear in the polynomial.
        '''

        return tuple(sorted(reduce(operator.or_, [set(m[1].keys()) for m in self._monomials if m[1]], set())))

    @ property
    def right_hand_side(self):
        '''
        Returns, if there is, the right hand-side term, False otherwise.
        '''

        ## if not self._monomials[-1][1]:
        ##     return self._monomials[-1]  # Check this
        for monomial in self._monomials:
            if not monomial[1]:
                return monomial[0]
        return False

    @ property
    def print_format(self):
        return self._print_format

    @ print_format.setter
    def print_format(self, val):
        self._print_format = bool(val)

    @ property
    def zeros(self):
        if len(self.letters) - 1:
            return NotImplemented
        divisors = lambda n: [1] + [x for x in xrange(2, n//2 +1) if not n % x] + [n]
        if not self.right_hand_side:
            return []
        divs = divisors(self.right_hand_side)
        adivs = map(operator.neg, divs)
        return tuple([x for x in divs + adivs if not self(x)])

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
        if right_hand_side:
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
        return filter(None, raw[:-1]) + [raw[-1]]

    def islinear(self):
        '''
        Returns True if the polynomial is linear, False otherwise.
        '''

        return all(exp <= 1 for monomial in self._monomials for var, exp in monomial[1].iteritems())

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

        return self.powers(letter) == range(self.max_power(letter), -1, -1)

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

        try:
           self._monomials = self._check_other(pol_or_monomials)._monomials
        except AttributeError:
            return NotImplemented

        if self.simplify:
            self._simplify()
        return self

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

        self._monomials = tuple(sorted(self._check_other(pol_or_monomials)._monomials + self._monomials, cmp=self._cmp, reverse=True))
        self._simplify()

    def insert(self, index, monomial):
        '''
        Deprecated method
        '''
        raise DeprecationWarning('This method is deprecated, use append instead')
        tmp_monomials = list(self._monomials)
        tmp_monomials.insert(index, monomial)
        self._monomials = tuple(tmp_monomials)
        self._simplify()

    def _simplify(self):
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

    def _cmp(self, a, b):
        '''
        Comparator function used to sort the monomials.
        '''

        try:                         ## Change this - ugly!
            ma = max(a[1].values())
        except ValueError:
            ma = 0
        try:
            mb = max(b[1].values())
        except ValueError:
            mb = 0 ########################################

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

    def _format(self):
        return ' '.join([self._m_format(monomial).replace('-', '- ') if monomial[0] < 0 \
                    else ('+ ' + self._m_format(monomial) if self._m_format(monomial) else '') for monomial in self._monomials]).strip()

    def _m_format(self, monomial):
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

        if self._print_format:   ## Implement this
            return tmp_coefficient + ''.join(var_list).replace('^', '') \
                .replace('0', unichr(8304)).replace('1', unichr(185)) \
                .replace('2', unichr(178)).replace('3', unichr(179)) \
                .replace('4', unichr(8308)).replace('5', unichr(8309)) \
                .replace('6', unichr(8310)).replace('7', unichr(8311)) \
                .replace('8', unichr(8312)).replace('9', unichr(8313)).encode('utf-8')
        return tmp_coefficient + ''.join(var_list)

    def _check_other(self, a):
        if isinstance(a, int):
            return Polynomial(((a, {}),))
        elif isinstance(a, str):
            return polynomial(a)
        elif isinstance(a, tuple):
            return Polynomial(a)
        return a

    def __repr__(self):
        return self._format()

    def __eq__(self, other):
        def _filter(mons):
            tmp_mons = []
            for m in mons:
                if m[0]:
                    tmp_mons.append(m)
            return tmp_mons
        #other = self._check_other(other)
        return sorted(_filter(self._monomials)) == sorted(_filter(other._monomials))

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self._monomials)

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __nonzero__(self):
        return bool(len(self))

    def __contains__(self, other):
        return set(self._check_other(other)._monomials).issubset(self._monomials)

    def __copy__(self):
        return copy.copy(self._monomials)

    def __deepcopy__(self):
        return copy.deepcopy(self._monomials)

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

    def __call__(self, val):   ## TODO: Change for other letters
        letter = self.letters[0]
        i = '+'.join(['%s*%s' % (str(c), ''.join(['%s**%s' % (letter, exp) for letter, exp in vars.iteritems()]))
                        for c, vars in (self._monomials[:-1] if self.right_hand_side else self._monomials)]) \
                    .replace('+-', '-').replace('**1', '')
        return eval(i, {letter: val})

    def __add__(self, other):
        try:
            other = self._check_other(other)
            return Polynomial(self._monomials + other._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        try:
            other = self._check_other(other)
            return Polynomial(self._monomials + (-other)._monomials)
        except (AttributeError, TypeError):
            return NotImplemented

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        other = self._check_other(other)
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

    def __divmod__(self, other):
        other = self._check_other(other)
        def _set_up(pol):
             if not pol.letters:
                 return self._make_complete()
             for m in pol._monomials:
                 for var in self.letters:
                     if var not in m[1]:
                         m[1][var] = 0
             self._make_complete(letter)

        def _div(a, b):
            if len(b) == 1:
                b = (1, b)

            new_coefficient = fractions.Fraction(str(a[0] / b[0]))
            new_vars = copy.copy(a[1])
            for letter, exp in b[1].iteritems():
                new_vars[letter] = a[1][letter] - exp

            return Polynomial(((new_coefficient, new_vars),))

        other = self._check_other(other)
        A = Polynomial(copy.deepcopy(self._monomials))
        B = Polynomial(copy.deepcopy(other._monomials))
        Q = Polynomial()

        d = {}
        for l in B.letters:
            d[B.max_power(l)] = l
        letter = d[max(d.keys())]

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
        quotient, remainder = divmod(self, other)
        if not remainder:
            return Polynomial
        return remainder

    def __pow__(self, exp):
        try:
            return reduce(operator.mul, [self]*exp)
        except (AttributeError, TypeError):
            return NotImplemented


class AlgebraicFraction(object):
    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator

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
        Returns the denominator of the AlgebraicFraction.
        '''

        return self._denominator

    @ denominator.setter
    def numerator(self, val):
        '''
        Sets the denominator of the AlgebraicFraction
        '''

        self._denominator = val

    @ property
    def terms(self):
        '''
        Returns both the numerator and the denominator.
        '''

        return (self._numerator, self._denominator)

    def __repr__(self):
        return 'AlgebraicFraction(%s, %s)' % (self._numerator, self._denominator) ## For compatibility

    def __str__(self):
        a, b = str(self._numerator), str(self._denominator)
        sep = max((len(a), len(b)))*u'\u2212'.encode('utf-8')
        len_ = len(sep)//2
        return '\n'.join([a.center(len_), sep, b.center(len_)])