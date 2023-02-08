.PHONY: all run

TARGET := clox
CMAKE_FLAGS := -DCMAKE_BUILD_TYPE=Debug

all: 
	@rm -rf build
	@cmake $(CMAKE_FLAGS) -B build
	@cmake --build build

run: all
	./build/$(TARGET)

gdb: all
	gdb ./build/$(TARGET) -tui

