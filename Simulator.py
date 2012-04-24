import numpy

import solver.ODESolver
import Function


class Simulator(object):
    def __init__(self):
        self.__next_time = 0.0
        self.__dimension = 0
        self.__dimension_algebraic = 0
        self.outputs_series = []

        self.solver = None

    def initialize(self, solver, functions, variables, variables_algebraic=[]):
        '''Initialize solver

        1. Set variables.
        2. Initialize global time.
        3. Clear outputs.
        4. Set functions.
        '''
        if len(functions) != len(variables) + len(variables_algebraic):
            print 'The number of functions and the number of variables', \
                  'must be equal.'
            return -1

        self.solver = solver

        self.__dimension = len(variables)
        variable_array = numpy.array(variables)
        if variables_algebraic != []:
            # For DAESolver
            self.__dimension_algebraic = len(variables_algebraic)
            self.__dimension += self.__dimension_algebraic
            variable_algebraic_array = numpy.array(variables_algebraic)
            self.solver.initialize(variable_array, variable_algebraic_array)
        else:
            self.__dimension_algebraic = 0
            self.solver.initialize(variable_array)

        # The first event must be scheduled at the current time (dt=0)
        self.__next_time = self.solver.get_current_time()
        self.outputs_series = []

        # Register Functions
        for function in functions:
            self.solver.register_function(function)

        return 0

    def log_data(self):
        '''Log the local time and the variables.'''
        outputs = numpy.array([self.solver.get_current_time()])
        variable_array = numpy.empty(self.__dimension)

        if self.__dimension_algebraic > 0:
            variable_differential_array = numpy.empty(
                self.__dimension - self.__dimension_algebraic)
            variable_algebraic_array = numpy.empty(self.__dimension_algebraic)
            self.solver.get_variable_differential_array(
                variable_differential_array)
            self.solver.get_variable_algebraic_array(
                variable_algebraic_array)
            variable_array = numpy.append(variable_differential_array,
                variable_algebraic_array)
        else:
            self.solver.get_variable_array(variable_array)

        outputs = numpy.append(outputs, variable_array)
        self.outputs_series.append(outputs)

    def get_logged_data(self):
        '''Get the logged data series.'''
        return numpy.array(self.outputs_series)

    def get_current_time(self):
        '''Get the current time.'''
        if self.solver is not None:
            return self.solver.get_current_time()
        else:
            return 0.0

    def get_variable(self, idx):
        '''Get a variable value.'''
        return self.solver.get_variable(idx)

    def __step(self):
        self.solver.integrate(self.__next_time)
        state_event = self.solver.step()
        self.__next_time = self.solver.reschedule()
        self.log_data()
        return state_event

    def step(self, n=1):
        '''Solve n step.'''
        try:
            for i in range(n):
                if self.__step() != 0:
                    break
        except:
            pass

    def run(self, duration):
        '''Run the solver'''
        if duration < 0: return

        stop_time = self.get_current_time() + duration
        try:
            while self.__next_time <= stop_time:
                if self.__step() != 0:
                    break
            if self.get_current_time() < stop_time:
                self.__next_time = stop_time
                self.__step()
        except:
            pass

    def register_status_event(self, status_event_list):
        '''Register status events.

        status_event_list = [status event 1, ..., status event N]
            status event is a dictionary register following attribute.
            'id': index of variable array.
            'thres': if variable value is reached this value,
                     the event is araised.
            'code': status code for this status event.
            'flag': 0 indicate the variables_differential,
                    1 indicate the variables_algebraic.
        '''
        for status_event in status_event_list:
            self.solver.register_status_event(status_event)

class ODESimulator(Simulator):
    def __init__(self, m, w, reaction_network=None, maxiter=10, ratelaws={}):
        super(ODESimulator, self).__init__()

        # self.world is not udpated during the simulation
        # now this is just for the initialization
        self.model, self.world = m, w

        if reaction_network is None:
            self.reaction_network = self.model.generate_reaction_network(
                self.world.get_species(), maxiter)
        else:
            self.reaction_network = reaction_network

        # self.ratelaws = ratelaws
        fmaker = Function.FunctionMaker()
        # self.functions = fmaker.make_functions(
        #     self.model, reaction_network, self.world.volume)
        self.functions = fmaker.make_functions(
            self.world, self.reaction_network, ratelaws=ratelaws)
        self.initialize(solver.ODESolver.ODESolver(), 
                        self.functions, self.world.data)

    def get_species(self):
        # this method returns a list of species objects,
        # but not of species IDs.
        return [self.model.concrete_species[sid]
                for sid in self.world.get_species()]

    def get_min_step_interval(self):
        return self.solver.get_min_step_interval()

    def set_min_step_interval(self, value):
        self.solver.set_min_step_interval(value)

    def get_max_step_interval(self):
        return self.solver.get_max_step_interval()

    def set_max_step_interval(self, value):
        self.solver.set_max_step_interval(value)

    def get_tolerance(self):
        return self.solver.get_tolerance()

    def set_tolerance(self, value):
        self.solver.set_tolerance(value)

    def get_absolute_tolerance_factor(self):
        return self.solver.get_absolute_tolerance_factor()

    def set_absolute_tolerance_factor(self, value):
        self.solver.set_absolute_tolerance_factor(value)

    def get_derivative_tolerance_factor(self):
        return self.solver.get_derivative_tolerance_factor()

    def set_derivative_tolerance_factor(self, value):
        self.solver.set_derivative_tolerance_factor(value)

    def get_state_tolerance_factor(self):
        return self.solver.get_state_tolerance_factor()

    def set_state_tolerance_factor(self, value):
        self.solver.set_state_tolerance_factor(value)
