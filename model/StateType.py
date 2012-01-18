class StateType(object):
    '''Defines the state type of the component.'''

    def __init__(self, name, states, **attrs):
        '''
        Initializes the state type.

        name: The name of this state type.
        states: List of the states for this state type.
        attrs: Map of attributes.
        '''
        #import pdb; pdb.set_trace()

        # Checks the input values.
        assert len(states)
        state_list = []
        for state in states:
            assert state not in state_list
            state_list.append(state)

        # Sets to the attributes.
        self.__name = name
        self.__states = state_list

        # Initializes the map for various attributes.
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def name(self):
        '''Returns the name of this state type.'''
        return self.__name

    @property
    def states(self):
        '''Returns the list of states.'''
        return self.__states

    def state_index(self, value):
        '''
        Returns the array index of given state value.

        value: A value to get the index.
        '''
        assert value in self.__states
        return self.__states.index(value)

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
        return str(self.__states)


