.. currentmodule:: pypol

.. _operations:

Operators
#########

Basic operators
===============

Actually, :mod:`pypol` supports all five basic polynomial operations:

.. hlist::
    :columns: 2

    * :ref:`add`
    * :ref:`sub`
    * :ref:`mul`
    * :ref:`div`
    * :ref:`pow`
    * :ref:`mod`

.. _add:

Sum
---

.. method:: Polynomial.__add__

    The sum is a basic operation::
    
        >>> polynomial('x2 - y3 + 2') + polynomial('x3')
        - y^3 + x^3 + x^2 + 2
    
    the second term can be:
        * a polynomial
        * a string
        * an integer
        * a tuple of tuples (not list)
    
    Some examples::
    
        >>> polynomial('x2 - y3 + 2') + 5
        - y^3 + x^2 + 7
        >>> polynomial('x2 - y3 + 2') + '-x2 + y - 5'
        - y^3  + y - 3
        >>> polynomial('x2 - y3 + 2') + ((2, {'x': 3}),)
        - y^3 + 2x^3 + x^2 + 2
        >>> polynomial('x2 - y3 + 2') + ((2, {'x': 3}), (3, {}))
        - y^3 + 2x^3 + x^2 + 5
        >>> polynomial('x2 - y3 + 2') + [(2, {'x': 3}), (3, {})]
        
        Traceback (most recent call last):
          File "<pyshell#61>", line 1, in <module>
            polynomial('x2 - y3 + 2') + [(2, {'x': 3}), (3, {})]
        TypeError: unsupported operand type(s) for +: 'Polynomial' and 'list'


.. _sub:

Subtraction
-----------

.. method:: Polynomial.__sub__

    The subtraction is based on the addition, it takes advantages of the operator ``__neg__`` (:ref:`neg`)::
    
        >>> - polynomial('x3') # uses __neg__
        - x^3
        >>> polynomial('x2 - y3 + 2') - polynomial('x3')
        - y^3 - x^3 + x^2 + 2
        >>> polynomial('x2 - y3 + 2') - 'x3 - 5'
        - y^3 - x^3 + x^2 + 7
        >>> polynomial('x2 - y3 + 2') - 5
        - y^3 + x^2 - 3
        >>> polynomial('x2 - y3 + 2') - ((3, {'x': 2}),)
        - y^3 - 2x^2 + 2
    
    ``a - b`` is the same as ``a + -b``, so when __sub__ is called it does something like this::
    
        return Polynomial(a.monomials + (-b).monomials)

.. _mul:

Multiplication
--------------

.. method:: Polynomial.__mul__

    Like, addition and subtraction, the second term can be:
        * a polynomial
        * a string
        * an integer
        * a tuple of tuples (not list)
    
    ::
    
        >>> polynomial('x2 - y3 + 2') * polynomial('x3')
        + x^5 - x^3y^3 + 2x^3
        >>> polynomial('x2 - y3 + 2') * 'x'
        - xy^3 + x^3 + 2x
        >>> polynomial('x2 - y3 + 2') * 3
        - 3y^3 + 3x^2 + 6
        >>> polynomial('x2 - y3 + 2') * ((2, {'x': 2}),)
        + 2x^4 - 2x^2y^3 + 4x^2


.. _div:

Division
--------

Performs the division of two polynomials.

__divmod__
++++++++++

.. method:: Polynomial.__divmod__

    Returns both the quotient and the remainder of the division::
    
        >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> q
        + 2x + 4
        >>> divmod(p, q)
        (+ 3/2x^2 - 2x + 9/2, - 15)
    
    test::
    
        >>> quotient, rem = divmod(p, q)
        >>> quotient
        + 3/2x^2 - 2x + 9/2
        >>> rem
        - 15
        >>> quotient * q + rem
        + 3x^3 + 2x^2 + x + 3
        >>> quotient * q + rem == p
        True
    
    Raises :exc:`ValueError` if the polynomials are not divisible::
    
        >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4, 4, -1, 2])
        >>> p, q
        (+ 3x^3 + 2x^2 + x + 3, + 2x^4 + 4x^3 + 4x^2 - x + 2)
        >>> ## the degree of q is higher than the degree of p
        >>> divmod(p, q)
        
        Traceback (most recent call last):
          File "<pyshell#115>", line 1, in <module>
            divmod(p, q)
          File "core.py", line 218, in wrapper
            return wrapped(self, other)
          File "core.py", line 1329, in __divmod__
        ValueError: The polynomials are not divisible
    
    You can use :func:`funcs.divisible` too::
    
        >>> funcs.divisible(p, q)
        False

__div__
+++++++

.. method:: Polynomial.__div__

    Returns only the quotient, even if there is a remainder::
    
        >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> q
        + 2x + 4
        >>> divmod(p, q)
        (+ 3/2x^2 - 2x + 9/2, - 15) ## There is a remainder
        >>> p / q
        + 3/2x^2 - 2x + 9/2
        >>> (p / q) * q
        + 3x^3 + 2x^2 + x + 18
        >>> (p / q) * q != p
        True


