'''
  RuleEntity-like objects.

  $Id: RuleEntity.py,v 1.7 2012/05/09 08:38:14 knishida Exp $
'''
from model.Error import Error

disp = True

class RuleEntity(object):
    '''The class corresponds to Entity.'''
    def __init__(self, key, k = 0, effector = None):
        self.__key = key
        self.__components = []
        self.__k = k
        self.__effector = effector

    @property
    def key(self):
        return self.__key

    @property
    def components(self):
        return self.__components

    @property
    def k(self):
        return self.__k

    @property
    def effector(self):
        return self.__effector

    def join(self, comp):
        if isinstance(comp, RuleEntityComponent):
            self.components.append(comp)
        else:
            raise TypeError
        return self

    def toRES(self):
        return RuleEntitySet(self, k = self.k, effector = self.effector)

    def toRESL(self):
        return self.toRES().toRESL(k = self.k, effector = self.effector)

    def __getitem__(self, key):
        if disp:
            print 'RuleEntity.__getitem__() * self:', self, ', key:', key
        return self.toRES().__getitem__(key)

    def __getattr__(self, key):
        if disp:
            print 'RuleEntity.__getattr__() * self:', self, ', key:', key
        return self.toRES().__getattr__(key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntity.__add__() * self:', self, ', rhs:', rhs
        return self.toRES().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntity.__or__()* self:', self, ', rhs:', rhs
        return self.toRES().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntity.__gt__()* self:', self, ', rhs:', rhs
        return self.toRES().__gt__(rhs)

    def __str__(self):
        comp = [str(i) + ',' for i in self.components]
        return reduce(lambda a, b: a + b, [self.key + '('] + comp)[:-1] + ')'


class RuleEntityComponent(object):
    '''The class corresponds to EntityComponent.'''
    def __init__(self, key, bind = None, state = None, label = None):
        self.__key = str(key)
        self.__bind = bind
        self.__state = state
        self.__label = label

    @property
    def key(self):
        return self.__key

    def get_bind(self):
        return self.__bind
    def set_bind(self, bind):
        self.__bind = bind
    bind = property(get_bind, set_bind)

    @property
    def state(self):
        return self.__state

    @property
    def label(self):
        return self.__label

    def __str__(self):
        str_key = str(self.key)
        
        # state of component
        if isinstance(self.state, tuple): # 'Y=(U, P)'
            sta = [i + ', ' for i in self.state]
            str_state = reduce(lambda a, b: a + b, ['=('] + sta)[:-2] + ')'
        elif self.state != None: # 'Y=U' | 'Y=U[1]'
            str_state = '=' + self.state
        else: # 'Y'
            str_state = ''

        # bind of component
        if self.bind != None: # 'Y[1]' | 'Y=U[1]'
            str_bind = '[' + str(self.bind) + ']'
        else: # 'Y' / 'Y=(U, P)'
            str_bind = ''

        return str_key + str_state + str_bind


class RuleEntitySet(object):
    '''The set of RuleEntity.  This class corresponds to Species.'''
    def __init__(self, en, k = 0, effector = None):
        self.__entities = [en]
        self.__k = k
        self.__effector = effector

    @property
    def entities(self):
        return self.__entities

    @property
    def k(self):
        return self.__k

    @property
    def effector(self):
        return self.__effector

    def join(self, en):
        if isinstance(en, RuleEntity):
            self.entities.append(en)
        else:
            raise TypeError
        return

    def toRES(self):
        return self

    def toRESL(self):
        return RuleEntitySetList(self, k = self.k, effector = self.effector)

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key
        if isinstance(key, (int, float)):
            print '[MoleculeInits_RE] ' + str(self) + ' [' + str(key) + ']'
            self.__effector = str(key)
            return self
        elif isinstance(key, tuple):
            self.__effector = key
        else:
            self.__effector = (key,)
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySet.__getattr__()* self:', self, ', key:', key
        return PartialEntity(self, key)

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySet.__add__()* self:', self, ', rhs:', rhs
        return self.toRESL().__add__(rhs)

    def __or__(self, rhs):
        if disp:
            print 'RuleEntitySet.__or__()* self:', self, ', rhs:', rhs
        return self.toRESL().__or__(rhs)

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntitySet.__gt__()* self:', self, ', rhs:', rhs
        return self.toRESL().__gt__(rhs)
        
    def __str__(self):
        ent = [str(i) + '.' for i in self.entities]
        return reduce(lambda a, b: a + b, ent)[:-1]


class RuleEntitySetList(object):
    '''The list of RuleEntitySets(aka Species.)'''
    def __init__(self, sp, k = 0, effector = None):
        self.__species = [sp.toRES()]
        self.__k = k
        self.__effector = effector

    @property
    def species(self):
        return self.__species

    def get_k(self):
        return self.__k
    def set_k(self, k):
        self.__k = k
    k = property(get_k, set_k)

    def get_effector(self):
        return self.__effector
    def set_effector(self, effector):
        self.__effector = effector
    effector = property(get_effector, set_effector)

    def join(self, sp):
        self.species.append(sp.toRES())
        return

    def toRESL(self):
        return self

    def __getitem__(self, key):
        if disp:
            print 'RuleEntitySetList.__getitem__()* self:', self, ', key:', key
        if isinstance(key, tuple):
            self.__effector = key
        else:
            self.__effector = (key,)
        return self

    def __getattr__(self, key):
        if disp:
            print 'RuleEntitySetList.__getattr__()* self:', self, ', key:', key
        pass

    def __add__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__add__()* self:', self, ', rhs:', rhs
        self.join(rhs)
        self.set_k(rhs.k)
        self.set_effector(rhs.effector)
        return self

    def __or__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__or__()* self:', self, ', rhs:', rhs
        self.__k = rhs
        return self

    def __gt__(self, rhs):
        if disp:
            print 'RuleEntitySetList.__gt__()* self:', self, ', rhs:', rhs
        return Rule(self, rhs, '>')

    def __str__(self):
        spe = [str(i) + ' + ' for i in self.species]
        return reduce(lambda a, b: a + b, spe)[:-3]
        

class PartialEntity(object):
    '''The class represents Complete RuleEntity(Set) and partial Entity.'''
    def __init__(self, sp, key):
        self.__sp = sp.toRES() if sp != None else None
        self.__key = key

    @property
    def key(self):
        return self.__key

    @property
    def sp(self):
        return self.__sp
        
    def __call__(self, *args, **kwargs):
        if disp:
            print 'PartialEntity.__call__()* self:', self, ', args', args

        ent = RuleEntity(self.key)
        #import pdb; pdb.set_trace()

        for i in args:
            if isinstance(i, RuleEntityComponent): # l[1]
                ent.join(i)
            else: # d
                ent.join(RuleEntityComponent(i))
        for k, v in kwargs.items():
            if isinstance(v, RuleEntityComponent): # Y=U[1]
                ent.join(RuleEntityComponent(k, bind = v.bind, state = v.key))
            elif isinstance(v, tuple): # A=(U, P)
                st = tuple([str(i) for i in v])
                ent.join(RuleEntityComponent(k, state = st))
            else: # X=P or X=1 (v.key isn't used becasuse int has no key)
                ent.join(RuleEntityComponent(k, state = str(v)))

        if self.sp == None:
            self.__sp = ent.toRES()
        else:
            self.sp.join(ent)

        return self.sp


class Rule(object):
    '''The class corresponds to ReactionRule.'''
    def __init__(self, reactants, products, direction = '>'):
        self.__reactants = reactants.toRESL()
        self.__products = products.toRESL()
        self.__direction = direction
        self.__k = products.k
        self.__effector = products.effector

        print '[ReactionRules_RE] ' + str(self)

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
    def k(self):
        return self.__k

    @property
    def effector(self):
        return self.__effector

    def __str__(self):
        if self.effector != None:
            eff = [str(i) + ', ' for i in self.effector]
            str_eff = reduce(lambda a, b: a + b, [' ['] + eff)[:-2] + ']'
        else:
            str_eff = ''

        rule = str(self.reactants) + ' > ' + str(self.products)
        rule += str_eff + ' | ' + str(self.k)
        return rule

