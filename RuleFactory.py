class RuleFactoryProduct(object):
    def __init__(self, key, *args, **kwargs):
        self.key = key
        self.__factory = None

    def set_factory(self, factory):
        self.__factory = factory

    def get_factory(self):
        # if self.__factory is None:
        #     raise Error, "No factory is assigned."
        return self.__factory

    factory = property(get_factory, set_factory)

class AnyCallable(RuleFactoryProduct):
    def __init__(self, key, *args, **kwargs):
        RuleFactoryProduct.__init__(key, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = self.factory.create_RuleEntity(self.key, *args, **kwarg)
        return obj

class RuleEntity(RuleFactoryProduct):
    def __init__(self, key, *args, **kwargs):
        RuleFactoryProduct.__init__(key, *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
    
class RuleFactory(object):
    def create_AnyCallable(self, *args, **kwargs):
        obj = AnyCallable(*args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, *args, **kwargs):
        obj = RuleEntity(*args, **kwargs)
        obj.factory = self
        return obj

class MoleculeTypesAnycallable(AnyCallable):
    def __call__(self, *args, **kwargs):
        obj = AnyCallable.__call__(self, *args, **kwargs)

        # self.factory.model.add_species(...)

        return obj

class MoleculeTypesRuleFactory(RuleFactory):
    def __init__(self, model):
        RuleFactory.__init__(self)

        self.model = model

    def create_AnyCallable(self, *args, **kwargs):
        obj = MoleculeTypesAnyCallable(*args, **kwargs)
        obj.factory = self
        return obj

class MoleculeInitsAnycallable(AnyCallable):
    def __call__(self, *args, **kwargs):
        obj = AnyCallable.__call__(self, *args, **kwargs)

        return obj

class MoleculeInitsRuleFactory(RuleFactory):
    def __init__(self, model):
        RuleFactory.__init__(self)

        self.model = model

    def create_AnyCallable(self, *args, **kwargs):
        obj = MoleculeInitsAnyCallable(*args, **kwargs)
        obj.factory = self
        return obj

class ReactionRulesAnycallable(AnyCallable):
    def __call__(self, *args, **kwargs):
        obj = AnyCallable.__call__(self, *args, **kwargs)

        return obj

class ReactionRulesRuleFactory(RuleFactory):
    def __init__(self, model):
        RuleFactory.__init__(self)

        self.model = model

    def create_AnyCallable(self, *args, **kwargs):
        obj = ReactionRulesAnyCallable(*args, **kwargs)
        obj.factory = self
        return obj
