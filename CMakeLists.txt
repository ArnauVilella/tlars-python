cmake_minimum_required(VERSION 3.10)
project(tlars)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Find Eigen
find_package(Eigen3 3.3 REQUIRED NO_MODULE)
include_directories(/usr/include/eigen3)

# Add the extension module
pybind11_add_module(_tlars_cpp 
    tlars/src/tlars_cpp.cpp
    tlars/src/tlars_wrapper.cpp
)

# Link against Eigen
target_link_libraries(_tlars_cpp PRIVATE Eigen3::Eigen)

# Include directories
target_include_directories(_tlars_cpp PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/tlars/src
    ${EIGEN3_INCLUDE_DIR}
    /usr/include/eigen3
) 