.. module:: pypol

The :mod:`pypol` package
=========================

.. include:: global.rst

.. contents:: Table of contents

Functions
---------

.. autosummary::

    pypol.poly1d
    pypol.poly1d_2
    pypol.polynomial
    pypol.algebraic_fraction
    pypol.monomial
    pypol.parse_polynomial
    pypol.gcd
    pypol.lcm

Classes
-------

.. autosummary::

    pypol.Polynomial
    pypol.AlgebraicFraction

The :mod:`~pypol.funcs` module
--------------------------------

Utility functions
+++++++++++++++++

.. autosummary::

    pypol.funcs.divisible
    pypol.funcs.from_roots
    pypol.funcs.random_poly
    pypol.funcs.polyder
    pypol.funcs.polyint
    pypol.funcs.polyint_

Numbers
+++++++

.. autosummary::

    pypol.funcs.bin_coeff

The :mod:`~pypol.roots` module
--------------------------------

Simple algorithms
+++++++++++++++++

.. autosummary::

    pypol.roots.ruffini
    pypol.roots.quadratic
    pypol.roots.cubic

Newton's method and derived
+++++++++++++++++++++++++++

.. autosummary::

    pypol.roots.newton
    pypol.roots.halley
    pypol.roots.householder
    pypol.roots.schroeder
    pypol.roots.laguerre

Other methods
+++++++++++++

.. autosummary::

    pypol.roots.durand_kerner
    pypol.roots.brent
    pypol.roots.bisection

The :mod:`~pypol.series` module
---------------------------------

This module implements some of the most common polynomial sequences.

Lucas polynomial sequences
++++++++++++++++++++++++++

.. autosummary::

    pypol.series.lucas_seq
    pypol.series.fibonacci
    pypol.series.lucas
    pypol.series.pell
    pypol.series.pell_lucas
    pypol.series.jacobsthal
    pypol.series.jacob_lucas
    pypol.series.fermat
    pypol.series.fermat_lucas
    pypol.series.chebyshev_t
    pypol.series.chebyshev_u

Bernoulli and Euler sequences
+++++++++++++++++++++++++++++

.. autosummary::

    pypol.series.bernoulli
    pypol.series.bern_num
    pypol.series.euler
    pypol.series.euler_num
    pypol.series.genocchi

Other series
++++++++++++

.. autosummary::

    pypol.series.hermite_prob
    pypol.series.hermite_phys
    pypol.series.abel
    pypol.series.gegenbauer
    pypol.series.laguerre
    pypol.series.laguerre_g