
cdef extern from "Gillespie.hpp":
    ctypedef struct c_Solver "GillespieSolver":
        double step()
    c_Solver *new_solver "new GillespieSolver"()
    void delete_solver "delete" (c_Solver*)

cdef class GillespieSolver:
    cdef c_Solver *thisptr
    def __cinit__(self):
        self.thisptr = new_solver()

    def __del__(self):
        delete_solver(self.thisptr)

    def step(self):
        return self.thisptr.step()


