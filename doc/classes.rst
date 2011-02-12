.. currentmodule:: pypol

Classes
=======

pypol's classes are two: :class:`Polynomial` and :class:`AlgebraicFraction`.

:class:`Polynomial` class reference
-----------------------------------

In all these examples we use this method to make a polynomial::

    Polynomial(parse_polynomial('3x^2 - 3'))

but, for convenience we, can also use this method::

    polynomial('3x^2 - 3')

which gives the same result.
Where *polynomial* is the function :func:`polynomial` of the pypol module.

The main class in pypol is :class:`Polynomial`:

.. class:: Polynomial(monomials=(), simplify=True)

    .. automethod:: from_roots

    .. autoattribute:: monomials

    .. automethod:: ordered_monomials

    .. automethod:: sort

    .. autoattribute:: coefficients

    .. automethod:: gcd()

    .. automethod:: lcm()

    .. autoattribute:: degree

    .. autoattribute:: letters

    .. autoattribute:: joint_letters

    .. automethod:: max_letter(alphabetically=True)

    .. autoattribute:: eval_form

    .. autoattribute:: right_hand_side

    .. autoattribute:: rhs

    .. automethod:: get

    .. automethod:: raw_powers

    .. automethod:: max_power

    .. automethod:: min_power

    .. automethod:: powers

    .. automethod:: islinear

    .. automethod:: is_square_diff

    .. automethod:: isordered

    .. automethod:: iscomplete

    .. automethod:: invert

    .. automethod:: isnum

    .. automethod:: filter

    .. automethod:: update(pol_or_monomials,simplify=None)

    .. automethod:: append(pol_or_monomials)

    .. automethod:: div_all

    .. automethod:: simplify

    .. automethod:: _key

    .. automethod:: _make_complete

    .. automethod:: __call__



:class:`AlgebraicFraction` class reference
------------------------------------------

.. warning::

    This class is still in development and could have some bugs.

pypol supports the algebraic fractions, although now it is very limited. It supports all the four basic operation but at the moment it does not simplify the fraction.

In all these examples we assume::

    a, b = polynomial('3x - 5'), polynomial('2a')


.. autoclass:: AlgebraicFraction(numerator, denominator)

    .. autoattribute:: numerator

    .. autoattribute:: denominator

    .. autoattribute:: terms

    .. automethod:: invert

    .. automethod:: update

    .. automethod:: simplify