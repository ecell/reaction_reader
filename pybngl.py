'''
  refactored pybngl.py
'''
from __future__ import with_statement
from model.Model import *
# from model.Species import Species
# from model.Error import Error
# from model.general_func import *
import types

import World
import Simulator
import RuleFactory

disp = False

class MoleculeTypesAnyCallable(RuleFactory.AnyCallable):
    def __call__(self, *args, **kwargs):
        if disp:
            print 'MoleculeTypesAnyCallable.__call__()*',
            print ' self:', self, ', args:', args, ', kwargs:', kwargs

        obj = super(MoleculeTypesAnyCallable, self).__call__(*args, **kwargs)

        for entity in obj.entities:
            entity_name = str(entity.name)
            entity_type = self.factory.model.add_entity_type(entity_name)

            for component in entity.components:
                component_name = str(component.name)
                if component.kwargs.get('state') != None:
                    state_name = 'state_' + entity_name + '_' + component_name
                    state_type = [str(i) for i in component.kwargs['state']]
                    state = self.factory.model.add_state_type(state_name,
                                                              state_type)
                    entity_type.add_component(component_name,
                                              {component_name: state})
                else:
                    entity_type.add_component(component_name)

            if disp:
                print '[MoleculeTypes] ' + str(obj)

        return obj
        # return entity_type

class MoleculeTypesRuleFactory(RuleFactory.RuleFactory):
    def create_AnyCallable(self, *args, **kwargs):
        obj = MoleculeTypesAnyCallable(*args, **kwargs)
        obj.factory = self
        return obj

class MoleculeInitsRuleEntitySet(RuleFactory.RuleEntitySet):
    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key

        obj = super(MoleculeInitsRuleEntitySet, self).__getitem__(key)

        converter = RuleEntityConverter()
        species = converter.RuleEntitySet_to_Species(obj)

        obj.factory.model.register_species(species)
        obj.factory.kwargs['seed_species'][species] = key

        if disp:
            # print '[MoleculeInits] ' + str(obj) + ' [' + str(obj.key) + ']'
            print '[MoleculeInits] ' + species.str_simple() + ' [' + str(obj.key) + ']'

        return self
        # return species

class MoleculeInitsRuleFactory(RuleFactory.RuleFactory):
    def __init__(self, *args, **kwargs):
        super(MoleculeInitsRuleFactory, self).__init__(*args, **kwargs)

    def create_RuleEntitySet(self, *args, **kwargs):
        obj = MoleculeInitsRuleEntitySet(*args, **kwargs)
        obj.factory = self
        return obj

class ReactionRulesRuleEntitySetList(RuleFactory.RuleEntitySetList):
    def __gt__(self, rhs):
        if disp:
            print 'ReactionRulesRuleEntitySetList.__gt__()*',
            print ' self:', self, ', rhs:', rhs

        obj = super(ReactionRulesRuleEntitySetList, self).__gt__(rhs)

        c = RuleEntityConverter()

        reactants = [c.RuleEntitySet_to_Species(i) for i in obj.reactants.species]
        products = [c.RuleEntitySet_to_Species(i) for i in obj.products.species]

        if isinstance(obj.key, tuple):
            effector_list = list(obj.key)
        elif obj.key != None:
            effector_list = [obj.key]
        else:
            effector_list = []
        effectors = [c.RuleEntitySet_to_Species(i) for i in effector_list]

        for i in reactants + products + effectors:
            obj.factory.model.register_species(i)

        rule = obj.factory.model.add_reaction_rule(reactants, products,
                                                   k = obj.rhs)

        if disp:
            # print '[ReactionRules] ' + str(obj)
            print '[ReactionRules] ' + rule.str_simple()

        return obj
        # return rule

    def __eq__(self, rhs):
        if disp:
            print 'ReactionRulesRuleEntitySetList.__eq__()*',
            print ' self:', self, ', rhs:', rhs

        obj = super(ReactionRulesRuleEntitySetList, self).__eq__(rhs)

        c = RuleEntityConverter()

        reactants = [c.RuleEntitySet_to_Species(i) for i in obj.reactants.species]
        products = [c.RuleEntitySet_to_Species(i) for i in obj.products.species]

        if isinstance(obj.key, tuple):
            effector_list = list(obj.key)
        elif obj.key != None:
            effector_list = [obj.key]
        else:
            effector_list = []
        effectors = [c.RuleEntitySet_to_Species(i) for i in effector_list]

        for i in reactants + products + effectors:
            obj.factory.model.register_species(i)

        rule0 = obj.factory.model.add_reaction_rule(reactants, products,
                                                    k = obj.rhs[0])
        rule1 = obj.factory.model.add_reaction_rule(products, reactants,
                                                    k = obj.rhs[1])

        if disp:
            # print '[ReactionRules] ' + str(obj)
            print '[ReactionRules] ' + rule0.str_simple()
            print '[ReactionRules] ' + rule1.str_simple()

        return obj
        # return rule

