class Component(object):
    '''The component in a molecule.'''
    def __init__(self, id, name, state_types={}, **attrs):
        '''
        Initializes the component.

        id: The ID of this component.
        name: The name of this component.
        state_types: Map of state types of this component.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__name = name

        # Initializes the attributes for the internal states.
        self.__state_types = state_types.copy()

        # Initializes the map for various attributes.
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def id(self):
        '''Returns the identifier of this component.'''
        return self.__id

    @property
    def name(self):
        '''Returns the name of this component.'''
        return self.__name

    @property
    def state_types(self):
        '''Returns the the state types.'''
        return self.__state_types

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

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Component('
        retval += 'id=%d, ' % self.__id
        retval += 'name=\'%s\', ' % self.__name
        retval += 'state_types={'
        for i, (name, state_type) in enumerate(self.state_types.iteritems()):
            if i > 0:
                retval += ', '
            retval += '\'%s\': %s' % (name, state_type)
        retval += '}, '
        retval += 'attrs=%s' % self.__attrs
        retval += ')'
        return retval
