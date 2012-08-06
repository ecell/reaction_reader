CPP  = g++
OPTIONS = -g -lgsl -lgslcblas -Wall -DUNITTEST
OBJS = Gillespie.cpp

compile: Gillespie.hpp
	$(CPP) $(OBJS) $(OPTIONS)

build: setup.py Gillespie.hpp
	python setup.py build_ext --inplace

run:
	./a.out

clean:
	rm a.out
