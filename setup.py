from setuptools import setup

version = '0.2'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-extensions',
    'django-nose',
    'South',
    'django-celery',
    'requests',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='threedi-task',
      version=version,
      description="Task tracking",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Jackie Leng',
      author_email='Jackie.Leng@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['threedi_task'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
