'''
$Header: /home/takeuchi/0613/pybngl.py,v 1.64 2012/02/10 00:54:22 takeuchi Exp $
'''

from __future__ import with_statement
from model.Model import *
#from model.model import Model
#from model.model import Species
#from model.model import BINDING_SPECIFIED
#from model.model import BINDING_NONE
#from model.model import BINDING_ANY
#from model.model import BINDING_UNSPECIFIED
#from model.parser import Parser
#from solver.ODESolver import ODESolver
#from process.process import FunctionMaker
#from Simulator import Simulator
#from model.model import IncludingEntityCondition
#from model.model import NotCondition
#from model.model import AndCondition
#from model.model import REACTANTS
#from model.model import PRODUCTS
#from model.model import Error
#from optparse import OptionParser

from model.Species import Species
from model.parser import Parser
from solver.ODESolver import ODESolver
from process.process import FunctionMaker
from Simulator import Simulator
from model.Error import Error

# Avogadro's number
N_A = 6.0221367e+23


class AnyCallable(object):
    with_label = False
    global_list = []
    tmp_list = []

    @classmethod
    def get_with_label(cls):
        return cls.with_label

    @classmethod
    def set_with_label(cls, value):
        cls.with_label = value

    @classmethod
    def cls_global_list(cls):
        return cls.global_list

    @classmethod
    def cls_tmp_list(cls):
        return cls.tmp_list

    @classmethod
    def set_tmp_list(cls, value):
        cls.tmp_list = value

    def __init__(self, key, outer=None):
        # print "start:", key

        self.cls_tmp_list().append({'name': key})

        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

    def __call__(self, *arg, **kwarg):
        # print "end:", self._key

        tmp_list = self.cls_tmp_list()
        matched_indices = []

        for i, a_dict in enumerate(tmp_list):
            if a_dict.get('name') == self._key:
                matched_indices.append(i)

        parent   = tmp_list.pop(matched_indices[-1])
        children = tmp_list[matched_indices[-1]:]
        del tmp_list[matched_indices[-1]:]
        tmp_list.append({'name': parent['name'], 'children': children})

        if len(tmp_list) >= 3 and tmp_list[-2].get('name') is '.':
            if tmp_list[-3].get('name') is '.':
                tmp_list[-3]['children'].append(tmp_list.pop(-1))
                tmp_list.pop(-1)
            elif 'children' in tmp_list[-2]:     # > A.B [C]
                pass
            else:
                dot_list = [tmp_list.pop(-3), tmp_list.pop(-1)]
                tmp_list[-1]['children'] = dot_list

        return self

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, key):
        try:
            return super(AnyCallable, self).__getattr__(key)
        except:
            self.cls_tmp_list().append({'name': '.'})
            return type(self)(key, self)

    def __getitem__(self, key):
        # print "parameter: " + str(key)
        tmp_list = self.cls_tmp_list()

        if type(key) == int or type(key) == float: # [1]
            addval = {'type': 'bracket', 'value': str(key)}
            if "children" in tmp_list[-1]:
                tmp_list[-1]['children'].append(addval)
            else:
                tmp_list[-1]['children'] = [addval]
        else: # [michaelis_menten]
            effect_list = tmp_list[2:]
            del tmp_list[2:]
            addval = {'xxx': 'effector', 'value': effect_list}

            if len(tmp_list) >= 3: # 7/20 pattern 3) L.R>L+R[]
                tmp_list.append(addval)
            else:
                tmp_list[1]['children'].append(addval)

        return self

    def operator(self, rhs):
        tmp_list = self.cls_tmp_list()

        eff_dict = None

        for i, v in enumerate(tmp_list[1]['children']):
            if v.get('xxx') == 'effector':
                eff_dict = tmp_list[1]['children'].pop(i)

        for i, v in enumerate(tmp_list[0]['children']):
            if v.get('name') == '_':
                tmp_list[0]['children'].pop(i)
                rhs = 'neq'

        tmp_dict = {'type': rhs, 'children': tmp_list}
        if eff_dict:
            tmp_dict.update(eff_dict)

        self.cls_global_list().append(tmp_dict)

        # tmp_list = [] and self.tmp_list = [] doesn't work
        self.set_tmp_list([])

    def __gt__(self, rhs):
        self.operator('gt')

    def __lt__(self, rhs):
        term = self.cls_tmp_list().pop(-1)
        self.cls_tmp_list()[0]['children'].append(term)
        return True

    def __ne__(self, rhs):
        self.operator('neq')

    def __add__(self,rhs):
        tmp_list = self.cls_tmp_list()

        if tmp_list[-2].get('type') == 'add':      # A+B+C(reactants)
            tmp_list[-2]['children'].append(tmp_list.pop(-1))

        elif len(tmp_list) == 2:                   # A+B(reactants)
            add_list = [tmp_list.pop(-2), tmp_list.pop(-1)]
            add_dict = {'type': 'add', 'children': add_list}
            tmp_list.append(add_dict)


        elif tmp_list[1]['children'][-1].get('type') == 'effector':
            eff_dict = tmp_list[1]['children'].pop(-1)

            if tmp_list[1].get('type') == 'add':   # A+B+C [D](products)
                tmp_list[1]['children'].append(eff_dict['value'].pop(0))
                tmp_list[1]['children'].append(eff_dict)

            else:                                  # A+B [D](products)
                add_list = [tmp_list.pop(-1), eff_dict['value'].pop(0)]
                add_list.append(eff_dict)
                add_dict = {'type': 'add', 'children': add_list}
                tmp_list.append(add_dict)


        elif tmp_list[1].get('type') == 'add':     # A+B+C(products)
            for i in range(2, len(tmp_list)):
                tmp_list[1]['children'].append(tmp_list[i])
            del tmp_list[2:]

        else:                                      # A+B(products)
            add_list = tmp_list[1:]
            del tmp_list[1:]
            add_dict = {'type':'add', 'children': add_list}
            tmp_list.append(add_dict)

        return self

    def __or__(self, rhs):
        addval = {'type': 'bracket', 'value':rhs}
        if len(self.cls_tmp_list()) >= 3: # 7/20 pattern 3) L.R>L+R[]
            self.cls_tmp_list().append(addval)
        else:
            self.cls_tmp_list()[1]['children'].append(addval)

    def __mod__(self, rhs):
        # print "label: " + str(rhs)

        if type(rhs) in (int, float):
            addval = {'type': 'label', 'value': str(rhs)}
            self.set_with_label(True)

            if "children" in self.cls_tmp_list()[-1]:
                self.cls_tmp_list()[-1]['children'].append(addval)
            else:
                self.cls_tmp_list()[-1]['children'] = [addval]

