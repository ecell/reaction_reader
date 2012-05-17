'''
  RuleProduct classes.
'''
from model.Error import Error
from RuleFactory import *

disp = False

class RuleFactoryProduct(object):
    def __init__(self, *args, **kwargs):
        self.__factory = None

    def set_factory(self, factory):
        self.__factory = factory
    def get_factory(self):
        return self.__factory
    factory = property(get_factory, set_factory)

    def __len__(self):
        return 1


class AnyCallable(RuleFactoryProduct):
    def __init__(self, name, *args, **kwargs):
        super(AnyCallable, self).__init__(name, *args, **kwargs)
        self.__name = name

    @property
    def name(self):
        return self.__name

    def toRuleEntityComponent(self): # only name information is used.
        return self.factory.create_RuleEntityComponent(self.name)

    def __call__(self, *args, **kwargs):
        return self.factory.create_PartialEntity(None, 
                                          self.name).__call__(*args, **kwargs)

    def __getitem__(self, key):
        return self.factory.create_RuleEntityComponent(self.name, bind = key)

    def __str__(self):
        return str(self.name)


class RuleEntityComponent(RuleFactoryProduct):
    '''The class corresponds to EntityComponent.'''
#    def __init__(self, name, bind = None, state = None, label = None):
    def __init__(self, name, *args, **kwargs):
#        self.__name = str(name)
#        self.__bind = bind # str
#        self.__state = state # str (want to change to list)
#        self.__label = label # str?
        self.__name = name
        self.__args = args
        self.__kwargs = kwargs

#        import pdb; pdb.set_trace()
        # kwargs niha bind toka state ga kuru
        # args ha nani mo konai

    @property
    def name(self):
        return self.__name

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

#    def get_bind(self):
#        return self.__bind
#    def set_bind(self, bind):
#        self.__bind = bind
#    bind = property(get_bind, set_bind)

#    @property
#    def state(self):
#        return self.__state

#    @property
#    def label(self):
#        return self.__label


    def toRuleEntityComponent(self):
        return self

    def __str__(self):

        kw = ''
        for k, v in self.kwargs.iteritems():
            if type(v) == tuple:
                kw += str(k) + ':' + str([str(i) for i in v]) + ','
            else:
                kw += str(k) + ':' + str(v) + ','

        return str(self.name) + '{' + kw[:-1] + '}'

#        # state of component
#        if isinstance(self.state, tuple): # 'Y=(U, P)'
#            sta = [i + ', ' for i in self.state]
#            str_state = reduce(lambda a, b: a + b, ['=('] + sta)[:-2] + ')'
#        elif self.state != None: # 'Y=U' | 'Y=U[1]'
#            str_state = '=' + self.state
#        else: # 'Y'
#            str_state = ''
#        if len(self.state) == 0:
#            str_state = ''
#        elif len(self.state) == 1:
#            str_state = '=' + self.state[0]
#        elif len(self.state) >= 2:
#            sta = [i + ', ' for i in self.state]
#            str_state = reduce(lambda a, b: a + b, ['=('] + sta)[:-2] + ')'
            

#        # bind of component
#        if self.bind != None: # 'Y[1]' | 'Y=U[1]'
#            str_bind = '[' + str(self.bind) + ']'
#        else: # 'Y' / 'Y=(U, P)'
#            str_bind = ''
#
#        return str_name + str_state + str_bind


class RuleEntity(object):
    '''The class corresponds to Entity.'''
    def __init__(self, name, rhs = None, key = None):
        self.__name = name
        self.__components = []
        self.__rhs = rhs # renamed from 'k'
        self.__key = key # renamed from 'effector'

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
        # if isinstance(comp, RuleEntityComponent):
