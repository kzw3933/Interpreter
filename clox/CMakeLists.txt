cmake_minimum_required(VERSION 3.9)
project(clox)
include_directories(${CMAKE_CURRENT_DIR}/include)
add_executable(clox chunk.c compiler.c debug.c main.c memory.c scanner.c value.c vm.c)