from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import setuptools
import numpy as np
import platform
import glob

__version__ = '0.7.14'

# Prepare environment for compilation
include_dirs = [
    "pybind11/include",
    "carma/include",
    "/usr/include",
    "src",
    np.get_include(),
]

# Check for Armadillo from environment variables
armadillo_include = os.environ.get('ARMADILLO_INCLUDE_DIR', '').strip()
if armadillo_include:
    include_dirs.append(armadillo_include)
elif platform.system() == 'Windows':
    include_dirs.append(os.path.join('C:', os.sep, 'armadillo', 'include'))

libraries = []
library_dirs = []

skip_linking = platform.system() == 'Windows' and os.environ.get('SKIP_ARMADILLO_LINKING', '').strip() == '1'
use_openblas = platform.system() == 'Windows' and os.environ.get('USE_OPENBLAS', '').strip() == '1'

if platform.system() == 'Windows' and not skip_linking:
    armadillo_lib = os.environ.get('ARMADILLO_LIB_DIR', '').strip()
    if armadillo_lib:
        library_dirs.append(armadillo_lib)
        libraries.append('armadillo')

        # Auto-detect BLAS/LAPACK library (needed to resolve symbols from armadillo.lib)
        lib_files = glob.glob(os.path.join(armadillo_lib, '*.lib'))
        blas_found = False
        blas_candidates = ['mkl_rt', 'mkl_rt.2', 'mkl_rt.1', 'blas', 'openblas', 'cblas', 'libblas']
        for candidate in blas_candidates:
            candidate_path = os.path.join(armadillo_lib, candidate + '.lib')
            if os.path.isfile(candidate_path):
                libraries.append(candidate)
                blas_found = True
                break

        # Fallback: glob for any mkl_rt*.lib file
        if not blas_found:
            mkl_libs = glob.glob(os.path.join(armadillo_lib, 'mkl_rt*.lib'))
            if mkl_libs:
                mkl_lib_name = os.path.splitext(os.path.basename(mkl_libs[0]))[0]
                libraries.append(mkl_lib_name)
                blas_found = True

        # Fallback: scan for any BLAS-like library
        if not blas_found:
            for f in lib_files:
                basename = os.path.basename(f).lower()
                if any(name in basename for name in ['blas', 'lapack', 'mkl', 'openblas']):
                    lib_name = os.path.splitext(os.path.basename(f))[0]
                    libraries.append(lib_name)
                    blas_found = True
                    break

        # Check for separate lapack library (not needed if using MKL which includes LAPACK)
        if blas_found and not any('mkl' in lib for lib in libraries):
            for candidate in ['lapack', 'liblapack']:
                candidate_path = os.path.join(armadillo_lib, candidate + '.lib')
                if os.path.isfile(candidate_path):
                    libraries.append(candidate)
                    break
    else:
        libraries.append('armadillo')
        lib_path = os.path.join('C:', os.sep, 'armadillo', 'lib')
        library_dirs.append(lib_path)
elif skip_linking and use_openblas:
    blas_dir = os.environ.get('BLAS_LAPACK_DIR', '').strip()
    if blas_dir:
        library_dirs.append(blas_dir)
        libraries.append('openblas')
    else:
        openblas_dir = os.environ.get('OPENBLAS_HOME', '').strip()
        if openblas_dir:
            for root, dirs, files in os.walk(openblas_dir):
                for file in files:
                    if file.endswith('.lib'):
                        lib_dir = os.path.dirname(os.path.join(root, file))
                        library_dirs.append(lib_dir)
                        lib_name = os.path.splitext(file)[0]
                        libraries.append(lib_name)
                        break
                if libraries:
                    break
elif platform.system() == 'Darwin':
    pass  # macOS: use the Accelerate framework
elif platform.system() != 'Windows':
    libraries.extend(['armadillo', 'blas', 'lapack'])

arma_no_blas = os.environ.get('ARMA_NO_BLAS', '').strip() == '1'

define_macros = [
    ("ARMA_USE_EXTERN_CXX11_RNG", "1"),
]

if platform.system() == 'Darwin':
    define_macros.append(("ARMA_USE_BLAS", "1"))
    define_macros.append(("ARMA_USE_LAPACK", "1"))
    define_macros.append(("ARMA_DONT_USE_WRAPPER", "1"))
elif arma_no_blas:
    define_macros.append(("ARMA_DONT_USE_BLAS", "1"))
    define_macros.append(("ARMA_DONT_USE_LAPACK", "1"))
    define_macros.append(("ARMA_DONT_USE_WRAPPER", "1"))

extra_link_args_ext = []
if platform.system() == 'Darwin':
    extra_link_args_ext = ['-framework', 'Accelerate']

ext_modules = [
    Extension(
        'tlars.tlars_cpp',
        ['src/tlars_cpp_pybind.cpp', 'src/tlars_cpp.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        define_macros=define_macros,
        extra_link_args=extra_link_args_ext,
        language='c++'
    ),
]


def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    import os
    with tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False) as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        fname = f.name
    try:
        compiler.compile([fname], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
        return False
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass
    return True


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc', '/std:c++14'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append('-std=c++14')
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO="%s"' % self.distribution.get_version())

            if os.environ.get('ARMA_USE_EXTERN_CXX11_RNG', '').strip() == '1':
                opts.append('/DARMA_USE_EXTERN_CXX11_RNG')

            if os.environ.get('SKIP_ARMADILLO_LINKING', '').strip() == '1':
                for ext in self.extensions:
                    if 'armadillo' in ext.libraries:
                        ext.libraries.remove('armadillo')

            if os.environ.get('USE_OPENBLAS', '').strip() == '1':
                opts.append('/DARMA_USE_BLAS')
                opts.append('/DARMA_USE_LAPACK')

        for ext in self.extensions:
            ext.extra_compile_args = opts.copy()
            ext.extra_link_args = link_opts.copy()
            ext.define_macros = [(name, value) for name, value in ext.define_macros]

        build_ext.build_extensions(self)

setup(
    name='tlars',
    version=__version__,
    author='Arnau Vilella',
    author_email='avp@connect.ust.hk',
    url='https://github.com/ArnauVilella/tlars-python',
    description='Python port of the tlars R package by Jasin Machkour',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['numpy'],
    setup_requires=['pybind11>=2.12', 'numpy'],
    cmdclass={'build_ext': BuildExt},
    packages=['tlars'],
    zip_safe=False,
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
)
