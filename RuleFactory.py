'''
  RuleFactory classes.
'''
from RuleProduct import AnyCallable


class RuleFactory(object):
    def __init__(self, model = None, parser = None):
        self.__model = model
        self.__parser = parser

    def create_AnyCallable(self, name, *args, **kwargs):
        obj = AnyCallable(name, *args, **kwargs)
        obj.facotry = self
        return obj

#    def create_RuleEntityComponent(self, name, bind = None, 
#                                   state = None, label = None):
#        obj = RuleEntityComponent(name, bind, state, label)
#        obj.factory = self
#        return obj
    def create_RuleEntityComponent(self, name, *args, **kwargs):
        obj = RuleEntityComponent(name, *args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, name, rhs = None, key = None):
        obj = RuleEntity(name, rhs, key)
        obj.facotry = self
        return obj

    def create_RuleEntitySet(self, en, rhs = None, key = None):
        obj = RuleEntitySet(en, rhs, key)
        obj.factory = self
        return obj

    def create_RuleEntitySetList(self, sp, rhs = None, key = None):
        obj = RuleEntitySetList(sp, rhs, key)
        obj.factory = self
        return obj

    def create_PartialEntity(self, sp, name):
        obj = PartialEntity(sp, name)
        obj.factory = self
        return obj

    def create_Rule(self, reactants, products, direction = '>'):
        obj = Rule(reactants, products, direction)
        obj.factory = self
        return obj
