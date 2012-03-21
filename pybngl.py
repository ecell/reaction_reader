'''
$Header: /home/takeuchi/0613/pybngl.py,v 1.64 2012/02/10 00:54:22 takeuchi Exp $
'''

from __future__ import with_statement
import sys
import pdb
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
    def __init__(self, key, outer=None):
        global tmp_list

        tmp_list.append({'name': key})

#        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

    def __call__(self, *arg, **kwarg):
        global tmp_list

#        print "end:" + self._key

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

        global tmp_list

        try:
            return super(AnyCallable, self).__getattr__(key)
        except:
            tmp_list.append({'name': '.'})
            return AnyCallable(key, self)

    def __getitem__(self, key):
        global tmp_list

#        print "parameter: " + str(key)

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
        global global_list
        global tmp_list

#        print rhs

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

        global_list.append(tmp_dict)

        tmp_list = []

    def __gt__(self, rhs):
        self.operator('gt')

    def __lt__(self, rhs):
#        print "lt"
        tmp_list[0]['children'].append(tmp_list.pop(-1))
        return True

    def __ne__(self, rhs):
        self.operator('neq')

    def __add__(self,rhs):
        global tmp_list

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
#        print rhs

        addval = {'type': 'bracket', 'value':rhs}
        if len(tmp_list) >= 3: # 7/20 pattern 3) L.R>L+R[]
            tmp_list.append(addval)
        else:
            tmp_list[1]['children'].append(addval)

    def __mod__(self, rhs):
#        print "label: " + str(rhs)

        global label_flag

        if type(rhs) == int or type(rhs) == float: # %1
            addval = {'type': 'label', 'value': str(rhs)}
            label_flag = True

            if "children" in tmp_list[-1]:
                tmp_list[-1]['children'].append(addval)
            else:
                tmp_list[-1]['children'] = [addval]

class MyDict(dict):
    def __init__(self):
        super(MyDict, self).__init__()

    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        retval = self.get(key)
        if retval is None:
            retval = AnyCallable(key)
        return retval

class ReactionRules(object):
    def __init__(self, m, verbose=False):
        self.model = m
        self.verbose = verbose

    def is_verbose(self):
        return self.verbose

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global label_flag

        if self.is_verbose():
            print_tree(global_list)

        con_list = []
        speed = speed_r = 0
        condition = None
        func_name = func_name_r = 'MassAction'
        effector_list = []

        for id, v in enumerate(global_list):

            # create effector list
            if v.get('value') != None:
                effector_list = [read_species(parser, i) for i in v['value']]

            # create reactants/products

            reactants, con_list = read_patterns(
                self.model, parser, v['children'][0])
            products, con_list = read_patterns(
                self.model, parser, v['children'][1])

#            for con_idx, con_func in enumerate(con_list):
#                if type(con_func) == float:   # [SPEED_FUNCTION]
#                    speed = speed_r = con_func
#                    con_list.pop(con_idx)
#                elif type(con_func) == tuple: # [MassAction2(.1, .2)]
#                    speed = con_func[0]
#                    speed_r = con_func[int(bool(con_func[1]))]
#                    con_list.pop(con_idx)

#            if len(con_list) >= 2:            # [CONDITION_FUNCTION]
#                condition = AndCondition(con_list)
#            elif con_list != []:
#                condition = con_list[0]
#            else:
#                condition = None

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
            lbflag = True in [r.has_label() for r in reactants+products]
            

            # Generates reaction rule.
            rule = self.model.add_reaction_rule(
                reactants, products, condition, 
                k_name=func_name, k=speed, e_list=effector_list, lbl=lbflag)
            if v['type'] == 'neq':
                # condition = swap_condition(con_list)
                rule = self.model.add_reaction_rule(
                    products, reactants, condition, k_name=func_name_r, 
                    k=speed_r, e_list=effector_list, lbl=lbflag) # label_flag)

class MoleculeTypes(object):
    def __init__(self, m, loc=None):
        self.model = m
        self.loc = loc

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global tmp_list

        mole_entity_list = [] # string. check for double registration such as A and A.B.

        for i in tmp_list:

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
                
                parser.add_entity_type(tmpmole)

        tmp_list = []


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

def read_patterns(m, p, species):
    s_list = []
    con_list = []

    if species.get('type') == 'add':
        for entity in species['children']:
            if 'name' in entity:
                sp = read_species(p, entity)
#                sp.concrete = False
                sp2 = m.register_species(sp)
                if (label_flag) and (not sp.equals(sp2)):
                    s_list.append(sp)
                else: s_list.append(sp2)

            elif entity.get('type') == 'bracket':
                con_list.append(entity['value'])

    else:
        sp = read_species(p, species)
#        sp.concrete = False
        sp2 = m.register_species(sp)
#        sp.concrete = False

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
    def __init__(self, m):
        self.model = m
        self.seed_species = {}

    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global tmp_list

        self.seed_species = {}
        for i in tmp_list:
            sp = read_species(parser, i)
            sp.concrete = True

            species_str_list = [
                x.str_simple() for x in self.seed_species.keys()]
            if sp.str_simple() in species_str_list:
                raise ValueError

            sp = self.model.register_species(sp)

            self.seed_species[sp] = \
                float(i['children'].pop(-1)['value']) * N_A

        tmp_list = []

