'''
$Header: /home/takeuchi/0613/process/process.py,v 1.10 2012/02/10 01:18:12 takeuchi Exp $
'''

from rate_functions import MassActionFluxProcess, MichaelisUniUniFluxProcess


class Function(object):
    def __init__(self):
        self.process_coef_pairs = []

    def add_process(self, process, coef):
        self.process_coef_pairs.append((process, coef))

    def __fire_processes(self, variable_array, time):
        for process, coef in self.process_coef_pairs:
            yield coef * process(variable_array, time)

    def __call__(self, variable_array, time):
        return sum(self.__fire_processes(variable_array, time)) + 0.0

    def __str__(self):
        retval = '[%s]' % (', '.join([
                    '{process: %s, coef: %s}' % (process, coef)
                    for process, coef in self.process_coef_pairs]))
        return retval

class FunctionMaker(object):
    def make_functions(self, w, reaction_results, rate_reactions={}):
        '''Make functions from model
        '''
        __rate_reactions = dict(mass_action=MassActionFluxProcess,
                                michaelis_uni_uni=MichaelisUniUniFluxProcess)
        __rate_reactions.update(rate_reactions)

        sid_list = w.get_species()

        # initialize function list
        functions = []
        for i in range(w.size()):
            function = Function()
            functions.append(function)

        # the correspondence between indices and elements 
        # (species or volumes) should be hidden in world object.
        idx_map, widx = {}, len(sid_list)
        for idx, sid in enumerate(sid_list):
            idx_map[sid] = idx

        for result in reaction_results:
            r = result.reaction_rule

            for reaction in result.reactions:
                # print reaction.str_simple()
                reactants = []
                for reactant in reaction.reactants:
                    reactants.append(
                        dict(id=idx_map[reactant.id], coef=1, vid=widx))

                products = []
                for product in reaction.products:
                    products.append(
                        dict(id=idx_map[product.id], coef=1, vid=widx))

                # r['effectors'] -> reaction['effectors']?
                effectors = []
                for effector in r['effectors']:
                    # for sid in sid_list:
                    #     species = m.concrete_species[sid]
                    #     if effector.matches(species):
                    #         effectors.append(
                    #             {'id': idx_map[sid], 'coef': 0})
                    # coef has no mean for effectors
                    effectors.append(
                        dict(id=idx_map[effector.id], coef=0, vid=widx))

                if r['func_def'] is None:
                    process_name, args, kwargs = (
                        r['k_name'], r['args'], r['kwargs'])

                    if process_name in __rate_reactions.keys():
                        process = __rate_reactions[process_name](
                            reactants, products, effectors, args, kwargs)
                    else:
                        raise Exception('Unsupported process: %s' % (
                                process_name))
                else:
                    process = r['func_def'](
                        reactants, products, effectors)
    
                for reactant in reactants:
                    functions[reactant['id']].add_process(
                        process, -reactant['coef'])
                for product in products:
                    functions[product['id']].add_process(
                        process, +product['coef'])
    
        return functions
