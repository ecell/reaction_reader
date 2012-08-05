
cdef extern from "Gillespie.hpp":
    ctypedef struct c_Solver "GillespieSolver":
        double step()
        void set_current_time(double)
        double get_current_time()
        double duration(double)
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

    def duration(self,dt):
        return self.thisptr.duration(dt)

    def get_current_time(self):
        return self.thisptr.get_current_time()

    def set_current_time(self,new_t):
        self.thisptr.set_current_time(new_t)
