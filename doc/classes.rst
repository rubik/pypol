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

.. autoclass:: Polynomial([, monomials=()[, simplify=True]])

    .. automethod:: monomials()

    .. automethod:: ordered_monomials()

    .. automethod:: coefficients()

    .. automethod:: coeff_gcd()

    .. automethod:: coeff_lcm()

    .. automethod:: gcd()

    .. automethod:: lcm()

    .. automethod:: degree()

    .. automethod:: letters()

    .. automethod:: joint_letters()

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

    .. automethod:: update

    .. automethod:: append

    .. automethod:: div_all

    .. automethod:: simplify

    .. automethod:: _cmp

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