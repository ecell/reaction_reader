#import model
import sys
from Model import Model
from Species import Species
from ReactionRule import ReactionRule
from general_func import *

class Parser(object):

    def __init__(self):
        self.__entity_types = {}

    @property
    def entity_types(self):
        '''Returns the map of entity types.(2012-04-23)'''
        return self.__entity_types

    def add_entity_type(self, entity_type):
        self.__entity_types[entity_type.name] = entity_type

    def parse_species_array(self, sp_str_list, model=None):
        sp_list = []
        for sp_str in sp_str_list:
            sp = self.parse_species(sp_str)
#            print "# *** sp_str_list in parser.parer_species_array ***"
#            print '# ', str(sp_str_list)
#            print "# *** sp  in parser.parer_species_array ***"
#            print '# ', str(sp).partition("@")[0].replace('\n','')
#            print "# *** end of parser.parer_species_array ***"
            if sp is None:
                print sp_str
            if model != None:
                sp = model.register_species(sp)
            sp_list.append(sp)
        return sp_list

    def __split_species_array_string(self, sp_array_str):
        plus_index_set = set()
        for i in range(len(sp_array_str)):
            if sp_array_str[i] == '+':
                plus_index_set.add(i)
        inside_bracket = False
        for i in range(len(sp_array_str)):
            if sp_array_str[i] == '(':
                inside_bracket = True
                continue
            elif sp_array_str[i] == ')':
                inside_bracket = False
                continue
            elif sp_array_str[i] == '+':
                if inside_bracket:
                    plus_index_set.remove(i)
        plus_index_list = list(plus_index_set)
        plus_index_list.sort()
        split_str_list = []
        start_index = 0
        for index in plus_index_list:
            split_str_list.append(sp_array_str[start_index:index])
            start_index = index + 1
            if start_index >= len(sp_array_str):
                return None
        split_str_list.append(sp_array_str[start_index:len(sp_array_str)])
        return split_str_list

    def parse_reaction(self, rule_text, m, id=0, concrete=False, \
            condition=None, register=False, **attrs):
        rp_str_list = rule_text.split('->')
        if len(rp_str_list) != 2:
            return None
        reactants_str = rp_str_list[0]
        if reactants_str.isspace() or len(reactants_str) == 0:
            reactants = []
        else:
            reactants_str_list = self.__split_species_array_string(\
                reactants_str)
            reactants = self.parse_species_array(reactants_str_list, m)
        products_str = rp_str_list[1]
        if products_str.isspace() or len(products_str) == 0:
            products = []
        else:
            products_str_list = self.__split_species_array_string(\
                products_str)
            products = self.parse_species_array(products_str_list, m)
        if register:
            rule = m.add_reaction_rule(reactants, products, condition, **attrs)
        else:
            rule = ReactionRule(id, m, reactants, products, concrete, \
                condition, **attrs)
        return rule


