'''
  refactored pybngl.py

  $Id: pybngl.py,v 1.7 2012/05/09 08:39:25 knishida Exp $
'''

from __future__ import with_statement
from model.Model import *
from model.Species import Species
from model.parser import Parser
from model.Error import Error
from model.EntityType import EntityType
from model.StateType import StateType
from model.Binding import Binding
import types

import World
import Simulator

from RuleEntity import *

class Factory(object):
    def __init__(self):
        pass

    def create_AnyCallable(self, *args, **kwargs):
        obj = AnyCallable(*args, **kwargs)
        return obj


class AnyCallable(object):
    model = None

    def __init__(self, key, outer=None, **kwargs):
        self.key = key
        self.outer = outer
        self.entity = None

    def __call__(self, *args, **kwargs):
        return PartialEntity(None, self.key).__call__(*args, **kwargs)

    def __getitem__(self, key):
        return RuleEntityComponent(self.key, bind = key)

    def __str__(self):
        return str(self.key)


class MoleculeTypesAnycallable(AnyCallable):
    def __init__(self, key, outer=None, **kwargs):
        super(MoleculeTypesAnycallable, self).__init__(key, outer, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super(MoleculeTypesAnycallable, self).__call__(*args, **kwargs)
        print '[MoleculeTypes] ' + str(obj)
        return obj


class MoleculeInitsAnycallable(AnyCallable):
    def __init__(self, key, outer=None, **kwargs):
        super(MoleculeInitsAnycallable, self).__init__(key, outer, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super(MoleculeInitsAnycallable, self).__call__(*args, **kwargs)
        print '[MoleculeInits_pb] ' + str(obj)
        return obj


class ReactionRulesAnycallable(AnyCallable):
    def __init__(self, key, outer=None, **kwargs):
        super(ReactionRulesAnycallable, self).__init__(key, outer, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super(ReactionRulesAnycallable, self).__call__(*args, **kwargs)
        print '[ReactionRules_pb] ' + str(obj)
        return obj


class MyDict(dict):
    def __init__(self, model, parser):
        super(MyDict, self).__init__()
        self.newcls = [type('MyAnyCallable', (AnyCallable, ), 
                            dict(m=model, p=parser))]
        self.factory = Factory()
        
    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        retval = self.get(key)
        if retval is None:
            newcls= self.get_anycallable_cls()
            retval = newcls(key, section=type(retval).__name__)
#            retval = self.factory.create_AnyCallable(
#                key, section=type(retval).__name__)
        return retval

    def get_anycallable_cls(self):
        return self.newcls[-1]

class MoleculeTypes(object):
    def __init__(self, m, p, mydict, loc=None):
        self.model, self.parser, self.mydict = m, p, mydict
        self.loc = loc
        self.section = 'MoleculeTypes'

    def __str__(self):
        return self.section

    def __enter__(self):
        self.mydict.newcls.append(type('MyAnyCallable',
                                       (MoleculeTypesAnycallable, ), {}))
        self.mydict.newcls[-1].model = self.model
        self.mydict.newcls[-1].parser = self.parser

    def __exit__(self, *args):
        pass

class MoleculeInits(object):
    def __init__(self, m, p, mydict):
        self.model, self.parser, self.mydict = m, p, mydict
        self.seed_species = {}
        self.section = 'MoleculeInits'

    def __str__(self):
        return self.section

    def __enter__(self):
        self.mydict.newcls.append(type('MyAnyCallable',
                                       (MoleculeInitsAnycallable, ), {}))
        self.mydict.newcls[-1].model = self.model
        self.mydict.newcls[-1].parser = self.parser
        self.mydict.newcls[-1].seed_species = self.seed_species

    def __exit__(self, *args):
        pass

class ReactionRules(object):
    def __init__(self, m, p, mydict):
        self.model, self.parser, self.mydict = m, p, mydict
        self.section = 'ReactionRules'

    def __str__(self):
        return self.section

    def __enter__(self):
        self.mydict.newcls.append(type('MyAnyCallable',
                                       (ReactionRulesAnycallable, ), {}))
        self.mydict.newcls[-1].model = self.model
        self.mydict.newcls[-1].parser = self.parser


    def __exit__(self, *args):
        pass

    def __oldexit__(self, *args):
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

class Pybngl(object):
    def __init__(self, verbose=False, loc=None, fout=sys.stdout):
        self.verbose = verbose
        self.fout = fout
        self.loc = loc

    def is_verbose(self):
        return self.verbose

    def parse_model(self, filename, m=None, p=None):
        if m is None: m = Model()
        if p is None: p = Parser()

        namespace = MyDict(m, p)

        namespace['reaction_rules'] = ReactionRules(
            m, p, namespace)
        namespace['molecule_inits'] = MoleculeInits(
            m, p, namespace)
        namespace['molecule_types'] = MoleculeTypes(
            m, p, namespace, loc=self.loc)

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
            self.fout.write('# << species >>\n')
            cnt = 1
            for sp_id in sorted(m.concrete_species.iterkeys()):
                sp = m.concrete_species[sp_id]
                self.fout.write('# %d %s\n' % (cnt, sp.str_simple()))
                cnt += 1
            self.fout.write('#\n')

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
