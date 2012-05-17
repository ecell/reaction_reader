'''
  refactored pybngl.py
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

from RuleFactory import RuleFactory
from RuleProduct import *

disp = False


class MoleculeTypesRuleFactory(RuleFactory):
    def create_AnyCallable(self, name, *args, **kwargs):
        obj = MoleculeTypesAnyCallable(name, *args, **kwargs)
        obj.factory = self
        return obj

#    def create_RuleEntityComponent(self, name, bind = None, 
#                                   state = None, label = None):
#        obj = MoleculeTypesRuleEntityComponent(name, bind, state, label)
#        obj.factory = self
#        return obj

    def create_RuleEntityComponent(self, name, *args, **kwargs):
        obj = MoleculeTypesRuleEntityComponent(name, *args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, name, rhs = None, key = None):
        obj = MoleculeTypesRuleEntity(name, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySet(self, en, rhs = None, key = None):
        obj = MoleculeTypesRuleEntitySet(en, rhs, key)
        obj.factory = self
        return obj

#    def create_RuleEntitySetList(self, sp, rhs = None, key = None):
#        obj = MoleculeTypesRuleEntitySetList(sp, rhs, key)
#        obj.factory = self
#        return obj

    def create_PartialEntity(self, sp, name):
        obj = MoleculeTypesPartialEntity(sp, name)
        obj.factory = self
        return obj

#    def create_Rule(self, reactants, products, direction = '>'):
#        obj = MoleculeTypesRule(reactants, products, direction)
#        obj.factory = self
#        return obj


class MoleculeInitsRuleFactory(RuleFactory):
    def create_AnyCallable(self, name, *args, **kwargs):
        obj = MoleculeInitsAnyCallable(name, *args, **kwargs)
        obj.factory = self
        return obj

#    def create_RuleEntityComponent(self, name, bind = None, 
#                                   state = None, label = None):
#        obj = MoleculeInitsRuleEntityComponent(name, bind, state, label)
#        obj.factory = self
#        return obj
    def create_RuleEntityComponent(self, name, *args, **kwargs):
        obj = MoleculeInitsRuleEntityComponent(name, *args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, name, rhs = None, key = None):
        obj = MoleculeInitsRuleEntity(name, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySet(self, en, rhs = None, key = None):
        obj = MoleculeInitsRuleEntitySet(en, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySetList(self, sp, rhs = None, key = None):
        obj = MoleculeInitsRuleEntitySetList(sp, rhs, key)
        obj.factory = self
        return obj

    def create_PartialEntity(self, sp, name):
        obj = MoleculeInitsPartialEntity(sp, name)
        obj.factory = self
        return obj

#    def create_Rule(self, reactants, products, direction = '>'):
#        obj = MoleculeInitsRule(reactants, products, direction)
#        obj.factory = self
#        return obj


class ReactionRulesRuleFactory(RuleFactory):
    def create_AnyCallable(self, name, *args, **kwargs):
        obj = ReactionRulesAnyCallable(name, *args, **kwargs)
        obj.factory = self
        return obj

#    def create_RuleEntityComponent(self, name, bind = None, 
#                                   state = None, label = None):
#        obj = ReactionRulesRuleEntityComponent(name, bind, state, label)
#        obj.factory = self
#        return obj
    def create_RuleEntityComponent(self, name, *args, **kwargs):
        obj = ReactionRulesRuleEntityComponent(name, *args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, name, rhs = None, key = None):
        obj = ReactionRulesRuleEntity(name, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySet(self, en, rhs = None, key = None):
        obj = ReactionRulesRuleEntitySet(en, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySetList(self, sp, rhs = None, key = None):
        obj = ReactionRulesRuleEntitySetList(sp, rhs, key)
        obj.factory = self
        return obj

    def create_PartialEntity(self, sp, name):
        obj = ReactionRulesPartialEntity(sp, name)
        obj.factory = self
        return obj

    def create_Rule(self, reactants, products, direction = '>'):
        obj = ReactionRulesRule(reactants, products, direction)
        obj.factory = self
        return obj


class MoleculeTypesAnyCallable(AnyCallable):
    def __call__(self, *args, **kwargs):
        if disp:
            print 'MoleculeTypesAnyCallable.__call__()*',
            print ' self:', self, ', args:', args, ', kwargs:', kwargs

        obj = self.factory.create_PartialEntity(None,
                                         self.name).__call__(*args, **kwargs)
        print '[MoleculeTypes] ' + str(obj)

        # tmpmole = self.factory.model.add_entity_type(str(obj.en[0].name))

        return obj


class MoleculeInitsAnyCallable(AnyCallable):
    pass


class ReactionRulesAnyCallable(AnyCallable):
    pass


class MoleculeTypesRuleEntityComponent(RuleEntityComponent):
    pass


class MoleculeInitsRuleEntityComponent(RuleEntityComponent):
    pass


class ReactionRulesRuleEntityComponent(RuleEntityComponent):
    pass


class MoleculeTypesRuleEntity(RuleEntity):
    pass


class MoleculeInitsRuleEntity(RuleEntity):
    pass


class ReactionRulesRuleEntity(RuleEntity):
    pass


class MoleculeTypesRuleEntitySet(RuleEntitySet):
    pass


class MoleculeInitsRuleEntitySet(RuleEntitySet):
    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key

        if isinstance(key, (int, float)):
            print '[MoleculeInits] ' + str(self) + ' [' + str(key) + ']'
            self.key = str(key)
            return self
        elif isinstance(key, tuple):
            self.key = key
        else:
            self.key = (key,)
        return self


class ReactionRulesRuleEntitySet(RuleEntitySet):
    pass


#class MoleculeTypesRuleEntitySetList(RuleEntitySetList):
#    pass


class MoleculeInitsRuleEntitySetList(RuleEntitySetList):
    pass


class ReactionRulesRuleEntitySetList(RuleEntitySetList):
    pass


class MoleculeTypesPartialEntity(PartialEntity):
    pass


class MoleculeInitsPartialEntity(PartialEntity):
    pass


class ReactionRulesPartialEntity(PartialEntity):
    pass


#class MoleculeTypesRule(Rule):
#    pass


#class MoleculeInitsRule(Rule):
#    pass


class ReactionRulesRule(Rule):
    def __init__(self, reactants, products, direction = '>'):
        super(ReactionRulesRule, self).__init__(reactants, products, direction)

        if disp:
            print 'ReactionRulesRule.__init__()*',
            print ' self:', self, ', reactants:', reactants,
            print ', products:', products, ', direction', direction

        print '[ReactionRules] ' + str(self)


class MyDict(dict):
    def __init__(self):
        super(MyDict, self).__init__()
        self.factory = []

    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        retval = self.get(key)
        if retval is None:
            retval = self.factory[-1].create_AnyCallable(key)
        return retval


class MoleculeTypes(object):
    def __init__(self, m, p, mydict, loc=None):
        self.model, self.parser, self.mydict = m, p, mydict
        self.loc = loc

    def __enter__(self):
        self.mydict.factory.append(MoleculeTypesRuleFactory(
                self.model, self.parser))

    def __exit__(self, *args):
        self.mydict.factory.pop()


class MoleculeInits(object):
    def __init__(self, m, p, mydict):
        self.model, self.parser, self.mydict = m, p, mydict
        self.seed_species = {}

    def __enter__(self):
        self.mydict.factory.append(MoleculeInitsRuleFactory(
                self.model, self.parser))

    def __exit__(self, *args):
        self.mydict.factory.pop()


class ReactionRules(object):
    def __init__(self, m, p, mydict):
        self.model, self.parser, self.mydict = m, p, mydict

    def __enter__(self):
        self.mydict.factory.append(ReactionRulesRuleFactory(
                self.model, self.parser))

    def __exit__(self, *args):
        self.mydict.factory.pop()

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

        namespace = MyDict()

        namespace['reaction_rules'] = ReactionRules(m, p, namespace)
        namespace['molecule_inits'] = MoleculeInits(m, p, namespace)
        namespace['molecule_types'] = MoleculeTypes(m, p, namespace,
                                                    loc=self.loc)

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
