cmake_minimum_required(VERSION 3.22)
project(Ex3a C)

set(CMAKE_C_STANDARD 99)

include_directories(.)

add_executable(Ex3a
        linked_list.c
        linked_list.h
        markov_chain.c
        markov_chain.h
        tweets_generator.c)
