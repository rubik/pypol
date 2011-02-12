.. module:: pypol.roots
    :synopsis: A collection of some root-finding algorithms
    
.. moduleauthor:: Michele Lacchia (michelelacchia@gmail.com)
.. sectionauthor:: Michele Lacchia (michelelacchia@gmail.com)

The :mod:`~pypol.roots` module
==============================

.. versionadded:: 0.4

Here are some root-finding algorithm, such as :func:`ruffini`'s method, :func:`quadratic` formula, :func:`cubic` formula, :func:`newton`'s method, :func:`halley`'s method, :func:`householder`'s method, :func:`schroeder`'s method, :func:`brent`'s method, and :func:`bisection`.

Simple algorithms and formulas
++++++++++++++++++++++++++++++

.. autofunction:: ruffini

.. autofunction:: quadratic

.. autofunction:: cubic

.. autofunction:: quartic

Newton's method and derived
+++++++++++++++++++++++++++

.. autofunction:: newton

.. autofunction:: halley

.. autofunction:: householder

.. autofunction:: schroeder

.. autofunction:: laguerre

.. autofunction:: muller

.. autofunction:: ridder

Other methods
+++++++++++++

.. autofunction:: durand_kerner(poly, start=(0.4 + 0.9j), epsilon=1.12e-16)

.. autofunction:: brent

.. autofunction:: bisection