class MyDict(dict):
    def __init__(self):
        super(MyDict, self).__init__()

        self.newcls = type('MyAnyCallable', (AnyCallable, ), {})

    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        retval = self.get(key)
        if retval is None:
            retval = self.newcls(key)
        return retval

class ReactionRules(object):
    def __init__(self, m, p, newcls, verbose=False):
        self.model, self.parser, self.newcls = m, p, newcls
        self.verbose = verbose

    def is_verbose(self):
        return self.verbose

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        if self.is_verbose():
            print_tree(self.newcls.global_list)

        con_list = []
        speed = speed_r = 0
        condition = None
        func_name = func_name_r = 'MassAction'
        effector_list = []

        for id, v in enumerate(self.newcls.global_list):

            # create effector list
            if v.get('value') != None:
                effector_list = [read_species(self.parser, i) 
                                 for i in v['value']]

            # create reactants/products
            reactants, con_list = read_patterns(
                self.model, self.parser, v['children'][0], 
                self.newcls.with_label)
            products, con_list = read_patterns(
                self.model, self.parser, v['children'][1], 
                self.newcls.with_label)

            # for con_idx, con_func in enumerate(con_list):
            #     if type(con_func) == float:   # [SPEED_FUNCTION]
            #         speed = speed_r = con_func
            #         con_list.pop(con_idx)
            #     elif type(con_func) == tuple: # [MassAction2(.1, .2)]
            #         speed = con_func[0]
            #         speed_r = con_func[int(bool(con_func[1]))]
            #         con_list.pop(con_idx)

            # if len(con_list) >= 2:            # [CONDITION_FUNCTION]
            #     condition = AndCondition(con_list)
            # elif con_list != []:
            #     condition = con_list[0]
            # else:
            #     condition = None

            # set speed function
            for con_idx, con_func in enumerate(con_list):

                if type(con_func) in [int, float]:        # | 0.1
                    speed = con_func

                elif type (con_func) == list:             # | MassAction(0.1)
                    func_name = con_func[0]
                    speed = con_func[1]
                    
                elif type(con_func) == tuple:
                    if type(con_func[0]) in [int, float]: # | 0.1 of (0.1, 0.2)
                        speed = con_func[0]

                    if type(con_func[1]) in [int, float]: # | 0.2 of (0.1, 0.2)
                        speed_r = con_func[1]

                    if type(con_func[0]) == list: # | MA(1) of (MA(1), MA(0.2))
                        func_name = con_func[0][0]
                        speed = con_func[0][1]

                    if type(con_func[1]) == list: # | MA(2) of (MA(1), MA(0.2))
                        func_name_r = con_func[1][0]
                        speed_r = con_func[1][1]

            # Checks whether reactants/products have any labels.
            # lbflag = True in [r.has_label() for r in reactants + products]

            # Generates reaction rule.
            rule = self.model.add_reaction_rule(
                reactants, products, condition, 
                k_name=func_name, k=speed, e_list=effector_list, 
                lbl=self.newcls.with_label)
            if v['type'] == 'neq':
                # condition = swap_condition(con_list)
                rule = self.model.add_reaction_rule(
                    products, reactants, condition, k_name=func_name_r, 
                    k=speed_r, e_list=effector_list, 
                    lbl=self.newcls.with_label)

