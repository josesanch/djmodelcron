# encoding: utf-8
from distutils.core import setup

from setuptools import find_packages

import djmodelcron

setup(
    name='djmodelcron',
    version=djmodelcron.VERSION,
    author='José Sánchez Moreno',
    author_email='jose@o2w.es',
    packages=find_packages(),
    license='MIT',
    description=u'Generic cron task for running instances of django models',
    long_description=open('README.rst').read(),
    url='https://github.com/josesanch/djmodelcron',
    platforms="All platforms",
    install_requires=[
        'celery',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: SQL',
    ],

)
