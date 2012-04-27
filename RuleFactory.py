class FactoryProduct(object):
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

class AnyCallable(FactoryProduct):
    def __init__(self, key, *args, **kwargs):
        FactoryProduct.__init__(key, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = self.factory.create_rule_entity(self.key, *args, **kwarg)
        return obj

class RuleEntity(FactoryProduct):
    def __init__(self, key, *args, **kwargs):
        FactoryProduct.__init__(key, *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
    
class RuleFactory:
    def create_any_callable(self, *args, **kwargs):
        obj = AnyCallable(self, *args, **kwargs)
        obj.factory = self
        return obj

    def create_rule_entity(self, *args, **kwargs):
        obj = RuleEntity(self, *args, **kwargs)
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

    def create_any_callable(self, *args, **kwargs):
        obj = MoleculeTypesAnyCallable(self, *args, **kwargs)
        obj.factory = self
        return obj

class
