from distutils.core import setup

setup(name='pypol',
      version='0.1',
      description='Python polynomial library',
      author='Michele Lacchia',
      author_email='michelelacchia@gmail.com',
      url='http://pypol.altervista.org/',
      download_url='http://github.com/rubik/pypol/downloads/',
      packages=['src', 'tests', 'doc'],
      scripts=['doc/classes.rst', 'doc/index.rst', 'doc/tutorial.rst', 'doc/functions.rst', 'doc/make.bat', 'doc/Makefile',],
      classifiers=['Topic :: Scientific/Engineering :: Mathematics'],
      )