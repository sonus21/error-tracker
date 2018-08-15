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


file_text = read(fpath('flask_error/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='flask-error-monitor',
    version=grep('__version__'),
    url='https://github.com/sonus21/flask-error-monitor/',
    license='BSD',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Simple and Extensible Error Manager framework for Flask',
    long_description=desc(),
    packages=['flask_error', ],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        "Flask",
        "Flask-Mail",
        "Flask-SQLAlchemy",
    ],
    tests_require=[
        'pyquery',
        'nose'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector'
)