__truediv__
+++++++++++

.. method:: Polynomial.__truediv__

    If the polynomials are divisible, returns the quotient of the division, otherwise returns an :class:`AlgebraicFraction`::
    
        >>> from pypol import *
        >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4])
        >>> from operator import truediv
        >>> truediv(p, q)
        AlgebraicFraction(+ 3x³ + 2x² + x + 3, + 2x + 4)
        >>> print truediv(p, q)
        + 3x³ + 2x² + x + 3
        −−−−−−−−−−−−−−−−−−−−−
               + 2x + 4      
        >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4, 4, -1, 2])
        >>> truediv(p, q)
        AlgebraicFraction(+ 3x³ + 2x² + x + 3, + 2x⁴ + 4x³ + 4x² - x + 2)
        >>> print truediv(p, q)
            + 3x³ + 2x² + x + 3    
        −−−−−−−−−−−−−−−−−−−−−−−−−−−−−
        + 2x⁴ + 4x³ + 4x² - x + 2


.. _pow:

Exponentiation
--------------

.. method:: Polynomial.__pow__

    Raise the polynomial at the power *exp*::
    
        >>> p = poly1d([2, 3, 1])
        >>> p
        + 2x^2 + 3x + 1
        >>> p ** 2
        + 4x^4 + 12x^3 + 13x^2 + 6x + 1
        >>> p ** 4
        + 16x^8 + 96x^7 + 248x^6 + 360x^5 + 321x^4 + 180x^3 + 62x^2 + 12x + 1
    
    Raises TypeError if *exp* is a float::
    
        >>> p ** 0.5 ## Square root, not supported
        
        Traceback (most recent call last):
          File "<pyshell#147>", line 1, in <module>
            p ** 0.5 ## Square root, not supported
        TypeError: unsupported operand type(s) for ** or pow(): 'Polynomial' and 'float'


.. _mod:

Mod
---

Returns the remainder of the division of two polynomials::

    >>> p, q = poly1d([3, 2, 1, 3]), poly1d([2, 4])
    >>> p, q
    (+ 3x^3 + 2x^2 + x + 3, + 2x + 4)
    >>> j, r = divmod(p, q)
    >>> r
    - 15
    >>> p % q
    - 15


Other operators
===============

.. _eq:

__eq__
------

.. method:: Polynomial.__eq__

    Returns True if the two polynomials are equal, False otherwise::
    
        >>> p, q = poly1d([1, 2, 3]), polynomial('x^2 + 2x + 3')
        >>> p
        + x^2 + 2x + 3
        >>> q
        + x^2 + 2x + 3
        >>> p == q
        True
        >>> monomial(2) == poly1d([3]) ## 2 != 3
        False
    
    and::
    
        >>> q.update(poly1d([2, 0, 0, 1]))
        + 2x^3 + 1
        >>> q.monomials
        ((2, {'x': 3}), (0, {'x': 2}), (0, {'x': 1}), (1, {}))
        >>> p = polynomial('2x^3 + 1')
        >>> p == q
        True
        >>> p.monomials
        ((2, {'x': 3}), (1, {}))
        >>> q.monomials
        ((2, {'x': 3}), (0, {'x': 2}), (0, {'x': 1}), (1, {}))
        >>> p.monomials == q.monomials
        False
        >>> p == q
        True

__ne__
------

.. method:: Polynomial.__ne__

    Based on :ref:`eq`::
    
        >>> p, q = polynomial('3x-2'), monomial(3, x=1)
        >>> p, q
        (+ 3x - 2, + 3x)
        >>> p == q
        False
        >>> p != q
        True

__len__
-------

.. method:: Polynomial.__len__

    Returns the length of the polynomial, i.e. the number of true terms::
    
        >>> p = poly1d([3, 2, 1, 3])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> len(p)
        4
        >>> len(p.monomials)
        4
        >>> len(p) == len(p.monomials)
        True
    
    and::
    
        >>> p.update(poly1d([2, 0, 0, 1]))
        + 2x^3 + 1
        >>> len(p)
        2
        >>> p.monomials
        ((2, {'x': 3}), (0, {'x': 2}), (0, {'x': 1}), (1, {}))
        >>> len(p.monomials)
        4

__pos__
-------

.. method:: Polynomial.__pos__

    Dummy method that does nothing::
    
        >>> p = poly1d([3, 2, 1, 3])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> +p
        + 3x^3 + 2x^2 + x + 3
        >>> p == +p
        True

.. _neg:

__neg__
-------

.. method:: Polynomial.__neg__

    Negate the polynomial. Equivalent to: ``poly * -1``.
    ::
    
        >>> p = poly1d([3, 2, 1, 3])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> - p
        - 3x^3 - 2x^2 - x - 3
        >>> p * -1 == -p
        True
        >>> p == -p * -1
        True

__nonzero__
-----------

