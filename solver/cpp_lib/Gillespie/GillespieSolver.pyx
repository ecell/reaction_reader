import numpy as np
cimport numpy as np 

cdef extern from "Gillespie.hpp":
    ctypedef struct c_Solver "GillespieSolver":
        double step()
        double duration(double)
        void set_current_time(double)
        double get_current_time()
        int  get_current_state(int*,int)
        void set_current_state(int*,int)
        int  reaction_add()
        void reaction_add_substance(int,int,int)
        void reaction_add_product(int,int,int)
        void reaction_set_kinetic_parameter(int,double)
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

    def reaction_add(self):
        return self.thisptr.reaction_add()

    def reaction_add_substance(self,react_id,specie_index, stoichiometry):
        self.thisptr.reaction_add_substance(react_id,specie_index,stoichiometry)

    def reaction_add_product(self,react_id,specie_index,stoichiometry):
        self.thisptr.reaction_add_product(react_id,specie_index,stoichiometry)

    def reaction_set_kinetic_parameter(self,react_id,k):
        self.thisptr.reaction_set_kinetic_parameter(react_id,k)

    def set_current_state(self, np.ndarray py_array):
        cdef int *int_array = <int *>py_array.data
        #cdef int length = py_array.dimensions[0]
        cdef int length = len(py_array)
        self.thisptr.set_current_state(int_array, length)

    def get_current_state(self, np.ndarray py_array):
        cdef int *int_array = <int *>py_array.data 
        #cdef int length = py_array.dimentions[0]
        cdef int length = len(py_array)
        self.thisptr.get_current_state(int_array, length)
