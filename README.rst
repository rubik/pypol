===================================================
pypol - A Python library for manupulate polynomials
===================================================

© Copyrigth 2010-2011 Michele Lacchia alias (rubik, Python, python, Pythoner, x-reynik-x)
    See LICENSE file too

How to use it
-------------

Installation
++++++++++++

pypol is on PyPI too, so you can install it with *easy_install*::

    easy_install -U pypol_

WARNING
#########

Don't forget the underscore after pypol, because with::

    easy_install -U pypol

You will install another package and not this!


Then you can import it normally::

    >>> import pypol
    >>> 

See also the documentation:
`here <http://www.pypol.altervista.org/>`_

For some examples see the Wiki:
`wiki <http://github.com/rubik/pypol/wiki>`_

pypol is on PyPI too:
`Python Package Index <http://pypi.python.org/pypi/pypol_/0.3>`_

Documentation
-------------

To build the documentation cd to pypol/doc::

    $ cd /pypol/doc

and build the documentation files:

    * if you are on Windows run make.bat::

        $ make.bat html

    * if you are on Unix run make::

        $ make html

the files are in _build/html directory.

WARNING
#########

You must have `Sphinx <http://sphinx.pocoo.org/>`_ installed to build the documentation.
You can install it with this simple command::

    $ easy_install sphinx