class ReactionRulesRuleFactory(RuleFactory.RuleFactory):
    def create_RuleEntitySetList(self, *args, **kwargs):
        obj = ReactionRulesRuleEntitySetList(*args, **kwargs)
        obj.factory = self
        return obj

class RuleEntityConverter(object):
    def AnyCallable_to_EntityType(self, AC):
        pass

    def RuleEntitySet_to_Species(self, RES):
        species = Species()
        bind_pair = {}

        for entity in RES.entities:
            entity_name = str(entity.name)
            entity_type = RES.factory.model.entity_types[entity_name]
            en = species.add_entity(entity_type)

            for component in entity.components:
                component_name = str(component.name)
                comp = en.find_components(component_name)[0]
                comp.binding_state = BINDING_NONE
                state = None
                bind = None

                if hasattr(component.kwargs.get('state'), 'kwargs'): # Y=U[1]
                    state = component.kwargs['state'].name
                    bind = component.kwargs['state'].kwargs['bind']
                elif component.kwargs.get('state') != None: # Y=U
                    state = component.kwargs['state'].name
                elif component.kwargs.get('bind') != None: # Y[1]
                    bind = component.kwargs['bind']

                if state != None:
                    comp.set_state(comp.states.keys()[0], str(state))

                if bind != None:
                    if str(bind) != BINDING_ANY_STRING:
                        comp.binding_state = BINDING_SPECIFIED
                        if bind_pair.get(bind) == None:
                            bind_pair[bind] = comp
                        else:
                            species.add_binding(bind_pair[bind], comp)
                    else:
                        comp.binding_state = BINDING_ANY
                        species.add_binding(comp, None, False)

        species.concrete = True
        return species

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
    def __init__(self, m, mydict, loc=None):
        self.model, self.mydict = m, mydict
        self.loc = loc

    def __enter__(self):
        self.mydict.factory.append(MoleculeTypesRuleFactory(self.model))

    def __exit__(self, *args):
        self.mydict.factory.pop()

class MoleculeInits(object):
    def __init__(self, m, mydict):
        self.model, self.mydict = m, mydict
        self.seed_species = {}

    def __enter__(self):
        self.mydict.factory.append(MoleculeInitsRuleFactory(
                self.model, seed_species = self.seed_species))

    def __exit__(self, *args):
        self.mydict.factory.pop()