class Pybngl(object):
    def __init__(self, verbose=False, loc=None):
        self.verbose = verbose
        self.loc = loc

    def is_verbose(self):
        return self.verbose

    def parse_model(self, filename, m=None, maxiter=10, rulefilename=None):
        if m is None:
            m = Model()

        gvars = MyDict()
        gvars['reaction_rules'] = ReactionRules(m, verbose=self.is_verbose())
        gvars['molecule_inits'] = MoleculeInits(m)
        gvars['molecule_types'] = MoleculeTypes(m, loc=self.loc)

        exec file(filename) in gvars
        
        seed_species = gvars['molecule_inits'].seed_species

#        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#        seed_values = [10000 * N_A, 5000 * N_A, 2000 * N_A]

#        volume = 1

#        for i, v in enumerate(m.reaction_rules): print m.reaction_rules[v]

        try:
            reaction_results = m.generate_reaction_network(
                seed_species.keys(), maxiter)
        except Error, inst:
            print inst
            exit()

#        print reaction_results[0]

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
#            print '# << values >>'
#            print '# volume :', volume
#            print '#'

        # Outputs reactions to rulefile
        if rulefilename is not None:
            f = open(rulefilename, 'w')
            cnt = 1
            for result in reaction_results:
                for r in result.reactions:
                    f.write(str(cnt)+' '+str(r.str_simple())+'\n')
                    cnt += 1
            f.close()

        return m, reaction_results, seed_species

    def execute_simulation(self, m, reaction_results, seed_species, 
                           num_of_steps=0, duration=-1):
        sp_num = len(m.concrete_species)

        # Initial values for species.
        variables = []
        for i in range(sp_num):
            variables.append(0.0)
        for i, v in enumerate(seed_species.values()):
            variables[i] = v

        fm = FunctionMaker()
        sim = Simulator()

#        functions = fm.make_functions(m, reaction_results, volume)
        functions = fm.make_functions(m, reaction_results)
        the_solver = ODESolver()
        sim.initialize(the_solver, functions, variables)

        def sim_sub():
            if duration > 0:
                # duration is defined
                while (sim.the_time + the_solver.get_step_interval() 
                       < duration):
                    sim.step()

                if sim.the_time < duration:
                    sim.step()
                sim.the_time = duration
                the_solver.set_next_time(sim.the_time)
                the_solver.set_step_interval(
                    sim.the_time - the_solver.get_current_time())
                sim.step()

            else:
                # duration is not defined
                sim.step(num_of_steps)

        def sim_print():
            output_series = sim.get_logged_data()
            header = 'time, '
            for i, sp_id in enumerate(sorted(m.concrete_species.iterkeys())):
                if i > 0:
                    header += ', '
                sp = m.concrete_species[sp_id]
                header += sp.str_simple()
            print '# ', header
            print '#'
            for i in output_series:
                print i[0],
                for j in range(1, len(i)):
                    print i[j],
                print ''

            if num_of_steps > 0: 
                # num_of_steps == 0 raises an error by output_series[-1]
                output_terminal = output_series[-1]
                result = str(output_terminal[0])
                result += ': '
                for i, v in enumerate(output_terminal):
                    if i > 1:
                        result += ', '
                    if i > 0:
                        value = v / N_A
                        result += str(value)

                print '# ', header
                print '# ', result
                print '# ', len(output_series)

        sim_sub()
        sim_print()

        import os.path

        ##### ONLY FOR testLabel.py #####
        if os.path.split(filename) == 'testLabel.py':
            m.reaction_rules[45]._ReactionRule__attrs['k'] = 0.9
            m.reaction_rules[46]._ReactionRule__attrs['k'] = 0.1
            output_series = sim.get_logged_data()
            variables = output_series[-1][1:].tolist()

#            volume = 1
#            functions = fm.make_functions(m, reaction_results, volume)
            functions = fm.make_functions(m, reaction_results)
            the_solver = ODESolver()
            sim.initialize(the_solver, functions, variables)
            sim_sub()
            sim_print()
        ##### ONLY FOR testLabel.py #####


        ##### ONLY FOR testToy.py #####
        if os.path.split(filename) == 'testToy.py':
            m.reaction_rules[5]._ReactionRule__attrs['k'] = 0.0
            m.reaction_rules[6]._ReactionRule__attrs['k'] = 1.0
            output_series = sim.get_logged_data()
            variables = output_series[-1][1:].tolist()

#            volume = 1
#            functions = fm.make_functions(m, reaction_results, volume)
            functions = fm.make_functions(m, reaction_results)
            the_solver = ODESolver()
            sim.initialize(the_solver, functions, variables)
            sim_sub()
            sim_print()
        ##### ONLY FOR testLabel.py #####


if __name__ == '__main__':
    import optparse


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


    global_list = []
    tmp_list = []
    label_flag = False

    m = Model()
    parser = Parser()

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
        filename, m, maxiter=options.itr_num, rulefilename=options.rulefile)
    pybngl.execute_simulation(
        m, reaction_results, seed_species, 
        num_of_steps=options.step_num, duration=options.end_time)
