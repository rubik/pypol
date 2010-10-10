.. module:: pypol.funcs
    :synopsis: Utility functions to work with polynomials
.. moduleauthor:: Michele Lacchia <michelelacchia@gmail.com>
.. sectionauthor:: Michele Lacchia <michelelacchia@gmail.com>

.. |p3| image:: images/x2.gif
.. |p4| image:: images/poly1.gif
.. |p5| image:: images/indefinite_int.gif
    :alt: Indefinite integral
.. |p6| image:: images/-x.gif
.. |p7| image:: images/poly2.gif
.. |p8| image:: images/definite_int.gif
    :alt: Definite integral


The :mod:`funcs` module 
========================

.. versionadded:: 0.3

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
    * :func:`polyint_`

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

polyint\_
+++++++++

.. autofunction:: polyint_

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