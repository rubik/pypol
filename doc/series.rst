.. module:: pypol.series
    :synopsis: Generator functions for common sequences

.. moduleauthor:: Michele Lacchia (michelelacchia@gmail.com)
.. sectionauthor:: Michele Lacchia (michelelacchia@gmail.com)

.. versionadded:: 0.4


The :mod:`~pypol.series` module
=================================

This module implements the most common polynomial sequences, like Fibonacci's sequence (:func:`fibonacci`)

Lucas polynomials sequences
---------------------------

.. autoclass:: LucasSeq

.. automethod:: LucasSeq.__call__

.. autoattribute:: LucasSeq.cache

.. automethod:: LucasSeq.reset_cache

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

.. autofunction:: bernstein