Tutorial
========

This is the pypol tutorial. If you haven't installed it yet, see below.

First steps with pypol
----------------------

.. _install:

Download and install
++++++++++++++++++++

First of all, you need to get the files. To do this, go to the `github repository <http://github.com/rubik/pypol/downloads>`_ or to `PyPI <http://pypi.python.org/pypi/pypol_/0.4>`_ and download the right file.

If you downloaded the source package you need to unpack it::

    $ tar -xzfv pypol_-0.4.tar.gz

Now run the setup.py script::

    $ python setup.py install

Sometimes (particularly on Unix systems) you have to allow :file:`setup.py` to run with root security privileges::

    $ python setup.py install
    running install
    install_dir /usr/local/lib/python2.7/dist-packages/
    Checking .pth file support in /usr/local/lib/python2.7/dist-packages/
    error: can't create or remove files in install directory
    
    The following error occurred while trying to add or remove files in the
    installation directory:
    
        [Errno 13] Permission denied: '/usr/local/lib/python2.7/dist-packages/test-easy-install-4687.pth'
    
    The installation directory you specified (via --install-dir, --prefix, or
    the distutils default setting) was:
    
        /usr/local/lib/python2.7/dist-packages/
    
    Perhaps your account does not have write access to this directory?  If the
    installation directory is a system-owned directory, you may need to sign in
    as the administrator or "root" account.  If you do not have administrative
    access to this machine, you may wish to choose a different installation
    directory, preferably one that is listed in your PYTHONPATH environment
    variable.
    
    For information on other options, you may wish to consult the
    documentation at:
    
      http://packages.python.org/distribute/easy_install.html
    
    Please make the appropriate changes for your system and try again.

So try::

    $ sudo python setup.py install
    [sudo] password for user: 
    running install
    install_dir /usr/local/lib/python2.7/dist-packages/
    Checking .pth file support in /usr/local/lib/python2.7/dist-packages/
    /usr/bin/python -E -c pass
    TEST PASSED: /usr/local/lib/python2.7/dist-packages/ appears to support .pth files
    running bdist_egg
    running egg_info
    writing pypol_.egg-info/PKG-INFO
    writing top-level names to pypol_.egg-info/top_level.txt
    writing dependency_links to pypol_.egg-info/dependency_links.txt
    reading manifest file 'pypol_.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    warning: no files found matching 'README.textile'
    writing manifest file 'pypol_.egg-info/SOURCES.txt'
    installing library code to build/bdist.linux-i686/egg
    running install_lib
    running build_py
    creating build
    creating build/lib.linux-i686-2.7
    creating build/lib.linux-i686-2.7/pypol
    copying pypol/__init__.py -> build/lib.linux-i686-2.7/pypol
    copying pypol/core.py -> build/lib.linux-i686-2.7/pypol
    copying pypol/series.py -> build/lib.linux-i686-2.7/pypol
    copying pypol/funcs.py -> build/lib.linux-i686-2.7/pypol
    copying pypol/roots.py -> build/lib.linux-i686-2.7/pypol
    creating build/bdist.linux-i686
    creating build/bdist.linux-i686/egg
    creating build/bdist.linux-i686/egg/pypol
    copying build/lib.linux-i686-2.7/pypol/__init__.py -> build/bdist.linux-i686/egg/pypol
    copying build/lib.linux-i686-2.7/pypol/core.py -> build/bdist.linux-i686/egg/pypol
    copying build/lib.linux-i686-2.7/pypol/series.py -> build/bdist.linux-i686/egg/pypol
    copying build/lib.linux-i686-2.7/pypol/funcs.py -> build/bdist.linux-i686/egg/pypol
    copying build/lib.linux-i686-2.7/pypol/roots.py -> build/bdist.linux-i686/egg/pypol
    byte-compiling build/bdist.linux-i686/egg/pypol/__init__.py to __init__.pyc
    byte-compiling build/bdist.linux-i686/egg/pypol/core.py to core.pyc
    byte-compiling build/bdist.linux-i686/egg/pypol/series.py to series.pyc
    byte-compiling build/bdist.linux-i686/egg/pypol/funcs.py to funcs.pyc
    byte-compiling build/bdist.linux-i686/egg/pypol/roots.py to roots.pyc
    creating build/bdist.linux-i686/egg/EGG-INFO
    copying pypol_.egg-info/PKG-INFO -> build/bdist.linux-i686/egg/EGG-INFO
    copying pypol_.egg-info/SOURCES.txt -> build/bdist.linux-i686/egg/EGG-INFO
    copying pypol_.egg-info/dependency_links.txt -> build/bdist.linux-i686/egg/EGG-INFO
    copying pypol_.egg-info/top_level.txt -> build/bdist.linux-i686/egg/EGG-INFO
    zip_safe flag not set; analyzing archive contents...
    creating 'dist/pypol_-0.4-py2.7.egg' and adding 'build/bdist.linux-i686/egg' to it
    removing 'build/bdist.linux-i686/egg' (and everything under it)
    Processing pypol_-0.4-py2.7.egg
    creating /usr/local/lib/python2.7/dist-packages/pypol_-0.4-py2.7.egg
    Extracting pypol_-0.4-py2.7.egg to /usr/local/lib/python2.7/dist-packages
    Adding pypol- 0.4 to easy-install.pth file
    
    Installed /usr/local/lib/python2.7/dist-packages/pypol_-0.4-py2.7.egg
    Processing dependencies for pypol-==0.4
    Finished processing dependencies for pypol-==0.4

