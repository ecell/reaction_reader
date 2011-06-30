class MassActionFluxProcess:
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

