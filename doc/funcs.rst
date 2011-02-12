.. module:: pypol.funcs
    :synopsis: Utility functions to work with polynomials
.. moduleauthor:: Michele Lacchia <michelelacchia@gmail.com>
.. sectionauthor:: Michele Lacchia <michelelacchia@gmail.com>

The :mod:`~pypol.funcs` module 
==============================

.. versionadded:: 0.3

This module add some utility function to pypol.

.. note::

    In all these examples it will be assumed that all items in the ``pypol.funcs`` namespace have been imported::

        from pypol.funcs import *

Basic functions
---------------

The :mod:`pypol.funcs` module offers some basic functions for derivation, integration, interpolation and others.

.. autofunction:: divisible

.. autofunction:: from_roots

.. autofunction:: random_poly

.. autofunction:: polyder

.. autofunction:: polyint

.. autofunction:: polyint_

.. autofunction:: interpolate

.. autofunction:: divided_diff

Numbers
-------

Also, this module provides some functions to generate integer series, or numbers. Some of them are used in :mod:`pypol.series`: the :func:`stirling2` function is used in :func:`pypol.series.touchard` and :func:`pypol.series.bell`.

.. autofunction:: bin_coeff

.. autofunction:: harmonic

.. autofunction:: harmonic_g

.. autofunction:: stirling

.. autofunction:: stirling2

.. autofunction:: bell_num

.. autofunction:: entringer

.. autofunction:: lucas_num

.. autofunction:: pell_num

.. autofunction:: pell_lucas_num

.. autofunction:: jacobsthal_num

.. autofunction:: jacobsthal_lucas_num

.. autofunction:: fermat_num

.. autofunction:: fermat_lucas_num