Utility functions
=================

pypol module has some utility functions to work with polynomials:
    * :func:`polynomial`
    * :func:`make_polynomial`
    * :func:`parse_polynomial`
    * :func:`random_poly`

.. function:: polynomial([string=None[, simplify=True[, print_format=True]]])

    Returns a *Polynomial* object.

    string is a string that represent a polynomial, default is None.
    If simplify is True, the polynomial will be simplified on __init__ and on update.

    **Syntax rules**
        Powers can be expressed using the *^* symbol. If a digit follows a letter then it is interpreted as an exponent. So the following expressions are be equal::

             polynomial('2x^3y^2 + 1') == polynomial('2x3y2 + 1')

        but if there is a white space after the letter then the digit is interpreted as a positive coefficient.
        So this:::

             polynomial('2x3y 2 + 1')

        represents this polynomial:::

             2x^3y + 3

.. function:: make_polynomial(monomials[, simplify=True])

        Make a polynomial from a list of tuples.
        For example::

            >>> make_polynomial(parse_polynomial('2x + 3y - 4'))
            2x + 3y - 4
            >>> make_polynomial(((2, {'x': 1}), (3, {'y': 1}), (-4, {})))
            2x + 3y - 4

.. function:: are_similar(a, b)

    Returns True whether the two monomials *a* and *b* are similar, i.e. they have the same literal part, False otherwise.
    An example::

        >>> are_similar((-2, {'x': 2, 'y': 2}), (-2, {'x': 3}))
        False
        >>> are_similar((3, {'y': 4}), (4, {'y': 4}))
        True

.. function:: parse_polynomial(string[, max_length=None])

    Parses a string that represent a polynomial.
    It can parse integer coefficients, float coefficient and fractional coefficient.
    max_length represent the maximum length that the polynomial can have.

    See :func:`polynomial`'s syntax rules.
    An example:::

        >>> parse_polynomial('2x^3 - 3y + 2')
        [(2, {'x': 3}), (-3, {'y': 1}), (2, {})]
        >>> parse_polynomial('x3 - 3y2 + 2')
        [(1, {'x': 3}), (-3, {'y': 2}), (2, {})]

.. function:: random_poly([, coeff_range=xrange(-10, 11)[, len_=None[, letters='xyz'[, \
                            max_letters=3[, exp_range=xrange(1, 6)[, right_hand_side=None]]]]]])

    Returns a polynomial generated randomly.

    coeff_range is the range of the polynomial's coefficients, default is ``xrange(-10, 11)``.
    len\_ is the len of the polynomial. Default is None, in this case len\_ will be a random number chosen in coeff_range.
    letters are the letters that appear in the polynomial.
    max_letter is the maximum number of letter for every monomial.
    exp_range is the range of the exponents.
    if right_hand_side is True the polynomial will have a right_hand_side. Default is None, that means the right_hand_side will be chosen randomly.
    ::

        >>> random_poly()
         + 2x^4y^5 + 3y^5 + 5xy^5 + 10x^2y^3z^3 - 5z
    
        >>> random_poly()
         + 7xy^5 - 3z^4 - 2
        >>> random_poly(len_=3, letters='ab')
         + 9a^5 + 7a^2b^4 - 8ab^2