class ReactionRules(object):
    def __init__(self, m, mydict):
        self.model, self.mydict = m, mydict

    def __enter__(self):
        self.mydict.factory.append(ReactionRulesRuleFactory(self.model))

    def __exit__(self, *args):
        self.mydict.factory.pop()

    # def __exit__(self, *args):
    #     def is_func(value_):
    #         return value_ is None or (
    #             type(value_) in (int, float, types.FunctionType)) or (
    #             type(value_) in (list, tuple) and
    #             len(value_) > 0 and type(value_[0]) is str)

    #     def get_func(value_=None):
    #         func_name_, args_, kwargs_, func_def_ = (
    #             'mass_action', (0, ), {}, None)
    #         if value_ is None:
    #             # return defaults
    #             return func_name_, args_, kwargs_, func_def_
    #         elif type(value_) is types.FunctionType:
    #             return func_name_, args_, kwargs_, value_
    #         elif type(value_) in (int, float):
    #             # | 0.1
    #             return func_name_, (value_, ), kwargs_, func_def_
    #         else: # type(value_) in (list, tuple) and type(value_[0]) is str
    #             # | MassAction(0.1)
    #             if len(value_) == 1:
    #                 return value_[0], args_, kwargs_, func_def_
    #             elif len(value_) == 2:
    #                 return value_[0], value_[1], kwargs_, func_def_
    #             elif len(value_) > 2:
    #                 return value_[0], value_[1], value_[2], func_def_

    #     for idx, v in enumerate(self.newcls.global_list):
    #         # create effector list
    #         if v.get('value') is not None:
    #             effectors = [self.model.register_species(
    #                     read_species(self.parser, i)) for i in v['value']]
    #         else:
    #             effectors = []

    #         # create reactants/products
    #         reactants, con_list = read_patterns(
    #             self.model, self.parser, v['children'][0],
    #             self.newcls.with_label)
    #         products, con_list = read_patterns(
    #             self.model, self.parser, v['children'][1],
    #             self.newcls.with_label)

    #         # for con_idx, con_func in enumerate(con_list):
    #         #     if type(con_func) == float:   # [SPEED_FUNCTION]
    #         #         speed = speed_r = con_func
    #         #         con_list.pop(con_idx)
    #         #     elif type(con_func) == tuple: # [MassAction2(.1, .2)]
    #         #         speed = con_func[0]
    #         #         speed_r = con_func[int(bool(con_func[1]))]
    #         #         con_list.pop(con_idx)

    #         # if len(con_list) >= 2:            # [CONDITION_FUNCTION]
    #         #     condition = AndCondition(con_list)
    #         # elif con_list != []:
    #         #     condition = con_list[0]
    #         # else:
    #         #     condition = None
    #         # set speed function

    #         # condition is not supported now
    #         condition = None
    #         if len(con_list) > 0:
    #             con_func = con_list[0]
    #         else:
    #             con_func = None

    #         con_func_f, con_func_r = None, None
    #         if is_func(con_func):
    #             con_func_f = con_func
    #         elif type(con_func) in (list, tuple) and len(con_func) == 2 and (
    #             is_func(con_func[0]) and is_func(con_func[1])):
    #             con_func_f, con_func_r = con_func
    #         else:
    #             # unsupported expression (error?)
    #             pass

    #         func_name_f, args_f, kwargs_f, func_def_f = get_func(con_func_f)
    #         func_name_r, args_r, kwargs_r, func_def_r = get_func(con_func_r)

    #         # Checks whether reactants/products have any labels.
    #         # lbflag = True in [r.has_label() for r in reactants + products]

    #         # Generates reaction rule.
    #         # lbl is required by model.Model and model.ReactionRule
    #         attrs = dict(k_name=func_name_f, args=args_f, kwargs=kwargs_f,
    #                      effectors=effectors, func_def=func_def_f,
    #                      lbl=self.newcls.with_label)
    #         rule = self.model.add_reaction_rule(
    #             reactants, products, condition, **attrs)
    #         if v['type'] == 'neq':
    #             # condition = swap_condition(con_list)
    #             attrs = dict(k_name=func_name_r, args=args_r, kwargs=kwargs_r,
    #                          effectors=effectors, func_def=func_def_r,
    #                          lbl=self.newcls.with_label)
    #             rule = self.model.add_reaction_rule(
    #                 products, reactants, condition, **attrs)

class Pybngl(object):
    def __init__(self, verbose=False, loc=None, fout=sys.stdout):
        self.verbose = verbose
        self.fout = fout
        self.loc = loc

    def is_verbose(self):
        return self.verbose

    def parse_model(self, filename, m=None, params={}):
        if m is None: m = Model()

        namespace = MyDict()
        namespace.update(params)
        namespace['reaction_rules'] = ReactionRules(m, namespace)
        namespace['molecule_inits'] = MoleculeInits(m, namespace)
        namespace['molecule_types'] = MoleculeTypes(m, namespace,
                                                    loc=self.loc)

        exec file(filename) in namespace

        seed_species = namespace['molecule_inits'].seed_species

        # sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
        # seed_values = [10000 * N_A, 5000 * N_A, 2000 * N_A]
        # volume = 1
        # for i, v in enumerate(m.reaction_rules): print m.reaction_rules[v]

        # Outputs information to stdout
        if self.is_verbose():
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
        simulator, num_of_steps=0, duration=-1, fout=sys.stdout, verbose=True):
        # run simulation
        if duration > 0:
            # duration is defined
            simulator.run(duration)
        else:
            # duration is not defined
            simulator.step(num_of_steps)

        output_series = simulator.get_logged_data()

        if verbose:
            # print results
            header = 'time\t%s' % ('\t'.join([
                species.str_simple() for species in simulator.get_species()]))
            fout.write('#%s\n' % header)
            fout.write('#\n')

            for output in output_series:
                t, values = output[0], output[1: ]
                fout.write('%s\t%s\n' % (
                    t, '\t'.join(['%s' % value for value in values])))

        return output_series


    m = Model()

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
    m, seed_species, _ = pybngl.parse_model(filename, m)
    reaction_results = pybngl.generate_reaction_network(
        m, seed_species, maxiter=options.itr_num,
        rulefilename=options.rulefile)

    w = create_world(m, seed_species)
    simulator = Simulator.ODESimulator(m, w, reaction_results)

    output_series = execute_simulation(
        simulator, num_of_steps=options.step_num,
        duration=options.end_time, verbose=options.show_mes)
