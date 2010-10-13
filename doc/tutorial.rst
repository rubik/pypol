Tutorial
========

This is the pypol tutorial. If you haven't installed it yet, see below.

First steps with pypol
----------------------

.. _install:

Download and install
++++++++++++++++++++

First of all, you need to get the files. To do this, go to the `github repository <http://github.com/rubik/pypol/downloads>`_ or to `PyPI <http://pypi.python.org/pypi/pypol_/0.3>`_ and download the right file.

If you downloaded the source package you need to unpack it::

    $ tar -xzfv pypol_-0.3.tar.gz

Now run the setup.py script::

    $ python setup.py install

.. note::
    Sometimes you have to allow :file:`setup.py` to run with root security privileges::

        $ python setup.py install
            running install
            error: can't create or remove files in install directory
            
            The following error occurred while trying to add or remove files in the
            installation directory:
            
                [Errno 13] Permission denied: '/usr/local/lib/python2.6/dist-packages/test-easy-install-9562.write-test'
            
            The installation directory you specified (via --install-dir, --prefix, or
            the distutils default setting) was:
            
                /usr/local/lib/python2.6/dist-packages/
            
            Perhaps your account does not have write access to this directory?  If the
            installation directory is a system-owned directory, you may need to sign in
            as the administrator or "root" account.  If you do not have administrative
            access to this machine, you may wish to choose a different installation
            directory, preferably one that is listed in your PYTHONPATH environment
            variable.
            
            For information on other options, you may wish to consult the
            documentation at:
            
              http://peak.telecommunity.com/EasyInstall.html
            
            Please make the appropriate changes for your system and try again.

    So try::

        $ sudo python setup.py install
            [sudo] password for ~~~~~: 
            running install
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
            copying pypol/__init__.py -> build/lib.linux-i686-2.6/pypol
            copying pypol/funcs.py -> build/lib.linux-i686-2.6/pypol
            copying pypol/core.py -> build/lib.linux-i686-2.6/pypol
            creating build/bdist.linux-i686/egg
            creating build/bdist.linux-i686/egg/pypol
            copying build/lib.linux-i686-2.6/pypol/__init__.py -> build/bdist.linux-i686/egg/pypol
            copying build/lib.linux-i686-2.6/pypol/funcs.py -> build/bdist.linux-i686/egg/pypol
            copying build/lib.linux-i686-2.6/pypol/core.py -> build/bdist.linux-i686/egg/pypol
            byte-compiling build/bdist.linux-i686/egg/pypol/__init__.py to __init__.pyc
            byte-compiling build/bdist.linux-i686/egg/pypol/funcs.py to funcs.pyc
            byte-compiling build/bdist.linux-i686/egg/pypol/core.py to core.pyc
            creating build/bdist.linux-i686/egg/EGG-INFO
            copying pypol_.egg-info/PKG-INFO -> build/bdist.linux-i686/egg/EGG-INFO
            copying pypol_.egg-info/SOURCES.txt -> build/bdist.linux-i686/egg/EGG-INFO
            copying pypol_.egg-info/dependency_links.txt -> build/bdist.linux-i686/egg/EGG-INFO
            copying pypol_.egg-info/top_level.txt -> build/bdist.linux-i686/egg/EGG-INFO
            zip_safe flag not set; analyzing archive contents...
            creating 'dist/pypol_-0.3-py2.6.egg' and adding 'build/bdist.linux-i686/egg' to it
            removing 'build/bdist.linux-i686/egg' (and everything under it)
            Processing pypol_-0.3-py2.6.egg
            creating /usr/local/lib/python2.6/dist-packages/pypol_-0.3-py2.6.egg
            Extracting pypol_-0.3-py2.6.egg to /usr/local/lib/python2.6/dist-packages
            Adding pypol- 0.3 to easy-install.pth file
            
            Installed /usr/local/lib/python2.6/dist-packages/pypol_-0.3-py2.6.egg
            Processing dependencies for pypol-==0.3
            Finished processing dependencies for pypol-==0.3

Running the tests
+++++++++++++++++

If you want to run pypol's tests you only have to run *test_pypol.py*, that is in the *tests* directory::

    $ cd pypol_-0.3/tests
    $ python test_pypol.py
    ...............................
    ----------------------------------------------------------------------
    Ran 44 tests in 0.036s
    
    OK

