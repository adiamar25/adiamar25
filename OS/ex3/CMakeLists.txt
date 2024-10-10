cmake_minimum_required(VERSION 3.22)
project(ex3)

set(CMAKE_CXX_STANDARD 20)

add_executable(ex3 main.cpp
        Resources/MapReduceClient.h
        Resources/MapReduceFramework.h)
