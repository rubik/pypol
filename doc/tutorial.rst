Tutorial
========

This is the pypol tutorial. If you haven't installed it yet, see below.

First steps with pypol
----------------------

Download and install
++++++++++++++++++++

First of all, you need to get the files. To do this, go to the `github repository <http://github.com/rubik/pypol/downloads>`_ or to `PyPI <http://pypi.python.org/pypi/pypol_/0.3>`_ and download the right file.

If you downloaded the source you need to unpack it::

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

easy_install
############

pypol is on PyPI too. If you have setuptools installed you can get pypol doing this::

    $ easy_install pypol_

and **don't forget the underscore!** Because if you try::

    $ easy_install pypol

**you will install a different package!**

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

        +-----------+-----------------------------------------------------------+
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