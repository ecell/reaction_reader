import numpy


class SimulatorBase(object):
    def __init__(self):
        self.solver = None

    def initialize(self, m, w, reaction_network=None):
        self.model, self.world = w

        if reaction_network is None:
            self.reaction_network = self.model.generate_reaction_network(
                self.world.get_species(), maxiter)
        else:
            self.reaction_network = reaction_network

    def get_current_time(self):
        pass

    def log_data(self):
        pass

    def get_logged_data(self):
        pass

    def run(self, duration):
        pass



