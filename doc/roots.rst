.. module:: pypol.roots
    :synopsis: A collection of some root- finding algorithm
.. moduleauthor:: Michele Lacchia (michelelacchia@gmail.com)
.. sectionauthor:: Michele Lacchia (michelelacchia@gmail.com)

.. |p1| image:: images/quad_eq.gif
    :alt: Quadratic equation
.. |p2| image:: images/quad_poly.gif
.. |p8_5| image:: images/newton.gif
    :alt: Newton's method
.. |p9| image:: images/halley.gif
    :alt: Halley's method
.. |p10| image:: images/householder.gif
    :alt: Householder's method
.. |p11| image:: images/schroder.gif
    :alt: Schröder's method

The :mod:`roots` module
=======================

.. versionadded:: 0.4

Here are some root-finding algorithm, such as :func:`ruffini`'s method, :func:`quadratic` formula, :func:`newton`'s method, :func:`halley`'s method, :func:`householder`'s method, :func:`bisection` method, :func:`brent`'s method.

ruffini
+++++++

.. autofunction:: ruffini

quadratic
+++++++++

.. autofunction:: quadratic

newton
++++++

.. autofunction:: newton

halley
++++++

.. autofunction:: halley

householder
+++++++++++

.. autofunction:: householder

brent
+++++

.. autofunction:: brent

bisection
+++++++++

.. autofunction:: bisection