class MoleculeTypes(object):
    def __init__(self, m, p, newcls, loc=None):
        self.model, self.parser, self.newcls = m, p, newcls
        self.loc = loc

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        # string. check for double registration such as A and A.B.
        mole_entity_list = []

        for i in self.newcls.tmp_list:
            if i['name'] not in mole_entity_list and i['name'] != '.':
                tmpmole = self.model.add_entity_type(i['name'])
                mole_entity_list.append(i['name'])

                for j in i['children']:
                    if j.has_key('children'):
                        state_name = 'state_'+i['name']+'_'+j['name']
                        state = [k['name'] for k in j['children']]
                        p_state = self.model.add_state_type(state_name, state)
                        tmpmole.add_component(j['name'], {j['name']: p_state})
                    else:
                        tmpmole.add_component(j['name'])

                # for location (01/17)
                if self.loc is not None:
                    tmpmole.add_component('loc', {'loc': self.loc})
                
                self.parser.add_entity_type(tmpmole)

        self.newcls.tmp_list = []

def read_entity(sp, p, entity, binding_components):
    if 'type' in entity:
        return

    entity_name = entity['name']
    entity_type = p._Parser__entity_types[entity_name]
    en = sp.add_entity(entity_type)

    for i in filter(lambda x: 'name' in x, entity['children']):
        comp_name = i['name']
        components = en.find_components(comp_name)
        try:
            en_comp = components[0]
            en_comp.binding_state = BINDING_NONE

            if 'children' in i:
                for j in i['children']:

                    if 'name' in j:  # states input
                        en_comp.set_state(en_comp.states.keys()[0], j['name'])

                    if j.get('type') is 'bracket': # binding input
                        binding_type = j['value']
                        if binding_type == '+':
                            en_comp.binding_state = BINDING_ANY
                        elif binding_type == '?':
                            en_comp.binding_state = BINDING_UNSPECIFIED

                        elif binding_type.isdigit():
                            en_comp.binding_state = BINDING_ANY
                            binding_id = int(binding_type)
                            if not binding_id in binding_components:
                                binding_components[binding_id] = [en_comp]
                            else:
                                en_comp.binding_state = BINDING_SPECIFIED
                                tmp = binding_components[binding_id].pop()
                                tmp.binding_state = BINDING_SPECIFIED
                                binding_components[binding_id].append(tmp)
                                binding_components[binding_id].append(en_comp)

                    if j.get('type') == 'label': # labeling ID
                        en_comp.label = j['value']

        except IndexError:
            quit()
        except KeyError:
            pass

