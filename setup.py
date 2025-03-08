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

__version__ = '0.5.0'

# Detect platform
is_windows = sys.platform.startswith('win')

# Prepare environment for compilation
include_dirs = [
    "pybind11/include",
    "carma/include",
    "/usr/include",  # For Linux
    "src",
    np.get_include(),  # Add NumPy include directory explicitly
]

# Print NumPy include path for debugging
print(f"NumPy include path: {np.get_include()}")

# Check for Armadillo from environment variables
armadillo_include = os.environ.get('ARMADILLO_INCLUDE_DIR', '').strip()  # Strip any trailing spaces
if armadillo_include:
    include_dirs.append(armadillo_include)
    print(f"Using Armadillo include dir from environment: {armadillo_include}")
else:
    # Try to use hardcoded paths
    if platform.system() == 'Windows':
        include_dirs.append(os.path.join('C:', os.sep, 'armadillo', 'include'))
        print(f"Using hardcoded Windows Armadillo include path")

library_dirs = []
if platform.system() == 'Windows':
    # Ensure proper path format with backslash after C:
    lib_path = os.path.join('C:', os.sep, 'armadillo', 'lib')
    library_dirs.append(lib_path)
    print(f"Using hardcoded Windows Armadillo lib path: {lib_path}")

libraries = []
if platform.system() == 'Windows':
    libraries.append('armadillo')

# Define the extension module
ext_modules = [
    Extension(
        'tlars.tlars_cpp',
        ['src/tlars_cpp_pybind.cpp', 'src/tlars_cpp.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
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
            
            # Debugging information for Windows
            print(f"Compiler type: {ct}")
            print(f"Compiler flags: {opts}")
            print(f"Link flags: {link_opts}")
            
            # Add explicit include and library directories for Armadillo on Windows
            for ext in self.extensions:
                # Make sure NumPy include dir is in the includes
                numpy_include = np.get_include()
                if numpy_include not in ext.include_dirs:
                    ext.include_dirs.append(numpy_include)
                    print(f"Added NumPy include directory: {numpy_include}")
                
                if 'ARMADILLO_INCLUDE_DIR' in os.environ:
                    armadillo_include = os.environ['ARMADILLO_INCLUDE_DIR'].strip()  # Strip any trailing spaces
                    print(f"Using ARMADILLO_INCLUDE_DIR from environment: {armadillo_include}")
                    if armadillo_include not in ext.include_dirs:
                        ext.include_dirs.append(armadillo_include)
                else:
                    print("ARMADILLO_INCLUDE_DIR not found in environment, using default")
                    armadillo_path = os.path.join('C:', os.sep, 'armadillo', 'include')
                    if armadillo_path not in ext.include_dirs:
                        ext.include_dirs.append(armadillo_path)
                
                if 'ARMADILLO_LIBRARY' in os.environ:
                    lib_dir = os.path.dirname(os.environ['ARMADILLO_LIBRARY'])
                    print(f"Using lib directory from ARMADILLO_LIBRARY: {lib_dir}")
                    if lib_dir not in ext.library_dirs:
                        ext.library_dirs.append(lib_dir)
                else:
                    print("ARMADILLO_LIBRARY not found in environment, using default")
                    lib_path = os.path.join('C:', os.sep, 'armadillo', 'lib')
                    if lib_path not in ext.library_dirs:
                        ext.library_dirs.append(lib_path)
                
                if 'armadillo' not in ext.libraries:
                    ext.libraries.append('armadillo')
                
                # Clean up trailing spaces in include_dirs
                ext.include_dirs = [inc_dir.strip() if isinstance(inc_dir, str) else inc_dir 
                                    for inc_dir in ext.include_dirs]
                
                # Fix path formatting in library_dirs (ensure proper path separator)
                ext.library_dirs = [lib_dir.replace('C:/', 'C:\\').replace('C:', 'C:\\') 
                                    if isinstance(lib_dir, str) and lib_dir.startswith('C:') 
                                    else lib_dir for lib_dir in ext.library_dirs]
                
                print(f"Extension include_dirs: {ext.include_dirs}")
                print(f"Extension library_dirs: {ext.library_dirs}")
                print(f"Extension libraries: {ext.libraries}")

        for ext in self.extensions:
            ext.extra_compile_args += opts
            ext.extra_link_args += link_opts
        build_ext.build_extensions(self)

setup(
    name='tlars',
    version=__version__,
    author='Arnau Vilella',
    author_email='avp@connect.ust.hk',
    url='https://github.com/author/tlars-python',
    description='Python port of the tlars R package by Jasin Machkour',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0', 'numpy>=1.19.0', 'matplotlib>=3.3.0'],
    setup_requires=['pybind11>=2.6.0', 'numpy>=1.19.0'],
    cmdclass={'build_ext': BuildExt},
    packages=['tlars'],
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
    ],
)