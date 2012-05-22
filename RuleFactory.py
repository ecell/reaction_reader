disp = False


class RuleFactoryProduct(object):
    def __init__(self, *args, **kwargs):
        self.__factory = None

    def set_factory(self, factory):
        self.__factory = factory

    def get_factory(self):
        return self.__factory

    factory = property(get_factory, set_factory)

class AnyCallable(RuleFactoryProduct):
    def __init__(self, name, *args, **kwargs):
        super(AnyCallable, self).__init__(name, *args, **kwargs)

        self.__name = name

    @property
    def name(self):
        return self.__name

    def to_RuleEntityComponent(self):
        # only name information is used.
        return self.factory.create_RuleEntityComponent(self.name)

    def to_PartialRuleEntity(self):
        return self.factory.create_PartialRuleEntity(None, self.name)

    def __call__(self, *args, **kwargs):
        return self.to_PartialRuleEntity().__call__(*args, **kwargs)

    def __getitem__(self, key):
        return self.factory.create_RuleEntityComponent(self.name, bind=key)

    def __str__(self):
        return str(self.name)

class RuleEntityComponent(RuleFactoryProduct):
    '''The class corresponds to EntityComponent.'''

    def __init__(self, name, *args, **kwargs):
        super(RuleEntityComponent, self).__init__(name, *args, **kwargs)

        self.__name = name
        self.__args = args
        self.__kwargs = kwargs

    @property
    def name(self):
        return self.__name

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    def to_RuleEntityComponent(self):
        return self

    def __str__(self):
        kw = ''
        for k, v in self.kwargs.iteritems():
            if type(v) == tuple:
                kw += str(k) + ':' + str([str(i) for i in v]) + ','
            else:
                kw += str(k) + ':' + str(v) + ','

        return str(self.name) + '{' + kw[:-1] + '}'

