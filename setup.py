from distutils.core import setup

setup(name='pypol_',
      version='0.1',
      description='Python polynomial library',
      author='Michele Lacchia',
      author_email='michelelacchia@gmail.com',
      license='GNU GPL v3',
      url='http://pypol.altervista.org/',
      download_url='http://github.com/rubik/pypol/downloads/',
      packages=['pypol'],
      package_dir = {'pypol': 'src/*.py'},
      package_data={'pypol': ['tests/*.py']},
      classifiers=['Topic :: Scientific/Engineering :: Mathematics', 'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)', 'Natural Language :: English',
                   'Operating System :: OS Independent', 'Programming Language :: Python :: 2.6',
                   ],
      )