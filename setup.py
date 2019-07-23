import awkg
from pathlib import Path

from setuptools import setup

long_description = Path('README.md').read_text(encoding='utf-8', errors='ignore')

classifiers = [  # copied from https://pypi.org/classifiers/
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Text Processing',
    'Topic :: Utilities',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Filters',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
]

setup(
    name='awkg',
    version=awkg.__version__,
    description=awkg.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=classifiers,
    python_requires='>=3.5',
    url='https://github.com/thammegowda/awkg',
    download_url='https://github.com/thammegowda/awkg',
    platforms=['any'],
    author='Thamme Gowda',
    author_email='tgowdan@gmail.com',
    packages=['awkg'],  # for a single .py file, use py_modules=[]
    entry_points={
        'console_scripts': ['awkg=awkg:AWKG.main'],
    },
)

