pypol classes reference
=======================

pypol's classes are two: :class:`Polynomail` and :class:`AlgebraicFraction`.

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

    If *simplify* is True, then the polynomial will be simplified on __init__ and on :meth:`update`.
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

    .. method:: degree

        Returns the degree of the polynomial, i.e. the maximum degree of its monomials.
        An example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).degree
            3

    .. method:: letters

        Returns a tuple of all the letters that appear in the polynomial.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).letters
            ('x', 'y')

    .. method:: eval_form

        Returns a string form of the polynomial that can be used with eval::

            >>> e = Polynomial(parse_polynomial('2x^2 - 4x + 4')).eval_form
            >>> eval(e, {'x': 3})
            10

        If there are more than one letters, it returns NotImplemented.

    .. method:: right_hand_side

        Returns the right-hand side, if it exist, False otherwise.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).right_hand_side
            False
            >>> Polynomial(parse_polynomial('2x^3 + 4xy - 3')).right_hand_side
            -3

    .. method:: zeros

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

    .. method:: powers([, letter=None])

    .. method:: islinear()

    .. method:: isordered([, letter])

    .. method:: iscomplete([, letter=None])

    .. method:: update([, pol_or_monomials=None])

    .. method:: append()

    .. method:: simplify()

    .. method:: _cmp(a, b)

    .. method:: _make_complete(letter)


AlgebraicFraction class reference
---------------------------------

pypol supports the algebraic fractions, although now it is very limited. It supports all the four basic operation but at the moment it does not simplify the terms.

.. class:: AlgebraicFraction(numerator, denominator)

        This class represent an algebraic fraction object.
        It accepts two arguments: *numerator* and *denominator*.
        *numerator* is the numerator of the algebraic fraction, and *denominator* its denominator. Both the terms have to be two polynomials.