@echo on

set "CPLUS_INCLUDE_PATH=%LIBRARY_INC%;%CPLUS_INCLUDE_PATH%"
set "LIBRARY_PATH=%LIBRARY_LIB%;%LIBRARY_PATH%"

REM Point setup.py at conda-provided armadillo and BLAS/LAPACK
set "ARMADILLO_INCLUDE_DIR=%LIBRARY_INC%"
set "ARMADILLO_LIB_DIR=%LIBRARY_LIB%"

REM Debug: list available library files to diagnose BLAS/LAPACK linking
echo "=== Available .lib files in %LIBRARY_LIB% ==="
dir "%LIBRARY_LIB%\*.lib" 2>nul
echo "=== MKL-related .lib files ==="
dir "%LIBRARY_LIB%\mkl*.lib" 2>nul
dir "%LIBRARY_LIB%\blas*.lib" 2>nul
dir "%LIBRARY_LIB%\lapack*.lib" 2>nul
echo "=== End library listing ==="

%PYTHON% -m pip install . -vv --no-deps --no-build-isolation
if errorlevel 1 exit 1
