from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import setuptools
import numpy as np
import platform

# Add debugging information
print(f"sys.path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Environment variables:")
for k, v in os.environ.items():
    if 'ARM' in k.upper() or 'INCLUDE' in k.upper() or 'LIB' in k.upper():
        print(f"  {k}: {v}")

__version__ = '0.6.2'

import platform
import os
import subprocess

# Add platform detection
is_windows = sys.platform.startswith('win')
is_macos = sys.platform.startswith('darwin')
is_linux = sys.platform.startswith('linux')

# Detect architecture on macOS
is_arm64 = platform.machine() == 'arm64' if is_macos else False

# Prepare environment for compilation
include_dirs = [
    "pybind11/include",
    "carma/include",
    "/usr/include",  # For Linux
    "src",
    np.get_include(),  # Add NumPy include directory explicitly
]

# Set appropriate deployment target for macOS
if is_macos:
    # For arm64, we need at least macOS 11.0
    macosx_deployment_target = os.environ.get('MACOSX_DEPLOYMENT_TARGET', '')
    if not macosx_deployment_target:
        if is_arm64:
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '11.0'
        else:
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'  # For x86_64
    print(f"Using MACOSX_DEPLOYMENT_TARGET: {os.environ.get('MACOSX_DEPLOYMENT_TARGET')}")

# Platform-specific library configuration
libraries = []
library_dirs = []
extra_link_args = []

if is_windows:
    # Windows configuration (unchanged)
    if not skip_linking:
        libraries.append('armadillo')
        lib_path = os.path.join('C:', os.sep, 'armadillo', 'lib')
        library_dirs.append(lib_path)
    elif skip_linking and use_openblas:
        # OpenBLAS for Windows build (unchanged)
        blas_dir = os.environ.get('BLAS_LAPACK_DIR', '').strip()
        if blas_dir:
            library_dirs.append(blas_dir)
            libraries.append('openblas')
elif is_macos:
    # macOS-specific configuration
    # Use Accelerate framework instead of BLAS/LAPACK
    extra_link_args.extend(['-framework', 'Accelerate'])
    
    # Detect Armadillo from environment or Homebrew
    armadillo_include = os.environ.get('ARMADILLO_INCLUDE_DIR', '').strip()
    if armadillo_include:
        include_dirs.append(armadillo_include)
        print(f"Using Armadillo include from environment: {armadillo_include}")
    else:
        # Try to locate Armadillo via Homebrew
        try:
            brew_prefix = subprocess.check_output(['brew', '--prefix'], text=True).strip()
            arma_include_dir = os.path.join(brew_prefix, 'opt', 'armadillo', 'include')
            if os.path.exists(arma_include_dir):
                include_dirs.append(arma_include_dir)
                print(f"Found Armadillo include via Homebrew: {arma_include_dir}")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Homebrew not found or error finding Armadillo")
    
    # Define macOS-specific macros
    define_macros = [
        ("ARMA_USE_EXTERN_CXX11_RNG", "1"),
        ("ARMA_DONT_USE_WRAPPER", None),  # Necessary when using Accelerate
    ]
elif is_linux:
    # Linux configuration (unchanged)
    libraries.extend(['armadillo', 'blas', 'lapack'])

# Define the extension module
ext_modules = [
    Extension(
        'tlars.tlars_cpp',
        ['src/tlars_cpp_pybind.cpp', 'src/tlars_cpp.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        define_macros=define_macros,
        language='c++'
    ),
]

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
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

# A custom build extension for dealing with C++14 compiler requirements
class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc', '/std:c++14'],  # Use MSVC standard flag instead of GCC
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
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
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
            
            # Add Windows-specific flags for Armadillo - keeping only the necessary ones
            if os.environ.get('ARMA_USE_EXTERN_CXX11_RNG', '').strip() == '1':
                opts.append('/DARMA_USE_EXTERN_CXX11_RNG')
            
            # Debugging information for Windows
            print(f"Compiler type: {ct}")
            print(f"Compiler flags: {opts}")
            print(f"Link flags: {link_opts}")
        
            # Special handling for Windows when SKIP_ARMADILLO_LINKING=1
            if os.environ.get('SKIP_ARMADILLO_LINKING', '').strip() == '1':
                print("Windows build with SKIP_ARMADILLO_LINKING=1, removing armadillo from libraries")
                # Force remove armadillo from all extensions
                for ext in self.extensions:
                    if 'armadillo' in ext.libraries:
                        ext.libraries.remove('armadillo')
                        print(f"Removed armadillo from {ext.name} libraries: {ext.libraries}")
            
            # Add OpenBLAS flags if needed
            if os.environ.get('USE_OPENBLAS', '').strip() == '1':
                opts.append('/DARMA_USE_BLAS')
                opts.append('/DARMA_USE_LAPACK')
        
        for ext in self.extensions:
            ext.extra_compile_args = opts.copy()
            ext.extra_link_args = link_opts.copy()
            
            # Don't make any assumptions about STD_MUTEX
            # Just keep the macros as they are defined
            ext.define_macros = [(name, value) for name, value in ext.define_macros]
            
            # Print extension information for Windows
            if ct == 'msvc':
                print(f"Extension {ext.name} include_dirs: {ext.include_dirs}")
                print(f"Extension {ext.name} library_dirs: {ext.library_dirs}")
                print(f"Extension {ext.name} libraries: {ext.libraries}")
                print(f"Extension {ext.name} define_macros: {ext.define_macros}")
                
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
    install_requires=['pybind11>=2.6.0', 'numpy>=1.19.0', 'matplotlib>=3.3.0'],
    setup_requires=['pybind11>=2.6.0', 'numpy>=1.19.0', 'matplotlib>=3.3.0'],
    cmdclass={'build_ext': BuildExt},
    packages=['tlars'],
    zip_safe=False,
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
)