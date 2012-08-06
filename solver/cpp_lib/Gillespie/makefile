CPP  = g++
OPTIONS = -g -lgsl -Wall -DUNITTEST
OBJS = Gillespie.cpp

compile: Gillespie.hpp
	$(CPP) $(OBJS) $(OPTIONS)

build: setup.py
	python setup.py build_ext --inplace

run:
	./a.out

clean:
	rm a.out
