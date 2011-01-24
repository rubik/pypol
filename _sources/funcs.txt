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

The :mod:`pypol.funcs` module offers these basic functions:

.. hlist::
    :columns: 2

    * :func:`divisible`
    * :func:`from_roots`
    * :func:`random_poly`
    * :func:`polyder`
    * :func:`polyint`
    * :func:`polyint_`
    * :func:`interpolate`
    * :func:`divided_diff`

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

.. autofunction:: bin_coeff

.. autofunction:: harmonic

.. autofunction:: harmonic_g

.. autofunction:: stirling

.. autofunction:: stirling_2

.. autofunction:: bell_num