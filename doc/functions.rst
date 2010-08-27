Utility functions
=================

pypol module has some utility functions to work with polynomials:
    * polynomial
    * make_polynomial
    * parse_polynomial
    * random_poly

.. function:: polynomial([string=None[, simplify=True[, print_format=True]]])

    Returns a *Polynomial* object.

    string is a string that represent a polynomial, default is None.

    **Syntax rules**
        Powers can be expressed using the *^* symbol. If a digit follows a letter then it is interpreted as an exponent. So the following expressions are be equal::

             polynomial('2x^3y^2 + 1') == polynomial('2x3y2 + 1')

        but if there is a white space after the letter then the digit is interpreted as a positive coefficient.
        So this:::

             polynomial('2x3y 2 + 1')

        represents this polynomial:::

             2x^3y + 3

.. function:: make_polynomial()