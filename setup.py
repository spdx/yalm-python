from setuptools import setup, find_packages
import unittest

def test_suite():
    return unittest.TestLoader().discover('test',pattern='test_*.py')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'spdx_python_licensematching',
    version = '1.0',
    description = 'SPDX Implementation of License Matching Guidelines in Python',
    long_description = long_description,
    packages = find_packages(include=['normalize_license_text.*',
                                      'compare_template_text.*',
                                      'generate_differences.*',
                                      'resources.*',
                                      'test.*',
                                      'configuration.*',
                                      'examples.*',
                                      'match_against_all_templates'
                                      ]),
    include_package_data = True,
    zip_safe=False,
    test_suite='setup.test_suite',
    python_requires='>=3.5',
    author='Anshul Dutt Sharma',
    author_email='anshuldutt21@gmail.com',
    url='https://github.com/anshuldutt21/spdx_python_licensematching',
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7.5'
    ]
)
