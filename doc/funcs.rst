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
.. |p11| image:: images/bin_coeff.gif
    :alt: Binomial coefficient
.. |p12| image:: images/x^k.gif
.. |p13| image:: images/binomial.gif
.. |p14| image:: images/(-1)^k.gif


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
    * :func:`from_roots`
    * :func:`random_poly`
    * :func:`polyder`
    * :func:`polyint`
    * :func:`polyint_`
    * :func:`bin_coeff`

divisible
+++++++++

.. autofunction:: divisible

from_roots
++++++++++

.. autofunction:: from_roots

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

bin_coeff
+++++++++

.. autofunction:: bin_coeff

Series
------

In this module there are these functions:

.. hlist::
    :columns: 3

    * :func:`fibonacci`
    * :func:`hermite_prob`
    * :func:`hermite_phys`
    * :func:`chebyshev_t`
    * :func:`chebyshev_u`
    * :func:`abel`
    * :func:`gegenbauer`
    * :func:`laguerre`
    * :func:`laguerre_g`
    * :func:`bernoulli`
    * :func:`bern_num`
    * :func:`euler`
    * :func:`euler_num`
    * :func:`genocchi`

fibonacci
+++++++++

.. autofunction:: fibonacci

hermite_prob
++++++++++++

.. autofunction:: hermite_prob

hermite_phys
++++++++++++

.. autofunction:: hermite_phys

chebyshev_t
+++++++++++

.. autofunction:: chebyshev_t

chebyshev_u
+++++++++++

.. autofunction:: chebyshev_u

abel
++++

.. autofunction:: abel

gegenbauer
++++++++++

.. autofunction:: gegenbauer

laguerre
++++++++

.. autofunction:: laguerre


laguerre_g
++++++++++

.. autofunction:: laguerre_g

bernoulli
+++++++++

.. autofunction:: bernoulli

bern_num
++++++++

.. autofunction:: bern_num

euler
+++++

.. autofunction:: euler

euler_num
+++++++++

.. autofunction:: euler_num

genocchi
++++++++

.. autofunction:: genocchi