import numpy as np
import SimulatorBase
import solver.GillespieSolver
from model.Species import Species 
from model.Model import Model


class GillespieSimulator(SimulatorBase.SimulatorBase):
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
        return self.solver.get_current_time()

    def step(self, n = 1):
        dt = 0.0
        for _ in range(n):
            dt += self.solver.step()
        return dt

    def run(self, duration):
        return self.solver.run(duration)

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
            self.list_index2id.append(sp_id)

        #phase 2
        for r in self.reaction_network:
            solver_react_number = self.solver.reaction_add()
            for one_reaction in r.reactions:
                for one_reactant in one_reaction.reactants:
                    self.solver.reaction_add_substance(solver_react_number, 
                            self.dict_id2index[one_reactant.id], 1)

                for one_product in one_reaction.products:
                    self.solver.reaction_add_product(solver_react_number, 
                            self.dict_id2index[one_product.id], 1)

            # XXX 
            if hasattr(r,"k") is None:
                self.solver.reaction_set_kinetic_parameter(
                        solver_react_number, 0.5 )
            else:
                self.solver.reaction_set_kinetic_parameter(
                        solver_react_number, 0.5 )

        #prase 3
        array = np.empty(len(self.dict_id2index), np.int32)
        # XXX fill array by world.
        import pdb; pdb.set_trace() 
        for idx in range(len(self.dict_id2index)):
#            array[idx] = self.world.get_value(self.list_index2id[idx])
            array[idx] = 1000
        
        self.solver.set_current_state(array)
        
    def get_current_state(self):
        current_state_array = np.empty(len(self.dict_id2index), np.int32)
        self.solver.get_current_state(current_state_array)
        return current_state_array