.. method:: Polynomial.__nonzero__

    Returns True if the polynomial is not null, False otherwise::
    
        >>> p = poly1d([3, 2, 1, 3])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> bool(p)
        True
        >>> p.update('')
        
        >>> bool(p)
        False
        >>> if p:
                print 'not null'
            else:
                print 'null'
            
        null
        >>> p = poly1d([3, 2, 1, 3])
        >>> if p:
                print 'not null'
            else:
                print 'null'
            
        not null

__contains__
------------

.. method:: Polynomial.__contains__

    Returns True whether the supplied monomial is contained in the polynomial::
    
        >>> p = poly1d([3, 2, 1, 3])
        >>> p
        + 3x^3 + 2x^2 + x + 3
        >>> (3, {'x': 3})
        (3, {'x': 3})
        >>> (3, {'x': 3}) in p
        True
        >>> (3, {'x': 4}) in p
        False

__copy__
--------

.. method:: Polynomial.__copy__

Copies the polynomial monomials::

    >>> import copy
    >>> p = poly1d([1, 2, 12])
    >>> p
    + x^2 + 2x + 12
    >>> q = copy.copy(p)
    >>> q
    + x^2 + 2x + 12

but not self.simplify::

    >>> p = polynomial('3x - 2x + 4 - 9', simplify=False)
    >>> p
    + 3x - 2x + 4 - 9
    >>> q = copy.copy(p)
    >>> q
    + x - 5

__deepcopy__
------------

.. method:: Polynomial.__deepcopy__

Copies the polynomial monomials and self.simplify too::

    >>> import copy
    >>> p = poly1d([-3, 3, 5])
    >>> p
    - 3x^2 + 3x + 5
    >>> q = copy.deepcopy(p)
    >>> q
    - 3x^2 + 3x + 5
    >>> p = polynomial('3x - 2x + 4 - 9', simplify=False)
    >>> p
    + 3x - 2x + 4 - 9
    >>> q = copy.deepcopy(p)
    >>> q
    + 3x - 2x + 4 - 9

__getitem__
-----------

.. method:: Polynomial.__getitem__

Returns the monomials in position *p* in self.monomials::

    >>> p = poly1d([23, 32, 1, -0.232, 32])
    >>> p
    + 23x^4 + 32x^3 + x^2 - 0.232x + 32
    >>> p[0]
    (23, {'x': 4})
    >>> p[0:2]
    ((23, {'x': 4}), (32, {'x': 3}))
    >>> p[0:-1]
    ((23, {'x': 4}), (32, {'x': 3}), (1, {'x': 2}), (-0.23200000000000001, {'x': 1}))
    >>> p[-1]
    (32, {})
    >>> p[1::-1]
    ((32, {'x': 3}), (23, {'x': 4}))

__setitem__
-----------

.. method:: Polynomial.__setitem__

Sets the monomial in position *p* to *v*::

    >>> p = poly1d([2, -2, -1, 3])
    >>> p
    + 2x^3 - 2x^2 - x + 3
    >>> p[0]=(.1, {'x': 2})
    >>> p
    + 0.1x^2 - 2x^2 - x + 3
    >>> p.simplify()
    >>> p
    - 1.9x^2 - x + 3
    >>> p[:2] = ((.3, {'x': 3}), (-2, {'x': 2}))
    >>> p
    + 0.3x^3 - 2x^2 + 3

.. warning::
    *p* must be a monomial-like tuple::

        >>> p[0] = .1

        Traceback (most recent call last):
          File "<pyshell#36>", line 1, in <module>
            p[0] = .1
          File "core.py", line 1209, in __setitem__
            tmp_monomials[p] = v
          File "core.py", line 1075, in <lambda>
        TypeError: 'float' object is unsubscriptable

    or a tuple of tuples if the length of the slice is greater than 1::

        >>> p = poly1d([2, -2, -1, 3])
        >>> p
        + 2x^3 - 2x^2 - x + 3
        >>> p[:3] = (1, 3, .2)
        
        Traceback (most recent call last):
          File "<pyshell#43>", line 1, in <module>
            p[:3] = (1, 3, .2)
          File "/home/miki/pypol_/pypol/core.py", line 1209, in __setitem__
            tmp_monomials[p] = v
          File "/home/miki/pypol_/pypol/core.py", line 1075, in <lambda>
        TypeError: 'int' object is unsubscriptable
        >>> p[:3] = ((3, {'y': 3}),(2, {'y': 2}), (3, {'x': 6}))
        >>> p
        + 3x^6 + 3y^3 + 2y^2 + 3

.. warning::

    This method **does not simplify automatically**::

        >>> p[:2] = ((2, {'x': 2}), (3, {}))
        >>> p
        + 2x^2 + 3 + 3
        >>> p.simplify()
        >>> p
        + 2x^2 + 6

__delitem__
-----------

.. method:: Polynomial.__delitem__

Deletes the monomial(s) in position *p*::

    >>> p = poly1d([2, -2, -1, 3])
    >>> p
    + 2x^3 - 2x^2 - x + 3
    >>> del p[0]
    >>> p
    - 2x^2 - x + 3
    >>> del p[:2]
    >>> p
    + 3

__call__
--------

Evaluate the polynomial, see :meth:`Polynomial.__call__`