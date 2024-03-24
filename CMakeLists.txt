cmake_minimum_required(VERSION 3.12)
project(clox)

include_directories(include)

file(GLOB C_SOURCES "src/*.c")

add_executable(clox ${C_SOURCES})