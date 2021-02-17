#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

__author__ = 'Tomáš Mikula'
__email__ = 'mail@tomasmikula.cz'
__version__ = '0.1.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pandas']

setup(
    author=__author__,
    author_email=__email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Python wrapper for easier manipulation with Dutch normative data for semantic concepts dataset.",
    install_requires=requirements,
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='concepts, dataset, semantic, dutch',
    name='dutch_concepts',
    packages=find_packages(
        include=['dutch_concepts', 'dutch_concepts.*']),
    url='https://github.com/mikulatomas/dutch-concepts',
    version=__version__,
    zip_safe=False,
)
