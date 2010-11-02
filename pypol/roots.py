# -*- coding: utf-8 -*-

'''
This module implements some root-finding algorithms, like the Newton's methods, or the Durand-Kerner method
(C) Copyright 2010 Michele Lacchia
'''

from __future__ import division

import math
import cmath
import decimal
import operator
from pypol import poly1d, monomial, Polynomial
from funcs import polyder

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

def linear(poly):
    assert 0 not in (poly[0], poly[1]), 'b or c cannot be equal to 0'
    return -1 * poly[0] / poly[1]

def quadratic(poly):
    '''
    Finds the two roots of the polynomial *poly* solving the quadratic equation: |p1|

    with the formula:
        |p2|.

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
    Finds the three roots of the polynomial *poly* solving the equation: |p22|.

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

def __quartic(poly):
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
    #if b == d == 0: # biquadratic
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
        a, b, c, d, e = poly.coefficients
    else:
        a, b, c, d, e = map(getattr(poly, 'get'), [4, 3, 2, 1, 0])

    f = float(c - (3*b**2 / 8))
    g = float(d + (b**3/ 8) - (b*c / 2))
    h = e - (3*b**4 / 256) + (b**2 * c / 16) - (b*d / 4)
    y = monomial(y=1)
    eq = y**3 + (f / 2) * y**2 + ((f**2 - 4*h) / 16) * y - g**2 / 64
    y1, y2, y3 = cubic(eq)
    print eq, y1, y2, y3
    roots = [cmath.sqrt(r) for r in (y1, y2, y3) if isinstance(r, complex)]
    if len(roots) >= 2:
        p, q = roots[:2]
    else:
        p, q = map(math.sqrt, [r for r in (y1, y2, y3) if r][:2])
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
        |p8_5|

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

    poly_d = polyder(poly);print poly_d

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
        |p9|

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
        |p10|

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
        |p21|

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
        |p23|

    where:

    |p30|

    |p31|

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

def durand_kerner(poly, start=complex(.4, .9), epsilon=1.12e-16):
    '''
    The Durand-Kerner method. It finds all the roots of the polynomials *poly*
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
    .. warning::
        In some case this function may not work!

    Finds the root of the polynomial *poly* using the *bisection method*.
    When it finds the root, it checks if ``-root`` is one root too. If so, it returns a two-length tuple, else a tuple
    with one root.

    :param float k: the increment of the two extreme point. The increment is calculated with the formula ``a + ak``.

    So, if *a* is 50, after the increment ``50 + 50*0.5`` *a* will be 75.
    *epsilon* sets the precision of the calculation. Smaller it is, greater is the precision.

    .. warning:: If *epsilon* is bigger than 5 or *k* is negative, :exc:`ValueError` is raised.
    .. warning:: NotImplemented is returned if:

            * *poly* has more than one letter
            * or the root is a complex number

    **References**

    `Wikipedia <http://en.wikipedia.org/wiki/Bisection_method>`_

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

    d, r = poly[0][1].values()[0], poly.right_hand_side
    while True:
        x_n = start - _hg(start)
        if x_n == start or abs(x_n - start) < epsilon:
            return x_n
        start = x_n