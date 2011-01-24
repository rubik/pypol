.. currentmodule:: pypol

Global functions
================

pypol module has some functions to work with polynomials. If you need other utility functions check the :mod:`pypol.funcs` and :mod:`pypol.roots` modules.

.. hlist::

    * :func:`polynomial`
    * :func:`algebraic_fraction`
    * :func:`monomial`
    * :func:`poly1d`
    * :func:`poly1d_2`
    * :func:`gcd`
    * :func:`lcm`


.. autofunction:: poly1d

.. autofunction:: poly1d_2

.. autofunction:: polynomial

.. _syntax-rules:

:func:`polynomial`'s syntax rules
---------------------------------

Powers can be expressed using the ``^`` symbol. If a digit follows a letter then it is interpreted as an exponent. So the following expressions are equal::

    >>> polynomial('2x^3y^2 + 1') == polynomial('2x3y2 + 1')
    True

        
but if there is a white space after the letter then the digit is interpreted as a positive coefficient.
So this::

    >>> polynomial('2x3y 2 + 1')

represents this polynomial::

        2x^3y + 3

::

    >>> polynomial('2x3y 2 + 1')
    + 2x^3y + 3

.. autofunction:: algebraic_fraction

.. autofunction:: monomial

.. autofunction:: parse_polynomial

.. autofunction:: gcd

.. autofunction:: lcm

.. seealso:: :mod:`pypol.funcs` for other utility functions.