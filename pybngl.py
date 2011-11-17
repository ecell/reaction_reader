'''
$Header: /home/takeuchi/Dropbox/quick/pybngl.py,v 1.50 2011/10/13 04:34:23 takeuchi Exp $
'''

from __future__ import with_statement
import sys
from model.Model import *
#from model.Model import Model
#from model.Model import BINDING_SPECIFIED
#from model.Model import BINDING_NONE
#from model.Model import BINDING_ANY
#from model.Model import BINDING_UNSPECIFIED
#from model.Model import IncludingEntityCondition
#from model.Model import NotCondition
#from model.Model import AndCondition
#from model.Model import REACTANTS
#from model.Model import PRODUCTS

from model.Species import Species
from model.parser import Parser
from solver.ODESolver import ODESolver
from process.process import FunctionMaker
from Simulator import Simulator
from optparse import OptionParser

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

        if type(rhs) == int or type(rhs) == float: # %1
            addval = {'type': 'label', 'value': str(rhs)}
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
    def __enter__(self):
        pass

    def __exit__(self, *arg):

        global seed_species

        print_tree(global_list)

        con_list = []
        speed = speed_r = 0
        condition = None

#        seed_species = parser.parse_species_array(sp_str_list, m)

        for id, v in enumerate(global_list):

            reactants, con_list = read_patterns(m, parser, v['children'][0])
            products, con_list = read_patterns(m, parser, v['children'][1])

            for con_idx, con_func in enumerate(con_list):
                if type(con_func) == float:   # [SPEED_FUNCTION]
                    speed = speed_r = con_func
                    con_list.pop(con_idx)
                elif type(con_func) == tuple: # [MassAction2(.1, .2)]
                    speed = con_func[0]
                    speed_r = con_func[int(bool(con_func[1]))]
                    con_list.pop(con_idx)

            if len(con_list) >= 2:            # [CONDITION_FUNCTION]
                condition = AndCondition(con_list)
            elif con_list != []:
                condition = con_list[0]
            else:
                condition = None

            rule = m.add_reaction_rule(reactants, products, condition, k_name='MassAction', k=speed)

            if v['type'] == 'neq':
                condition = swap_condition(con_list)
                rule = m.add_reaction_rule(products, reactants, condition, k_name='MassAction', k=speed_r)
            



class MoleculeTypes(object):
    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global tmp_list

        mole_entity_list = [] # string. check for double registration such as A and A.B.

        for i in tmp_list:

            if i['name'] not in mole_entity_list and i['name'] != '.':
                tmpmole = m.add_entity_type(i['name'])
                mole_entity_list.append(i['name'])

                for j in i['children']:
                    if j.has_key('children'):
                        state_name = 'state_'+i['name']+'_'+j['name']
                        state = [k['name'] for k in j['children']]
                        p_state = m.add_state_type(state_name, state)
                        tmpmole.add_component(j['name'], {j['name']: p_state})
                    else:
                        tmpmole.add_component(j['name'])

                parser.add_entity_type(tmpmole)

        tmp_list = []


def read_entity(sp, m, p, entity, binding_components):

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

                    if j.get('type') is 'bracket':
                    #if 'type' in j:  # binding input
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


        except IndexError:
            quit()
        except KeyError:
            pass


def read_species(m, p, species):

    sp = Species()

    bind_comp = {}

    if species['name'] == '.':  #   A.B
        for entity in species['children']:
            read_entity(sp, m, p, entity, bind_comp)
        for comps in bind_comp.itervalues():
            if len(comps) != 2:
                pass
            else:
                sp.add_binding(comps[0], comps[1])
    else:                       #   A
        read_entity(sp, m, p, species, bind_comp)

    return sp


def read_patterns(m, p, species):

    s_list = []
    con_list = []

    if species.get('type') == 'add':
        for entity in species['children']:
            if 'name' in entity:
                sp = read_species(m, p, entity)
                sp.concrete = False
                sp = m.register_species(sp)
                s_list.append(sp)

            elif entity.get('type') == 'bracket':
                con_list.append(entity['value'])

    else:
        sp = read_species(m, p, species)
        sp.concrete = False
        sp = m.register_species(sp)
        sp.concrete = False
        s_list.append(sp)


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
                    print_tree(i[j], n+12)
                else:
                    print i[j]

            else:
                print pr_str(n*bool(idx), j, i[j])


class MoleculeInits(object):
    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global tmp_list
        global seed_values
        global seed_species

        sp_list = []

        for i in tmp_list:

            seed_values.append(float(i['children'].pop(-1)['value'])*N_A)

            sp = read_species(m, parser, i)
            sp.concrete = True
            sp = m.register_species(sp)
            sp_list.append(sp)

        seed_species = sp_list

        tmp_list = []


class Pybngl(object):

    def __init__(self):
        globals = MyDict()
        globals['reaction_rules'] = ReactionRules()
        globals['molecule_inits'] = MoleculeInits()
        globals['molecule_types'] = MoleculeTypes()

        try:
            exec file(args[0]) in globals
            self.Simulation()
        except IndexError:
            OptParse.print_help()
            exit(1)
        
    def Simulation(self):
#        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#        seed_values = [10000 * N_A, 5000 * N_A, 2000 * N_A]

        fm = FunctionMaker()
        sim = Simulator()

        try:
            results = m.generate_reaction_network(seed_species, options.itr_num)
        except Error, inst:
            print inst
            exit()

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
        for result in results:
            for r in result.reactions:
                print '# ', cnt, r.str_simple()
                cnt += 1
        print '#'

	#import pdb; pdb.set_trace()

        if options.rulefile != None:
            f = open(options.rulefile, 'w')
            cnt = 1
            for result in results:
                for r in result.reactions:
                    f.write(str(cnt)+' '+str(r.str_simple())+'\n')
                    cnt += 1
            f.close

        sp_num = len(m.concrete_species)

        # Initial values for species.
        variables = []
        for i in range(sp_num):
            variables.append(0.0)
        for i, v in enumerate(seed_values):
            variables[i] = v


        volume = 1
        functions = fm.make_functions(m, results, volume)
        the_solver = ODESolver()
        sim.initialize(the_solver, functions, variables)



        if (end_time != -1):   # t_end is defined
            while(sim.the_time + the_solver.get_step_interval() <end_time):
                sim.step()
            sim.step()
            sim.the_time = end_time
            the_solver.set_next_time(sim.the_time)
            the_solver.set_step_interval(sim.the_time - the_solver.get_current_time())
            sim.step()

        else:                 # t_end is not defined
            sim.step(step_num)



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
            for j in i:
                print j,
            print ''

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


if __name__ == '__main__':

    N_A = 6.0221367e+23

    seed_values = []
    seed_species = []

    global_list = []
    tmp_list = []

    m = Model()
    parser = Parser()

    usage = "python pybngl.py [options] SIMULATION_FILE"
    OptParse = OptionParser(usage=usage)
    OptParse.add_option('-r', dest='rulefile', metavar='RULE_FILE', help='write rules to RULE_FILE')
    OptParse.add_option('-s', dest='step_num', type=int, default=120, help='set step num')
    OptParse.add_option('-i', dest='itr_num', type=int, default=1, help='set rule iteration num')
    OptParse.add_option('-d', dest='disap_flag', action='store_false', default=True, help='allow implicit disappearance')
    OptParse.add_option('-t', dest='end_time', type=float, default=-1, help='set step num')
    
    (options, args) = OptParse.parse_args()
    step_num = options.step_num
    m.disallow_implicit_disappearance = options.disap_flag
    end_time = options.end_time

    pybngl = Pybngl()
