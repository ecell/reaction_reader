class RuleEntity(object):
    '''This class corresponds to Entity.'''

    def __init__(self, key, *args, **attrs):
        '''Initializes the list.'''
        self.__key = key
        self.__components = [args]
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def key(self):
        '''Returns the key.'''
        return self.__key

    @property
    def self.components(self):
        return self.__components

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

    def join(self, comp):
        self.__components.append(comp)

    def __getattr__(self, key):
        return PartialEntity(key, self)

    def str_simple(self):
        ''' '''
        return self.__str__()

    def __str__(self):
        return self.key + [i.str_simple() for i in self.__components]
