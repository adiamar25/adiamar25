cmake_minimum_required(VERSION 3.22)
project(ex2)

set(CMAKE_CXX_STANDARD 17)

add_executable(ex2 main.cpp
        uthreads.h
        thread.h
        uthreads.cpp
        thread.cpp)
