Tutorial
========

This is the pypol tutorial. If you haven't installed it yet, see below.

First steps with pypol
----------------------

Download and install
++++++++++++++++++++

First of all, you need to get the modules. To do this, go to the `github repository <http://github.com/rubik/pypol/downloads>`_ and download the appropriate file.

Unpack it::

    $ tar xzf pypol-0.1.1.tar.gz

Now run the setup.py script::

    $ python setup.py install



Running the tests
+++++++++++++++++

If you want to run pypol's tests you only have to run *test_pypol.py*, that is in the *tests* directory::

    $ cd pypol_-0.2/tests
    $ python test_pypol.py
    ...............................
    ----------------------------------------------------------------------
    Ran 44 tests in 0.036s
    
    OK

or run setup.py::

    $ cd pypol_-0.2
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

To build, change directory and go to pypol/doc::

    $ cd pypol_-0.1/doc

* On **Windows**
    Run make.bat *<target>*

* On **Unix**/**Mac OS X**
    Run make *<target>*

Where *<target>* is one of: 

        +-----------+-----------------------------------------------------------+
        |  Target   |                           Purpose                         |
        +===========+===========================================================+
        |    html   |  to make standalone HTML files                            |
        +-----------+-----------------------------------------------------------+
        | singlehtml|  to make a single large HTML file                         |
        +-----------+-----------------------------------------------------------+
        |  dirhtml  |  to make HTML files named index.html in directories       |
        +-----------+-----------------------------------------------------------+
        |   pickle  |  to make pickle files                                     |
        +-----------+-----------------------------------------------------------+
        |   json    |  to make JSON files                                       |
        +-----------+-----------------------------------------------------------+
        |  htmlhelp |  to make HTML files and a HTML help project               |
        +-----------+-----------------------------------------------------------+
        |  qthelp   |  to make HTML files and a qthelp project                  |
        +-----------+-----------------------------------------------------------+
        |  devhelp  |  to make HTML files and a Devhelp project                 |
        +-----------+-----------------------------------------------------------+
        |    epub   |  to make an epub                                          |
        +-----------+-----------------------------------------------------------+
        |   latex   |  to make LaTeX files, you can set PAPER=a4 or PAPER=letter|
        +-----------+-----------------------------------------------------------+
        |  latexpdf |  to make LaTeX files and run them through pdflatex        |
        +-----------+-----------------------------------------------------------+
        |    text   |  to make text files                                       |
        +-----------+-----------------------------------------------------------+
        |    man    |  to make manual pages                                     |
        +-----------+-----------------------------------------------------------+