import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

setup(
    name='tap',
    description='Python bindings for the Tap API',
    long_description='',
    author='obytes',
    url='https://github.com/obytes/tap-python',
    keywords='tap api payments',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=[
        'pytest >= 3.4',
        'pytest-mock >= 1.7',
        'pytest-xdist >= 1.22',
        'pytest-cov >= 2.5',
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/obytes/tap-python/issues',
        'Documentation': 'https://tap.com/docs/api/python',
        'Source Code': 'https://github.com/obytes/tap-python',
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
