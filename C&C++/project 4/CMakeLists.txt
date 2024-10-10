cmake_minimum_required(VERSION 3.22)
project(ex4)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ex4
        Activation.h
        Dense.h
        main.cpp
        Matrix.h
        MlpNetwork.h
        MlpNetwork.cpp
        Matrix.cpp
        Dense.cpp
        Activation.cpp
        main.cpp
)
