from setuptools import setup, Extension
import numpy as np

tlars_extension = Extension(
    'tlars._tlars_cpp',
    sources=['tlars/src/tlars_cpp.cpp', 'tlars/src/tlars_wrapper.cpp'],
    include_dirs=[
        np.get_include(),
        '/usr/include/eigen3',
        '/usr/include/python3.12',
        '/usr/include/pybind11'
    ],
    extra_compile_args=['-std=c++11'],
    language='c++'
)

setup(
    name='tlars',
    version='0.1.0',
    description='Python implementation of the tlars package',
    author='Original: Jasin Machkour, Python port: Arnau Vilella',
    author_email='avp@connect.ust.hk',
    packages=['tlars'],
    ext_modules=[tlars_extension],
    install_requires=[
        'numpy>=1.19.0'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Statistics',
    ],
) 