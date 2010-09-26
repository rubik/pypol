.. currentmodule:: pypol

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

    .. automethod:: monomials()

    .. automethod:: ordered_monomials()

    .. automethod:: sort()

    .. automethod:: coefficients()

    .. automethod:: gcd()

    .. automethod:: lcm()

    .. automethod:: degree()

    .. automethod:: letters()

    .. automethod:: joint_letters()

    .. automethod:: max_letter(alphabetically=True)

    .. automethod:: eval_form()

    .. automethod:: right_hand_side()

    .. automethod:: zeros()

    .. automethod:: raw_powers

    .. automethod:: max_power

    .. automethod:: min_power

    .. automethod:: powers

    .. automethod:: islinear

    .. automethod:: is_square_diff

    .. automethod:: isordered

    .. automethod:: iscomplete

    .. automethod:: invert

    .. method:: update([, pol_or_monomials[, simplify=None]])

        Updates the polynomial with another polynomial.
        This does not create a new instance, but replaces self.monomials with others monomials, then it simplifies.

        *pol_or_monomials* can be:
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

        If *simplify*, the polynomial will be simplified. Default is None, in this case *simplify* will be equal to self._simplify.

        .. seealso::
            The __init__ method: :class:`Polynomial`

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

    .. method:: append(pol_or_monomials)

       Appends the given monomials to self.monomials, then simplifies.

       *pol_or_monomials* can be:
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

    .. automethod:: div_all

    .. automethod:: simplify

    .. automethod:: _key

    .. automethod:: _make_complete

    .. automethod:: __call__



AlgebraicFraction class reference
---------------------------------

pypol supports the algebraic fractions, although now it is very limited. It supports all the four basic operation but at the moment it does not decompose the terms.

In all these examples we assume::

    a, b = polynomial('3x - 5'), polynomial('2a')


.. autoclass:: AlgebraicFraction(numerator, denominator) 

    .. automethod:: numerator()

    .. automethod:: denominator()

    .. automethod:: terms()

    .. automethod:: invert

    .. automethod:: simplify