# Constants for the condition of reaction rule.
REACTANTS = 1
PRODUCTS = 2

import sys
from Binding import *
from Condition import *
from Component import *
from Correspondence import *
from Entity import *
from EntityComponent import *
from EntityType import *
from Pair import *
from ReactionResult import *
from ReactionRule import *
from StateType import *

class Model(object):
    '''
    The rule-based model.
    '''

    def __init__(self, **attrs):
        '''
        Initializes this model.

        attrs: Map of attributes.
        '''
        self.__state_types = {}
        self.__entity_types = {}
        self.__species = {}
        self.__concrete_species = {}
        self.__reaction_rules = {}
        self.__reaction_results = {}
        self.__disallow_implicit_disappearance = True
        self.__serial_species = 0
        self.__serial_reaction_rules = 0
        self.__serial_reaction_results = 0
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def state_types(self):
        '''Returns the map of state types.'''
        return self.__state_types

    @property
    def entity_types(self):
        '''Returns the map of entity types.'''
        return self.__entity_types

    @property
    def species(self):
        '''Returns the map of all species.'''
        return self.__species

    @property
    def concrete_species(self):
        '''Returns the map of concrete species.'''
        return self.__concrete_species

    @property
    def reaction_rules(self):
        '''Returns the map of reaction rules.'''
        return self.__reaction_rules

    @property
    def reaction_results(self):
        '''Returns the map of reaction results.'''
        return self.__reaction_results

    @property
    def concrete_reactions(self):
        '''Returns the list of concrete reactions.'''
        reactions = []
        for result in self.reaction_results.itervalues():
            for reaction in result.reactions:
                reactions.append(reaction)
        reactions.sort(lambda x,y: x.id - y.id)
        return reactions

    def getdisallow_implicit_disappearance(self):
        '''
        Returns the flag whether to disallow implicit disappearance of 
        entities through the reaction.
        '''
        return self.__disallow_implicit_disappearance

    def setdisallow_implicit_disappearance(self, b):
        '''
        Sets the flag whether to disallow implicit disappearance of 
        entities through the reaction.

        b: The flag to set.
        '''
        self.__disallow_implicit_disappearance = b

    disallow_implicit_disappearance = property(\
        getdisallow_implicit_disappearance, \
        setdisallow_implicit_disappearance)

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

    def __setitem__(self, k, v):
        '''
        Sets the attributes.

        k: The key.
        v: The value.
        '''
        self.__attrs[k] = v

    def __getitem__(self, k):
        '''
        Returns the value of the attribute of given key.
        If given key is not found, returns None.

        k: The key.
        '''
        return self.__attrs.get(k, None)

    def add_state_type(self, name, states, **attrs):
        '''
        Creates and registers a new state type.

        name: the name of state type
        states: array of the states
        attrs: Map of attributes.
        '''
        assert name not in self.__state_types
        state_type = StateType(name, list(states), **attrs)
        self.__state_types[name] = state_type
        return state_type

    def add_entity_type(self, name, **attrs):
        '''
        Creates and registers a new entity type.

        states: a map of internal states of a spacies
        attrs: Map of attributes.
        '''
        assert name not in self.__entity_types
        entity_type = EntityType(name, **attrs)
        self.__entity_types[name] = entity_type
        return entity_type

    def register_species(self, species):
        '''
        Registeres a given species.
        Returns the registered species object.
        If equivalent pattern species already exists, returns it.

        species: a species
        '''
        # Checks whether given species already exists.
        for sp in self.__species.itervalues():
            if species.equals(sp):
                return sp

        # Updates the concreteness flag.
        species.concrete = species.check_concreteness()

        self.__serial_species += 1
        cp = species.copy(self.__serial_species)
        self.__species[self.__serial_species] = cp
        if species.concrete:
            self.__concrete_species[self.__serial_species] = cp
        return cp

    def add_reaction_rule(self, reactants, products, condition=None, \
        **attrs):
        '''
        Creates and registers a new reaction rule.

        reactants: List of pattern species of reactants.
        products: List of pattern species of products.
        condition: The condition for this reaction rule.
        attrs: Map of attributes.
        '''

        # Gets the condition for this reaction rule.
        cond = None
        if not condition is None:
             if isinstance(condition, list):
                 cond = AndCondition(condition)
             else:
                 cond = condition

        # Creates an instance of a reaction rule.
        serial = self.__serial_reaction_rules + 1
        reaction_rule = ReactionRule(serial, self, list(reactants), \
            list(products), False, cond, **attrs)

        # Checks whether given reaction rule is already exists.
        for rule in self.__reaction_rules.itervalues():
            if rule.equals(reaction_rule):
                # If an equivalent reaction rule already exists, 
                # returns None.
                return None

        self.__serial_reaction_rules = serial
        self.__reaction_rules[serial] = reaction_rule
        return reaction_rule

    def add_concrete_reaction(self, rule, reactants, products):
        '''
        Creates and registers a new reaction with concrete reactant 
        and product species.
        '''
        # Checks the concreteness.
        for sp in reactants:
            assert sp.check_concreteness()
        for sp in products:
            assert sp.check_concreteness()

        # Creates a concrete reaction.
        serial = self.__serial_reaction_results + 1
        reaction = ReactionRule(serial, self, reactants, products, True)

        # Checks whether the reaction satisfies the condition.
        if not rule.condition is None:
            if not rule.condition.satisfies(reaction):
                return None

        # Checks whether given reaction rule is already exists.
        for ex_rule_id, ex_result in self.reaction_results.iteritems():
            for ex_reaction in ex_result.reactions:
                if ex_reaction.equals(reaction):
                    if rule.id == ex_rule_id:
                        return None
                    else:
                        msg = 'A concrete reaction \n'
                        msg += '  %s\n' % reaction.str_simple()
                        msg += 'is generated from multiple reaction rules:\n'
                        msg += '  %s\n' % rule.str_simple()
                        msg += 'and \n'
                        msg += '  %s.' % ex_result.reaction_rule.str_simple()
                        raise Error(msg)

        # Updates the attributes.
        self.__serial_reaction_results = serial
        if not rule.id in self.reaction_results:
            self.reaction_results[rule.id] = ReactionResult(rule)
        self.reaction_results[rule.id].add_reaction(reaction)

        return reaction

    def generate_reactions(self, species_list):
        '''
        Generates the reactions by applying all reaction rules to given species 
        and generated species.
        '''
        result_list = []
        rules = self.reaction_rules.copy()
        sp_list = list(species_list)
        for rule in rules.itervalues():
            reactions = rule.generate_reactions_orig(sp_list)
            if len(reactions):
                result = ReactionResult(rule)
                for r in reactions:
                    result.add_reaction(r)
                result_list.append(result)
        return result_list

    def generate_reaction_network(self, species_list, max_iteration=1):
        '''
        Generates the reaction network by applying all reaction rules 
        to the species given and generated in iterations.

        species_list: The list of seed species.
        max_iteration: The maximum number of the iteration.
        '''

        assert max_iteration > 0

        # Reactions for each reaction ruls.
        reaction_list_map = {}
        for (rule_id, rule) in self.reaction_rules.iteritems():
            reaction_list_map[rule_id] = []

        # Initializes the list of species with given seed species.
        sp_list = list(species_list)

        # Loops until the list of species does not vary or up to the 
        # max iteration number.
        for i in range(max_iteration):

            # The counter for new species.
            new_species_cnt = 0

            # Finds the reaction rules and reactions.
            results = self.generate_reactions(sp_list)

            # Loops for the results.
            for result in results:
                rule = result.reaction_rule

                # Loops for the reactions.
                for reaction in result.reactions:
                    # Checks whether created reaction exists in the list 
                    # of reactions.
                    exists = False
                    reaction_list = reaction_list_map[rule.id]
                    for r in reaction_list:
                        if r.equals(reaction):
                            exists = True
                            break

                    # If the created reaction is a new one, add it 
                    # to the list of reactions.
                    if not exists:
                        reaction_list.append(reaction)

                    # Loops for the reactant species.
                    for p in reaction.products:
                        # Checks whether created species exists 
                        # in the list of species.
                        exists = False
                        for sp in sp_list:
                            if p.equals(sp):
                                exists = True
                                break
                        # If the created species is a new one, add it 
                        # to the species list.
                        if not exists:
                            sp_list.append(p)
                            new_species_cnt += 1

            # If new species are not generated, breaks the loop.
            if not new_species_cnt:
                break

        # Creates the returned value.
        result_list = []
        for (rule_id, reactions) in reaction_list_map.iteritems():
            rule = self.reaction_rules[rule_id]
            result = ReactionResult(rule)
            for r in reactions:
                result.add_reaction(r)
            result_list.append(result)

        return result_list




class Error(Exception):
    '''The error.'''

    def __init__(self, value):
        '''
        Initializes this error object.

        value: A value set to this error.
        '''
        self.__value = value

    def __str__(self):
        '''Returns the string representation of this object.'''
        return str(self.__value)