class RuleEntity(RuleFactoryProduct):
    '''The class corresponds to Entity.'''
    def __init__(self, name, rhs=None, key=None):
        super(RuleEntity, self).__init__(name, rhs, key)

        self.__name = name
        self.__components = []
        self.__rhs = rhs
        self.__key = key

    @property
    def name(self):
        return self.__name

    @property
    def components(self):
        return self.__components

    @property
    def k(self):
        return self.__k

    @property
    def rhs(self):
        return self.__rhs

    @property
    def key(self):
        return self.__key

    def join(self, comp):
        # if not issubclass(type(comp), RuleEntityComponent):
        #     raise TypeError
        self.components.append(comp)
        return self

    def to_RuleEntity(self):
        return self

    def to_RuleEntitySet(self):
        return self.factory.create_RuleEntitySet(
            self, rhs=self.rhs, key=self.key)

    def to_RuleEntitySetList(self):
        return self.to_RuleEntitySet().to_RuleEntitySetList()

    def __getitem__(self, key):
        if disp:
            print 'RuleEntity.__getitem__() * self:', self, ', key:', key
        return self.to_RuleEntitySet().__getitem__(key)

    def __getattr__(self, key):
        if disp:
            print 'RuleEntity.__getattr__() * self:', self, ', key:', key
        return self.to_RuleEntitySet().__getattr__(key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntity.__add__() * self:', self, ', rhs:', rhs
        return self.to_RuleEntitySet().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntity.__or__()* self:', self, ', rhs:', rhs
        return self.to_RuleEntitySet().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntity.__gt__()* self:', self, ', rhs:', rhs
        return self.to_RuleEntitySet().__gt__(rhs)

    def __str__(self):
        comp = [str(i) + ',' for i in self.components]
        return reduce(lambda a, b: a + b, [self.name + '('] + comp)[:-1] + ')'

class RuleEntitySet(RuleFactoryProduct):
    '''The set of RuleEntity.  This class corresponds to Species.'''

    def __init__(self, en, rhs=None, key=None):
        super(RuleEntitySet, self).__init__(en, rhs, key)

        self.__entities = [en]
        self.__rhs = rhs # renamed from 'k'
        self.__key = key # renamed from 'effector'

    @property
    def entities(self):
        return self.__entities

    @property
    def rhs(self):
        return self.__rhs

    def set_key(self, key):
        self.__key = key

    def get_key(self):
        return self.__key

    key = property(get_key, set_key)

    def join(self, en):
        # if not issubclass(type(en), RuleEntity):
        #     raise TypeError
        self.entities.append(en)
        return

    def to_RuleEntitySet(self):
        return self

    def to_RuleEntitySetList(self):
        return self.factory.create_RuleEntitySetList(
            self, rhs=self.rhs, key=self.key)

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key
        self.key = key
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySet.__getattr__()* self:', self, ', key:', key
        return self.factory.create_PartialRuleEntity(self, key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySet.__add__()* self:', self, ', rhs:', rhs
        return self.to_RuleEntitySetList().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntitySet.__or__()* self:', self, ', rhs:', rhs
        return self.to_RuleEntitySetList().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntitySet.__gt__()* self:', self, ', rhs:', rhs
        return self.to_RuleEntitySetList().__gt__(rhs)
        
    def __str__(self):
        ent = [str(i) + '.' for i in self.entities]
        return reduce(lambda a, b: a + b, ent)[:-1]

class RuleEntitySetList(RuleFactoryProduct):
    '''The list of RuleEntitySets(aka Species.)'''

    def __init__(self, sp, rhs=None, key=None):
        super(RuleEntitySetList, self).__init__(sp, rhs, key)

        self.__species = []
        self.__rhs = rhs
        self.__key = key

        self.join(sp)

    @property
    def species(self):
        return self.__species

    def get_rhs(self):
        return self.__rhs

    def set_rhs(self, rhs):
        self.__rhs = rhs

    rhs = property(get_rhs, set_rhs)

    def get_key(self):
        return self.__key

    def set_key(self, key):
        self.__key = key

    key = property(get_key, set_key)

    def join(self, sp):
        assert sp is not None 
        assert (issubclass(sp.__class__, RuleEntity)
                or issubclass(sp.__class__, RuleEntitySet))

        self.species.append(sp.to_RuleEntitySet())
        return

    def to_RuleEntitySetList(self):
        return self

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySetList.__getitem__()* self:', self, ', key:', key

        self.key = key
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySetList.__getattr__()* self:', self, ', key:', key

        pass

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__add__()* self:', self, ', rhs:', rhs

        assert (issubclass(rhs.__class__, RuleEntity)
                or issubclass(rhs.__class__, RuleEntitySet)
                or issubclass(rhs.__class__, RuleEntitySetList))

        self.join(rhs)
        self.set_rhs(rhs.rhs)
        self.set_key(rhs.key)
        return self

    def __or__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__or__()* self:', self, ', rhs:', rhs

        self.rhs = rhs
        return self

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__gt__()* self:', self, ', rhs:', rhs

        return self.factory.create_Rule(self, rhs, '>')

    def __str__(self):
        spe = [str(i) + ' + ' for i in self.species]
        return reduce(lambda a, b: a + b, spe)[:-3]

class PartialRuleEntity(RuleFactoryProduct):
    '''The class represents Complete RuleEntity(Set) and partial Entity.'''

    def __init__(self, sp, name):
        if disp:
            print 'PartialRuleEntity.__init__()* self:', self,
            print ', sp:', sp, ', name:', name

        super(PartialRuleEntity, self).__init__(sp, name)

        if sp is None:
            self.__sp = None
        else:
            assert (issubclass(sp.__class__, RuleEntity)
                    or issubclass(sp.__class__, RuleEntitySet))

            self.__sp = sp.to_RuleEntitySet()

        self.__name = name

    @property
    def name(self):
        return self.__name

    def get_sp(self):
        return self.__sp

    def set_sp(self, sp):
        self.__sp = sp

    sp = property(get_sp, set_sp)

    def __call__(self, *args, **kwargs):
        if disp:
            print 'PartialRuleEntity.__call__()* self:', self, ', args', args

        ent = self.factory.create_RuleEntity(self.name)

        assert all([(issubclass(i.__class__, AnyCallable) 
                     or issubclass(i.__class__, RuleEntityComponent)) 
                    for i in args])

        for i in args:
            ent.join(i.to_RuleEntityComponent())

        for k, v in kwargs.items():
            # if isinstance(v, RuleEntityComponent): # Y=U[1]
            #     ent.join(self.factory.create_RuleEntityComponent(
            #             k, bind=v.bind, state=v.name))
            # elif isinstance(v, tuple): # Y=(U, 1)
            #     st = tuple([str(i) for i in v])
            #     ent.join(self.factory.create_RuleEntityComponent(
            #             k, state=st))
            # else: # Y=U or Y=1
            #     ent.join(self.factory.create_RuleEntityComponent(
            #             k, state=str(v)))

            ent.join(self.factory.create_RuleEntityComponent(k, state=v))

        if self.sp is None:
            self.sp = ent.to_RuleEntitySet()
        else:
            self.sp.join(ent)

        return self.sp

class Rule(RuleFactoryProduct):
    '''The class corresponds to ReactionRule.'''
    def __init__(self, reactants, products, direction='>'):
        super(Rule, self).__init__(reactants, products, direction)

        assert issubclass(reactants.__class__, RuleEntitySetList)
        assert issubclass(products.__class__, RuleEntitySetList)

        self.__reactants = reactants
        self.__products = products
        self.__direction = direction
        self.__rhs = products.rhs
        self.__key = products.key

    @property
    def reactants(self):
        return self.__reactants

    @property
    def products(self):
        return self.__products

    @property
    def direction(self):
        return self.__direction

    @property
    def rhs(self):
        return self.__rhs

    @property
    def key(self):
        return self.__key

    def __str__(self):
        if self.key is None:
            str_eff = ''
        elif type(self.key) == tuple:
            eff = [str(i) + ', ' for i in self.key]
            str_eff = reduce(lambda a, b: a + b, [' ['] + eff)[:-2] + ']'
        else:
            str_eff = ' [' + str(self.key) + ']'

        rule = str(self.reactants) + ' > ' + str(self.products)
        rule += str_eff + ' | ' + str(self.rhs)
        return rule

class RuleFactory(object):
    def __init__(self, model=None, parser=None):
        self.__model = model
        self.__parser = parser

    @property
    def model(self):
        return self.__model

    @property
    def parser(self):
        return self.__parser

    def create_AnyCallable(self, *args, **kwargs):
        obj = AnyCallable(*args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntityComponent(self, *args, **kwargs):
        obj = RuleEntityComponent(*args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntity(self, *args, **kwargs):
        obj = RuleEntity(*args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntitySet(self, *args, **kwargs):
        obj = RuleEntitySet(*args, **kwargs)
        obj.factory = self
        return obj

    def create_RuleEntitySetList(self, *args, **kwargs):
        obj = RuleEntitySetList(*args, **kwargs)
        obj.factory = self
        return obj

    def create_PartialRuleEntity(self, *args, **kwargs):
        obj = PartialRuleEntity(*args, **kwargs)
        obj.factory = self
        return obj

    def create_Rule(self, *args, **kwargs):
        obj = Rule(*args, **kwargs)
        obj.factory = self
        return obj
