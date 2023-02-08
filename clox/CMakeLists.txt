cmake_minimum_required(VERSION 3.9)
project(clox)
include_directories(${CMAKE_CURRENT_DIR}/include)
add_executable(clox vm.c chunk.c debug.c main.c  compiler.c   memory.c scanner.c value.c object.c)