import numpy


class Simulator:
    def __init__(self):
        self.__next_time = 0.0
        self.dimension = 0
        self.dimension_algebraic = 0
        self.outputs_series = []
        self.solver = None

    # def make_functions(self, model, reaction_results, volume):
    #     '''Make functions from model
    #     '''
    #     from process.process import FunctionMaker
    #     function_maker = FunctionMaker()
    #     return function_maker.make_functions(model, reaction_results, volume)

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

        self.dimension = len(variables)
        variable_array = numpy.array(variables)
        if variables_algebraic != []:
            # For DAESolver
            self.dimension_algebraic = len(variables_algebraic)
            self.dimension += self.dimension_algebraic
            variable_algebraic_array = numpy.array(variables_algebraic)
            self.solver.initialize(variable_array, variable_algebraic_array)
        else:
            self.dimension_algebraic = 0
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
        variable_array = numpy.empty(self.dimension)

        if self.dimension_algebraic > 0:
            variable_differential_array = numpy.empty(
                self.dimension - self.dimension_algebraic)
            variable_algebraic_array = numpy.empty(self.dimension_algebraic)
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