def read_species(p, species):
    sp = Species()

    bind_comp = {}

    if species['name'] == '.':  #   A.B
        for entity in species['children']:
            read_entity(sp, p, entity, bind_comp)
        for comps in bind_comp.itervalues():
            if len(comps) != 2:
                pass
            else:
                sp.add_binding(comps[0], comps[1])
    else:                       #   A
        read_entity(sp, p, species, bind_comp)

    return sp

def read_patterns(m, p, species, label_flag=True):
    s_list = []
    con_list = []

    if species.get('type') == 'add':
        for entity in species['children']:
            if 'name' in entity:
                sp = read_species(p, entity)
                # sp.concrete = False
                sp2 = m.register_species(sp)
                if (label_flag) and (not sp.equals(sp2)):
                    s_list.append(sp)
                else: s_list.append(sp2)

            elif entity.get('type') == 'bracket':
                con_list.append(entity['value'])

    else:
        sp = read_species(p, species)
        # sp.concrete = False
        sp2 = m.register_species(sp)
        # sp.concrete = False

        if (label_flag) and (not sp.equals(sp2)):
            s_list.append(sp)     # add labeled species
        else: s_list.append(sp2)  # add normal species

        for i in [i for i in species['children'] if 'type' in i]:
            if i.get('type') == 'bracket':
                con_list.append(i['value'])

    return s_list, con_list

def swap_condition(con_list):
    def swap_side(con):
        if con.__class__.__name__ == 'NotCondition':
            return NotCondition(swap_side(con.condition))
        if con.side == REACTANTS:
            side = PRODUCTS
        else:
            side = REACTANTS
        return IncludingEntityCondition(side, con.index+1, con.entity_type)

    new_condition = None

    if len(con_list) == 0:
        new_conditin = None
    elif len(con_list) == 1:
        new_condition = swap_side(con_list[0])
    else:
        new_condition = AndCondition([swap_side(i) for i in con_list])

    return new_condition

def print_tree(a, n=0):
    def pr_str(n, j, v=''):
        return ' '*n + j + ' : ' + str(v)

    for idx, i in enumerate(a): # rules
        for j in i:             # j = ['type'|'name'|'children'|'value']

            if i[j] == []:
                print ''

            elif j == 'children' or j == 'value':
                print pr_str(n, j),
                if type(i[j]) == list:
                    if type(i[j][0]) == dict: # for species
                        print_tree(i[j], n+12)
                    else:
                        print i[j]  # for function (['MassAction', 0.3])

                else:
                    print i[j]

            else:
                print pr_str(n*bool(idx), j, i[j])

class MoleculeInits(object):
    def __init__(self, m, p, newcls):
        self.model, self.parser, self.newcls = m, p, newcls
        self.seed_species = {}

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        self.seed_species = {}
        for i in self.newcls.tmp_list:
            sp = read_species(self.parser, i)
            sp.concrete = True

            species_str_list = [
                x.str_simple() for x in self.seed_species.keys()]
            if sp.str_simple() in species_str_list:
                raise ValueError

            sp = self.model.register_species(sp)

            self.seed_species[sp] = \
                float(i['children'].pop(-1)['value']) * N_A

        self.newcls.tmp_list = []