#        if issubclass(type(comp), RuleEntityComponent):
#            self.components.append(comp)
#        else:
#            raise TypeError
#        return self
        self.components.append(comp)
        return self

    def toRuleEntity(self):
        return self

    def toRuleEntitySet(self):
        return self.factory.create_RuleEntitySet(self, rhs = self.rhs,
                                                 key = self.key)

    def toRuleEntitySetList(self):
        return self.toRuleEntitySet().toRuleEntitySetList(rhs = self.rhs,
                                                key = self.key)

    def __getitem__(self, key):
        if disp:
            print 'RuleEntity.__getitem__() * self:', self, ', key:', key
        return self.toRuleEntitySet().__getitem__(key)

    def __getattr__(self, key):
        if disp:
            print 'RuleEntity.__getattr__() * self:', self, ', key:', key
        return self.toRuleEntitySet().__getattr__(key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntity.__add__() * self:', self, ', rhs:', rhs
        return self.toRuleEntitySet().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntity.__or__()* self:', self, ', rhs:', rhs
        return self.toRuleEntitySet().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntity.__gt__()* self:', self, ', rhs:', rhs
        return self.toRuleEntitySet().__gt__(rhs)

    def __str__(self):
        comp = [str(i) + ',' for i in self.components]
        return reduce(lambda a, b: a + b, [self.name + '('] + comp)[:-1] + ')'


class RuleEntitySet(RuleFactoryProduct):
    '''The set of RuleEntity.  This class corresponds to Species.'''
    def __init__(self, en, rhs = None, key = None):
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
#        if issubclass(type(en), RuleEntity):
#            self.entities.append(en)
#        else:
#            raise TypeError
#        return
        self.entities.append(en)
        return

    def toRuleEntitySet(self):
        return self

    def toRuleEntitySetList(self):
        return self.factory.create_RuleEntitySetList(self, rhs = self.rhs,
                                                     key = self.key)

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key
#        if isinstance(key, (int, float)):
#            self.key = str(key)
#            return self
#        elif isinstance(key, tuple):
#            self.key = key
#        else:
#            self.key = (key,)
        self.key = key
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySet.__getattr__()* self:', self, ', key:', key
        return self.factory.create_PartialEntity(self, key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySet.__add__()* self:', self, ', rhs:', rhs
        return self.toRuleEntitySetList().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntitySet.__or__()* self:', self, ', rhs:', rhs
        return self.toRuleEntitySetList().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntitySet.__gt__()* self:', self, ', rhs:', rhs
        return self.toRuleEntitySetList().__gt__(rhs)
        
    def __str__(self):
        ent = [str(i) + '.' for i in self.entities]
        return reduce(lambda a, b: a + b, ent)[:-1]


class RuleEntitySetList(RuleFactoryProduct):
    '''The list of RuleEntitySets(aka Species.)'''
    def __init__(self, sp, rhs = None, key = None):
        self.__species = [sp.toRuleEntitySet()]
        self.__rhs = rhs # renamed from 'k'
        self.__key = key # renamed from 'effector'

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
        self.species.append(sp.toRuleEntitySet())
        return

    def toRuleEntitySetList(self):
        return self

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySetList.__getitem__()* self:', self, ', key:', key
#        if isinstance(key, tuple):
#            self.key = key
#        else:
#            self.key = (key,)
        self.key = key
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySetList.__getattr__()* self:', self, ', key:', key
        pass

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__add__()* self:', self, ', rhs:', rhs
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
        

class PartialEntity(RuleFactoryProduct):
    '''The class represents Complete RuleEntity(Set) and partial Entity.'''
    def __init__(self, sp, name):
        if disp:
            print 'PartialEntity.__init__()* self:', self,
            print ', sp:', sp, ', name:', name
        self.__sp = sp.toRuleEntitySet() if sp != None else None
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
            print 'PartialEntity.__call__()* self:', self, ', args', args

        ent = self.factory.create_RuleEntity(self.name)

        for i in args:
            ent.join(i.toRuleEntityComponent())
        for k, v in kwargs.items():

#            if isinstance(v, RuleEntityComponent): # Y=U[1]
#                ent.join(self.factory.create_RuleEntityComponent(k, 
#                                                 bind = v.bind, state = v.name))
#            elif isinstance(v, tuple): # Y=(U, 1)
#                st = tuple([str(i) for i in v])
#                ent.join(self.factory.create_RuleEntityComponent(k, state = st))
#            else: # Y=U or Y=1
#                ent.join(self.factory.create_RuleEntityComponent(k, 
#                                                 state = str(v)))
            ent.join(self.factory.create_RuleEntityComponent(k, state = v))

        if self.sp == None:
            self.sp = ent.toRuleEntitySet()
        else:
            self.sp.join(ent)

        return self.sp


class Rule(RuleFactoryProduct):
    '''The class corresponds to ReactionRule.'''
    def __init__(self, reactants, products, direction = '>'):
        self.__reactants = reactants.toRuleEntitySetList()
        self.__products = products.toRuleEntitySetList()
        self.__direction = direction
        self.__rhs = products.rhs # renamed from 'k'
        self.__key = products.key # renamed from 'effector'

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

        if self.key == None:
            str_eff = ''
        elif type(self.key) == tuple:
            eff = [str(i) + ', ' for i in self.key]
            str_eff = reduce(lambda a, b: a + b, [' ['] + eff)[:-2] + ']'
        else:
            str_eff = ' [' + str(self.key) + ']'

        rule = str(self.reactants) + ' > ' + str(self.products)
        rule += str_eff + ' | ' + str(self.rhs)
        return rule
