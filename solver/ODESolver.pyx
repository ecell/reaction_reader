'''
$Header: /home/takeuchi/0613/solver/ODESolver.pyx,v 1.2 2011/10/06 01:42:02 takeuchi Exp takeuchi $
'''

__all__ = ["ODESolver"]

cdef extern from "Defs.hpp":
    ctypedef struct StatusEvent:
        long int variable_index
        double threshold
        long int status_code

cdef extern from "Function.hpp":
    ctypedef struct c_Function "Function":
        pass

cdef extern from "PythonFunction.hpp":
    ctypedef struct c_PythonFunction "PythonFunction":
        pass
    c_PythonFunction *new_PythonFunction "new PythonFunction"(object)
    void del_PythonFunction "delete"(c_PythonFunction*) 

cdef extern from "numpy/ndarrayobject.h":
    void import_array() 

cdef extern from "numpy/arrayobject.h":
    ctypedef int intp
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags


cdef extern from "ODESolver.hpp":
    ctypedef struct c_Solver "ODESolver":
        void register_status_event(StatusEvent)
        void register_function(c_Function*)
        void initialize(double*, long int)
        void get_variable_array(double*, long int)
        double get_value(long int)
        double get_current_time()
        long int step()
        void integrate(double)
        double reschedule()
        void set_next_time(double)
        double get_step_interval()
        void set_step_interval(double)
        double get_next_time()
        double get_tolerance()
        double set_tolerance(double)
        double get_absolute_tolerance_factor()
        double set_absolute_tolerance_factor(double)
        double get_derivative_tolerance_factor()
        double set_derivative_tolerance_factor(double)
        double get_state_tolerance_factor()
        double set_state_tolerance_factor(double)
    c_Solver *new_Solver "new ODESolver"()
    void del_Solver "delete"(c_Solver*) 

cdef extern from "CallStep.hpp":
    ctypedef struct StepResult:
        long int state_event
        int err
    StepResult call_step(c_Solver *)


cdef class ODESolver:
    '''Wrapper class of ODESolver'''
    cdef c_Solver *thisptr

    def __cinit__(self):
        self.thisptr = new_Solver()

    def __del__(self):
        del_Solver(self.thisptr)

    def register_function(self, callable):
        '''Set a first order ordinal diferential equation.'''
        cdef c_PythonFunction* pyfun = new_PythonFunction(callable)
        self.thisptr.register_function(<c_Function*>pyfun)

    def initialize(self, ndarray py_variable_array):
        '''Initialize solver
        Set variables.
        '''
        cdef double *variable_array = <double *>py_variable_array.data
        cdef int dimension = py_variable_array.dimensions[0]
        self.thisptr.initialize(variable_array, dimension)

    def get_variable_array(self, ndarray py_variable_array):
        '''Get the variables.'''
        cdef double *variable_array = <double *>py_variable_array.data
        cdef int dimension = py_variable_array.dimensions[0]
        self.thisptr.get_variable_array(variable_array, dimension)

    def get_variable(self, index):
        '''Get the variable value specified by index.'''
        return self.thisptr.get_value(index)

    def get_current_time(self):
        '''Get the current time.'''
        return self.thisptr.get_current_time()

    def get_step_interval(self):
        '''Get the current step interval.'''
        return self.thisptr.get_step_interval()

    def integrate(self, a_time):
        '''Integrate'''
        self.thisptr.integrate(a_time)

    def step(self):
        '''Solve one step.'''
        cdef StepResult step_result
        step_result = call_step(self.thisptr)
        if step_result.err:
            raise Exception
        return step_result.state_event

    def reschedule(self):
        '''Schedule the next time.'''
        return self.thisptr.reschedule()

    def register_status_event(self, py_status_event):
        '''Register a status event'''
        cdef StatusEvent status_event
        status_event.variable_index = py_status_event['id']
        status_event.threshold = py_status_event['thres']
        status_event.status_code = py_status_event['code']
        self.thisptr.register_status_event(status_event)

    def set_next_time(self, hoge):
        '''set next time'''
        self.thisptr.set_next_time(hoge)

    def set_step_interval(self, a_time):
        '''Set the step interval.'''
        self.thisptr.set_step_interval(a_time)

    def get_next_time(self):
        '''Get the next time.'''
        return self.thisptr.get_next_time()

    def get_tolerance(self):
        return self.thisptr.get_tolerance()

    def set_tolerance(self, value):
        self.thisptr.set_tolerance(value)

    def get_absolute_tolerance_factor(self):
        return self.thisptr.get_absolute_tolerance_factor()

    def set_absolute_tolerance_factor(self, value):
        self.thisptr.set_absolute_tolerance_factor(value)

    def get_derivative_tolerance_factor(self):
        return self.thisptr.get_derivative_tolerance_factor()

    def set_derivative_tolerance_factor(self, value):
        self.thisptr.set_derivative_tolerance_factor(value)

    def get_state_tolerance_factor(self):
        return self.thisptr.get_state_tolerance_factor()

    def set_state_tolerance_factor(self, value):
        self.thisptr.set_state_tolerance_factor(value)

import_array()
