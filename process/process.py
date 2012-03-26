'''
$Header: /home/takeuchi/0613/process/process.py,v 1.10 2012/02/10 01:18:12 takeuchi Exp $
'''
import inspect
import sys

# Avogadro's number
# N_A = 6.0221367e+23


def MassAction(k):
    return ["MassAction", k]

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
        self.process_list = []

    def add_process(self, coefficient, process):
        self.process_list.append(
            {'coef': coefficient, 'func': process})

    def __process(self, variable_array, time):
        for process in self.process_list:
            yield process['coef'] * process['func'](
                variable_array, time)

    def __call__(self, variable_array, time):
        return sum(self.__process(variable_array, time)) + 0.0

    def __str__(self):
        retval = '[%s]' % (', '.join([
            '{coef: %s, func: %s}' % (elem['coef'], elem['func'])
            for elem in self.process_list]))
        return retval

class FunctionMaker(object):
    def __create_rule_list(self, m, reaction_results):
        '''Create rule list from network rules of model.
        '''
        sid_list = m.concrete_species.keys()

        vid_map = {}
        for vid, sid in enumerate(sid_list):
            vid_map[sid] = vid

        rule_list = []
        for result in reaction_results:
            r = result.reaction_rule

            for reaction in result.reactions:
                rule = {}

                rule['k'] = r['k']
                rule['k_name'] = r['k_name']
                rule['desc'] = reaction.str_simple()
                rule['func_def'] = r['func_def']

                rule['reactants'] = []
                for reactant in reaction.reactants:
                    rule['reactants'].append(
                        {'id': vid_map[reactant.id], 'coef': 1})

                rule['products'] = []
                for product in reaction.products:
                    rule['products'].append(
                        {'id': vid_map[product.id], 'coef': 1})

                # e_list -> effectors
                rule['effectors'] = []
                for effector in r['effectors']:
                    for sid in sid_list:
                        species = m.concrete_species[sid]
                        if effector.matches(species):
                            rule['effectors'].append(
                                {'id':  vid_map[sid], 'coef': 1})
                            
                rule_list.append(rule)

        return rule_list

    def make_functions(self, m, reaction_results):
        '''Make functions from model
        '''
        sid_list = m.concrete_species.keys()

        # Function list
        functions = []
        for i in range(len(sid_list)):
            function = Function()
            functions.append(function)

        # Creates rule list.
        rule_list = self.__create_rule_list(m, reaction_results)

        # Process list
        for rule in rule_list:
            if rule['func_def'] is None:
                # todo!!: move user function definition
                k_name = rule['k_name']
                # todo!!: (re)move "volume" paramter
                if k_name == 'MassAction':
                    volume = 1
                    args = (rule['k'], volume)
                    process = MassActionFluxProcess(
                        rule['reactants'], [], [],
                        args)
                    # process = MassActionFluxProcess(
                    #     rule['reactants'], rule['products'],
                    #     rule['effectors'], args)
                elif k_name == 'MichaelisUniUni':
                    process = MichaelisUniUniFluxProcess(
                        rule['reactants'], rule['products'], rule['effectors'],
                        rule['k'])
                else:
                    msg = 'Unsupported process: %s' % k_name
                    raise Exception(msg)
            else:
                process = rule['func_def'](
                    rule['reactants'], rule['products'], rule['effectors'])

            for reactant in rule['reactants']:
                functions[reactant['id']].add_process(
                    -reactant['coef'], process)
            for product in rule['products']:
                functions[product['id']].add_process(
                    +product['coef'], process)

        return functions
