.PHONY: all run

TARGET := clox

all: 
	@rm -rf build
	@cmake -B build
	@cmake --build build

run: 
	./build/$(TARGET)

