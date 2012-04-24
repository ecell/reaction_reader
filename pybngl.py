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
from model.Error import Error

import types

import World
import Simulator


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
    def get_global_list(cls):
        return cls.global_list

    @classmethod
    def get_tmp_list(cls):
        return cls.tmp_list

    @classmethod
    def set_tmp_list(cls, value):
        cls.tmp_list = value

    def __init__(self, key, outer=None):
        # print "start:", key

        self.get_tmp_list().append({'name': key})

        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

    def __call__(self, *args, **kwargs):
        # print "end:", self._key

        tmp_list = self.get_tmp_list()
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
            elif 'children' in tmp_list[-2]:
                # > A.B [C]
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
            self.get_tmp_list().append({'name': '.'})
            return type(self)(key, self)

    def __getitem__(self, key):
        # print "parameter: " + str(key)
        tmp_list = self.get_tmp_list()

        if type(key) == int or type(key) == float:
            # [1]
            addval = {'type': 'bracket', 'value': str(key)}
            if "children" in tmp_list[-1]:
                tmp_list[-1]['children'].append(addval)
            else:
                tmp_list[-1]['children'] = [addval]
        else:
            # [michaelis_menten]
            effect_list = tmp_list[2:]
            del tmp_list[2:]
            addval = {'xxx': 'effector', 'value': effect_list}

            if len(tmp_list) >= 3: # 7/20 pattern 3) L.R>L+R[]
                tmp_list.append(addval)
            else:
                tmp_list[1]['children'].append(addval)

        return self

    def operator(self, rhs):
        tmp_list = self.get_tmp_list()

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

        self.get_global_list().append(tmp_dict)

        # tmp_list = [] and self.tmp_list = [] don't work
        self.set_tmp_list([])

    def __gt__(self, rhs):
        self.operator('gt')

    def __lt__(self, rhs):
        term = self.get_tmp_list().pop(-1)
        self.get_tmp_list()[0]['children'].append(term)
        return True

    def __ne__(self, rhs):
        self.operator('neq')

    def __add__(self,rhs):
        tmp_list = self.get_tmp_list()

        if tmp_list[-2].get('type') == 'add':
            # A+B+C(reactants)
            tmp_list[-2]['children'].append(tmp_list.pop(-1))
        elif len(tmp_list) == 2:
            # A+B(reactants)
            add_list = [tmp_list.pop(-2), tmp_list.pop(-1)]
            add_dict = {'type': 'add', 'children': add_list}
            tmp_list.append(add_dict)
        elif tmp_list[1]['children'][-1].get('type') == 'effector':
            eff_dict = tmp_list[1]['children'].pop(-1)

            if tmp_list[1].get('type') == 'add':
                # A+B+C [D](products)
                tmp_list[1]['children'].append(eff_dict['value'].pop(0))
                tmp_list[1]['children'].append(eff_dict)
            else:
                # A+B [D](products)
                add_list = [tmp_list.pop(-1), eff_dict['value'].pop(0)]
                add_list.append(eff_dict)
                add_dict = {'type': 'add', 'children': add_list}
                tmp_list.append(add_dict)
        elif tmp_list[1].get('type') == 'add':
            # A+B+C(products)
            for i in range(2, len(tmp_list)):
                tmp_list[1]['children'].append(tmp_list[i])
            del tmp_list[2:]
        else:
            # A+B(products)
            add_list = tmp_list[1:]
            del tmp_list[1:]
            add_dict = {'type':'add', 'children': add_list}
            tmp_list.append(add_dict)

        return self

    def __or__(self, rhs):
        addval = {'type': 'bracket', 'value':rhs}
        if len(self.get_tmp_list()) >= 3: # 7/20 pattern 3) L.R>L+R[]
            self.get_tmp_list().append(addval)
        else:
            self.get_tmp_list()[1]['children'].append(addval)

    def __mod__(self, rhs):
        # print "label: " + str(rhs)

        if type(rhs) in (int, float):
            addval = {'type': 'label', 'value': str(rhs)}
            self.set_with_label(True)

            if "children" in self.get_tmp_list()[-1]:
                self.get_tmp_list()[-1]['children'].append(addval)
            else:
                self.get_tmp_list()[-1]['children'] = [addval]

class MyDict(dict):
    def __init__(self):
        super(MyDict, self).__init__()

        self.newcls = type('MyAnyCallable', (AnyCallable, ), {})

    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        if key in ('True', 'False'):
            return eval(key)

        retval = self.get(key)
        if retval is None:
            retval = self.newcls(key)
        return retval

