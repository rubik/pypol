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



Run the tests
+++++++++++++

If you want to run pypol's tests you only have to run *testpypol.py*, that is in the *tests* directory::

    $ cd pypol_-0.1/tests
    $ python testpypol.py
    ...............................
    ----------------------------------------------------------------------
    Ran 31 tests in 0.036s
    
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