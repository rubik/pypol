Polynomial class reference
==========================

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

    .. :method: monomials

        monomials is a property that returns the polynomial's monomials.
        Example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).monomials
            ((2, {'x': 3}), (4, {'y': 1, 'x': 1}))

        You can also set the monomials::

            >>> p = Polynomial(parse_polynomial('2x^3 + 4xy'))
            >>> p.monomials = ((2, {}),) # The comma!
            >>> p
            + 2

    .. :method: ordered_monomials([, cmp=None[, key=None[, reverse=False]]])

        Applies :func:`sorted` to self.monomials, with cmp, key and reverse arguments.

    .. :method: degree

        Returns the degree of the polynomial, i.e. the maximum degree of its monomials.
        An example::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).degree
            3

    .. :method: letters

        Returns a tuple of all the letters that appear in the polynomial.
        ::

            >>> Polynomial(parse_polynomial('2x^3 + 4xy')).letters
            ('x', 'y')