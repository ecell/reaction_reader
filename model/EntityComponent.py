from general_func import *

class EntityComponent(object):
    '''An component in an entity object.'''

    def __init__(self, component, entity, **attrs):
        '''
        Initializes this entity component.

        component: The component for this entity component.
        entity: The entity that this entity component belongs to.
        attrs: Map of attributes.
        '''
 
        self.__component = component
        self.__entity = entity

        # Initializes the component states.
        self.__states = {}
        for (state_name, state_type) in component.state_types.iteritems():
            self.__states[state_name] = STATE_UNSPECIFIED

        # Initializes the attributes for biding.
        self.__binding_state = BINDING_UNSPECIFIED
        self.__binding = None

        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def id(self):
        '''Returns the ID.'''
        return self.__component.id

    @property
    def component(self):
        '''Returns the Component class object.'''
        return self.__component

    @property
    def entity(self):
        '''Returns the entity that this component belongs to.'''
        return self.__entity

    @property
    def name(self):
        '''Returns the name.'''
        return self.__component.name

    @property
    def state_types(self):
        '''Returns the state types.'''
        return self.__component.state_types

    @property
    def states(self):
        '''Returns the map of the states.'''
        return self.__states

    def set_state(self, state_name, state_value):
        '''
        Sets the state.

        state_name: The name of state.
        state_value: The value set to the state.
        '''
        assert state_name in self.state_types
        # assert state_value in self.state_types[state_name].states
        state_type = self.state_types[state_name]
        if state_value == STATE_UNSPECIFIED_STRING:
            index = -1
        else:
            index = state_type.state_index(state_value)
        self.__states[state_name] = index

    def getbinding_state(self):
        '''Returns the binding state.'''
        return self.__binding_state

    def setbinding_state(self, state):
        '''
        Sets the binding state.

        state: The binding state to set.
        '''
        self.__binding_state = state

    binding_state = property(getbinding_state, setbinding_state)

    def getbinding(self):
        '''Returns the binding.'''
        return self.__binding

    def setbinding(self, binding):
        '''
        Sets the binding.

        binding: A binding to set.
        '''
        self.__binding = binding

    binding = property(getbinding, setbinding)

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

    def is_specific(self):
        '''
        Checks whether this component has specific properties.
        '''
        if not self.__has_concrete_binding_state():
            return False
        for state in self.states.itervalues():
            if state == STATE_UNSPECIFIED:
                return False
        return True

    def __compare_states(self, comp):
        for (name, self_state) in self.states.iteritems():
            state = comp.states[name]
            if self_state == STATE_UNSPECIFIED:
                if state != STATE_UNSPECIFIED:
                    return False
        return True

    def __has_concrete_binding_state(self):
        return self.binding_state == BINDING_SPECIFIED \
            or self.binding_state == BINDING_NONE

    def is_more_specific(self, comp):
        '''
        Checks whether this component is equally or more specific 
        than the given one.

        comp: A component to compare with this component.
        '''
        assert self.component == comp.component

        if self.__has_concrete_binding_state():
            return self.__compare_states(comp)
        else:
            if self.binding_state == comp.binding_state:
                # The case that both components are in the state of 
                # 'EXISTS' or 'UNSPECIFIED'.
                return self.__compare_states(comp)
            else:
                return False

    def matches(self, comp):
        '''
        Returns whether this component matches the given pattern.

        comp: A component as a pattern.
        '''
        assert self.component == comp.component

        # checks component states
        for (name, state) in comp.states.iteritems():
            if state != STATE_UNSPECIFIED:
                self_state = self.__states[name]
                if state != self_state:
                    return False

        # checks binding states
        state = comp.binding_state
        if state is BINDING_SPECIFIED:
            # Only SPECIFIED state is permitted.
            if self.binding_state != BINDING_SPECIFIED:
                return False
        elif state is BINDING_ANY:
            # SPECIFIED state and EXISTS state are permitted.
            if self.binding_state != BINDING_ANY \
                and self.binding_state != BINDING_SPECIFIED:
                return False
        elif state is BINDING_NONE:
            # Only NOT_EIXSTS state is permitted.
            if self.binding_state != BINDING_NONE:
                return False
        # Any states are permitted for remaining UNSPECIFIED case.

        return True

    def __state_repr(self, name, index):
        if index == STATE_UNSPECIFIED:
            return '?'
        else:
            return self.state_types[name].states[index]

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = self.name
        if len(self.states):
#            retval += '~'
            retval += '('
        if len(self.states) == 1:
            item = self.states.items()[0]
            state_name = item[0]
            index = item[1]
            retval += self.__state_repr(state_name, index)
        if len(self.states):
            retval += ')'
        elif len(self.states) > 1:
            retval += '['
            for i, (state_name, index) in enumerate(self.states.iteritems()):
                if i > 0:
                    retval += ','
                retval += state_name
                retval += ':'
                retval += self.__state_repr(state_name, index)
            retval += ']'
        if self.binding_state != BINDING_NONE:
#            retval += '!'
            retval += '['
        if self.binding_state == BINDING_SPECIFIED and self.binding is not None:
            retval += '%d' % self.binding.id
        elif self.binding_state == BINDING_UNSPECIFIED:
            retval += BINDING_UNSPECIFIED_STRING
        elif self.binding_state == BINDING_ANY:
            retval += BINDING_ANY_STRING
        if self.binding_state != BINDING_NONE:
            retval += ']'
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'EntityComponent('
        retval += 'id=%d, ' % self.id
        retval += 'name=\'%s\', ' % self.name
        if len(self.component.state_types):
            retval += 'states={'
            for i, (state_id, index) in enumerate(self.states.iteritems()):
                if i > 0:
                    retval += ', '
                retval += '\'%s\': \'%s\'' % (state_id, \
                    self.__state_repr(state_id, index))
            retval += '}, '
        if self.binding_state == BINDING_SPECIFIED:
            binding_state_str = 'specified'
        elif self.binding_state == BINDING_UNSPECIFIED:
            binding_state_str = 'unspecified'
        elif self.binding_state == BINDING_ANY:
            binding_state_str = 'exists'
        elif self.binding_state == BINDING_NONE:
            binding_state_str = 'not exist'
        retval += 'binding_state=\'%s\'' % binding_state_str
        if self.binding is not None:
            retval += ', '
            retval += 'binding=\'%d\'' % self.binding.id
        if hasattr(self, "label"):
            retval += ', label="%s"' % self.label
        retval += ')'
        return retval


