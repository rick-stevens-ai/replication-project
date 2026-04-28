CXX ?= mpiicpc
CXXFLAGS ?= -O3 -xHost -qopenmp -std=c++17 -Wall

all: wl3_mpi

wl3_mpi: wl3_mpi.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f wl3_mpi
