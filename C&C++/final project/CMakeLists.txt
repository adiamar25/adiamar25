cmake_minimum_required(VERSION 3.22)
project(final_project)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(final_project
        vl_vector.hpp
        presubmit.cpp
        vl_string.hpp
        #        append_string.cpp
)
