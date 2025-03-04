from setuptools import setup, Extension
import numpy as np
import os
import sys
import platform

# Get environment variables for include directories
eigen_include_dir = os.environ.get('EIGEN_INCLUDE_DIR', '/usr/include/eigen3')
armadillo_include_dir = os.environ.get('ARMADILLO_INCLUDE_DIR', '/usr/include')

# Default include directories
include_dirs = [
    np.get_include(),
    eigen_include_dir,
    armadillo_include_dir,
]

# Add platform-specific include directories
if platform.system() == 'Windows':
    # For Windows, add vcpkg paths if available
    vcpkg_root = os.environ.get('VCPKG_ROOT')
    if vcpkg_root:
        include_dirs.extend([
            os.path.join(vcpkg_root, 'installed', 'x64-windows', 'include'),
            os.path.join(vcpkg_root, 'installed', 'x64-windows', 'include', 'eigen3'),
        ])
    # Add Python include directory
    if sys.version_info.major == 3:
        include_dirs.append(f'/usr/include/python3.{sys.version_info.minor}')
        include_dirs.append(f'C:\\Python3{sys.version_info.minor}\\include')
elif platform.system() == 'Darwin':  # macOS
    include_dirs.extend([
        '/usr/local/include',
        '/usr/local/include/eigen3',
        f'/usr/local/opt/python@3.{sys.version_info.minor}/Frameworks/Python.framework/Versions/3.{sys.version_info.minor}/include/python3.{sys.version_info.minor}m',
    ])
else:  # Linux
    include_dirs.extend([
        f'/usr/include/python3.{sys.version_info.minor}',
        '/usr/include/pybind11',
    ])

# Set compiler flags
extra_compile_args = ['-std=c++11']
if platform.system() == 'Windows':
    extra_compile_args = ['/std:c++11', '/EHsc']

tlars_extension = Extension(
    'tlars._tlars_cpp',
    sources=['tlars/src/tlars_cpp.cpp', 'tlars/src/tlars_wrapper.cpp'],
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
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