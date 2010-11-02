.. module:: pypol.funcs
    :synopsis: Utility functions to work with polynomials
.. moduleauthor:: Michele Lacchia <michelelacchia@gmail.com>
.. sectionauthor:: Michele Lacchia <michelelacchia@gmail.com>

.. include:: global.rst

The :mod:`funcs` module 
========================

.. versionadded:: 0.3

.. contents:: Table of contents

This module add some utility function to pypol.

.. note::

    In all these examples it will be assumed that all items in the ``pypol.funcs`` namespace have been imported::

        from pypol.funcs import *

Basic functions
---------------

The :mod:`pypol.funcs` module offers these basic functions:

.. hlist::
    :columns: 2

    * :func:`divisible`
    * :func:`from_roots`
    * :func:`random_poly`
    * :func:`polyder`
    * :func:`polyint`
    * :func:`polyint_`
    * :func:`bin_coeff`


.. autofunction:: divisible

.. autofunction:: from_roots

.. autofunction:: random_poly

.. autofunction:: polyder

.. autofunction:: polyint

.. autofunction:: polyint_

.. autofunction:: bin_coeff

Series
------

In this module there are these functions:

.. hlist::
    :columns: 3

    * :func:`lucas_seq`
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

Lucas polynomials sequences
+++++++++++++++++++++++++++

.. autofunction:: lucas_seq(n, p, q, zero=Polynomial(), one=monomial(1))

.. autofunction:: fibonacci

.. autofunction:: lucas

.. autofunction:: pell

.. autofunction:: pell_lucas

.. autofunction:: jacobsthal

.. autofunction:: jacob_lucas

.. autofunction:: fermat

.. autofunction:: fermat_lucas

.. autofunction:: chebyshev_t

.. autofunction:: chebyshev_u

Bernoulli and Euler sequences
+++++++++++++++++++++++++++++

.. autofunction:: bernoulli

.. autofunction:: bern_num

.. autofunction:: euler

.. autofunction:: euler_num

.. autofunction:: genocchi

Other series
++++++++++++

.. autofunction:: hermite_prob

.. autofunction:: hermite_phys

.. autofunction:: laguerre

.. autofunction:: laguerre_g

.. autofunction:: abel

.. autofunction:: gegenbauer

.. autofunction:: touchard