class ReactionRules(object):
    def __init__(self, m, p, newcls):
        self.model, self.parser, self.newcls = m, p, newcls

    def __enter__(self):
        pass

    def __exit__(self, *args):
        def is_func(value_):
            return value_ is None or (
                type(value_) in (int, float, types.FunctionType)) or (
                type(value_) in (list, tuple) and 
                len(value_) > 0 and type(value_[0]) is str)

        def get_func(value_=None):
            func_name_, args_, kwargs_, func_def_ = (
                'mass_action', (0, ), {}, None)
            if value_ is None:
                # return defaults
                return func_name_, args_, kwargs_, func_def_
            elif type(value_) is types.FunctionType:
                return func_name_, args_, kwargs_, value_
            elif type(value_) in (int, float):
                # | 0.1
                return func_name_, (value_, ), kwargs_, func_def_
            else: # type(value_) in (list, tuple) and type(value_[0]) is str
                # | MassAction(0.1)
                if len(value_) == 1:
                    return value_[0], args_, kwargs_, func_def_
                elif len(value_) == 2:
                    return value_[0], value_[1], kwargs_, func_def_
                elif len(value_) > 2:
                    return value_[0], value_[1], value_[2], func_def_
            
        for idx, v in enumerate(self.newcls.global_list):
            # create effector list
            if v.get('value') is not None:
                effectors = [self.model.register_species(
                        read_species(self.parser, i)) for i in v['value']]
            else:
                effectors = []

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

            # condition is not supported now
            condition = None
            if len(con_list) > 0:
                con_func = con_list[0]
            else:
                con_func = None

            con_func_f, con_func_r = None, None
            if is_func(con_func):
                con_func_f = con_func
            elif type(con_func) in (list, tuple) and len(con_func) == 2 and (
                is_func(con_func[0]) and is_func(con_func[1])):
                con_func_f, con_func_r = con_func
            else:
                # unsupported expression (error?)
                pass

            func_name_f, args_f, kwargs_f, func_def_f = get_func(con_func_f)
            func_name_r, args_r, kwargs_r, func_def_r = get_func(con_func_r)

            # Checks whether reactants/products have any labels.
            # lbflag = True in [r.has_label() for r in reactants + products]

            # Generates reaction rule.
            # lbl is required by model.Model and model.ReactionRule
            attrs = dict(k_name=func_name_f, args=args_f, kwargs=kwargs_f,
                         effectors=effectors, func_def=func_def_f,
                         lbl=self.newcls.with_label)
            rule = self.model.add_reaction_rule(
                reactants, products, condition, **attrs)
            if v['type'] == 'neq':
                # condition = swap_condition(con_list)
                attrs = dict(k_name=func_name_r, args=args_r, kwargs=kwargs_r,
                             effectors=effectors, func_def=func_def_r,
                             lbl=self.newcls.with_label)
                rule = self.model.add_reaction_rule(
                    products, reactants, condition, **attrs)

class MoleculeTypes(object):
    def __init__(self, m, p, newcls, loc=None):
        self.model, self.parser, self.newcls = m, p, newcls
        self.loc = loc

    def __enter__(self):
        pass

    def __exit__(self, *args):
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

                    if 'name' in j:
                        # states input
                        en_comp.set_state(en_comp.states.keys()[0], j['name'])

                    if j.get('type') is 'bracket':
                        # binding input
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

                    if j.get('type') == 'label':
                        # labeling ID
                        en_comp.label = j['value']

        except IndexError:
            quit()
        except KeyError:
            pass

def read_species(p, species):
    sp = Species()

    bind_comp = {}

    if species['name'] == '.':
        # A.B
        for entity in species['children']:
            read_entity(sp, p, entity, bind_comp)
        for comps in bind_comp.itervalues():
            if len(comps) != 2:
                pass
            else:
                sp.add_binding(comps[0], comps[1])
    else:
        # A
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
            # add labeled species
            s_list.append(sp)
        else:
            # add normal species
            s_list.append(sp2)

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

def print_tree(a, n=0, fout=sys.stdout):
    def pr_str(n, j, v=''):
        return ' ' * n + j + ' : ' + str(v)

    for idx, i in enumerate(a):
        # for each rule
        # key in ('type', 'name', 'children', 'value')
        for key, value in i.items():
            if value == []:
                fout.write('\n')
            elif key in ('children', 'value'):
                fout.write('%s ' % pr_str(n, key))

                if type(value) == list:
                    if type(value[0]) == dict:
                        # for each species
                        print_tree(value, n + 12, fout)
                    else:
                        # for each function like (['MassAction', 0.3])
                        fout.write('%s\n' % str(value))
                else:
                    fout.write('%s\n' % str(value))
            else:
                fout.write('%s\n' % pr_str(n if idx > 0 else 0, key, value))

