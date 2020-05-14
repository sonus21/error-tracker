import os
import re
from setuptools import setup


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    info = read('README.rst')
    return info


file_text = read(fpath('error_tracker/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='error-tracker',
    version=grep('__version__'),
    url='https://github.com/sonus21/error-tracker/',
    license="BSD-3-Clause",
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Simple and Extensible Error Monitoring/Tracking framework for Python',
    keywords=['Flask', 'error-tracker', 'exception-tracking', 'exception-monitoring', "Django"],
    long_description=desc(),
    long_description_content_type='text/x-rst',
    packages=['error_tracker', ],
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    zip_safe=False,
    platforms='any',
    install_requires=[
        "six",
    ],
    extras_require={
        "Django": ["Django"],
        "DRF": ["djangorestframework"],
        "Flask": ["Flask", "Flask-SQLAlchemy"],
    },
    tests_require=[
        "Flask-Mail",
        'pyquery'
        "Django",
        "djangorestframework",
        "Flask",
        "Flask-SQLAlchemy"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
