.. module:: pypol.series
    :synopsis: Generator functions for common sequences

.. moduleauthor:: Michele Lacchia (michelelacchia@gmail.com)
.. sectionauthor:: Michele Lacchia (michelelacchia@gmail.com)

.. versionadded:: 0.4

.. include:: global.rst

The :mod:`~pypol.series` module
=================================

.. contents:: Table of contents

This module implements the most common polynomial sequences, like:

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
---------------------------

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
-----------------------------

.. autofunction:: bernoulli

.. autofunction:: bern_num

.. autofunction:: euler

.. autofunction:: euler_num

.. autofunction:: genocchi

Other series
------------

.. autofunction:: hermite_prob

.. autofunction:: hermite_phys

.. autofunction:: laguerre

.. autofunction:: laguerre_g

.. autofunction:: abel

.. autofunction:: gegenbauer

.. autofunction:: touchard