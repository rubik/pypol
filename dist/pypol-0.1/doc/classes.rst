pypol classes reference
=======================

pypol's classes are two: :class:`Polynomial` and :class:`AlgebraicFraction`.

Polynomial class reference
--------------------------

In all these examples we use this method to make a polynomial::

    Polynomial(parse_polynomial('3x^2 - 3'))

but, for convenience we, can also use this method::

    polynomial('3x^2 - 3')

which gives the same result.
Where *polynomial* is the function :func:`polynomial` of the pypol module.

The main class in pypol is :class:`Polynomial`:

.. class:: Polynomial([, monomials=()[, simplify=True]])

    A :class:`Polynomial` is an object that represents a Polynomial.
    It accepts two arguments: *monomials* and *simplify*.

    *monomials* is a tuple of tuples that represents all the polynomial's monomials.

    If *simplify* is True, then the polynomial will be simplified on __init__ and on :meth:`update`. See also :meth:`simplify`
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

    We can use the :func:`parse_polynomial` function too.

    .. method:: monomials

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

    .. method:: ordered_monomials([, cmp=None[, key=None[, reverse=False]]])

        Applies :func:`sorted` to self.monomials, with cmp, key and reverse arguments.

    .. mehtod:: coefficients

        **property**

        Returns the polynomial's coefficients::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 5')).coefficients
            [2, 4, -5]

    .. method:: degree

        **property**

        Returns the degree of the polynomial, i.e. the maximum degree of its monomials.
        An example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).degree
            3

    .. method:: letters

        **property**

        Returns a tuple of all the letters that appear in the polynomial.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).letters
            ('x', 'y')

    .. method:: eval_form

        **property**

        Returns a string form of the polynomial that can be used with eval::

            >>> e = Polynomial(parse_polynomial('2x^2 - 4x + 4')).eval_form
            >>> eval(e, {'x': 3})
            10

        If there are more than one letters, it returns NotImplemented.

    .. method:: right_hand_side

        **property**

        Returns the right-hand side, if it exist, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).right_hand_side
            False
            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 3')).right_hand_side
            -3

    .. method:: zeros

        **property**

        Returns a tuple containing all the polynomial's zeros.
        Returns NotImplemented when:

        * there are more than one letters
        * there isn't the right-hand side and there are more than one letters or the sum of the polynomial's
            coefficients is not 0

        For example::

            >>> Polynomial(parse_polynomial('2x - 4')).zeros
            (2,)

    .. method:: raw_powers([, letter=None])

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

        See also :meth:`powers`.

    .. method:: max_power(letter)

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
        See also :meth:`min_power`.

    .. method:: min_power(letter)

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
        See also :meth:`max_power`.

    .. method:: powers([, letter=None])

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

        See also: :meth:`raw_powers`

    .. method:: islinear()

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

    .. method:: isordered([, letter=None])

        Returns True whether the polynomial is ordered, False otherwise.
        If letter is None, it checks for all letters; if the polynomial is ordered for all letters, it returns True, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + x - 5')).isordered('x')
            False
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).isordered('a')
            True

        See also :meth:`iscomplete`

    .. method:: iscomplete([, letter=None])

        Returns True whether the polynomial is complete, False otherwise.
        If letter is None it checks for all the letters of the polynomial.
        ::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete('a')
            True
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete('x')
            False
            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).iscomplete()
            False

        See also: :meth:`isordered`

    .. method:: invert([, v=1])

        Returns an :class:`AlgebraicFraction` object with *v* as :meth:`AlgebraicFraction.numerator` and this polynomial as :meth:`AlgebraicFraction.denominator`::

            >>> Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).invert()
            AlgebraicFraction(+ 1, + 3x³ - a² + a - 5)
            >>> print Polynomial(parse_polynomial('3x^3 - a^2 + a - 5')).invert(3)
                    + 3         
            −−−−−−−−−−−−−−−−−−−−
            + 3x³ - a² + a - 5

        See also: :meth:`AlgebraicFraction.invert`

    .. method:: update([, pol_or_monomials=None])

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

        See also: :meth:`append`

    .. method:: append()

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

        See also: :meth:`update`

    .. method:: simplify()

        Simplifies the polynomial. This is done automatically on the __init__ and on the :meth:`update` methods if self._simplify is True
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

    .. method:: _cmp(a, b)

            Comparator function used to sort the polynomial's monomials. You should not change it nor call it.
            See (NotImplemented)

    .. method:: _make_complete(letter)

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

    .. method:: __call__(*args, **kwargs)

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

AlgebraicFraction class reference
---------------------------------

pypol supports the algebraic fractions, although now it is very limited. It supports all the four basic operation but at the moment it does not simplify the terms.

In all these examples we assume::

    a, b = polynomial('3x - 5'), polynomial('2a')


.. class:: AlgebraicFraction(numerator, denominator)

        This class represent an algebraic fraction object.
        It accepts two arguments: *numerator* and *denominator*.
        *numerator* is the numerator of the algebraic fraction, and *denominator* its denominator. Both the terms have to be two polynomials.
        ::

            >>> AlgebraicFraction(a, b)
            AlgebraicFraction(+ 3x - 5, + 2a)

    .. method:: numerator

        **property**

        Returns the numerator of the :class:`AlgebraicFraction`.
        ::

            >>> AlgebraicFraction(a, b).numerator
            + 3x - 5

    .. method:: denominator

        **property**

        Returns the denominator of the :class:`AlgebraicFraction`.
        ::

            >>> AlgebraicFraction(a, b).denominator
            + 2a

    .. method:: terms

        **property**

        Returns both the :meth:`numerator` and the :meth:`denominator`::

            >>> AlgebraicFraction(a, b).terms
            (+ 3x - 5, + 2a)

    .. method:: invert()

        Returns a new :class:`AlgebraicFraction` object with the numerator and the denominator swapped::

            >>> c = AlgebraicFraction(a, b)
            >>> c
            AlgebraicFraction(+ 3x - 5, + 2a)
            >>> d = c.swap()
            >>> d
            AlgebraicFraction(+ 2a, + 3x - 5)
            >>> c.swap() == AlgebraicFraction(b, a)
            True

        See also: :meth:`Polynomial.invert`