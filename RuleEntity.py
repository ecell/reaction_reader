from model.Error import Error

class RuleEntity(object):
    '''This class corresponds to Entity.'''
    def __init__(self, key, k = 0, effector = None):
        self.__key = key
        self.__components = []
        self.__k = k
        self.__effector = effector

    @property
    def key(self):
        '''Returns the key.'''
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
        self.components.append(comp)
        return

    def __getitem__(self, key):
        # print 'RuleEntity.__getitem__() * self:', self, ', key:', key
        if type(key) == int or type(key) == float:
            print '[MoleculeInits] ' + str(self) + ' [' + str(key) + ']'
            return float(key)
        else:
            self.__effector = key
            return self

    def __or__(self, rhs):
        # print 'RuleEntity.__or__()* self:', self, ', rhs:', rhs
        self.__k = rhs
        return self

    def __getattr__(self, key):
        # print 'RuleEntity.__getattr__() * self:', self, ', key:', key
        return PartialEntity(self, key)

    def __add__(self, rhs):
        # print 'RuleEntity.__add__() * self:', self, ', rhs:', rhs
        resl = RuleEntitySetList(self)
        resl.join(rhs)
        resl.set_k(rhs.k)
        resl.set_effector(rhs.effector)
        return resl

    def __gt__(self, rhs):
        # print 'RuleEntity.__gt__()* self:', self, ', rhs:', rhs
        return Rule(self, rhs, '>')

    def __str__(self):
        comp = [str(i) + ',' for i in self.components]
        return reduce(lambda a, b: a + b, [self.key + '('] + comp)[:-1] + ')'


class RuleEntityComponent(object):
    '''This class corresponds to EntityComponent.'''
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
        str_key = ''
        str_state = ''
        str_bind = ''
        
        if type(self.key) == str:
            str_key = self.key
        else:
            str_key = self.key.key

        if type(self.state) == tuple: # Y=(U, P)
            tmp = '=('
            for i in self.state:
                tmp += i + ', '
            str_state = tmp[:-2] + ')'
        elif self.state != None: #Y=U
            str_state = '=' + self.state

        if self.bind != None:
            str_bind = '[' + str(self.bind) + ']'

        return str_key + str_state + str_bind


class RuleEntitySet(object):
    '''The set of RuleEntity.  This class corresponds to Species.'''
    def __init__(self, en, k = 0, effector = None):
        self.__entities = [en,]
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
        self.entities.append(en)
        return

    def __getitem__(self, key):
        # print 'RuleEntitySet.__getitem__()* self:', self, ', key:', key
        if type(key) == int or type(key) == float:
            print '[MoleculeInits] ' + str(self) + '[' + str(key) + ']'
            return float(key)
        else:
            self.__effector = key
            return self
        
    def __or__(self, rhs):
        # print 'RuleEntitySet.__or__()* self:', self, ', rhs:', rhs
        self.__k = rhs
        return self

    def __getattr__(self, key):
        # print 'RuleEntitySet.__getattr__()* self:', self, ', key:', key
        return PartialEntity(self, key)

    def __add__(self, rhs):
        # print 'RuleEntitySet.__add__()* self:', self, ', rhs:', rhs
        resl = RuleEntitySetList(self)
        resl.join(rhs)
        resl.set_k(rhs.k)
        resl.set_effector(rhs.effector)
        return resl

    def __gt__(self, rhs):
        # print 'RuleEntitySet.__gt__()* self:', self, ', rhs:', rhs
        return Rule(self, rhs, '>')

    def __str__(self):
        ent = [str(i) + '.' for i in self.entities]
        return reduce(lambda a, b: a + b, ent)[:-1]


class RuleEntitySetList(object):
    '''The list of RuleEntitySets(aka Species.)'''
    def __init__(self, sp, k = 0, effector = None):
        self.__species = [self.toRES(sp),]
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
        self.species.append(self.toRES(sp))
        return

    def toRES(self, re):
        if type(re) == RuleEntity:
            return RuleEntitySet(re, k = re.k, effector = re.effector)
        elif type(re) == RuleEntitySet:
            return re
        else:
            raise TypeError

    def __getitem__(self, key):
        # print 'RuleEntitySetList.__getitem__()* self:', self, ', key:', key
        self.__effector = key
        return self

    def __or__(self, rhs):
        # print 'RuleEntitySetList.__or__()* self:', self, ', rhs:', rhs
        self.__k = rhs
        return self

    def __add__(self, rhs):
        # print 'RuleEntitySetList.__add__()* self:', self, ', rhs:', rhs
        self.join(rhs)
        self.set_k(rhs.k)
        self.set_effector(rhs.effector)
        return self

    def __gt__(self, rhs):
        # print 'RuleEntitySetList.__gt__()* self:', self, ', rhs:', rhs
        return Rule(self, rhs, '>')

    def __str__(self):
        spe = [str(i) + ' + ' for i in self.species]
        return reduce(lambda a, b: a + b, spe)[:-3]
        

class PartialEntity(object):
    def __init__(self, sp, key):
        self.__key = key

        if type(sp) == RuleEntitySet:
            self.__sp = sp
        elif type(sp) == RuleEntity:
            self.__sp = RuleEntitySet(sp, k = sp.k, effector = sp.effector)
        else:
            raise TypeError

    @property
    def key(self):
        return self.__key
        
    @property
    def sp(self):
        return self.__sp
        
    def __call__(self, *args, **kwargs):
        entity = RuleEntity(self.key)

        for i in args:
            if type(i) == RuleEntityComponent: # l[1]
                entity.join(i)
            else: # d
                entity.join(RuleEntityComponent(i))
        for k, v in kwargs.items():
            if type(v) == RuleEntityComponent: # Y=U[1]
                entity.join(RuleEntityComponent(k, bind = v.bind, state = v.key))
            else:  # X=P or X=1
                entity.join(RuleEntityComponent(k, state = str(v)))

        self.sp.join(entity)

        return self.sp

    def __str__(self):
        return self.key + self.sp


class Rule(object):
    def __init__(self, reactants, products, direction = '>'):
        self.__direction = direction
        self.__k = products.k
        self.__effector = products.effector

        setlists = []
        for ent in [reactants, products]:
            if type(ent) in [RuleEntity, RuleEntitySet]:
                setlist = RuleEntitySetList(ent)
            elif type(ent) == RuleEntitySetList:
                setlist = ent
            else:
                raise Error('Incomplete reaction rule.')
            setlists.append(setlist)
        [self.__reactants, self.__products] = setlists

        print '[ReactionRules] ' + str(self)

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
            if type(self.effector) == tuple:
                str_eff = ' ['
                for i in self.effector:
                    str_eff += str(i) + ', '
                str_eff = str_eff[:-2] + ']'
            else:
                str_eff = ' [' + str(self.effector) + '] '
        else:
            str_eff = ''

        rule = str(self.reactants) + ' > ' + str(self.products)
        rule += str_eff + '| ' + str(self.k)
        return rule

