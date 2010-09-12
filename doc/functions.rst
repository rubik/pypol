.. currentmodule:: pypol

Utility functions
=================

pypol module has some utility functions to work with polynomials:

.. hlist::

    * :func:`polynomial`
    * :func:`algebraic_fraction`
    * :func:`monomial`
    * :func:`make_polynomial`
    * :func:`parse_polynomial`
    * :func:`random_poly`
    * :func:`root`

.. Temporary down:
    * :func:`gcd`
    * :func:`gcd_p`
    * :func:`lcm`
    * :func:`lcm_p`


polynomial
----------

.. autofunction:: polynomial

.. _syntax-rules:

:func:`polynomial`'s syntax rules
+++++++++++++++++++++++++++++++++

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

algebraic_fraction
------------------

.. autofunction:: algebraic_fraction

monomial
--------

.. autofunction:: monomial

.. This functions are still in developement
    gcd
    ---
    
    .. autofunction:: gcd
    
    gcd_p
    -----
    
    .. autofunction:: gcd_p
    
    lcm
    ---
    
    .. autofunction:: lcm
    
    lcm_p
    -----
    
    .. autofunction:: lcm_p

make_polynomial
---------------

.. autofunction:: make_polynomial

are_similar
-----------

.. autofunction:: are_similar

parse_polynomial
----------------

.. autofunction:: parse_polynomial

random_poly
-----------

.. autofunction:: random_poly

root
----

.. autofunction:: root


.. rubric:: Footnotes

.. [#f1] See `wikipedia <http://en.wikipedia.org/wiki/Bisection_method>`_