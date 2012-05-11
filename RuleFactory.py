'''
  RuleFactory classes.

  $Id$
'''

from RuleProduct import AnyCallable

class RuleFactory(object):
    def __init__(self, model = None, parser = None):
        self.__model = model
        self.__parser = parser

    def create_AnyCallable(self, key, outer = None, **kwargs):
        obj = AnyCallable(key, outer, **kwargs)
        obj.facotry = self
        return obj

    def create_RuleEntityComponent(self, key, bind = None, 
                                   state = None, label = None):
        obj = RuleEntityComponent(key, bind, state, label)
        obj.factory = self
        return obj

    def create_RuleEntity(self, key, k = 0, effector = None):
        obj = RuleEntity(key, k, effector)
        obj.facotry = self
        return obj

    def create_RuleEntitySet(self, en, k = 0, effector = None):
        obj = RuleEntitySet(en, k, effector)
        obj.factory = self
        return obj

    def create_RuleEntitySetList(self, sp, k = 0, effector = None):
        obj = RuleEntitySetList(sp, k, effector)
        obj.factory = self
        return obj

    def create_PartialEntity(self, sp, key):
        obj = PartialEntity(sp, key)
        obj.factory = self
        return obj

    def create_Rule(self, reactants, products, direction = '>'):
        obj = Rule(reactants, products, direction)
        obj.factory = self
        return obj