or run them with setup.py::

    $ cd pypol_-0.3
    $ sudo python setup.py test
    running test
    running egg_info
    writing pypol_.egg-info/PKG-INFO
    writing top-level names to pypol_.egg-info/top_level.txt
    writing dependency_links to pypol_.egg-info/dependency_links.txt
    reading manifest file 'pypol_.egg-info/SOURCES.txt'
    writing manifest file 'pypol_.egg-info/SOURCES.txt'
    running build_ext
    pypol_.tests.test_pypol.TestFunctions.testAreSimilar ... ok
    pypol_.tests.test_pypol.TestFunctions.testGcd ... ok
    pypol_.tests.test_pypol.TestFunctions.testLcm ... ok
    pypol_.tests.test_pypol.TestFunctions.testMonomial ... ok
    pypol_.tests.test_pypol.TestFunctions.testParsePolynomial ... ok
    pypol_.tests.test_pypol.TestFunctions.testPolynomial ... ok
    pypol_.tests.test_pypol.TestFunctions.testRandomPoly ... ok
    pypol_.tests.test_pypol.TestFunctions.testRoot ... ok
    pypol_.tests.test_pypol.TestPolynomial.testAdd ... ok
    pypol_.tests.test_pypol.TestPolynomial.testCoeffGcd ... ok
    pypol_.tests.test_pypol.TestPolynomial.testCoeffLcm ... ok
    pypol_.tests.test_pypol.TestPolynomial.testComplete ... ok
    pypol_.tests.test_pypol.TestPolynomial.testContains ... ok
    pypol_.tests.test_pypol.TestPolynomial.testDelitem ... ok
    pypol_.tests.test_pypol.TestPolynomial.testDiv ... ok
    pypol_.tests.test_pypol.TestPolynomial.testDivAll ... ok
    pypol_.tests.test_pypol.TestPolynomial.testDivmod ... ok
    pypol_.tests.test_pypol.TestPolynomial.testEq ... ok
    pypol_.tests.test_pypol.TestPolynomial.testEvalForm ... ok
    pypol_.tests.test_pypol.TestPolynomial.testGcd ... ok
    pypol_.tests.test_pypol.TestPolynomial.testGetitem ... ok
    pypol_.tests.test_pypol.TestPolynomial.testIsSquareDiff ... ok
    pypol_.tests.test_pypol.TestPolynomial.testJointLetters ... ok
    pypol_.tests.test_pypol.TestPolynomial.testLcm ... ok
    pypol_.tests.test_pypol.TestPolynomial.testLen ... ok
    pypol_.tests.test_pypol.TestPolynomial.testLetters ... ok
    pypol_.tests.test_pypol.TestPolynomial.testLinear ... ok
    pypol_.tests.test_pypol.TestPolynomial.testMod ... ok
    pypol_.tests.test_pypol.TestPolynomial.testMul ... ok
    pypol_.tests.test_pypol.TestPolynomial.testNe ... ok
    pypol_.tests.test_pypol.TestPolynomial.testNeg ... ok
    pypol_.tests.test_pypol.TestPolynomial.testNonzero ... ok
    pypol_.tests.test_pypol.TestPolynomial.testOrdered ... ok
    pypol_.tests.test_pypol.TestPolynomial.testOrderedMonomials ... ok
    pypol_.tests.test_pypol.TestPolynomial.testPos ... ok
    pypol_.tests.test_pypol.TestPolynomial.testPow ... ok
    pypol_.tests.test_pypol.TestPolynomial.testPowers ... ok
    pypol_.tests.test_pypol.TestPolynomial.testRawPowers ... ok
    pypol_.tests.test_pypol.TestPolynomial.testSetitem ... ok
    pypol_.tests.test_pypol.TestPolynomial.testSort ... ok
    pypol_.tests.test_pypol.TestPolynomial.testSub ... ok
    pypol_.tests.test_pypol.TestPolynomial.testTruediv ... ok
    pypol_.tests.test_pypol.TestPolynomial.testUpdate ... ok
    pypol_.tests.test_pypol.TestPolynomial.testZeros ... ok
    
    ----------------------------------------------------------------------
    Ran 44 tests in 0.461s
    
    OK



Building this documentation
+++++++++++++++++++++++++++

To build the documentation, change directory and go to pypol/doc::

    $ cd pypol_-0.3/doc

* On **Windows**
    Run make.bat *<target>*

* On **Unix**/**Mac OS X**
    Run make *<target>*

Where *<target>* is one of: 

        +----------------+------------------------------------------------------------+
        | **html**       |  to make standalone HTML files                             |
        +----------------+------------------------------------------------------------+
        | **singlehtml** |  to make a single large HTML file                          |
        +----------------+------------------------------------------------------------+
        | **dirhtml**    |  to make HTML files named index.html in directories        |
        +----------------+------------------------------------------------------------+
        | **pickle**     |  to make pickle files                                      |
        +----------------+------------------------------------------------------------+
        | **json**       |  to make JSON files                                        |
        +----------------+------------------------------------------------------------+
        | **htmlhelp**   |  to make HTML files and a HTML help project                |
        +----------------+------------------------------------------------------------+
        | **qthelp**     |  to make HTML files and a qthelp project                   |
        +----------------+------------------------------------------------------------+
        | **devhelp**    |  to make HTML files and a Devhelp project                  |
        +----------------+------------------------------------------------------------+
        |  **epub**      |  to make an epub                                           |
        +----------------+------------------------------------------------------------+
        | **latex**      |  to make LaTeX files, you can set PAPER=a4 or PAPER=letter |
        +----------------+------------------------------------------------------------+
        | **latexpdf**   |  to make LaTeX files and run them through pdflatex         |
        +----------------+------------------------------------------------------------+
        |  **text**      |  to make text files                                        |
        +----------------+------------------------------------------------------------+
        |  **man**       |  to make manual pages                                      |
        +----------------+------------------------------------------------------------+

Cookbook
--------

Here is pypol cookbook. All examples assume::

    >>> from pypol import *


Creating a polynomial
+++++++++++++++++++++

Use :func:`pypol.poly1d`, :func:`pypol.poly1d_2`, :func:`pypol.polynomial`, and :func:`pypol.monomial`::

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
    Traceback (most recent call last):
      File "<pyshell#21>", line 1, in <module>
        q / p
      File "core.py", line 1453, in __divmod__
        raise ValueError('The polynomials are not divisible')
    ValueError: The polynomials are not divisible
    >>> del p[1]
    >>> q / p
    + 3x^6 + 9x^4 - 11x^3 + 27x^2 - 51x + 103
    >>> divmod(q, p)
    (+ 3x^6 + 9x^4 - 11x^3 + 27x^2 - 51x + 103, - 207x^2 + 411x - 206)
    >>> quot, rem = divmod(q, p)
    >>> quot * p + rem
    + 3x^9 - 5x^6
    >>> q
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

Differentiation and itegration
++++++++++++++++++++++++++++++

There are three functions: :func:`pypol.funcs.polyder` (to find the derivative),
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


Root-finding
++++++++++++

