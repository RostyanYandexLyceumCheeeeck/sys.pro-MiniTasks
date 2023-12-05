.PHONY: all clean

all: ./build
	./run.sh

./build: foreignmodule.c
	python3 setup.py build

clean:
	python3 setup.py clean