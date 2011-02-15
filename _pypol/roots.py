#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials and algebraic fractions.

Author: Michele Lacchia <michelelacchia@gmail.com>
Copyright: 2010-2011 Michele Lacchia
License: GNU GPL

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
- Python 2.6 (or 2.7)

This module implements some root-finding algorithms, like the Newton's methods, or the Durand-Kerner method

Copyright (C) 2010-2011 Michele Lacchia
'''

from __future__ import division

import math
import cmath
import decimal
import operator
from pypol import poly1d, monomial, Polynomial
from funcs import polyder, divided_diff

def ruffini(poly):
    '''
    Returns the real integer roots (if there are any) of the polynomial basing on the right-hand side. If the polynomial has not the right-hand side, returns an empty list.

    **Examples**

    ::

        >>> p = poly1d([1, 5, 5, -5, -6])
        >>> p
        + x^4 + 5x^3 + 5x^2 - 5x - 6
        >>> ruffini(p)
        [-1, 1]
        >>> p(-1), p(1)
        (0, 0)

    and we can go on::

        >>> p2, p3 = p / (x - 1), p / (x + 1)
        >>> p2, p3
        (+ x^3 + 6x^2 + 11x + 6, + x^3 + 4x^2 + x - 6)
        >>> ruffini(p2), ruffini(p3)
        ([-1, -2, -3], [1])
        >>> p2(-1), p2(-2), p2(-3)
        (0, 0, 0)
        >>> p3(1)
        0
        >>> p4, p5, p6 = p2 / (x - 1), p2 / (x - 2), p / (x - 3)
        >>> p4, p5, p6
        (+ x^2 + 7x + 18, + x^2 + 8x + 27, + x^3 + 8x^2 + 29x + 82)
        >>> ruffini(p4), ruffini(p5), ruffini(p6)
        ([], [], [])

    there are no more real roots, but if we try :func:`quadratic`::

        >>> quadratic(p4), quadratic(p5)
        (((-3.5+2.3979157616563596j), (-3.5-2.3979157616563596j)), ((-4+3.3166247903553998j), (-4-3.3166247903553998j)))

    .. versionadded:: 0.3
    '''

    def _divs(n):
        d = [1] + [x for x in xrange(2, n // 2 + 1)] + [n]
        return map(operator.neg, d) + d

    p = poly.right_hand_side
    if not p:
        return []
    return [x for x in _divs(p) if not poly(x)]

def quadratic(poly):
    '''
    Finds the two roots of the polynomial *poly* solving the quadratic equation: :math:`ax^2 + bx + c = 0`

    with the formula:
        :math:`\\frac{-b\pm \sqrt{b^2 - 4ac}}{2a}`

    :raises: :exc:`AssertionError` if the polynomial's degree is not 2.
    :rtype: 2 numbers (integer, float or complex) in a tuple

    **Examples**

    ::

        >>> p = poly1d([1, 0, -4])
        >>> p
        + x^2 - 4
        >>> quadratic(p)
        (2.0, -2.0)
        >>> p(2)
        0
        >>> p(-2)
        0
        >>> p = poly1d([2, 3, 1])
        >>> p
        + 2x^2 + 3x + 1
        >>> quadratic(p)
        (-0.5, -1.0)
        >>> p(-0.5)
        0.0
        >>> p(-1.0)
        0.0

    this functions can return complex numbers too::

        >>> p = poly1d([-4, 5, -3])
        >>> p
        - 4x^2 + 5x - 3
        >>> quadratic(p)
        ((0.625-0.59947894041408989j), (0.625+0.59947894041408989j))

    but the precision is lower::

        >>> p = poly1d([-4, 5, -3])
        >>> p
        - 4x^2 + 5x - 3
        >>> quadratic(p)
        ((0.625-0.59947894041408989j), (0.625+0.59947894041408989j))
        >>> r1 = (0.625-0.59947894041408989j)
        >>> p(r1)
        (-4.4408920985006262e-16+0j)
        >>> r2 = (0.625+0.59947894041408989j)
        >>> p(r2)
        (-4.4408920985006262e-16+0j)

    .. versionadded:: 0.3
    '''

    poly = poly.filter()
    assert poly.degree == 2, 'The polynomial\'s degree must be 2'
    if len(poly.coefficients) == 3:
        a, b, c = poly.coefficients
    else:
        a, b, c = map(getattr(poly, 'get'), [2, 1, 0])
    r = b ** 2 - 4*a*c
    if r < 0:
        r = complex(imag=(-r) ** 0.5)
    else:
        r = r ** 0.5
    return ((-b + r) / (2*a), (-b - r) / (2*a))

def cubic(poly):
    '''
    Finds the three roots of the polynomial *poly* solving the equation: :math:`ax^3 + bx^2 + cx + d = 0`.

    :raises: :exc:`AssertionError` if the polynomial's degree is not 3.
    :rtype: 3 numbers (integer, float or complex) in a tuple

    **Examples**

    ::

        >>> k = poly1d([3, -2, 45, -1])
        >>> k
        + 3x^3 - 2x^2 + 45x - 1
        >>> cubic(k)
        (0.022243478406449024, (0.3222115941301088+3.8576995055778323j), (0.3222115941301088-3.8576995055778323j))
        >>> k = poly1d([-9, 12, -2, -34])
        >>> k
        - 9x^3 + 12x^2 - 2x - 34
        >>> cubic(k)
        (-1.182116114781928, (1.2577247240576306+1.2703952413531459j), (1.2577247240576306-1.2703952413531459j))
        >>> k = poly1d([1, 1, 1, 1])
        >>> cubic(k)
        (-1.0, (5.551115123125783e-17+0.9999999999999999j), (5.551115123125783e-17-0.9999999999999999j))
        >>> k(-1.)
        0.0
        >>> k = poly1d([-1, 1, 0, 1])
        >>> cubic(k)
        (1.4655712318767669, (-0.23278561593838348+0.7925519925154489j), (-0.23278561593838348-0.7925519925154489j))
        >>> k(cubic(k)[0])
        3.9968028886505635e-15

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Cubic_function>`_ | `MathWorld <http://mathworld.wolfram.com/CubicFormula.html>`_ | `1728 <http://www.1728.com/cubic.htm>`_
    '''

    poly = poly.filter()
    assert poly.degree == 3, 'The polynomial\'s degree must be 3'
    if len(poly.coefficients) == 4:
        a, b, c, d = poly.coefficients
    else:
        a, b, c, d = map(getattr(poly, 'get'), [3, 2, 1, 0])

    if a == 0:
        poly = poly1d([a, b, c, d])
        return quadratic(poly)
    f = ((3*c / a) - (b**2 / a**2)) / 3
    g = ((2*b**3 / a**3) - (9*b*c / a**2) + (27*d / a)) / 27
    h = (g**2 / 4) + (f**3 / 27)
    if h > 0: # only 1 root is real
        b_3a = - (b / (3*a))
        r = -(g / 2) + math.sqrt(h)
        if r < 0:
            s = -((-r) ** (1/3))
        else:
            s = r ** (1/3)
        t = -(g / 2) - math.sqrt(h)
        if t < 0:
            u = - ((-t) ** (1/3))
        else:
            u = t ** (1/3)

        x1 = (s + u) + b_3a
        x2 = complex(-(s + u) / 2 + b_3a, (s - u) * math.sqrt(3) / 2)
        x3 = complex(-(s + u) / 2 + b_3a, -(s - u) * math.sqrt(3) / 2)

        if poly(x1) and not poly(round(x1)):
            x1 = round(x1)
        return x1, x2, x3

    if f == g == h == 0: # all 3 roots are real and equal
        d_a = d / a
        if d_a < 0:
            x1 = x2 = x3 = (-d_a) ** (1/3)
        else:
            x1 = x2 = x3 = -((d / a) ** (1/3))

        x1 = x1*1e14; x1 = round(x1); x1 = (x1/1e14)
        x2 = x2*1e14; x2 = round(x2); x2 = (x2/1e14)
        x3 = x3*1e14; x3 = round(x3); x3 = (x3/1e14)

        return x1, x2, x3

    if h <= 0: # all 3 roots are real
        i = math.sqrt((g**2 / 4) - h)
        j_ = i ** (1 / 3)
        k = math.acos(-(g / (2*i)))
        l = -j_
        m = math.cos(k / 3)
        n = math.sqrt(3) * math.sin(k / 3)
        p = -(b / (3*a))
        x1 = 2*j_ * math.cos(k / 3) + p
        x2 = l * (m + n) + p
        x3 = l * (m - n) + p

        x1 = x1*1e14; x1 = round(x1); x1 = (x1/1e14)
        x2 = x2*1e14; x2 = round(x2); x2 = (x2/1e14)
        x3 = x3*1e14; x3 = round(x3); x3 = (x3/1e14)

        if poly(x1) and not poly(round(x1)):
            x1 = round(x1)
        if poly(x2) and not poly(round(x2)):
            x2 = round(x2)
        if poly(x3) and not poly(round(x3)):
            x3 = round(x3)
        return x1, x2, x3

def quartic(poly):
    '''
    Finds all four roots of a fourth-degree polynomial *poly*::

    :raises: :exc:`AssertionError` if the polynomial's degree is not 4
    :rtype: 4 numbers (integer, float or complex) in a tuple

    **Examples**

    When all the roots are real::

        >>> from pypol.roots import *
        >>> from pypol.funcs import from_roots
        >>> p = from_roots([1, -4, 2, 3])
        >>> p
        + x^4 - 2x^3 - 13x^2 + 38x - 24
        >>> quartic(p)
        [1, 3.0, -4.0, 2.0]
        >>> map(p, quartic(p))
        [0, 0.0, 0.0, 0.0]
        >>> p = from_roots([-1, 42, 2, -19239])
        >>> p
        + x^4 + 19196x^3 - 827237x^2 + 769644x + 1616076
        >>> quartic(p)
        [-1, 42.0, -19239.0, 2.0]
        >>> map(p, quartic(p))
        [0, 0.0, 3.0, 0.0]

    Otherwise, if there are complex roots it loses precision and this is due to floating point numbers::

        >>> from pypol import *
        >>> from pypol.roots import *
        >>> 
        >>> p = poly1d([1, -3, 4, 2, 1])
        >>> p
        + x^4 - 3x^3 + 4x^2 + 2x + 1
        >>> quartic(p)
        ((1.7399843312651568+1.5686034407060976j), (1.7399843312651568-1.5686034407060976j), (-0.23998433126515695+0.35301727734776445j), (-0.23998433126515695-0.35301727734776445j))
        >>> map(p, quartic(p))
        [(8.8817841970012523e-16+8.4376949871511897e-15j), (8.8817841970012523e-16-8.4376949871511897e-15j), (8.3266726846886741e-15-2.7755575615628914e-15j), (8.3266726846886741e-15+2.7755575615628914e-15j)]
        >>> p = poly1d([4, -3, 4, 2, 1])
        >>> p
        + 4x^4 - 3x^3 + 4x^2 + 2x + 1
        >>> quartic(p)
        ((0.62277368382725595+1.0277469284099872j), (0.62277368382725595-1.0277469284099872j), (-0.24777368382725601+0.33425306402324328j), (-0.24777368382725601-0.33425306402324328j))
        >>> map(p, quartic(p))
        [(-2.5313084961453569e-14+3.730349362740526e-14j), (-2.5313084961453569e-14-3.730349362740526e-14j), (1.354472090042691e-14-1.2101430968414206e-14j), (1.354472090042691e-14+1.2101430968414206e-14j)]

    **References**

    `MathWorld <http://mathworld.wolfram.com/QuarticEquation.html>`_
    '''

    assert poly.degree == 4, 'The polynomial\'s degree must be 4'
    if len(poly.coefficients) == 5:
        a, b, c, d, e = poly.coefficients
    else:
        a, b, c, d, e = map(getattr(poly, 'get'), [4, 3, 2, 1, 0])

    poly = poly1d([a, b, c, d, e])
    if not poly(1):
        roots = [1]
        roots.extend(cubic(poly / 'x - 1'))
        return roots
    if not poly(-1):
        roots = [-1]
        roots.extend(cubic(poly / 'x + 1'))
        return roots
    #if b == d == 0: # biquadratic ## DECOMMENT THIS?
    #    l = poly.letters[0]
    #    for m in poly.monomials:
    #        m[1][l] = m[1][l] / 2
    #    print poly
    #    poly_ = poly(x=monomial(z=1))
    #    return quadratic(poly_)
    if (a, b) == (0, 0):
        return quadratic(Polynomial(poly[2:]))
    if a == 0:
        return cubic(Polynomial(poly[1:]))

    poly = poly.div_all(a, int=True)
    if len(poly.coefficients) == 5:
        a, b, c, d, e = map(float, poly.coefficients)
    else:
        a, b, c, d, e = map(float, map(getattr(poly, 'get'), [4, 3, 2, 1, 0]))

    f = c - 3*b**2 / 8
    g = d + b**3 / 8 - b*c / 2
    h = e - 3*b**4 / 256 + b**2 * c / 16 - b*d / 4
    y = monomial(y=1)
    eq = y**3 + (f / 2) * y**2 + ((f**2 - 4*h)/16)*y - g**2 / 64
    y1, y2, y3 = cubic(eq)
    roots = [cmath.sqrt(r) for r in (y1, y2, y3) if isinstance(r, complex)]
    if len(roots) >= 2:
        p, q = roots[:2]
    else:
        try:
            p, q = map(math.sqrt, [r for r in (y1, y2, y3) if r][:2])
        except ValueError:
            p, q = map(cmath.sqrt, [r for r in (y1, y2, y3) if r][:2])
    r = -g / (8*p*q)
    s = b / (4*a)
    x1 = p + q + r - s
    x2 = p - q - r - s
    x3 = - p + q - r - s
    x4 = - p - q + r - s
    return x1, x2, x3, x4

def newton(poly, start, epsilon=float('-inf')):
    '''
    Finds one root of the polynomial *poly*, with this iteration formula:
        :math:`x_{n + 1} = x_n - \\frac{f(x_n)}{f'(x_n)}`

    :param start: the start value for evaluate ``poly(x)``.
    :param epsilon: the precision of the calculus (default to ``float('-inf')``).
    :type start: integer, float or complex
    :type epsilon: integer or float
    :rtype: integer of float

    **Examples**

    ::

        >>> k = poly1d([2, 5, 3])
        >>> k
        + 2x^2 + 5x + 3

    the roots of this polynomial are ``-1`` and ``-1.5``.
    We start with 10::

        >>> newton(k, 10)
        -1.0000000000000002

    so we try ``-1``::

        >>> newton(k, -1)
        -1
        >>> k(-1)
        0

    We have one root! We continue::

        >>> newton(k, -2)
        -1.5
        >>> k(-1.5)
        0.0

    This function can find complex roots too (if *start* is a complex number)::

        >>> k = poly1d([1, -3, 6])
        >>> k
        + x^2 - 3x + 6
        >>> roots.quadratic(k)
        ((1.5+1.9364916731037085j), (1.5-1.9364916731037085j))
        >>> roots.newton(k, complex(100, 1))
        (1.5+1.9364916731037085j)
        >>> roots.newton(k, complex(100, -1))
        (1.5-1.9364916731037085j)

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Halley's_method>`_ |
    `MathWorld <http://mathworld.wolfram.com/HalleysMethod.html>`_

    .. versionadded:: 0.3
    '''

    poly_d = polyder(poly)

    while True:
        p_s = poly(start)
        if not p_s:
            break
        x_n = start - p_s / poly_d(start)
        if start == x_n or abs(start - x_n) < epsilon:
            break
        start = x_n

    return start

def halley(poly, start, epsilon=float('-inf')):
    '''
    Finds one root of the polynomial *poly* using the Halley's method, with this iteration formula:
        :math:`x_{n + 1} = x_n - \\frac{2f(x_n)f'(x_n)}{2[f'(x_n)]^2 - f(x_n)f''(x_n)}`

    :param start: the start value to evaluate ``poly(x)``
    :param epsilon: the precision, default to ``float('-inf')``
    :type start: integer, float or complex
    :type epsilon: integer or float
    :rtype: integer or float

    **Examples**

    We want to find the roots of the polynomial: ``x^3 - 4x^2 - x - 4``::

        >>> p = (x + 1) * (x - 1) * (x + 4) ## its roots are: -1, 1, -4
        >>> p
        + x^3 + 4x^2 - x - 4

    starting from an high number::

        >>> halley(p, 90)
        1.0
        >>> p(1.)
        0.0

    then we get lower::

        >>> halley(p, -1)
        -1.0
        >>> p(-1.)
        0.0

    and lower::

        >>> halley(p, -90)
        -4.0
        >>> p(-4.)
        0.0

    so we can say that the roots are: ``1``, ``-1``, and ``-4``.

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Halley's_method>`_ |
    `MathWorld <http://mathworld.wolfram.com/HalleysMethod.html>`_

    .. versionadded:: 0.4
    '''

    p_d, p_d_ = polyder(poly), polyder(poly, 2)
    while True:
        x_n = start - (2 * poly(start) * p_d(start))/(2 * p_d(start) ** 2 - poly(start) * p_d_(start))
        if x_n == start or abs(x_n - start) < epsilon:
            return x_n
        start = x_n

def householder(poly, start, epsilon=float('-inf')):
    '''
    Finds one root of the polynomial *poly* using the Householder's method, with this iteration formula:
        :math:`x_{n + 1} = x_n - \\frac{f(x_n)}{f'(x_n)} \\Big\{ 1 + \\frac{f(x_n)f''(x_n)}{2[f'(x_n)]^2} \\Big\}`

    :param start: the start value to evaluate ``poly(x)``
    :param epsilon: the precision, default to ``float('-inf')``
    :type start: integer, float or complex
    :type epsilon: integer or float
    :rtype: integer or float

    **Examples**

    Let's find the roots of the polynomial ``x^4 + x^3 - 5x^2 + 3x``::

        >>> p = (x + 3) * (x - 1) ** 2 * x
        >>> p
        + x^4 + x^3 - 5x^2 + 3x
        >>> householder(p, 100)
        1.0000000139750058
        >>> householder(p, 2)
        1.0000000140746257
        >>> r = householder(p, 2)
        >>> p(r)
        0.0
        >>> householder(p, -100)
        -3.0
        >>> r = householder(p, -100)
        >>> p(r)
        0.0

    if the precision is lower, the result will be worse::

        >>> householder(p, 100, 0.1)
        1.0623451865071678
        >>> householder(p, 100, 0.00001)
        1.0000036436860307
        >>> householder(p, 100, 0.00000001)
        1.0000000049370159
        >>> householder(p, -100, 0.1)
        -3.0000022501789867
        >>> householder(p, -100, 0.001)
        -3.0

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Householder's_method>`_ |
    `MathWorld <http://mathworld.wolfram.com/HouseholdersMethod.html>`_

    .. versionadded:: 0.4
    '''

    p_d, p_d_ = polyder(poly), polyder(poly, 2)
    while True:
        x_n = start - (poly(start)/p_d(start))*(1 + (poly(start) * p_d_(start)) / (2 * p_d(start) ** 2))
        if x_n == start or abs(x_n - start) < epsilon:
            return x_n
        start = x_n

def schroeder(poly, start, epsilon=float('-inf')):
    '''
    Finds one root of the polynomial *poly* using the Schröder's method, with the iteration formula:
        :math:`x_{n + 1} = x_n - \\frac{f(x_n)f'(x_n)}{[f'(x_n)]^2 - f(x_n)f''(x_n)}`

    :param start: the start value to evaluate ``poly(x)``
    :param epsilon: the precision, default to ``float('-inf')``
    :type start: integer, float or complex
    :type epsilon: integer or float
    :rtype: integer or float

    **Examples**

    ::

        >>> k = poly1d([3, -4, -1, 4])
        >>> k
        + 3x^3 - 4x^2 - x + 4
        >>> schroeder(k, 100)
        -0.859475828371609
        >>> k(schroeder(k, 100))
        0.0
        >>> schroeder(k, 100j)
        (1.0964045808524712-0.5909569632973221j)
        >>> k(schroeder(k, 100))
        -1.1102230246251565e-16j
        >>> schroeder(k, -100j)
        (1.0964045808524712+0.5909569632973221j)
        >>> k(schroeder(k, 100))
        1.1102230246251565e-16j
    '''

    p_d, p_d_ = polyder(poly), polyder(poly, 2)
    while True:
        ps, pd = poly(start), p_d(start)
        x_n = start - (ps * pd) / (pd ** 2 - ps * p_d_(start))
        if x_n == start or abs(x_n - start) < epsilon:
            return x_n
        start = x_n

def laguerre(poly, start, epsilon=float('-inf')):
    '''
    Finds one root of the polynomial *poly* using the Laguerre's method, with the iteration formula:
        :math:`x_{k + 1} = x_k - \\frac{n}{max[G \pm \sqrt{(n - 1)(nH - G^2)}]}`

    where:

    :math:`G = \\frac{p'(x_k)}{p(x_k)}`

    :math:`H = G^2 - \\frac{p''(x_k)}{p(x_k)}`

    :param start: the start value to evaluate ``poly(x)``
    :param epsilon: the precision, default to ``float('-inf')``
    :type start: integer, float or complex
    :type epsilon: integer or float
    :rtype: complex

    **Examples**

    ::

        >>> k = poly1d([32, -123, 43, 2])
        >>> k
        + 32x^3 - 123x^2 + 43x + 2
        >>> laguerre(k, 100)
        (3.448875873899064+0j)
        >>> k(laguerre(k, 100))
        (2.5579538487363607e-13+0j)
        >>> laguerre(k, 1)
        (0.43639990661090833+0j)
        >>> k(laguerre(k, 1))
        0j
        >>> laguerre(k, -100)
        (-0.041525780509971674+0j)
        >>> k(laguerre(k, -100))
        0j
    '''

    p_d, p_d_, n = polyder(poly), polyder(poly, 2), poly.degree
    start = complex(start)
    while True:
        px = poly(start)
        if not px:
            return start
        g = p_d(start) / px
        h = g ** 2 - p_d_(start) / px
        dp = cmath.sqrt((n - 1) * (n * h - g**2))
        d1 = g + dp
        d2 = g - dp
        if abs(d2) > abs(d1):
            d = d2
        else:
            d = d1
        a = n / d
        x_n = start - a
        if str(start) == str(x_n) or abs(start - x_n) < epsilon:
            return start
        start = x_n

def muller(poly, x_k, x_k2=None, x_k3=None, epsilon=float('-inf')):
    '''
    Finds the real roots of the polynomial *poly* starting from *x_k*.

    :param x_k2: an optional starting value
    :type x_k2: number (integer or float)
    :param x_k3: another optional starting value
    :type x_k3: number (integer or float)
    :param float epsilon: the precision. Default to `float('-inf')`, which means it will be as accurate as possible
    :rtype: number

    **Examples**

    ::

        >>> a = x.from_roots([1, -23, 2424, -2])
        >>> a
        + x^4 - 2400x^3 - 58155x^2 - 50950x + 111504
        >>> muller(a, 100)
        -2.0
        >>> muller(a, -1000)
        2424.0

    Muller's method is the most suitable for a function that finds all the roots of a polynomial::

        >>> def find_roots(poly):
            r = []
            for _ in xrange(poly.degree):
                next_root = muller(poly, 100)
                r.append(next_root)
                poly /= (x - next_root)
            return r
        
        >>> find_roots(a)
        [-2.0, -23.0, 2424.0, 1.0]
        >>> roots.quartic(a)
        [1, 2424.0, -23.0, -2.0]
        >>> a = x.from_roots([1, -1, 2323, -229, 24])
        >>> a
        + x^5 - 2118x^4 - 481712x^3 + 12769326x^2 + 481711x - 12767208
        >>> find_roots(a)
        [1.0, -1.0, -229.0, 2323.0, 24.0]

    With this function you can find the roots of polynomials of higher degrees::

        >>> a = x.from_roots([1, -1, 2323, -229, 24, -22])
        >>> a
        + x^6 - 2096x^5 - 528308x^4 + 2171662x^3 + 281406883x^2 - 2169566x - 280878576
        >>> find_roots(a)
        [-22.0, 1.0, -1.0, -229.0, 2323.0, 24.0]

    .. versionadded:: 0.5
    '''

    s = (-1 if x_k < 0 else 1)
    if not x_k2:
        x_k2 = x_k + s * .25
    if not x_k3:
        x_k3 = x_k2 + s * .25

    x = monomial(x=1)
    while True:
        w = divided_diff(poly, [x_k, x_k2]) + divided_diff(poly, [x_k, x_k3]) - divided_diff(poly, [x_k2, x_k3])
        y = poly(x_k) - w * (x - x_k) + divided_diff(poly, [x_k, x_k2, x_k3]) * (x - x_k) ** 2
        n = 2 * poly(x_k)
        k = w ** 2 - 4 * poly(x_k) * divided_diff(poly, [x_k, x_k2, x_k3])
        if k < 0:
            d_part = -math.sqrt(-k)
        else:
            d_part = math.sqrt(k)
        d = max(w + d_part, w - d_part)
        x_k1 = x_k - n / d
        if x_k1 == x_k or abs(x_k1 - x_k) < epsilon:
            return x_k1
        x_k, x_k2, x_k3 = x_k1, x_k, x_k2


def ridder(poly, x0, x1, epsilon=1e-9):
    '''
    Finds the roots  of the polynomial *poly*. Requires two starting points: *x0* and *x1*.

    :param epsilon: the precision. Default to `1e-9`. The smaller *epsilon* is, the more accurate the calculus.
    :raises: :exc:`ValueError` is the root is not bracketed in the interval :math:`[x0, x1]`
    :rtype: number (integer or float)

    **Examples**

    ::

        >>> a = x.from_roots([1, -232, 42])
        >>> ridder(a, 100, -1)
        Traceback (most recent call last):
          File "<pyshell#49>", line 1, in <module>
            ridder(a, 100, -1)
          File "roots.py", line 691, in ridder
            r = []
        ValueError: root is not bracketed

    We have to choose the two starting values so that the root is bracketed::

        >>> ridder(a, 100, 1)
        1
        >>> a /= (x - 1)
        >>> a
        + x^2 + 190x - 9744
        >>> ridder(a, 100, 1)
        41.99999999999998
        >>> ridder(a, 42, 1)
        42
        >>> a /= (x - 42)
        >>> a
        + x + 232
        >>> ridder(a, 100, -1000)
        -232.0

    .. versionadded:: 0.5
    '''

    p0, p1 = poly(x0), poly(x1)
    if p0 * p1 > 0: raise ValueError('root is not bracketed')
    if p0 == 0: return x0
    if p1 == 0: return x1

    l = 0
    while True:
        ## Compute the closer root
        x2 = 0.5 * (x0 + x1)
        p2 = poly(x2)
        s = math.sqrt(p2 ** 2 - p0 * p1)
        if s == 0: raise ValueError('cannot find the real root')
        dx = (x2 - x0) * p2 / s
        if p0 - p1 < 0: dx *= -1
        x_k = x2 + dx
        pk = poly(x_k)
        # Test for convergence
        if l > 0:
            if abs(x_k - oldx) < epsilon * max(abs(x_k), 1):
                return x_k
        oldx = x_k
        if p2 * pk > 0:
            if p0 * pk < 0:
                x1, p1 = x_k, pk
            else:
                x0, p0 = x_k, pk
        else:
            x0, x1, p0, p1 = x2, x_k, p2, pk
        l += 1

def durand_kerner(poly, start=complex(.4, .9), epsilon=1.12e-16):
    '''
    The Durand-Kerner method. It finds all the roots of the polynomials *poly* simultaneously.
    With some polynomials it works quite well::

        >>> from pypol.funcs import from_roots
        >>> p = from_roots([1, -3, 14, 5, -100])
        >>> p
        + x^5 + 83x^4 - 1671x^3 + 3097x^2 + 19490x - 21000
        >>> durand_kerner(p)
        ((1+0j), (5+0j), (-100+0j), (-3+0j), (13.999999999999998+0j))
        >>> map(p, durand_kerner(p))
        [0j, 0j, 0j, 0j, (-7.5669959187507629e-10+0j)]
        >>> p = from_roots([1, -3, 14, 5, -10, 4242])
        >>> p
        + x^6 - 4249x^5 + 29553x^4 + 598609x^3 - 2064094x^2 - 7468020x + 8908200
        >>> durand_kerner(p)
        ((1+0j), (-3+0j), (-10+0j), (5+0j), (4242-1.2727475858741762e-49j), (14+0j))
        >>> map(p, durand_kerner(p))
        [0j, 0j, 0j, 0j, (60112-1.7453195261352414e-31j), 0j]
        >>> p = poly1d([1, 2, -3, 1, -4])
        >>> durand_kerner(p)
        ((1.3407787867177585-9.656744866722633e-34j), (-0.084897978584602823-0.96623889223617843j), (-3.1709828295485529+8.2085042293591779e-34j), (-0.084897978584602823+0.96623889223617843j))
        >>> map(p, durand_kerner(p))
        [(-8.8817841970012523e-16-1.2923293554560813e-32j), (-4.4408920985006262e-16-2.2204460492503131e-16j), (3.5527136788005009e-15-3.8729295219100667e-32j), (-4.4408920985006262e-16+2.2204460492503131e-16j)]
        >>> durand_kerner(p)
        ((1+0j), (-2424+6.2230152778611417e-61j), (14+1.2446030555722283e-60j), (381.99999999999994+4.6672614583958563e-61j), (133-7.0008921875937844e-61j), (5-2.4892061111444567e-60j), (-100+3.3735033418337674e-80j), (-3+4.9784122222889134e-60j))
        >>> map(p, durand_kerner(p))
        [0j, (116436291584-3.6076395061767809e-37j), 3.0129989385594897e-47j, (-110296.125+3.1986819282098692e-42j), (212+2.8399399457319209e-44j), 8.8231056584250621e-48j, 1.032541429306196e-63j, -3.3300895740082056e-47j]

    But with other polynomials it could raise an :exc:`OverflowError`::

        >>> p = poly1d([-1, 2, -3, 1, 4])
        >>> p
        - x^4 + 2x^3 - 3x^2 + x + 4
        >>> durand_kerner(p)
        Traceback (most recent call last):
          File "<pyshell#20>", line 1, in <module>
            durand_kerner(p)
          File "roots.py", line 641, in durand_kerner
            >>> map(p, durand_kerner(p))
          File "core.py", line 1429, in __call__
            return eval(self.eval_form, letters)
          File "<string>", line 1, in <module>
        OverflowError: complex exponentiation

    In this cases you can use other root-finding algorithms, like :func:`laguerre` or :func:`halley`::

        >>> laguerre(p, 10)
        (5.0000000000018261+0j)
        >>> laguerre(p, 5)
        (5+0j)
        >>> p((5+0j))
        0j
        >>> halley(p, 10)
        5.0
        >>> halley(p, 100)
        14.0
        >>> halley(p, 1000)
        382.0
        >>> halley(p, -1000)
        -100.0
        >>> halley(p, -100)
        -100.0
        >>> halley(p, -10)
        -3.0
    '''

    roots = []
    for e in xrange(poly.degree):
        roots.append(start ** e)
    while True:
        new = []
        for i, r in enumerate(roots):
            new_r = r - (poly(r)) / (reduce(operator.mul, [(r - r_1) for j, r_1 in enumerate(roots) if i != j]))
            new.append(new_r)
        if all(str(n) == str(roots[i]) or abs(n - roots[i]) < epsilon for i, n in enumerate(new)):
            return tuple(new)
        roots = new

def brent(poly, a, b, epsilon=float('-inf')):
    '''
    Finds a root of the polynomial *poly*, with the Brent's method.

    :param a,b: The limits of the interval, where the root is searched
    :param epsilon: The precision, default to float('-inf')
    :rtype: integer or float

    **Examples**

        >>> p = poly1d([1, -4, 3, -4])
        >>> p
        + x^3 - 4x^2 + 3x - 4
        >>> brent(p, 100, -100)
        3.4675038570565078
        >>> r = brent(p, 100, -100)
        >>> p(r)
        -1.1723955140041653e-13

    If we start closer::

        >>> r = brent(p, 10, -10)
        >>> p(r)
        -1.7763568394002505e-15

    the precision is greater.

    **References**

    Pseudocode from `Wikipedia <http://en.wikipedia.org/wiki/Brent's_method#Algorithm>`_

    .. warning:: Doesn't seem to work in some cases.
    '''

    pa, pb = poly(a), poly(b)
    assert pa * pb < 0, 'poly(a) and poly(b) must have opposite sign'
    if abs(pa) < abs(pb):
        a, b = b, a

    c = a
    flag = True
    d = 0
    while True:
        pa, pb, pc, s = poly(a), poly(b), poly(c), float(0)

        if pb == 0 or abs(b - a) < epsilon:
            break

        if pa != pc and pb != pc:
            s1 = ((a * pb * pc) / ((pa - pb) * (pa - pc)))
            s2 = ((b * pa * pc) / ((pb - pa) * (pb - pc)))
            s3 = ((c * pa * pb) / ((pc - pa) * (pc - pb)))
            s =  s1 + s2 + s3
        else:
            s = b - pb * ((b - a) / (pb - pa))

        if 0 in (pb, poly(s)) or abs(b - a) < epsilon:
            break

        _1 = (3 * a + b) / 4
        c_1_ = s >= b and s <= _1
        c_1_1 = s >= _1 and s <= b

        c_1 = c_1_ or c_1_1
        c_2 = flag and abs(s - b) >= abs(b - c) / 2
        c_3 = not flag and abs(s - b) >= (c - d) / 2

        if c_1 or c_2 or c_3:
            s = (a + b) / 2
            flag = True
        else:
            flag = False

        d, c = c, b
        ps = poly(s)
        
        if pa * ps < 0:
            b = s
        else:
            a = s

        if abs(pa) < abs(pb):
            a, b = b, a

    return b

def bisection(poly, k=0.5, epsilon=float('-inf')):
    '''
    Finds the root of the polynomial *poly* using the *bisection method*.
    When it finds the root, it checks if ``-root`` is one root too. If so, it returns a two-length tuple, else a tuple
    with one root.

    :param float k: the increment of the two extreme point. The increment is calculated with the formula ``a + ak``.

    So, if *a* is 50, after the increment ``50 + 50*0.5`` *a* will be 75.
    *epsilon* sets the precision of the calculation. Smaller it is, greater is the precision.

    :raises: :exc:`ValueError` if *epsilon* is bigger than 5 or *k* is negative
    :rtype: integer or float or NotImplemented when:

            * *poly* has more than one letter
            * or the root is a complex number

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bisection_method>`_

    .. warning::
        In some case this function may not work!

    .. versionadded:: 0.2
    .. versionchanged:: 0.3
    '''

    if k == 0:
        raise Warning('May not work with k = 0')

    if k < 0:
        raise ValueError('k value cannot be negative')

    if epsilon > 5:
        raise ValueError('epsilon cannot be greater than 5')

    assert len(poly.letters) == 1

    assert  not all(coeff > 0 for coeff in poly.coefficients) and \
            not all(exp & 1 == 0 for exp in poly.powers(poly.letters[0])), \
            'The root of the polynomial is a complex number'

    _d = lambda a, b: a * b < 0 # Check if discordant
    a, b, media = -90, 89, 0

    try:
        while True:
            nmedia = (a + b) / 2 # Midpoint
            if _d(poly(a), poly(nmedia)):
                b = nmedia
            elif _d(poly(b), poly(nmedia)):
                a = nmedia
            else: # Not discordant
                a, b = a + a*k, b + b*k
            if media == nmedia or abs(a - b) < epsilon:
                break
            media = nmedia
    except OverflowError:
        return NotImplemented

    return media

################################################################################
##                            Still in development                            ##
################################################################################

def lambert(poly, start, epsilon=float('-inf')):
    def _hg(n):
        return (((d - 1) * n ** d + (d + 1) * r) / ((d + 1) * n ** d + (d - 1) * r)) * n

    assert len(poly) == 2 and poly.right_hand_side, 'poly must be on the form x^d - r'

    d, r = poly[0][1].values()[0], -poly.right_hand_side
    while True:
        x_n = start - _hg(start)
        if x_n == start or abs(x_n - start) < epsilon:
            return x_n
        start = x_n