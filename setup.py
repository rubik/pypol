from setuptools import find_packages, setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        # Verify that py.test is installed
        subprocess.call(['easy_install', '-U', 'pytest'])
        subprocess.call(['py.test', 'tests/'] + sys.argv[2:])

setup(name='pypol_',
      version='0.5',
      description='Python polynomial library',
      author='Michele Lacchia',
      author_email='michelelacchia@gmail.com',
      license='GNU GPL v3',
      url='http://pypol.altervista.org/',
      download_url='http://github.com/rubik/pypol/downloads/',
      packages=find_packages(),
      include_package_data=True,
      cmdclass={'test': PyTest},
      platforms='any',
      classifiers=['Topic :: Scientific/Engineering :: Mathematics',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   ],
      )