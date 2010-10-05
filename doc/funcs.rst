.. module:: pypol.funcs
    :synopsis: Utility functions to work with polynomials
.. moduleauthor:: Michele Lacchia <michelelacchia@gmail.com>
.. versionadded:: 0.3
.. sectionauthor:: Michele Lacchia <michelelacchia@gmail.com>

The :mod:`funcs` module 
========================

This module add some utility function to pypol.

.. note::

    In all these examples it will be assumed that all items in the ``pypol.funcs`` namespace have been imported::

        from pypol.funcs import *

Basic functions
---------------

The :mod:`funcs` offers these basic functions:

.. hlist::
    :columns: 2

    * :func:`divisible`
    * :func:`random_poly`
    * :func:`polyder`
    * :func:`polyint`

divisible
+++++++++

.. autofunction:: divisible

random_poly
+++++++++++

.. autofunction:: random_poly

polyder
+++++++

.. autofunction:: polyder

polyint
+++++++

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
    * :func:`spread`
    * :func:`gegenbauer_r`
    * :func:`laguerre`

fib_poly
++++++++

.. autofunction:: fib_poly

fib_poly_r
++++++++++

.. autofunction:: fib_poly_r

hermite_prob
++++++++++++

.. autofunction:: hermite_prob

hermite_prob_r
++++++++++++++

.. autofunction:: hermite_prob_r

hermite_phys
++++++++++++

.. autofunction:: hermite_phys

hermite_phys_r
++++++++++++++

.. autofunction:: hermite_phys_r

chebyshev_t
+++++++++++

.. autofunction:: chebyshev_t

chebyshev_u
+++++++++++

.. autofunction:: chebyshev_u

abel
++++

.. autofunction:: abel

gegenbauer_r
++++++++++++

.. autofunction:: gegenbauer_r

laguerre
++++++++

.. autofunction:: laguerre


Root-finding
------------

At the moment these functions only are avaiable:

.. hlist::

    * :func:`quadratic`
    * :func:`newton`
    * :func:`ruffini`
    * :func:`bisection`

quadratic
+++++++++

.. autofunction:: quadratic

newton
++++++

.. autofunction:: newton

ruffini
+++++++

.. autofunction:: ruffini

bisection
+++++++++

.. autofunction:: bisection