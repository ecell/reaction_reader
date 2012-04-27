class RuleEntitySet(object):
    '''The set of RuleEntity.  This class corresponds to Species.'''

    def __init__(self, en, **attrs):
        '''Initializes the list.'''
        self.__entities = [en]
        self.__serial_entities = 0
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def entities(self):
        '''Returns the list of entities.'''
        return self.__entities

    @property
    def serial_entities(self):
        '''Returns the number of entities.'''
        return self.__serial_entities

    def __setitem__(self, k, v):
        '''
        Sets the attributes.

        k: The key.
        v: The value.
        '''
        self.__attrs[k] = v

    def __getitem__(self, k):
        '''
        Returns the value of the attribute of given key.
        If given key is not found, returns None.

        k: The key.
        '''
        return self.__attrs.get(k, None)

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

    def join(self, en):
        '''
        Adds entity to set.

        en: Entity.
        '''
        self.__entity.append(en)
        self.__serial_entity += 1

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
        print "parameter: " + key

        return float(key)
        

    def str_simple(self):
        ''''''
        return [i.str_simple() for i in self.__entities]