class Pybngl(object):
    def __init__(self, verbose=False, loc=None):
        self.verbose = verbose
        self.loc = loc

    def is_verbose(self):
        return self.verbose

    def parse_model(self, filename, m=None, p=None, 
                    maxiter=10, rulefilename=None):
        if m is None: m = Model()
        if p is None: p = Parser()

        namespace = MyDict()
        namespace['reaction_rules'] = ReactionRules(
            m, p, namespace.newcls, verbose=self.is_verbose())
        namespace['molecule_inits'] = MoleculeInits(
            m, p, namespace.newcls)
        namespace['molecule_types'] = MoleculeTypes(
            m, p, namespace.newcls, loc=self.loc)

        exec file(filename) in namespace
        seed_species = namespace['molecule_inits'].seed_species

        # sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
        # seed_values = [10000 * N_A, 5000 * N_A, 2000 * N_A]
        # volume = 1
        # for i, v in enumerate(m.reaction_rules): print m.reaction_rules[v]

        try:
            reaction_results = m.generate_reaction_network(
                seed_species.keys(), maxiter)
        except Error, inst:
            print inst
            exit()

        # Outputs information to stdout
        if self.is_verbose():
            print '# << reaction rules >>'
            cnt = 1
            for rule_id in sorted(m.reaction_rules.iterkeys()):
                rule = m.reaction_rules[rule_id]
                print '# ', cnt, rule.str_simple()
                cnt += 1
            print '#'

            print '# << species >>'
            cnt = 1
            for sp_id in sorted(m.concrete_species.iterkeys()):
                sp = m.concrete_species[sp_id]
                print '# ', cnt, sp.str_simple()
                cnt += 1
            print '#'

            print '# << reactions >>'
            cnt = 1
            for result in reaction_results:
                for r in result.reactions:
                    print '# ', cnt, r.str_simple()
                    cnt += 1
            print '#'
            # print '# << values >>'
            # print '# volume :', volume
            # print '#'

        # Outputs reactions to rulefile
        if rulefilename is not None:
            fout = open(rulefilename, 'w')
            cnt = 1
            for result in reaction_results:
                for r in result.reactions:
                    fout.write('%d %s\n' % (cnt, r.str_simple()))
                    cnt += 1
            fout.close()

        return m, reaction_results, seed_species

    def generate_simulator(self, m, reaction_results, seed_species):
        num_of_species = len(m.concrete_species)

        # Initial values for species.
        variables = []
        for i in range(num_of_species):
            variables.append(0.0)
        for i, v in enumerate(seed_species.values()):
            variables[i] = v

        fmaker = FunctionMaker()
        simulator = Simulator()

        # functions = fmaker.make_functions(m, reaction_results, volume)
        functions = fmaker.make_functions(m, reaction_results)
        simulator.initialize(ODESolver(), functions, variables)

        return (simulator, functions)


