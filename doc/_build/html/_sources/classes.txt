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

    .. method:: max_power(letter)

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

    .. method:: islinear()

    .. method:: islinear()

    .. method:: islinear()


AlgebraicFraction class reference
---------------------------------

pypol supports the algebraic fractions, although now it is very limited. It supports all the four basic operation but at the moment it does not simplify the terms.

.. class:: AlgebraicFraction(numerator, denominator)

        This class represent an algebraic fraction object.
        It accepts two arguments: *numerator* and *denominator*.
        *numerator* is the numerator of the algebraic fraction, and *denominator* its denominator. Both the terms have to be two polynomials.