Running the tests
+++++++++++++++++

If you want to run pypol's tests you only have to run the python files in the :file:`tests` directory::

    $ python test_pypol.py
    ================================= test session starts =================================
    platform linux2 -- Python 2.6.6 -- pytest-2.0.0
    collected 40 items 
    
    test_pypol.py .................s......................
    
    ======================== 39 passed, 1 skipped in 0.31 seconds =========================
    $ python test_funcs.py -v
    ================================= test session starts =================================
    platform linux2 -- Python 2.6.6 -- pytest-2.0.0 -- /usr/bin/python
    collected 12 items 
    
    test_funcs.py:34: TestFuncs.testDivisible PASSED
    test_funcs.py:38: TestFuncs.testRandomPoly PASSED
    test_funcs.py:53: TestFuncs.testPolyder PASSED
    test_funcs.py:59: TestFuncs.testPolyint PASSED
    test_funcs.py:68: TestFuncs.testPolyint_ PASSED
    test_funcs.py:78: TestFuncs.testInterpolation PASSED
    test_funcs.py:81: TestFuncs.testBinCoeff PASSED
    test_funcs.py:90: TestFuncs.testHarmonic PASSED
    test_funcs.py:104: TestFuncs.testGeneralizedHarmonic PASSED
    test_funcs.py:115: TestFuncs.testStirling PASSED
    test_funcs.py:124: TestFuncs.testStirling2 PASSED
    test_funcs.py:132: TestFuncs.testBellNumbers PASSED
    
    ============================== 12 passed in 0.80 seconds ==============================

or run them with :file:`setup.py`::

    $ cd pypol_-0.4
    $ sudo python setup.py test
    running test
    install_dir /usr/local/lib/python2.6/dist-packages/
    Searching for pytest
    Reading http://pypi.python.org/simple/pytest/
    Reading http://pytest.org
    Best match: pytest 2.0.0
    Processing pytest-2.0.0-py2.6.egg
    pytest 2.0.0 is already the active version in easy-install.pth
    Installing py.test script to /usr/local/bin
    Installing py.test-2.6 script to /usr/local/bin
    
    Using /usr/local/lib/python2.6/dist-packages/pytest-2.0.0-py2.6.egg
    Processing dependencies for pytest
    Finished processing dependencies for pytest
    ================================= test session starts =================================
    platform linux2 -- Python 2.6.6 -- pytest-2.0.0 -- /usr/bin/python
    collected 86 items 
    
    tests/test_funcs.py:34: TestFuncs.testDivisible PASSED
    tests/test_funcs.py:38: TestFuncs.testRandomPoly PASSED
    tests/test_funcs.py:53: TestFuncs.testPolyder PASSED
    tests/test_funcs.py:59: TestFuncs.testPolyint PASSED
    tests/test_funcs.py:68: TestFuncs.testPolyint_ PASSED
    tests/test_funcs.py:78: TestFuncs.testInterpolation PASSED
    tests/test_funcs.py:81: TestFuncs.testBinCoeff PASSED
    tests/test_funcs.py:90: TestFuncs.testHarmonic PASSED
    tests/test_funcs.py:104: TestFuncs.testGeneralizedHarmonic PASSED
    tests/test_funcs.py:115: TestFuncs.testStirling PASSED
    ... cut ...
    tests/test_series.py:156: TestSeries.testTouchard PASSED
    tests/test_series.py:164: TestSeries.testBell PASSED
    tests/test_series.py:174: TestSeries.testGegenbauer PASSED
    tests/test_series.py:180: TestSeries.testLaguerre PASSED
    tests/test_series.py:186: TestSeries.testGeneralizedLaguerre PASSED
    tests/test_series.py:192: TestSeries.testBernoulli PASSED
    tests/test_series.py:202: TestSeries.testBernoulliNumbers PASSED
    tests/test_series.py:217: TestSeries.testEuler PASSED
    tests/test_series.py:225: TestSeries.testEulerNumbers PASSED
    tests/test_series.py:235: TestSeries.testGenocchi PASSED
    
    ======================== 85 passed, 1 skipped in 3.38 seconds =========================



