'''
$Header: /home/takeuchi/0613/process/process.py,v 1.10 2012/02/10 01:18:12 takeuchi Exp $
'''
import inspect
import sys

# Avogadro's number
# N_A = 6.0221367e+23


def MassAction(*args):
    # args is required to be (k, )
    return ["MassAction", args]

def MichaelisUniUni(*args):
    # args is required to be (KmS, KmP, KcF, KcR, volume)
    return ["MichaelisUniUni", args]

class FluxProcess(object):
    # def conc(self, sp):
    #     '''returns values of species in sp_list which has species idx
    #     '''
    #     # return [va[i] for i in sp_list]
    #     # (args, varargs, varkw, locals) = inspect.getargvalues(frame)
    #     va = inspect.getargvalues(
    #         inspect.stack()[2][0]).locals['variable_array']
    #     return va[sp['id']]

    def exit_with_message(self, msng=None):
        if msg is not None:
            sys.stdout.write('%s\n' % msg)
        sys.exit()

class MassActionFluxProcess(FluxProcess):
    def __init__(self, reactants, products, effectors, args):
        # self.reactants, self.products, self.effectors = (
        #     reactants, products, effectors)
        self.reactants = reactants

        self.k_value, self.volume = args

    def __call__(self, variable_array, time):
        velocity = self.k_value * self.volume
        for r in self.reactants:
            coefficient = r['coef']
            value = variable_array[r['id']] / self.volume
            while coefficient > 0:
                velocity *= value
                coefficient -= 1
        return velocity

    def __str__(self):
        retval = 'MassActionFluxProcess('
        retval += 'k=%f, volume=%f, ' % (self.k_value, self.volume)
        retval += 'reactants=%s' % self.reactants
        retval += ')'
        return retval

class MichaelisUniUniFluxProcess(FluxProcess):
    def __init__(self, reactants, products, effectors, args):
        self.reactants, self.products, self.effectors = (
            reactants, products, effectors)

        self.KmS, self.KmP, self.KcF, self.KcR, self.volume = args

        # Get Species' name
        # print [x.str_simple() for x in self.species.values()]
        # for i, v in enumerate(species): print i+1, species[v].str_simple()

        # Get Reactors' name
        # print [i.str_simple() for i in effectors]

        if len(self.reactants) != 1 or len(self.products) != 1:
            self.exit_with_message(
                "the numbers of reactants and products must be 1.")

    def __call__(self, variable_array, time):
        # for i, v in enumerate(self.species):
        #     print self.species[v].str_simple(), variable_array[i]
        # def molar_conc(sp):
        #     """${3:function documentation}"""
        #     n = self.conc(sp)
        #     conc_v = n / self.volume
        #     mol_conc = conc_v / N_A
        #     return mol_conc

        S = variable_array[self.reactants[0]['id']] / self.volume
        P = variable_array[self.products[0]['id']] / self.volume
        E = variable_array[self.effectors[0]['id']] / self.volume

        # velocity = self.KcF * E * S / (self.KmS + S)
        velocity = self.KcF * S - self.KcR * P
        velocity /= self.KmS * self.KmP + self.KmP * S + self.KmS * P
        velocity *= self.volume
        return velocity

    def __str__(self):
        retval = 'MichaelisUniUniFluxProcess('
        retval += 'KmS=%f, KmP=%f, KcF=%f, KcR=%f, volume=%f, ' % (
            self.KmS, self.KmP, self.KcF, self.KcR, self.volume)
        retval += 'reactants=%s, ' % self.reactants
        retval += 'products=%s, ' % self.products
        retval += 'effectors=%s' % self.effectos
        retval += ')'
        return retval

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
    def make_functions(self, m, reaction_results):
        '''Make functions from model
        '''
        sid_list = m.concrete_species.keys()

        # initialize function list
        functions = []
        for i in range(len(sid_list)):
            function = Function()
            functions.append(function)

        vid_map = {}
        for vid, sid in enumerate(sid_list):
            vid_map[sid] = vid

        for result in reaction_results:
            r = result.reaction_rule

            for reaction in result.reactions:
                # print reaction.str_simple()
                reactants = []
                for reactant in reaction.reactants:
                    reactants.append(
                        {'id': vid_map[reactant.id], 'coef': 1})

                products = []
                for product in reaction.products:
                    products.append(
                        {'id': vid_map[product.id], 'coef': 1})

                # r['effectors'] -> reaction['effectors']?
                effectors = []
                for effector in r['effectors']:
                    for sid in sid_list:
                        species = m.concrete_species[sid]
                        if effector.matches(species):
                            # coef has no mean for effectors
                            effectors.append(
                                {'id':  vid_map[sid], 'coef': 0})

                if r['func_def'] is None:
                    # todo!!: move user function definition
                    process_name = r['k_name']
                    # todo!!: (re)move "volume" paramter
                    if process_name == 'MassAction':
                        volume = 1
                        args = r['k'] + (volume, )
                        process = MassActionFluxProcess(
                            reactants, [], [], args)
                        # process = MassActionFluxProcess(
                        #     reactants, products, effectors, args)
                    elif process_name == 'MichaelisUniUni':
                        process = MichaelisUniUniFluxProcess(
                            reactants, products, effectors, r['k'])
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
