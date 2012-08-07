import numpy as np
import SimulatorBase
import solver.GillespieSolver
from model.Species import Species 
from model.Model import Model


class GillespieSimurator(SimulatorBase.SimulatorBase):
    def __init__(self, m, w, reaction_network=None, maxiter=10):
        self.solver = solver.GillespieSolver.GillespieSolver()
        self.model, self.world = m, w
        self.dict_id2index = {}     # Spicies id -> index 
        self.list_index2id = []     # index -> Specied id

        if reaction_network is None:
            self.reaction_network = self.model.generate_reaction_network(
                    self.world.get_specied(), maxiter)
        else:
            self.reaction_network = reaction_network


    def get_current_time(self):
        return self.get_current_time()

    def step(self, n = 1):
        for i in range(n):
            if self.step() == 0.0:
                break 

    def run(self, duration):
        self.run(duration)

    def get_current_time(self):
        if self.solver is not None:
            return self.solver.get_current_time()
        else:
            return 0.0

    def set_kinetic_parameter(self, reaction_num, k):
        self.solver.reaction_set_kinetic_parameter(reaction_num, k)

    def compile_reaction(self):
        '''
        Transrate reactionrule into  
        1, make dictionary to convert id into index
        2, regist reactinos.
        3, set_current_state
        '''
        #phase 1.
        for idx, sp_id in enumerate(self.model.concrete_species.iterkeys()):
            self.dict_id2index[sp_id] = idx
            self.list_index2id[idx] = sp_id

        #phase 2
        for r in self.reaction_network:
            solver_react_number = self.solver.reaction_add()
            for one_reactant in r.reactants:
                self.solver.reaction_add_substance(solver_react_number, self.dict_id2index[one_reactant], 1)

            for one_product in r.products:
                self.solver.reaction_add_product(solver_react_number, self.dict_id2index[one_product], 1)

        #prase 3
        array = np.empty(len(self.id2index), np.int32)
        # XXX fill array by world.
        for idx in range(len(self.id2index)):
            array[idx] = self.w.get_value(list_index2id[idx])
        
        self.solver.set_current_state(array)
        
