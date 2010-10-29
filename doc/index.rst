.. pypol documentation master file, created by
   sphinx-quickstart on Thu Aug 26 17:23:17 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: pypol

Welcome to pypol v0.3 documentation!
====================================

:Author: Michele Lacchia (michelelacchia@gmail.com)
:Release: |release|
:Date: |today|

pypol is a Python library that allows you to manipulate polynomials. This is the main page of the documentation.

Installation
------------

pypol is on `PyPI <http://pypi.python.org/pypi/pypol_/0.3>`_ too. If you have setuptools installed, you can use **easy_install**::

    $ easy_install -U pypol_

and **don't forget the underscore!** Because if you try::

    $ easy_install pypol

**you will install a different package!**

.. seealso::
    :ref:`install`

Overview
--------

These are just some features of pypol::

    >>> from pypol import *
    >>> p1 = x**3 - 2*x**2 - 4
    >>> p1
    + x^3 - 2x^2 - 4
    >>> p1.degree
    3
    >>> p1.letters
    ('x',)
    >>> p1.coefficients
    [1, -2, -4]
    >>> p1.eval_form
    '1*x**3-2*x**2-4'
    >>> p1.right_hand_side
    -4
    >>> del p1[-1]
    >>> p1
    + x^3 - 2x^2
    >>> p1.right_hand_side
    False
    >>> p1.append(-4)
    >>> p1
    + x^3 - 2x^2 - 4
    >>> p1.to_plist()
    [[1, 3], [-2, 2], [-4, 0]]
    >>> p2 = poly1d([2, -4, 3, -1])
    >>> p2
    + 2x^3 - 4x^2 + 3x - 1
    >>> p2 / p1
    + 2
    >>> divmod(p2, p1)
    (+ 2, + 3x + 7)
    >>> q, r = divmod(p2, p1)
    >>> q * p1 + r
    + 2x^3 - 4x^2 + 3x - 1
    >>> q * p1 + r == p2
    True
    >>> roots ## pypol.roots
    <module 'pypol.roots' from '/pypol/roots.py'>
    >>> del p1[0]
    >>> p1
    - 2x^2 - 4
    >>> roots.quadratic(p1)
    (-1.4142135623730951j, 1.4142135623730951j)
    >>> r1, r2 = roots.quadratic(p1)
    >>> p1(r1)
    (8.8817841970012523e-16-0j)
    >>> p1(r2)
    (8.8817841970012523e-16+0j)
    >>> p1(-1)
    -6
    >>> p1(3)
    -22

Contents
--------

.. toctree::
   :maxdepth: 3
   :numbered:
   
   tutorial.rst
   classes.rst
   functions.rst
   operations.rst
   funcs.rst
   roots.rst
   contacts.rst
   changelog.rst
