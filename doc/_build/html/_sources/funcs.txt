.. module:: pypol.funcs
    :synopsis: Utility functions to work with polynomials

The :mod:`funcs` module 
========================

This module add some utility function to pypol.

Basic functions
---------------

The :mod:`funcs` offers these basic functions:

.. hlist::
    :columns: 2

    * :func:`divisible`
    * :func:`gcd`
    * :func:`lcm`
    * :func:`random_poly`
    * :func:`polyder`
    * :func:`polyint`

.. autofunction:: divisible

.. autofunction:: gcd

.. autofunction:: lcm

.. autofunction:: random_poly

.. autofunction:: polyder

.. autofunction:: polyint

Series
------

In this module there are these functions:

.. hlist::
    :columns: 3

    * :func:`fib_poly`
    * :func:`fib_poly_r`
    * :func:`hermite_prob`
    * :func:`hermite_prob_r`
    * :func:`hermite_phys`
    * :func:`hermite_phys_r`
    * :func:`chebyshev_t`
    * :func:`chebyshev_u`
    * :func:`abel`

.. autofunction:: fib_poly

.. autofunction:: fib_poly_r

.. autofunction:: hermite_prob

.. autofunction:: hermite_prob_r

.. autofunction:: hermite_phys

.. autofunction:: hermite_phys_r

.. autofunction:: chebyshev_t

.. autofunction:: chebyshev_u

.. autofunction:: abel


Root-finding
------------

At the moment these functions only are avaiable:

.. hlist::

    * :func:`quadratic`
    * :func:`bisection`

.. autofunction:: quadratic

.. autofunction:: bisection



.. rubric:: Footnotes

.. [#f1] See `wikipedia <http://en.wikipedia.org/wiki/Bisection_method>`_