cmake_minimum_required(VERSION 3.27)
project(Ex1 C)

set(CMAKE_C_STANDARD 99)

include_directories(.)

add_executable(Ex1
        cipher.c
        cipher.h
        main.c
        tests.c
        tests.h)
