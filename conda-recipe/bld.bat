@echo on

:: Remove vendored carma so the conda-forge host package is used instead
if exist carma rmdir /s /q carma

set "CPLUS_INCLUDE_PATH=%LIBRARY_INC%\carma;%LIBRARY_INC%;%CPLUS_INCLUDE_PATH%"
set "LIBRARY_PATH=%LIBRARY_LIB%;%LIBRARY_PATH%"

set "ARMADILLO_INCLUDE_DIR=%LIBRARY_INC%"
set "ARMADILLO_LIB_DIR=%LIBRARY_LIB%"

%PYTHON% -m pip install . -vv --no-deps --no-build-isolation
if errorlevel 1 exit 1