class MoleculeInits(object):
    def __init__(self, m, p, newcls):
        self.model, self.parser, self.newcls = m, p, newcls
        self.seed_species = {}

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.seed_species = {}
        for i in self.newcls.tmp_list:
            sp = read_species(self.parser, i)
            sp.concrete = True

            species_str_list = [
                x.str_simple() for x in self.seed_species.keys()]
            if sp.str_simple() in species_str_list:
                raise ValueError

            sp = self.model.register_species(sp)

            self.seed_species[sp] = float(i['children'].pop(-1)['value'])

        self.newcls.tmp_list = []

class Pybngl(object):
    def __init__(self, verbose=False, loc=None, fout=sys.stdout):
        self.verbose = verbose
        self.fout = fout
        self.loc = loc

        self.namespace = MyDict()

    def is_verbose(self):
        return self.verbose

    def parse_model(self, filename, m=None, p=None, params={}):
        if m is None: m = Model()
        if p is None: p = Parser()

        namespace = self.namespace
        namespace.update(params)
        namespace['reaction_rules'] = ReactionRules(
            m, p, namespace.newcls)
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

        # Outputs information to stdout
        if self.is_verbose():
            print_tree(namespace.newcls.global_list, fout=self.fout)

            self.fout.write('# << reaction rules >>\n')
            cnt = 1
            for rule_id in sorted(m.reaction_rules.iterkeys()):
                rule = m.reaction_rules[rule_id]
                self.fout.write('# %d %s\n' % (cnt, rule.str_simple()))
                cnt += 1
            self.fout.write('#\n')

            self.fout.write('# << species >>\n')
            cnt = 1
            for sp_id in sorted(m.concrete_species.iterkeys()):
                sp = m.concrete_species[sp_id]
                self.fout.write('# %d %s\n' % (cnt, sp.str_simple()))
                cnt += 1
            self.fout.write('#\n')

            # self.fout.write('# << values >>\n')
            # self.fout.write('# volume : %g\n' % volume)
            # self.fout.write('#\n')

        return m, seed_species, namespace

    def generate_reaction_network(
        self, m, seed_species, rulefilename=None, maxiter=10):
        try:
            reaction_results = m.generate_reaction_network(
                seed_species.keys(), maxiter)
        except Error, inst:
            print inst
            exit()

        # Outputs information to stdout
        if self.is_verbose():
            self.fout.write('# << reactions >>\n')
            cnt = 1
            for result in reaction_results:
                for r in result.reactions:
                    self.fout.write('# %d %s\n' % (cnt, r.str_simple()))
                    cnt += 1
            self.fout.write('#\n')

        # Outputs reactions to rulefile
        if rulefilename is not None:
            fout = open(rulefilename, 'w')
            cnt = 1
            for result in reaction_results:
                for r in result.reactions:
                    fout.write('%d %s\n' % (cnt, r.str_simple()))
                    cnt += 1
            fout.close()        

        return reaction_results

def create_world(m, seed_species):
    w = World.World()
    w.add_species(m.concrete_species.keys())
    for species, value in seed_species.items():
        w.set_value(species.id, value)
    w.model = m
    return w


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

    def execute_simulation(
        simulator, num_of_steps=0, duration=-1, fout=sys.stdout):
        # run simulation
        if duration > 0:
            # duration is defined
            simulator.run(duration)
        else:
            # duration is not defined
            simulator.step(num_of_steps)

        output_series = simulator.get_logged_data()
        
        # print results
        header = 'time\t%s' % ('\t'.join([
            species.str_simple() for species in simulator.get_species()]))
        fout.write('#%s\n' % header)
        fout.write('#\n')

        for output in output_series:
            t, values = output[0], output[1: ]
            fout.write('%s\t%s\n' % (
                t, '\t'.join(['%s' % value for value in values])))

        # import os.path
        # ##### ONLY FOR label.py #####
        # if os.path.split(filename) == 'label.py':
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
        # ##### ONLY FOR label.py #####


        # ##### ONLY FOR toy.py #####
        # if os.path.split(filename) == 'toy.py':
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
        # ##### ONLY FOR toy.py #####

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
    m, seed_species, _ = pybngl.parse_model(filename, m, p)
    reaction_results = pybngl.generate_reaction_network(
        m, seed_species, maxiter=options.itr_num, 
        rulefilename=options.rulefile)

    w = create_world(m, seed_species)
    simulator = Simulator.ODESimulator(m, w, reaction_results)

    output_series = execute_simulation(
        simulator, num_of_steps=options.step_num,
        duration=options.end_time)
