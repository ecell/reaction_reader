import inspect as ins
import sys

class FluxProcess(object):
    def conc(self, sp):
        '''
        returns values of species in sp_list which has species idx
        '''
        # return [va[i] for i in sp_list]

        va = ins.getargvalues(ins.stack()[2][0]).locals['variable_array']
        return va[sp['id']]

    def invalid_func(self, message):
        print message
        sys.exit()

#        retval = []
#
#        try:
#            for i in sp_list:
#                retval.append(va[i])
#        except IndexError:
#            print 'IndexError in FluxProcess.'
#            sys.exit()
#        else:
#            return retval


class MichaelisUniUniFluxProcess(FluxProcess):
    def __init__(self, KmS, KmP, KcF, KcR, volume, reactant, product, effectors):
        self.volume = volume
        self.KmS = KmS
        self.KmP = KmP
        self.KcF = KcF
        self.KcR = KcR
        self.reactant = reactant
        self.N_A = 6.0221367e+23
        self.product = product
        self.effector = effectors

        # Get Species' name
        # print [x.str_simple() for x in self.species.values()]
        # for i, v in enumerate(species): print i+1, species[v].str_simple()

        # Get Reactors' name
        # print [i.str_simple() for i in effectors]

        if (len(self.reactant) != 1) or (len(self.product) != 1):
            self.invalid_func("number of reactant and product must be 1.")

    def __call__(self, variable_array, time):
        # Get Species' value
        # print variable_array

        # Print Species' name and value
        # for i, v in enumerate(self.species):
        #     print self.species[v].str_simple(), variable_array[i]
        
        # (2011/11/29) : example of conc()
        #sp_list = [x['id'] for x in self.reactants]

        def molar_conc(sp):
            """${3:function documentation}"""
            n = self.conc(sp)
            conc_v = n / self.volume
            mol_conc = conc_v / self.N_A

            return mol_conc

        #print self.conc(sp_list)
        S = molar_conc(self.reactant[0])
        P = molar_conc(self.product[0])

        velocity = (self.KcF * S - self.KcR * P) / (self.KmS * self.KmP + self.KmP * S + self.KmS * P)

        print "# velocity :", velocity

        return velocity

    def __str__(self):
        retval = 'OriginalFunction('
        retval += 'k=%f, ' % self.k_value
        retval += 'reactants=%s' % self.reactants
        retval += 'species=%s' % self.species
        retval += 'effectors=%s' % self.effectos
        retval += ')'
        return retval

class MassActionFluxProcess(FluxProcess):
    def __init__(self, k_value, volume, reactants):
        self.volume = volume
        self.k_value = k_value
        self.reactants = reactants
        self.N_A = 6.0221367e+23

    def __call__(self, variable_array, time):
        velocity = self.k_value * self.volume * self.N_A
        for r in self.reactants:
            coefficient = r['coef']
            value = variable_array[r['id']]
            while coefficient > 0:
                velocity *= value / (self.volume * self.N_A)
                coefficient -= 1
        return velocity

    def __str__(self):
        retval = 'MassAction('
        retval += 'k=%f, ' % self.k_value
        retval += 'reactants=%s' % self.reactants
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
        retval = '['
        for i, p in enumerate(self.process_list):
            if i > 0:
                retval += ', '
            retval += '{'
            retval += 'coef:%s' % p['coef']
            retval += ', '
            retval += 'func:%s' % p['func']
            retval += '}'
        retval += ']'
        return retval

class FunctionMaker(object):
    def __create_rule_list(self, m, reaction_results):
        '''Create rule list from network rules of model.'''
        variable_id_map = {}
        for i, sp_id in enumerate(m.concrete_species.iterkeys()):
            sp = m.species[sp_id]
            variable_id_map[sp_id] = i

        rule_list = []
        for result in reaction_results:
            r = result.reaction_rule

            for reaction in result.reactions:
                rule = {}

                rule['k'] = r['k']
                rule['k_name'] = r['k_name']
                rule['desc'] = reaction.str_simple()

                rule['reactants'] = []
                for reactant in reaction.reactants:
                    variable_id = variable_id_map[reactant.id]
                    rule['reactants'].append(\
                        {'id': variable_id, 'coef': 1})

                rule['products'] = []
                for product in reaction.products:
                    variable_id = variable_id_map[product.id]
                    rule['products'].append(\
                        {'id': variable_id, 'coef': 1})

                rule['e_list'] = []
                for effector in r['e_list']:
                    for i in m.concrete_species.iteritems():
                        if effector.matches(i[1]):
                            variable_id = variable_id_map[i[0]]
                            rule['e_list'].append(\
                                {'id': variable_id, 'coef': 1})

                rule_list.append(rule)


        return rule_list

    def make_functions(self, m, reaction_results, volume):
        '''Make functions from model
        '''

        # Creates rule list.
        rule_list = self.__create_rule_list(m, reaction_results)

        # Process list
        processes = []
        for rule in rule_list:

            k_name = rule['k_name']
            if k_name == 'MassAction':
                process = MassActionFluxProcess(rule['k'], volume,
                    rule['reactants'])
            elif k_name == 'MichaelisUniUni':
                vals = rule['k']
                process = MichaelisUniUniFluxProcess(vals[0], vals[1],
                          vals[2], vals[3], volume, rule['reactants'], 
                          rule['products'], rule['e_list'])
            else:
                msg = 'Unsupported process: %s' % k_name
                raise Exception(msg)
            processes.append(process)

        # Function list
        functions = []
        for i in range(len(m.concrete_species)):
            function = Function()
            functions.append(function)

        # Add Processes
        process_id = 0
        for rule in rule_list:
            for reactant in rule['reactants']:
                functions[reactant['id']].add_process(
                    -reactant['coef'], processes[process_id])
            for product in rule['products']:
                functions[product['id']].add_process(
                    product['coef'], processes[process_id])
            process_id += 1

        return functions

