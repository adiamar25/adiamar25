cmake_minimum_required(VERSION 3.22)
project(ex5)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ex5
        Movie.cpp
        Movie.h
#        print_main.cpp
        RecommendationSystem.h
        RecommendationSystemLoader.cpp
        RecommendationSystemLoader.h
        User.cpp
        User.h
        UsersLoader.cpp
        UsersLoader.h
        RecommendationSystem.cpp
        presubmit.cpp
        presubmit.cpp)