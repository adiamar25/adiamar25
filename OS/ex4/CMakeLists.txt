cmake_minimum_required(VERSION 3.22)
project(ex4)

set(CMAKE_CXX_STANDARD 17)

add_executable(ex4
        MemoryConstants.h
        PhysicalMemory.h
        SimpleTest.cpp
        VirtualMemory.cpp
        VirtualMemory.h
        PhysicalMemory.cpp)