Building this documentation
+++++++++++++++++++++++++++

To build the documentation, change directory and go to :file:`pypol/doc`::

    $ cd pypol_-0.4/doc

* On **Windows**
    Run :command:`make.bat <target>`

* On **Unix**/**Mac OS X**
    Run :command:`make <target>`

Where *<target>* is one of: 

        +----------------+-----------------------------------------------------------------+
        | **html**       |  to make standalone HTML files                                  |
        +----------------+-----------------------------------------------------------------+
        | **singlehtml** |  to make a single large HTML file                               |
        +----------------+-----------------------------------------------------------------+
        | **dirhtml**    |  to make HTML files named index.html in directories             |
        +----------------+-----------------------------------------------------------------+
        | **pickle**     |  to make pickle files                                           |
        +----------------+-----------------------------------------------------------------+
        | **json**       |  to make JSON files                                             |
        +----------------+-----------------------------------------------------------------+
        | **htmlhelp**   |  to make HTML files and a HTML help project                     |
        +----------------+-----------------------------------------------------------------+
        | **qthelp**     |  to make HTML files and a qthelp project                        |
        +----------------+-----------------------------------------------------------------+
        | **devhelp**    |  to make HTML files and a Devhelp project                       |
        +----------------+-----------------------------------------------------------------+
        |  **epub**      |  to make an epub                                                |
        +----------------+-----------------------------------------------------------------+
        | **latex**      |  to make LaTeX files, you can set PAPER=a4 or PAPER=letter      |
        +----------------+-----------------------------------------------------------------+
        | **latexpdf**   |  to make LaTeX files and run them through pdflatex              |
        +----------------+-----------------------------------------------------------------+
        |  **text**      |  to make text files                                             |
        +----------------+-----------------------------------------------------------------+
        |  **man**       |  to make manual pages                                           |
        +----------------+-----------------------------------------------------------------+
        |  **changes**   |  to make an overview of all changed/added/deprecated items      |
        +----------------+-----------------------------------------------------------------+
        | **linkcheck**  |  to check all external links for integrity                      |
        +----------------+-----------------------------------------------------------------+
        |  **doctest**   |  to run all doctests embedded in the documentation (if enabled) |
        +----------------+-----------------------------------------------------------------+


Cookbook
--------

Here is pypol cookbook. All examples assume::

    >>> from pypol import *


Creating a polynomial
+++++++++++++++++++++

Use :func:`pypol.poly1d`, :func:`pypol.poly1d_2`, :func:`pypol.polynomial`, or :func:`pypol.monomial` to create a polynomial::

    >>> p = poly1d([1, 2, -3, 4])
    >>> p
    + x^3 + 2x^2 - 3x + 4
    >>> q = poly1d_2([[3, 9], [-5, 6]])
    >>> q
    + 3x^9 - 5x^6
    >>> r = polynomial('.3x^4 - 2x^5 + 4x')
    >>> r
    - 2x^5 + 3/10x^4 + 4x
    >>> m = monomial(-3)
    >>> m
    - 3
    >>> m.monomials
    ((-3, {}),)
    >>> m2 = monomial(-3, x=1, y=3, z=2)
    >>> m2
    - 3xy^3z^2
    >>> m2.monomials
    ((-3, {'y': 3, 'x': 1, 'z': 2}),)
    >>> len(m2)
    1


The :class:`pypol.Polynomial` class
++++++++++++++++++++++++++++++++++++++

::

    >>> p = poly1d([1, 2, -3, 4])
    >>> type(p)
    <class 'pypol.core.Polynomial'>
    >>> p.monomials
    ((1, {'x': 3}), (2, {'x': 2}), (-3, {'x': 1}), (4, {}))
    >>> p.coefficients
    [1, 2, -3, 4]
    >>> p.letters
    ('x',)
    >>> p.append(-2)
    >>> p
    + x^3 + 2x^2 - 3x + 2
    >>> p.append('4xy')
    >>> p
    + x^3 + 2x^2 + 4xy - 3x + 2
    >>> p.letters
    ('x', 'y')
    >>> del p[1]
    >>> p
    + x^3 + 4xy - 3x + 2
    >>> p.gcd
    + 1
    >>> p.lcm
    + 12x^3y
    >>> p.degree
    3

.. seealso::
    :class:`pypol.Polynomial` class reference.


Operations
++++++++++

::

    >>> p / q
    Traceback (most recent call last):
      File "<pyshell#20>", line 1, in <module>
        p / q
      File "/core.py", line 1436, in __divmod__
        raise ValueError('The polynomials are not divisible')
    ValueError: The polynomials are not divisible
    >>> q / p
    + 3x^6 - 6x^5 + 21x^4 - 77x^3 + 241x^2 - 797x + 2625
    >>> divmod(q, p)
    (+ 3x^6 - 6x^5 + 21x^4 - 77x^3 + 241x^2 - 797x + 2625,
     - 8605x^2 + 11063x - 10500)
    >>> quot, rem = divmod(q, p)
    >>> quot, rem 
    (+ 3x^6 - 6x^5 + 21x^4 - 77x^3 + 241x^2 - 797x + 2625,
     - 8605x^2 + 11063x - 10500)
    >>> quot * p + rem
    + 3x^9 - 5x^6
    >>> quot * p + rem == q
    True
    >>> j = poly1d([-3, 2, 1])
    >>> j
    - 3x^2 + 2x + 1
    >>> j * -3
    + 9x^2 - 6x - 3
    >>> j * '-x^3'
    + 3x^5 - 2x^4 - x^3
    >>> j * ((1, {'y': 3}), (-2, {}))
    - 3x^2y^3 + 2xy^3 + y^3 + 6x^2 - 4x - 2
    >>> j
    - 3x^2 + 2x + 1
    >>> k = poly1d([1, 2])
    >>> k
    + x + 2
    >>> j + k
    - 3x^2 + 3x + 3
    >>> j - k
    - 3x^2 + x - 1
    >>> j + -k == j - k
    True

.. seealso::
    :ref:`operations`

Differentiation and integration
+++++++++++++++++++++++++++++++

Currently, there are three functions: :func:`pypol.funcs.polyder` (to find the derivative),
:func:`pypol.funcs.polyint` (to find the indefinite integral) and :func:`pypol.funcs.polyint_` (to find the definite integral)::

    >>> p = poly1d([1, 3, -3, -1])
    >>> p
    + x^3 + 3x^2 - 3x - 1
    >>> funcs.polyder(p)
    + 3x^2 + 6x - 3
    >>> funcs.polyder(p, 2)
    + 6x + 6
    >>> funcs.polyder(p, 2) == funcs.polyder(funcs.polyder(p))
    True
    >>> funcs.polyder(p, 3)
    + 6
    >>> funcs.polyder(p, 4)
    
    >>> funcs.polyder(p, 5)
    
    >>> funcs.polyint(p)
    + 1/4x^4 + x^3 - 3/2x^2 - x
    >>> funcs.polyint(p, 2)
    + 1/20x^5 + 1/4x^4 - 1/2x^3 - 1/2x^2
    >>> funcs.polyint(p, 2) == funcs.polyint(funcs.polyint(p))
    True
    >>> funcs.polyint(p, 2, [3, 1]) ## Integration costants
    + 1/20x^5 + 1/4x^4 - 1/2x^3 - 1/2x^2 + 3x + 1
    >>> funcs.polyint(p, 3, [3, 1, -4, 3, 2]) ## Integration costants, polyint will use only the first three (m = 3)
    + 1/120x^6 + 1/20x^5 - 1/8x^4 - 1/6x^3 + 3/2x^2 + x - 4
    >>> funcs.polyint_(p, 10, -2) ## Definite integral
    3348.0
    >>> funcs.polyint_(p, -10, -2) ## Definite integral
    1368.0
    >>> funcs.polyint_(p, -10, -10) ## If the limits are equal the result will be 0
    0.0


Series
++++++

The :mod:`pypol.series` module defines some functions, like::

    >>> from pypol.series import *
    >>> fibonacci(2)
    + x
    >>> fibonacci(21)
    + x^20 + 19x^18 + 153x^16 + 680x^14 + 1820x^12 + 3003x^10 + 3003x^8 + 1716x^6 + 495x^4 + 55x^2 + 1
    >>> hermite_prob(12)
    + x^12 - 66x^10 + 1485x^8 - 13860x^6 + 51975x^4 - 62370x^2 + 10395
    >>> hermite_phys(12)
    + 4096x^12 - 135168x^10 + 1520640x^8 - 7096320x^6 + 13305600x^4 - 7983360x^2 + 665280
    >>> chebyshev_t(19)
    + 262144x^19 - 1245184x^17 + 2490368x^15 - 2723840x^13 + 1770496x^11 - 695552x^9 + 160512x^7 - 20064x^5 + 1140x^3 - 19x
    >>> chebyshev_u(17) ## Chebyshev polynomials of the second kind
    + 131072x^17 - 524288x^15 + 860160x^13 - 745472x^11 + 366080x^9 - 101376x^7 + 14784x^5 - 960x^3 + 18x
    >>> abel(12)
    + x^12 - 132ax^11 + 7920a^2x^10 - 285120a^3x^9 + 6842880a^4x^8 - 114960384a^5x^7 + 1379524608a^6x^6 - 11824496640a^7x^5 + 70946979840a^8x^4 - 283787919360a^9x^3 + 681091006464a^10x^2 - 743008370688a^11x
    >>> abel(9, 'k')
    + x^9 - 72kx^8 + 2268k^2x^7 - 40824k^3x^6 + 459270k^4x^5 - 3306744k^5x^4 + 14880348k^6x^3 - 38263752k^7x^2 + 43046721k^8x
    >>> laguerre_g(2)
    + 1/2a^2 + 3/2a - ax + 1 + 1/2x^2 - 2x
    >>> laguerre_g(2, 't')
    + 1/2t^2 + 3/2t - tx + 1 + 1/2x^2 - 2x
    >>> bernoulli(2)
    + x^2 - x + 1/6
    >>> bern_num(2)
    Fraction(1, 6)
    >>> euler(3)
    + x^3 - 3/2x^2 + 1/4

Root-finding
++++++++++++

The :mod:`pypol.roots` module implements some root-finding algorithms::

    >>> from pypol.roots import *
    >>> k = poly1d([3, -4, -1, 4])
    >>> k
    + 3x^3 - 4x^2 - x + 4
    >>> newton(k, 100)
    -0.859475828371609
    >>> newton(k, -10)
    -0.859475828371609
    >>> k(newton(k, -10))
    0.0
    >>> newton(k, complex(100, 1))
    (1.0964045808524712-0.5909569632973221j)
    >>> k(newton(k, complex(100, 1)))
    -1.1102230246251565e-16j
    >>> newton(k, complex(100, -1))
    (1.0964045808524712+0.5909569632973221j)
    >>> k(newton(k, complex(100, -1)))
    1.1102230246251565e-16j
    >>> halley(k, 100)
    -0.859475828371609
    >>> householder(k, 100)
    -0.859475828371609
    >>> halley(k, 1j)
    (1.0964045808524712-0.5909569632973221j)
    >>> householder(k, complex(.4, .9))
    (1.0964045808524712+0.5909569632973221j)
    >>> schroeder(k, 100)
    -0.859475828371609
    >>> schroeder(k, 100j)
    (1.0964045808524712-0.5909569632973221j)
    >>> schroeder(k, -100j)
    (1.0964045808524712+0.5909569632973221j)
    >>> cubic(k) ## All in one
    (-0.8594758283716091, (1.0964045808524712+0.590956963297322j), (1.0964045808524712-0.590956963297322j))