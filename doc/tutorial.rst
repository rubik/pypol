Tutorial
========

This is the pypol tutorial. If you haven't installed it yet, see below.

First steps with pypol
----------------------

First of all, you need to get the modules. To do this, go to the `github repository <http://github.com/rubik/pypol/downloads>`_ and download the appropriate file.

Unpack it::

    $ tar xzf pypol-0.1.1.tar.gz

For the installation see below.

.. topic:: Installing pypol on Windows and Unix

    * On Windows:
        Simply run the executable file::

            $ pypol-0.1.1.exe

    * On Unix:
        You have to run the setup.py script::

            $ python setup.py install


Run the tests
-------------

If you want to run pypol's tests you only have to run testpypol.py, that is in the *tests* directory::

    $ cd pypol/tests
    $ python testpypol.py
    ...............................
    ----------------------------------------------------------------------
    Ran 31 tests in 0.036s
    
    OK
