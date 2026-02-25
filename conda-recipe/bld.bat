@echo on

set "CPLUS_INCLUDE_PATH=%LIBRARY_INC%;%CPLUS_INCLUDE_PATH%"
set "LIBRARY_PATH=%LIBRARY_LIB%;%LIBRARY_PATH%"

REM Point setup.py at conda-provided armadillo and BLAS/LAPACK
set "ARMADILLO_INCLUDE_DIR=%LIBRARY_INC%"
set "ARMADILLO_LIB_DIR=%LIBRARY_LIB%"

%PYTHON% -m pip install . -vv --no-deps --no-build-isolation
if errorlevel 1 exit 1
