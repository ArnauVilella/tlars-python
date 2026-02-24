@echo on

set "CPLUS_INCLUDE_PATH=%LIBRARY_INC%;%CPLUS_INCLUDE_PATH%"
set "LIBRARY_PATH=%LIBRARY_LIB%;%LIBRARY_PATH%"

%PYTHON% -m pip install . -vv --no-deps --no-build-isolation
if errorlevel 1 exit 1
