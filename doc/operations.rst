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
    >>> 


.. _sub:

Subtraction
-----------

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

__divmod__
++++++++++


__div__
+++++++


__truediv__
+++++++++++



.. _pow:

Exponentiation
--------------


.. _mod:

Mod
---



Other operators
===============

__eq__
------

__ne__
------

__len__
-------

__pos__
-------

.. _neg:

__neg__
-------

__nonzero__
-----------

__contains__
------------

__copy__
--------

__deepcopy__
------------

__getitem__
-----------

__setitem__
-----------

__delitem__
-----------

__call__
--------