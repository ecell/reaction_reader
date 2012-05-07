from model.Error import Error

def make_setlist(entity1, entity2):
    '''Takes 2 RuleEntity-like objects and returns EntitySetList.

    entity1: RuleEntity or RuleEntitySet or RuleEntitySetList
    entity2: RuleEntity or RuleEntitySet or RuleEntitySetList
    '''
    setlist = RuleEntitySetList()

    for ent in [entity1, entity2]:
        if type(ent) == RuleEntity:
            setlist.join(RuleEntitySet(ent, k = ent.k, effector = ent.effector))
        elif type(ent) == RuleEntitySet:
            setlist.join(ent)
        elif type(ent) == RuleEntitySetList:
            setlist = ent
        else:
            raise TypeError

    setlist.set_k(entity2.k)
    setlist.set_effector(entity2.effector)

    return setlist


def make_rule(entity1, entity2):
    '''Takes 2 RuleEntitySet and returns Rule.

    entity1: RuleEntity or RuleEntitySet or RuleEntitySetList
    entity2: RuleEntity or RuleEntitySet or RuleEntitySetList
    '''
    setlists = []

    for ent in [entity1, entity2]:
        if type(ent) == RuleEntity:
            setlist = RuleEntitySetList(k = ent.k, effector = ent.effector)
            setlist.join(RuleEntitySet(ent, k = ent.k, effector = ent.effector))
        elif type(ent) == RuleEntitySet:
            setlist = RuleEntitySetList(k = ent.k, effector = ent.effector)
            setlist.join(ent)
        elif type(ent) == RuleEntitySetList:
            setlist = ent
        else:
            raise Error('Incomplete reaction rule.')
        setlists.append(setlist)

    return Rule(setlists[0], setlists[1], '>')


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

    def __getitem__(self, key):
        '''
        egf(r).egfr(l) [100]
        '''

        if type(key) == int or type(key) == float:
            print '[MoleculeInits] ' + str(self) + ' [' + str(key) + ']'
            # print [(str(i), str(i.key), str(i.state), i.bind) for i in self.components]
            # print [(type(i), type(i.key), type(i.state), type(i.bind)) for i in self.components]

            return float(key)

        else:
            # print key, type(key)
            self.__effector = key
            return self


    def join(self, comp):
        self.components.append(comp)

    def __getattr__(self, key):
        return PartialEntity(key, self)

    def __gt__(self, rhs):
        '''
        Creates a new reaction rule, registers it to model, and returns it.

        rhs: RuleEntitySetList that represents products.
        '''
        # print 'RuleEntity.__gt__()'
        return make_rule(self, rhs)

    def __or__(self, rhs):
        # print 'RuleEntity.__or__()'
        self.__k = rhs
        return self

    def __add__(self, rhs):
        # print 'RuleEntity.__add__()'
        return make_setlist(self, rhs)

    def __str__(self):
        tmp = self.key + '('
        for i in self.components:
            tmp += str(i) + ','
        return tmp[:-1] + ')'


class RuleEntityComponent(object):
    def __init__(self, key, bind = None, state = None, label = None, **attrs):
        self.__key = str(key)
        self.__bind = bind
        self.__state = state
        self.__label = label
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def key(self):
        return self.__key

#    @property
#    def bind(self):
#        return self.__bind

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

    def __setitem__(self, k, v):
        self.__attrs[k] = v

    def __getitem__(self, k):
        return self.__attrs.get(k, None)

    @property
    def attributes(self):
        return self.__attrs

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
                tmp += i.key + ', '
            str_state = tmp[:-2] + ')'
        elif self.state == None: # 
            str_state = ''
        else: #Y=U
            str_state = '=' + str(self.state)

        if self.bind != None:
            str_bind = '[' + str(self.bind) + ']'

        return str_key + str_state + str_bind


class RuleEntitySet(object):
    '''The set of RuleEntity.  This class corresponds to Species.'''
    def __init__(self, en, k = 0, effector = None, **attrs):
        self.__entities = [en,]
        self.__k = k
        self.__effector = effector
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def entities(self):
        return self.__entities

    @property
    def k(self):
        return self.__k

    @property
    def effector(self):
        return self.__effector

    @property
    def attributes(self):
        return self.__attrs

    def join(self, en):
        self.entities.append(en)

        return

    def __getattr__(self, key):
        '''
        egf(r).egfr(l)
        '''
        return PartialEntity(key, self)

    def __getitem__(self, key):
        '''
        egf(r).egfr(l) [100]
        '''
        self.__effector = key
        return self
        
    def __or__(self, rhs):
        # print 'RuleEntitySet.__or__()'
        self.__k = rhs
        return self

    def __add__(self, rhs):
        # print 'RuleEntitySet.__add__()'
        return make_setlist(self, rhs)

    def __gt__(self, rhs):
        # print 'RuleEntitySet.__gt__()'
        return make_rule(self, rhs)

    def __str__(self):
        tmp = ''
        for i in self.entities:
            tmp += str(i) + '.'
        return tmp[:-1]

        
class RuleEntitySetList(object):
    '''The list of RuleEntitySets(aka Species.)'''
    def __init__(self, k = 0, effector = None):
        self.__species = []
        self.__k = k
        self.__effector = effector

    @property
    def species(self):
        return self.__species

#    @property
#    def k(self):
#        return self.__k
    def get_k(self):
        return self.__k
    def set_k(self, k):
        self.__k = k
    k = property(get_k, set_k)

#    @property
#    def effector(self):
#        return self.__effector
    def get_effector(self):
        return self.__effector
    def set_effector(self, effector):
        self.__effector = effector
    effector = property(get_effector, set_effector)

    def join(self, sp):
        '''
        Adds species to set.

        species: Species.
        '''
        self.species.append(sp)

        return

    def __gt__(self, rhs):
        '''
        Creates a new reaction rule, registers it to model, and returns it.

        rhs: RuleEntitySetList that represents products.
        '''
        # print 'RuleEntitySetList.__gt__()'
        return make_rule(self, rhs)

    def __or__(self, rhs):
        # print 'RuleEntitySetList.__or__()'
        self.__k = rhs
        return self

    def __add__(self, rhs):
        # print 'RuleEntitySetList.__add__()'
        return make_setlist(self, rhs)


    def __getitem__(self, key):
        self.__effector = key
        return self

    def __str__(self):
        tmp = ''
        for i in self.species:
            tmp += str(i) + ' + '
        return tmp[:-3]
        

class PartialEntity(object):
    def __init__(self, key, sp):
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
            else:  # X=P
                entity.join(RuleEntityComponent(k, state = v.key))

        self.sp.join(entity)

        return self.sp

    def __str__(self):
        return self.key + self.sp

class Rule(object):
    def __init__(self, reactants, products, direction):
        # *** CHECK *** only set values in __init__()
        self.__reactants = reactants # RuleEntitySetList
        self.__products = products   # RuleEntitySetList
        self.__direction = direction # '>' or '<' ('<' = '<_>')

        if products.effector != None:
            if type(products.effector) == tuple:
                str_eff = ' ['
                for i in products.effector:
                    str_eff += str(i) + ', '
                str_eff = str_eff[:-2] + ']'
            else:
                str_eff = ' [' + str(products.effector) + '] '
        else:
            str_eff = ''

        print '[ReactionRules] ' + str(reactants) + ' > ' + str(products) + str_eff + '| ' + str(products.k)

    @property
    def reactants(self):
        return self.__reactants

    @property
    def products(self):
        return self.__products

    @property
    def direction(self):
        return self.__direction
