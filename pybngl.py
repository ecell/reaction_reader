'''
$Header: /home/d8051105/shared/pybngl.py,v 1.38 2011/08/10 08:47:42 takeuchi Exp $
'''

from __future__ import with_statement
import sys
from model.model import Model
from model.model import Species
from model.model import BINDING_SPECIFIED
from model.model import BINDING_NONE
from model.model import BINDING_ANY
from model.model import BINDING_UNSPECIFIED
from model.parser import Parser
from solver.ODESolver import ODESolver
from process.process import FunctionMaker
from Simulator import Simulator
from model.model import IncludingEntityCondition
from model.model import NotCondition
from model.model import AndCondition
from model.model import REACTANTS
from model.model import PRODUCTS
from model.model import Error

N_A = 6.0221367e+23

seed_values = []
seed_species = []

#'''testODE_1.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)']
#seed_values = [10000. * N_A, 10000. * N_A]
step_num = 120

#'''testODE_2.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A]
#step_num = 120

#'''testODE_3.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~pU)']
#seed_values = [10000. * N_A, 5000. * N_A, 3000. * N_A]
#step_num = 120

#'''testODE_4.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~pU)']
#seed_values = [10000. * N_A, 5000. * N_A, 0.]
#step_num = 120

#'''testODE_5.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 100. * N_A]
#step_num = 120

#'''testODE_6.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 100. * N_A]
#step_num = 120

#'''testODE_7.ess'''
#sp_str_list = ['R(l,d,Y~U)', 'L(r!1).R(l!1,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 3000. * N_A]
#step_num = 120

#'''testODE_8.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'L(r!1).R(l!1,d,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 2000. * N_A]
#step_num = 120

#'''testODE_10.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)']
#seed_values = [10000. * N_A, 10000. * N_A]
#step_num = 120

#'''testODE_11.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 2000. * N_A]
#step_num = 200

#'''testODE_12.ess'''
#sp_str_list = ['R(l,d,Y~U)']
#seed_values = [10000. * N_A]
#step_num = 120

#'''testODE_13.ess'''
#sp_str_list = ['R(r1,r2)']
#seed_values = [10000. * N_A]
#results = m.generate_reaction_network(seed_species, 2)
#step_num = 300

#'''testODE_14.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#seed_values = [200. * N_A, 200. * N_A, 50. * N_A]
#step_num = 1000

#'''testODE_15.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)']
#seed_values = [10000. * N_A, 10000. * N_A]
#step_num = 40

#'''testODE_16.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)']
#seed_values = [10000. * N_A, 0.]
#step_num = 20

#'''testODE_17.ess'''
#sp_str_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U)','L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
#seed_values = [10000. * N_A, 10000. * N_A]
#step_num = 20

#'''testODE_18.ess'''
#sp_str_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U)','L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
#seed_values = [10000. * N_A, 10000. * N_A]
#step_num = 20

#'''testODE_9.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'L(r!1).R(l!1,d,Y~U)']
#seed_values = [10000. * N_A, 5000. * N_A, 2000. * N_A]
step_num = 120

#'''egfr.py'''
#sp_str_list = ['egfr(l, r, Y1068~Y, Y1148~Y)', 'egf(r)', 'Sos(dom)', 'Shc(PTB, Y317~Y)', 'Grb2(SH2, SH3)']
#seed_values = [10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A]
#step_num = 20

#'''RasRafMEKREK.py'''
#sp_str_list = ['RasG(raf,Y1~U,Y2~U)', 'Raf(ras,mek,p1,Y~U)', 'MEK(raf,erk,p2,Y1~U,Y2~U)', 'ERK(mek,p3,Y1~U,Y2~U)', 'Pase1(raf)', 'Pase2(mek)', 'Pase3(erk)']
#seed_values = [10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A]
#step_num = 20

#'''testODE_E.ess'''
#sp_str_list = ['Q(s, m, r, p~U)', 'S(q, v~pU)', 'M(q, v~pU)', 'R(q, v~pU)']
#seed_values = [10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A]
#sp_str_list = ['Q(t, l, f)', 'S(m, l)', 'M(m, l)', 'R(m, l)']
#seed_values = [10000. * N_A, 10000. * N_A, 10000. * N_A, 10000. * N_A]
#step_num = 20

#'''testODE_A.ess'''
#sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(a)']
#seed_values = [10000. * N_A, 10000. * N_A, 10000. * N_A]
#step_num = 120

m = Model()
parser = Parser()
fm = FunctionMaker()
sim = Simulator()

m.disallow_implicit_disappearance = True