if __name__ == '__main__':
    import optparse
    import sys


    def create_option_parser():
        usage = "python pybngl.py [options] SIMULATION_FILE"
        optparser = optparse.OptionParser(usage=usage)
        optparser.add_option('-r', dest='rulefile', metavar='RULE_FILE', 
                            help='write rules to RULE_FILE')
        optparser.add_option('-s', dest='step_num', type=int, default=120, 
                            help='set step num')
        optparser.add_option('-i', dest='itr_num', type=int, default=10, 
                            help='set rule iteration num')
        optparser.add_option('-d', dest='disap_flag', action='store_false', 
                            default=True, help='allow implicit disappearance')
        optparser.add_option('-t', dest='end_time', type=float, default=-1, 
                            help='set step num')
        optparser.add_option('-v', dest='show_mes', action='store_true', 
                            default=False, help='show verbose messages')
        optparser.add_option('-l', dest='loc_flag', action='store_true', 
                            default=False, help='use location description')
        return optparser

    def execute_simulation(simulator, functions, m, 
                           num_of_steps=0, duration=-1, fout=sys.stdout):
        # run simulation
        if duration > 0:
            # duration is defined
            while (simulator.the_time 
                   + simulator.solver.get_step_interval() < duration):
                simulator.step()
                
            if simulator.the_time < duration:
                simulator.step()
            simulator.the_time = duration
            simulator.solver.set_next_time(simulator.the_time)
            simulator.solver.set_step_interval(
                simulator.the_time - simulator.solver.get_current_time())
            simulator.step()
        else:
            # duration is not defined
            simulator.step(num_of_steps)

        output_series = simulator.get_logged_data()
        
        # print results
        species_name_list = [
            m.concrete_species[species_id].str_simple()
            for species_id in sorted(m.concrete_species.iterkeys())]
        header = 'time\t%s' % ('\t'.join(species_name_list))
        fout.write('#%s\n' % header)
        fout.write('#\n')

        for values in output_series:
            values /= N_A
            fout.write('%s\n' % (
                    '\t'.join(['%s' % value for value in values])))

        # if num_of_steps > 0: 
        #     # num_of_steps == 0 raises an error by output_series[-1]
        #     output_terminal = output_series[-1]
        #     result = str(output_terminal[0])
        #     result += ': '
        #     for i, v in enumerate(output_terminal):
        #         if i > 1:
        #             result += ', '
        #         if i > 0:
        #             value = v / N_A
        #             result += str(value)

        #     fout.write('#  %s\n' % header)
        #     fout.write('#  %s\n' % result)
        #     fout.write('#  %d\n' % len(output_series))

        # import os.path
        # ##### ONLY FOR testLabel.py #####
        # if os.path.split(filename) == 'testLabel.py':
        #     m.reaction_rules[45]._ReactionRule__attrs['k'] = 0.9
        #     m.reaction_rules[46]._ReactionRule__attrs['k'] = 0.1
        #     output_series = simulator.get_logged_data()
        #     variables = output_series[-1][1:].tolist()

        #     # volume = 1
        #     # functions = fmaker.make_functions(m, reaction_results, volume)
        #     functions = fmaker.make_functions(m, reaction_results)
        #     simulator.initialize(ODESolver(), functions, variables)
        #     sim_sub()
        #     sim_print()
        # ##### ONLY FOR testLabel.py #####


        # ##### ONLY FOR testToy.py #####
        # if os.path.split(filename) == 'testToy.py':
        #     m.reaction_rules[5]._ReactionRule__attrs['k'] = 0.0
        #     m.reaction_rules[6]._ReactionRule__attrs['k'] = 1.0
        #     output_series = simulator.get_logged_data()
        #     variables = output_series[-1][1:].tolist()

        #     # volume = 1
        #     # functions = fmaker.make_functions(m, reaction_results, volume)
        #     functions = fmaker.make_functions(m, reaction_results)
        #     simulator.initialize(ODESolver(), functions, variables)
        #     sim_sub()
        #     sim_print()
        # ##### ONLY FOR testLabel.py #####

        return output_series


    m, p = Model(), Parser()

    optparser = create_option_parser()
    (options, args) = optparser.parse_args()
    if len(args) == 0:
        optparser.print_help()
        exit(1)

    m.disallow_implicit_disappearance = options.disap_flag

    comp_state = None
    if options.loc_flag:
        # state_list = ['EC', 'EN', 'EM', 'PM', 'CP', 'NU', 'NM']
        # state_list = ['all', 'cyto', 'mem']
        state_list =  ['EC', 'EN', 'EM', 'PM', 'CP', 'NU', 'NM', 
                       'all', 'cyto', 'mem']
        comp_state = m.add_state_type('compartment', state_list)

    filename = args[0]
    pybngl = Pybngl(verbose=options.show_mes, loc=comp_state)
    m, reaction_results, seed_species = pybngl.parse_model(
        filename, m, p, maxiter=options.itr_num, rulefilename=options.rulefile)
    simulator, functions = pybngl.generate_simulator(
        m, reaction_results, seed_species)

    output_series = execute_simulation(
        simulator, functions, m, num_of_steps=options.step_num,
        duration=options.end_time)