global_list = []
tmp_list = []

class AnyCallable(object):
    def __init__(self, key, outer=None):
        global tmp_list

        tmp_list.append({"name": key})

#        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

    def __call__(self, *arg, **kwarg):
        global tmp_list

#        print "end:" + self._key

        matched_indices = []

        for i, a_dict in enumerate(tmp_list):
            if a_dict.get("name") == self._key:
                matched_indices.append(i)

        parent   = tmp_list.pop(matched_indices[-1])
        children = tmp_list[matched_indices[-1]:]
        del tmp_list[matched_indices[-1]:]
        tmp_list.append({"name": parent["name"], "children": children})

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
            tmp_list.append({"name": "."})
            return AnyCallable(key, self)

    def __getitem__(self, key):
        global tmp_list

#        print "parameter: " + str(key)

        if type(key) == int or type(key) == float: # [1]
            addval = {"type": "bracket", "value": str(key)}
            if "children" in tmp_list[-1]:
                tmp_list[-1]["children"].append(addval)
            else:
                tmp_list[-1]["children"] = [addval]

        else: # [michaelis_menten]
            effect_list = tmp_list[2:]
            del tmp_list[2:]
            addval = {"xxx": "effector", "value": effect_list}

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
        self.operator("gt")

    def __lt__(self, rhs):
#        print "lt"
        tmp_list[0]['children'].append(tmp_list.pop(-1))
        return True

    def __ne__(self, rhs):
        self.operator("neq")

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
        speed = 0
        speed_r = 0
        condition = None

#        seed_species = parser.parse_species_array(sp_str_list, m)

        for id, v in enumerate(global_list):

            reactants, con_list = read_patterns(m, parser, v['children'][0])
            products, con_list = read_patterns(m, parser, v['children'][1])

            for con_idx, con_func in enumerate(con_list):
                if type(con_func) == float:   # [SPEED_FUNCTION]
                    speed_r = con_func
                    speed = con_func
                    con_list.pop(con_idx)
                elif type(con_func) == tuple: # [MassAction2(.1, .2)]
                    speed = con_func[0]
                    if con_func[1] == None:
                       speed_r = con_func[0]
                    else:
                        speed_r = con_func[1]
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
            

#        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
#        seed_values = [10000 * N_A, 5000 * N_A, 2000 * N_A]

        try:
            results = m.generate_reaction_network(seed_species, 10)
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

        if len(sys.argv) == 3:
            f = open(sys.argv[2], 'w')

        cnt = 1
        for result in results:
            for r in result.reactions:
                print '# ', cnt, r.str_simple()
                if len(sys.argv) == 3:
                    f.write(str(cnt)+' '+str(r.str_simple())+'\n')
                cnt += 1
        print '#'

        if len(sys.argv) == 3:
            f.close


        sp_num = len(m.concrete_species)

        # Initial values for species.
        variables = []
        for i in range(sp_num):
            variables.append(0.0)
        for i, v in enumerate(seed_values):
            variables[i] = v

        global fm
        global sim

        volume = 1
        functions = fm.make_functions(m, results, volume)
        the_solver = ODESolver()
        sim.initialize(the_solver, functions, variables)

#        step_num = 120
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

        output_terminal = output_series[step_num - 1]
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



class MoleculeTypes(object):
    def __enter__(self):
        pass

    def __exit__(self, *arg):
        global tmp_list
        mole_entity_list = [] # string. check for double registration such as A and A.B.
        mole_state_list = []  # string. check for state_type registration.
        mole_state_dict = {}  # tuple.   key:State_type
        for i in tmp_list:

            if i['name'] not in mole_entity_list and i['name'] != '.':
                tmpmole = m.add_entity_type(i['name'])
                mole_entity_list.append(i['name'])

                for j in i['children']:
                    if j.has_key('children'):
                        if j['children'][0]['name'] not in mole_state_list:
                            new_state = j['children'][0]['name']
                            new_state_P = 'p' + new_state
                            p_state = m.add_state_type('state_'+new_state, [new_state, new_state_P])
                            mole_state_dict[new_state] = p_state
                            mole_state_list.append(new_state)
                        tmpmole.add_component(j['name'], {new_state: mole_state_dict[new_state]})
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

                    if 'type' in j:  # binding input
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


if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print 'Usage: # python %s ess_file [reaction_output]' % sys.argv[0]
    quit()


globals = MyDict()
globals['reaction_rules'] = ReactionRules()
globals['molecule_inits'] = MoleculeInits()
globals['molecule_types'] = MoleculeTypes()

exec file(sys.argv[1]) in globals
