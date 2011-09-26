# for the internal state
STATE_UNSPECIFIED = -1
STATE_UNSPECIFIED_STRING = '?'

# for binding state
BINDING_UNSPECIFIED = -1
BINDING_UNSPECIFIED_STRING = '?'
BINDING_NONE = 0
BINDING_SPECIFIED = 1
BINDING_ANY = 2
BINDING_ANY_STRING = '+'

# Constants for the condition of reaction rule.
REACTANTS = 1
PRODUCTS = 2

import sys

class StateType(object):
    '''Defines the state type of the component.'''

    def __init__(self, name, states, **attrs):
        '''
        Initializes the state type.

        name: The name of this state type.
        states: List of the states for this state type.
        attrs: Map of attributes.
        '''

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


class EntityType(object):
    '''The type of a molecular species.'''
    def __init__(self, name, **attrs):
        '''
        Initializes the entity type.

        name: The name of this entity type.
        attrs: Map of attributes.
        '''
        self.__name = name
        self.__components = {}
        self.__comp_serial = 0
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def name(self):
        '''Returns the name of this entity type.'''
        return self.__name

    @property
    def components(self):
        '''Returns the iterator of the components.'''
        return self.__components

    def add_component(self, name, state_types={}):
        '''
        Adds a component.

        name: The name a new component.
        state_types: List of state types for the new component.
        '''
        self.__comp_serial += 1
        comp = Component(self.__comp_serial, name, state_types)
        self.__components[self.__comp_serial] = comp
        return comp

    def find_components(self, name):
        '''
        Finds the components of the given name.

        name: The name of a component to find.
        '''
        comp_list = []
        for comp in self.components.itervalues():
            if comp.name == name:
                comp_list.append(comp)
        return comp_list

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
        retval = 'EntityType('
        retval += 'name=\'%s\', ' % self.__name
        retval += 'components={'
        for i, (comp_id, comp) in enumerate(self.components.iteritems()):
            if i > 0:
                retval += ', '
            retval += '%d: \'%s\'' % (comp_id, comp)
        retval += '}, '
        retval += 'attrs=%s' % self.__attrs
        retval += ')'
        return retval


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
        retval += ')'
        return retval


class Binding(object):
    '''The binding between two components.'''
    def __init__(self, id, species, component_1, component_2, temporary, \
        **attrs):
        '''
        Initializes the binding.

        id: ID of this biding.
        species: The graph that this binding belongs to.
        component_1: The first component.
        component_2: The second component.
        temporary: The temporary flag.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__species = species
        self.__component_1 = component_1
        self.__component_2 = component_2
        self.__temporary = temporary
        self.__deleted = False
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    def getid(self):
        '''Returns the ID.'''
        return self.__id

    def setid(self, id):
        '''
        Sets the ID.

        id: The ID set to this binding.
        '''
        self.__id = id

    id = property(getid, setid)

    @property
    def species(self):
        '''Returns the species that this binding belongs to.'''
        return self.__species

    @property
    def component_1(self):
        '''Returns the first component.'''
        return self.__component_1

    @property
    def component_2(self):
        '''Returns the second component.'''
        return self.__component_2

    @property
    def entity_1(self):
        '''Returns the first entity.'''
        return self.component_1.entity

    @property
    def entity_2(self):
        '''Returns the second entity.'''
        return self.component_2.entity

    def gettemporary(self):
        '''Returns the temporary flag.'''
        return self.__temporary

    def settemporary(self, b):
        '''
        Sets the temporary flag.

        b: The temporary flag to set.
        '''
        self.__temporary = b

    temporary = property(gettemporary, settemporary)

    def getdeleted(self):
        '''Returns the deleted flag.'''
        return self.__deleted

    def setdeleted(self, b):
        '''
        Sets the deleted flag.

        b: The deleted flag to set.
        '''
        self.__deleted = b

    deleted = property(getdeleted, setdeleted)

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

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

    def find_component(self, entity):
        '''
        Finds the component with given entity.

        entity: An entity.
        '''
        if self.entity_1 == entity:
            return self.component_1
        if self.entity_2 == entity:
            return self.component_2
        return None

    def find_counterpart_entity(self, entity):
        '''
        Finds an entity that is the counterpart to given entity.

        entity: An entity.
        '''
        if self.entity_1 == entity:
            return self.entity_2
        elif self.entity_2 == entity:
            return self.entity_1
        else:
            return None

    def matches(self, binding):
        '''
        Returns whether this binding matches a given binding.
        The type of entity and the ID of the components are compared.

        binding: A binding to compare with this object.
        '''
        # Compares the entity type of two entities.
        if self.entity_1.entity_type == self.entity_2.entity_type \
        and binding.entity_1.entity_type == binding.entity_2.entity_type:
            # The case that the type of two entities are equal.
            if self.entity_1.entity_type != binding.entity_1.entity_type:
                return False
            if self.component_1.id == binding.component_1.id \
            and self.component_2.id == binding.component_2.id:
                return True
            if self.component_1.id == binding.component_2.id \
            and self.component_2.id == binding.component_1.id:
                return True
            return False
        else:
            if self.entity_1.entity_type == binding.entity_1.entity_type \
            and self.entity_2.entity_type == binding.entity_2.entity_type:
                if self.component_1.id != binding.component_1.id:
                    return False
                if self.component_2.id != binding.component_2.id:
                    return False
            elif self.entity_1.entity_type == binding.entity_2.entity_type \
            and self.entity_2.entity_type == binding.entity_1.entity_type:
                if self.component_1.id != binding.component_2.id:
                    return False
                if self.component_2.id != binding.component_1.id:
                    return False
            else:
                return False
            return True

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Binding('
        retval += 'id=\'%d\', ' % self.__id
        retval += 'temporay=%s, ' % self.__temporary
        retval += 'deleted=%s, ' % self.__deleted
        retval += '%s(%d).%s' % (self.entity_1.name, self.entity_1.id, \
            self.component_1.name)
        retval += '-'
        retval += '%s(%d).%s' % (self.entity_2.name, self.entity_2.id, \
            self.component_2.name)
        retval += ')'
        return retval


class Entity(object):
    '''An entity of a species.'''

    def __init__(self, id, entity_type, species, **attrs):
        '''
        Initializes this entity.

        id: The ID of this entity.
        entity_type: The type of this entity.
        species: The species that this entity belongs to.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__entity_type = entity_type
        self.__species = species
        self.__components = {}
        for (comp_id, comp) in entity_type.components.iteritems():
            self.__components[comp_id] = EntityComponent(comp, self)
        self.__dummy = False
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    def getid(self):
        '''Returns the ID.'''
        return self.__id

    def setid(self, id):
        '''
        Sets the ID.

        id: The ID to set.
        '''
        self.__id = id

    id = property(getid, setid)

    @property
    def entity_type(self):
        '''Returns the entity type.'''
        return self.__entity_type

    @property
    def species(self):
        '''Returns the species that this entity belongs to.'''
        return self.__species

    @property
    def components(self):
        '''Returns the list of components.'''
        return self.__components

    def find_components(self, name):
        '''
        Finds the components of given name.

        name: The name of a component to find.
        '''
        comp_list = []
        for comp in self.components.itervalues():
            if comp.name == name:
                comp_list.append(comp)
        return comp_list

    @property
    def name(self):
        return self.__entity_type.name

    def getdummy(self):
        return self.__dummy

    def setdummy(self, b):
        self.__dummy = b

    dummy = property(getdummy, setdummy)

    @property
    def bindings(self):
        b_list = []
        for comp in self.components.itervalues():
            if not comp.binding is None:
                b_list.append(comp.binding)
        return b_list

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

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

    def is_specific(self):
        '''
        Checks whether this entity has specific properties.
        '''
        for comp in self.components.itervalues():
            if not comp.is_specific():
                return False
        return True

    def is_more_specific(self, entity):
        '''
        Checks whether this entity is equally or more specific 
        than the given one.
        '''
        assert self.entity_type is entity.entity_type
        for (comp_id, comp) in self.__components.iteritems():
            if not comp.is_more_specific(entity.components[comp_id]):
                return False
        return True

    def matches(self, pattern):
        '''
        Returns whether this entity matches the given entity pattern.
        '''
        # checks entity type
        if self.__entity_type.name != pattern.__entity_type.name:
            return False
        # checks component states
        for (component_id, pattern_comp) in pattern.components.iteritems():
            self_comp = self.__components[component_id]
            if not self_comp.matches(pattern_comp):
                return False
        return True

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = ''
        retval += '%s' % self.entity_type.name
        retval += '('
        for i, comp in enumerate(self.components.itervalues()):
            if i > 0:
                retval += ','
            retval += comp.str_simple()
        retval += ')'
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Entity('
        retval += 'id=%d, ' % self.id
        retval += 'entity_type=\'%s\', ' % self.entity_type.name
        retval += 'components={'
        for i, comp in enumerate(self.components.itervalues()):
            if i > 0:
                retval += ', '
            retval += '%s' % str(comp)
        retval += '}, '
        retval += 'dummy=%s, ' % self.dummy
        retval += 'attrs=%s' % self.__attrs
        retval += ')'
        return retval


class Species(object):
    '''The species.'''

    def __init__(self, id=0, **attrs):
        '''
        Initializes the species.

        id: The ID of this species. Value of zero is set by default.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__entities = {}
        self.__bindings = {}
        self.__dummy = False
        self.__concrete = False
        self.__serial_entity = 0
        self.__serial_binding = 0
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

        # List of information of the patterns that match to this species.
        self.__pattern_matching_info = {}

        # List of patterns that do not match to this species.
        self.__unmatched_patterns = []

    @property
    def id(self):
        '''Returns the ID.'''
        return self.__id

    @property
    def entities(self):
        '''Returns the list of entities in this species.'''
        return self.__entities

    @property
    def bindings(self):
        '''Returns the list of bindings in this species.'''
        return self.__bindings

    def getdummy(self):
        '''Returns the dummy flag.'''
        return self.__dummy

    def setdummy(self, b):
        '''
        Sets the dummy flag.

        b: The dummy flag to set.
        '''
        self.__dummy = b

    dummy = property(getdummy, setdummy)

    def getconcrete(self):
        '''Returns the concreteness flag.'''
        return self.__concrete

    def setconcrete(self, b):
        '''
        Sets the concrete flag.

        b: The concrete flag to set.
        '''
        self.__concrete = b

    concrete = property(getconcrete, setconcrete)

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

    @property
    def pattern_matching_info(self):
        '''Returns the information of pattern matching.'''
        return self.__pattern_matching_info

    def add_entity(self, entity_type):
        '''
        Add entities of this molecular species.

        entity_type: The type of species for the new entity.
        '''
        self.__serial_entity += 1
        entity = Entity(self.__serial_entity, entity_type, self)
        self.__entities[self.__serial_entity] = entity
        return entity

    def add_binding(self, component_1, component_2, temporary=False):
        '''
        Adds a binding between two components.

        component_1: The first component for new binding.
        component_2: The second component for new binding.
        temporay: The temporary flag for new binding.
        '''
        self.__serial_binding += 1
        b_id = self.__serial_binding

        # creates a binding object
        b = Binding(b_id, self, component_1, component_2, temporary)
        self.__bindings[b_id] = b

        # Sets the binding to entities if it is not temporary one.
        if not temporary:
            component_1.binding = b
            component_2.binding = b

        return b

    def remove_binding(self, binding):
        '''
        Removes the binding from this species.

        binding: A binding to be removed.
        '''
        assert binding in self.__bindings.values()
        b = self.__bindings[binding.id]
        b.component_1.binding = None
        b.component_2.binding = None
        del self.__bindings[binding.id]

    def add_elements(self, entity_list, binding_list):
        '''
        Adds entities and bindings.

        entity_list: List of entities added to this species.
        binding_list: List of bindings added to this species.
        '''
        for e in entity_list:
            self.__serial_entity += 1
            e.id = self.__serial_entity
            self.__entities[e.id] = e
        for b in binding_list:
            self.__serial_binding += 1
            b.id = self.__serial_binding
            self.__bindings[b.id] = b

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = ''
        for i, entity in enumerate(self.__entities.itervalues()):
            retval += entity.str_simple()
            if i < len(self.__entities) - 1:
                retval += '.'
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Species('
        retval += 'id=%d, ' % self.__id
        retval += 'dummy=%s, ' % self.dummy
        retval += 'concrete=%s, ' % self.concrete
        retval += 'attrs=%s, ' % self.__attrs
        retval += '\n'
        retval += 'entities={'
        for i, (en_id, entity) in enumerate(self.entities.iteritems()):
            if i > 0:
                retval += ', '
            retval += '\n'
            retval += '%d: \'%s\'' % (en_id, entity)
        retval += '\n'
        retval += '}, '
        retval += '\n'
        retval += 'bindings={'
        for i, (b_id, binding) in enumerate(self.bindings.iteritems()):
            if i > 0:
                retval += ', '
            retval += '\n'
            retval += '%d: \'%s\'' % (b_id, binding)
        retval += '\n'
        retval += '}'
        retval += ')'
        return retval

    def matches(self, pattern, use_cache=False):
        '''
        Returns whether this species matches the given pattern species.

        pattern: A pattern species.
        use_cache: A flag whether to use the cache.
        '''
        if use_cache:
            # Checks whether the given pattern is contained
            # in the matched list or unmatched list.
            for p in self.__unmatched_patterns:
                if p is pattern:
                    return False
            for info in self.pattern_matching_info.itervalues():
                if info.pattern is pattern:
                    return True
        info = PatternMatchingInfo(self, pattern)
        matched = self.__matches_sub(pattern, info, use_cache)
        if use_cache:
            if matched:
                self.__pattern_matching_info[pattern.id] = info
            else:
                self.__unmatched_patterns.append(pattern)
        return matched

    def __matches_sub(self, pattern, info, use_cache):

        # Compares the number of entities between this species
        # and given pattern.
        if len(self.__entities) < len(pattern.__entities):
            return False

        # Checks the internal states and binding states.
        entity_pairs = []
        matched_entities = {}
        for (p_id, p_entity) in pattern.entities.iteritems():
            matched_entities[p_id] = []
            for (s_id, s_entity) in self.entities.iteritems():
                if s_entity.matches(p_entity):
                    pair = PatternMatchingEntityPair(p_entity, s_entity)
                    entity_pairs.append(pair)
                    matched_entities[p_id].append(s_id)

        # If no matched entities exist for any entitiy
        # of the pattern, returns False.
        for entities in matched_entities.itervalues():
            if not len(entities):
                return False

        # Gets the list of entity correspondence between a reactant pattern 
        # and a species.
        correspondence_list = create_correspondence_list(entity_pairs)

        # Checks the binding for each correspondence.
        valid_correspondence_list = []
        correspondence_found = False
        for i, c in enumerate(correspondence_list):

            # Loop for all entity pairs of correspondence.
            valid_correspondence = True
            for j, pair in enumerate(c.pairs):
                p_en = pair.pattern_entity
                m_en = pair.matched_entity

                # Checks the equality of bindings.
                for p_b in  p_en.bindings:
                    p_c_en = p_b.find_counterpart_entity(p_en)

                    binding_found = False
                    for m_b in m_en.bindings:
                        # Skips unmatched binding.
                        if not m_b.matches(p_b):
                            continue

                        # Skips the binding with different components.
                        m_c_en = m_b.find_counterpart_entity(m_en)
                        p_comp = p_b.find_component(p_en).component
                        m_comp = m_b.find_component(m_en).component
                        if p_comp != m_comp:
                            continue
                        p_c_comp = p_b.find_component(p_c_en).component
                        m_c_comp = m_b.find_component(m_c_en).component
                        if p_c_comp != m_c_comp:
                            continue

                        # Counterpart entity must be contained 
                        # in the pair.
                        pair_found = False
                        for p in c.pairs:
                            if p == pair:
                                continue
                            if p.pattern_entity == p_c_en \
                            and p.matched_entity == m_c_en:
                                pair_found = True
                                break

                        if pair_found:
                            binding_found = True
                            break

                    # If matched binding is not found, returns False.
                    if not binding_found:
                        valid_correspondence = False
                        break

                if not valid_correspondence:
                    break

            if valid_correspondence:
                correspondence_found = True
                valid_correspondence_list.append(c)

            # If not caching the pattern matching information, 
            # returns true when one correspondence is found.
            if not use_cache and correspondence_found:
                return True

        # If no correspondence is found.
        if not correspondence_found:
            return False

        if use_cache:
            for c in valid_correspondence_list:
                info.add_correspondence(c)

        return True

    def equals(self, sp):
        '''
        Returns whether this species is equals to the given species.

        sp: A species to compare.
        '''
        if self == sp:
            return True
        if len(self.entities) != len(sp.entities):
            return False
        if len(self.bindings) != len(sp.bindings):
            return False
        if not self.matches(sp):
            return False
        if not sp.matches(self):
            return False
        return True

    def copy(self, id=0):
        '''
        Creates the copy of this species.

        id: The ID of copied species.
        '''
        s = Species(id)
        s.__attrs = self.__attrs.copy()
        s.__dummy = self.__dummy
        s.__concrete = self.__concrete
        for entity in self.entities.itervalues():
            e = s.add_entity(entity.entity_type)
            for (comp_id, comp) in entity.components.iteritems():
                c = e.components[comp_id]
                for (name, state) in comp.states.iteritems():
                    c.states[name] = comp.states[name]
                c.binding_state = comp.binding_state
            e.dummy = entity.dummy
        for binding in self.bindings.itervalues():
            e_1 = s.entities[binding.entity_1.id]
            e_2 = s.entities[binding.entity_2.id]
            c_1 = e_1.components[binding.component_1.id]
            c_2 = e_2.components[binding.component_2.id]
            s.add_binding(c_1, c_2)
        for (pattern_id, info) in self.pattern_matching_info.iteritems():
            cp_info = PatternMatchingInfo(s, info.pattern)
            for c in info.correspondences:
                cp_info.add_correspondence(c.copy())
            s.__pattern_matching_info[pattern_id] = cp_info
        s.__unmathced_patterns = list(self.__unmatched_patterns)
        return s

    def is_specific(self):
        '''
        Checks and returns whether this species has specific properties.
        '''
        for en in self.entities.itervalues():
            if not en.is_specific():
                return False
        return True

    def is_consistent(self):
        '''
        Checks and returns whether there is no inconsistency in this species.
        '''
        # Checks the consistency between the binding state of each component 
        # and the bindings in the attribute.
        for en in self.entities.itervalues():
            for comp in en.components.itervalues():
                if comp.binding_state == BINDING_NONE:
                    if not comp.binding is None:
                        return False
                if comp.binding_state == BINDING_SPECIFIED:
                    if comp.binding is None:
                        return False

        # Checks the bindings.
        for b in self.bindings.itervalues():
            # Checks the binding state of the components of each binding.
            if b.component_1.binding_state == BINDING_NONE:
                return False
            if b.component_2.binding_state == BINDING_NONE:
                return False

            # Checks whether both components of each binding exists in the
            # list of entities of this species.
            found_1 = False
            found_2 = False
            for en in self.entities.itervalues():
                if not found_1:
                    if b.component_1 in en.components.itervalues():
                        found_1 = True
                if not found_2:
                    if b.component_2 in en.components.itervalues():
                        found_2 = True
                if found_1 and found_2:
                    break
            if not found_1 or not found_2:
                return False

        return True

    def check_concreteness(self):
        '''
        Checks and returns whether this species is appropriate as a 
        concrete species.
        '''

        # Checks whether all states are unambiguous.
        if not self.is_specific():
            return False

        # Checks the consistency.
        if not self.is_consistent():
            return False

        # Checks whether all entities in this species are connected with 
        # the bindings or this species is composed of only one entity.
        entity_set_list = self.get_entity_set_list()
        if len(entity_set_list) > 1:
            return False

        return True

    def get_entity_set_list(self, init_list=[]):
        '''
        Returns a list of the sets of entities that constitute this species.

        init_list: The initial list of the sets of entities.
        '''
        entity_set_list = []

        # Copies the input list of entity sets.
        for s in init_list:
            entity_set_list.append(s.copy())

        for b in self.bindings.itervalues():
            e_1 = b.entity_1
            e_2 = b.entity_2
            if not len(entity_set_list):
                # Creates the first element.
                s = set()
                s.add(e_1)
                s.add(e_2)
                entity_set_list.append(s)
            else:
                set_1 = None
                for s in entity_set_list:
                    if e_1 in s:
                        set_1 = s
                        break
                set_2 = None
                for s in entity_set_list:
                    if e_2 in s:
                        set_2 = s
                        break
                if not set_1 is None:
                    if not set_2 is None:
                        s = set()
                        for e in set_1:
                            s.add(e)
                        for e in set_2:
                            s.add(e)
                        entity_set_list.remove(set_1)
                        if set_1 != set_2:
                            entity_set_list.remove(set_2)
                        entity_set_list.append(s)
                    else:
                        set_1.add(e_2)
                else:
                    if not set_2 is None:
                        set_2.add(e_1)
                    else:
                        s = set()
                        s.add(e_1)
                        s.add(e_2)
                        entity_set_list.append(s)

        # Loop for entities that have no bindings.
        isolated_entity_list = []
        for e in self.entities.itervalues():
            if len(e.bindings):
                continue
            found = False
            for entity_set in entity_set_list:
                if e in entity_set:
                    found = True
                    break
            if not found:
                isolated_entity_list.append(e)
        for e in isolated_entity_list:
            s = set()
            s.add(e)
            entity_set_list.append(s)

        return entity_set_list


class PatternMatchingInfo(object):
    '''Information of the pattern matching.'''

    def __init__(self, species, pattern):
        '''
        Initializes this object.

        species: The species to match.
        pattern: The pattern species.
        '''
        self.__species = species
        self.__pattern = pattern
        self.__correspondences = []

    @property
    def species(self):
        '''Returns the species to match.'''
        return self.__species

    @property
    def pattern(self):
        '''Returns the pattern species.'''
        return self.__pattern

    @property
    def correspondences(self):
        '''Returns the list of correspondences added to this object.'''
        return self.__correspondences

    def add_correspondence(self, c):
        '''
        Adds a correspondence.

        c: A correspondence.
        '''
        self.__correspondences.append(c)

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'PatternMatchingInfo('
        retval += 'Pattern=\'%s\', ' % self.pattern.str_simple()
        retval += 'Species=\'%s\', ' % self.species.str_simple()
        for i, c in enumerate(self.correspondences):
            if i > 0:
                retval += ', '
            retval += str(c)
        retval += ')'
        return retval


class Pair(object):
    '''The base class for a pair of objects.'''

    def has_equal_first_element(self, pair):
        '''
        Returns whether this pair has the same first entity 
        with a given pair.

        pair: A pair.
        '''
        raise Error('Not implemented.')

    def has_equal_second_element(self, pair):
        '''
        Returns whether this pair has the same second entity 
        with a given pair.

        pair: A pair.
        '''
        raise Error('Not implemented.')


class PatternMatchingEntityPair(Pair):
    '''
    A pair of entities.
    One is in a pattern species, and the other is in a species to match.
    '''

    def __init__(self, pattern_entity, matched_entity):
        '''
        Initializes this pair object.

        pattern_entity: An entity in a pattern species.
        matched_entity: An entity in a species to match.
        '''
        self.__pattern_entity = pattern_entity
        self.__matched_entity = matched_entity

    @property
    def pattern_entity(self):
        '''Returns the entity in a pattern species.'''
        return self.__pattern_entity

    @property
    def matched_entity(self):
        '''Returns the entity in a species to match.'''
        return self.__matched_entity

    def has_equal_first_element(self, pair):
        '''
        Returns whether this pair has the same first entity 
        with a given pair.

        pair: An entity pair.
        '''
        return self.__pattern_entity == pair.__pattern_entity

    def has_equal_second_element(self, pair):
        '''
        Returns whether this pair has the same second entity 
        with a given pair.

        pair: An entity pair.
        '''
        return self.__matched_entity == pair.__matched_entity

    def __cmp__(self, other):
        '''
        Compares this object with a given other pair and returns the result.

        other: A pair.
        '''
        if self.pattern_entity.id < other.pattern_entity.id:
            return -1
        elif self.pattern_entity.id > other.pattern_entity.id:
            return 1
        else:
            if self.matched_entity.id < other.matched_entity.id:
                return -1
            elif self.matched_entity.id > other.matched_entity.id:
                return 1
            else:
                return 0

    def __str__(self):
        '''Returns the string representation of this object.'''
        e_1 = self.pattern_entity
        e_2 = self.matched_entity
        retval = ''
        retval += '%s(%d)' % (e_1.name, e_1.id)
        retval += '-'
        retval += '%s(%d)' % (e_2.name, e_2.id)
        return retval


class ReactantProductEntityPair(Pair):
    '''
    A pair of entities in a reaction rule.
    One is in a reactant species, and the other is in a product species.
    '''

    def __init__(self, reactant_index, reactant_entity, \
        product_index, product_entity):
        '''
        Initializes this pair object.

        reactant_index: The reactant index.
        reactant_entity: The reactant entity.
        product_index: The product index.
        product_entity: The product entity.
        '''
        self.__reactant_index = reactant_index
        self.__reactant_entity = reactant_entity
        self.__product_index = product_index
        self.__product_entity = product_entity

    @property
    def reactant_index(self):
        '''Returns the index of reactant.'''
        return self.__reactant_index

    @property
    def reactant_entity(self):
        '''Returns the entity of reactant.'''
        return self.__reactant_entity

    @property
    def product_index(self):
        '''Returns the index of product.'''
        return self.__product_index

    @property
    def product_entity(self):
        '''Returns the entity of product.'''
        return self.__product_entity

    def has_equal_first_element(self, pair):
        '''
        Returns whether this pair has the same reactant index
        and reantant entity with a given pair.

        pair: A pair of reactant entity and product entity.
        '''
        return self.reactant_index == pair.reactant_index \
            and self.reactant_entity == pair.reactant_entity

    def has_equal_second_element(self, pair):
        '''
        Returns whether this pair has the same product index
        and product entity with a given pair.

        pair: A pair of reactant entity and product entity.
        '''
        return self.product_index == pair.product_index \
            and self.product_entity == pair.product_entity

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = ''
        retval += '%s(%d,%d)' % (self.reactant_entity.name, \
            self.reactant_index, self.reactant_entity.id)
        retval += '-'
        retval += '%s(%d,%d)' % (self.product_entity.name, \
            self.product_index, self.product_entity.id)
        return retval

    def __cmp__(self, other):
        '''
        Compares this object with a given other pair and returns the result.

        other: A pair.
        '''
        if self.reactant_index < other.reactant_index:
            return -1
        elif self.reactant_index > other.reactant_index:
            return 1
        else:
            if self.reactant_entity.id < other.reactant_entity.id:
                return -1
            elif self.reactant_entity.id > other.reactant_entity.id:
                return 1
            else:
                return self.__cmp_product(other)

    def __cmp_product(self, other):
        if self.product_index < other.product_index:
            return -1
        elif self.product_index > other.product_index:
            return 1
        else:
            if self.product_entity.id < other.product_entity.id:
                return -1
            elif self.product_entity.id > other.product_entity.id:
                return 1
            else:
                return 0


class ReactantSpeciesEntityPair(Pair):
    '''
    A pair of entities.
    One is in a reactant pattern species, and the other is in a concrete 
    species.
    '''

    def __init__(self, reactant_index, reactant_entity, \
        species_entity):
        '''
        Initializes this pair object.

        reactant_index: The reactant index.
        reactant_entity: The reactant entity.
        species_entity: The entity of the concrete species.
        '''
        self.__reactant_index = reactant_index
        self.__reactant_entity = reactant_entity
        self.__species_entity = species_entity

    @property
    def reactant_index(self):
        '''Returns the reactant index.'''
        return self.__reactant_index

    @property
    def reactant_entity(self):
        '''Returns the reactant entity.'''
        return self.__reactant_entity

    @property
    def species_entity(self):
        '''Returns the entity of the concrete species.'''
        return self.__species_entity

    def has_equal_first_element(self, pair):
        '''
        Returns whether this pair has the same reactant index
        and reantant entity with the given pair.

        pair: An entity pair of reactant pattern and a concrete species.
        '''
        return self.reactant_index == pair.reactant_index \
            and self.reactant_entity == pair.reactant_entity

    def has_equal_second_element(self, pair):
        '''
        Returns whether this pair has the same product entity 
        with the given pair.

        pair: An entity pair of reactant pattern and a concrete species.
        '''
        return self.species_entity == pair.species_entity

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = '%s(%d,%d)' % (self.reactant_entity.name, \
            self.reactant_index, self.reactant_entity.id)
        retval += '-'
        retval += '%s(%d)' % (self.species_entity.name, \
            self.species_entity.id)
        return retval

    def __cmp__(self, other):
        '''
        Compares this object with a given other pair and returns the result.

        other: A pair.
        '''
        if self.reactant_index < other.reactant_index:
            return -1
        elif self.reactant_index > other.reactant_index:
            return 1
        else:
            if self.reactant_entity.id < other.reactant_entity.id:
                return -1
            elif self.reactant_entity.id > other.reactant_entity.id:
                return 1
            else:
                return 0


class Correspondence(object):
    '''
    Correspondence between objects.
    '''

    def __init__(self):
        '''Initializes this object.'''
        self.__pairs = []

    @property
    def pairs(self):
        '''Returns all pairs added to this object.'''
        return self.__pairs

    def add_pair(self, pair):
        '''
        Adds a pair.

        pair: A pair to add.
        '''
        self.__pairs.append(pair)

    def copy(self):
        '''Creates and returns the copy of this object.'''
        c = Correspondence()
        c.__pairs = list(self.__pairs)
        return c

    def __eq__(self, other):
        '''
        Returns whether this object is equal to given correspondence.

        other: An corerspondence.
        '''
        return self.__pairs == other.__pairs

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Correspondence('
        for i, pair in enumerate(self.pairs):
            if i > 0:
                retval += ', '
            retval += str(pair)
        retval += ')'
        return retval


def create_correspondence_list(pairs):
    '''
    Creates a list of correspondences from given pairs.

    pairs: List of pairs.
    '''
    cp_pairs = list(pairs)
    cp_pairs.sort()

    # Creates the lists of pairs for each first entity.
    pair_lists = []
    cur_pair = None
    cur_list = []
    for i, pair in enumerate(cp_pairs):
        if i == 0:
            cur_pair = pair
        else:
            if not pair.has_equal_first_element(cur_pair):
                pair_lists.append(cur_list)
                cur_list = []
                cur_pair = pair
        cur_list.append(pair)
    if len(cur_list):
        pair_lists.append(cur_list)

    combination_lists = []
    for i, pair_list in enumerate(pair_lists):
        if i == 0:
            for pair in pair_list:
                combination_lists.append([pair])
        else:
            comb_lists_new = []
            for comb in combination_lists:
                for pair in pair_list:
                    exists = False
                    for el in comb:
                        if el.has_equal_second_element(pair):
                            exists = True
                            break
                    if exists:
                        continue
                    list_new = list(comb) + [pair]
                    comb_lists_new.append(list_new)
            combination_lists = comb_lists_new

    correspondence_list = []
    for comb in combination_lists:
        c = Correspondence()
        for pair in comb:
            c.add_pair(pair)
        correspondence_list.append(c)

    return correspondence_list


class ReactionRule(object):
    '''
    The reaction rule both for pattern species and for concrete species.
    '''

    def __init__(self, id, model, reactants, products, concrete, \
        condition=None, **attrs):
        '''
        Initializes this reaction rule.

        id: The ID of this reaction rule.
        model: The model.
        reactants: List of reactant species.
        products: List of product species.
        concrete: The concreteness of this reaction rule.
        condition: The condition for this reaction rule.
        attrs: Map of attributes.
        '''

#        print '# *** reactants ***'
#        for i in reactants:
#            print '# ', str(i).partition("@")[0].replace('\n','')
#            print '# '

#        print '# *** products ***'
#        for i in products:
#            print '# ', str(i).partition("@")[0].replace('\n','')
#            print '# '

        self.__id = id
        self.__model = model
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

        # Checks whether given species are registered to the model.
        for sp in reactants:
            assert sp in self.model.species.values()
        for sp in products:
            assert sp in self.model.species.values()

        if concrete:
            # Checks the concreteness of species.
            for sp in reactants:
                assert sp.check_concreteness()
            for sp in products:
                assert sp.check_concreteness()
        else:
            # Checks the consistency of species.
            for sp in reactants:
                assert sp.is_consistent()
            for sp in products:
                assert sp.is_consistent()

        # Reactants and products.
        # Attributes with prefix 'input' means that they holds 
        # bare input values.
        # Attributes without the prefix is modified in the case 
        # that species appears or disappear in a reaction: 
        # dummy species are add to reactants and products for the
        # case of appearance and disappearance, respectively.
        self.__reactants = list(reactants)
        self.__products = list(products)
        self.__input_reactants = list(reactants)
        self.__input_products = list(products)

        # List of temporarily created concrete species.
        # They are used when new species appears in this reaction.
        self.__temporary_species_list = []

        # List of correspondences between reactants and products.
        self.__reactant_product_correspondences = []

        if concrete:
            self.__condition = None
        else:
            # Sets the given condition to the attribute.
            self.__condition = condition

            # Adds the dummy species to the reactants.
            self.__add_dummies(reactants, products)

            # Creates the correspondence list.
            self.__create_correspondence()

    def __create_temporary_species(\
        self, entity_type_name, dummy):
        '''
        Creates a temporary species which are used when species 
        appear or disappear.
        '''
        species = Species()
        entity = species.add_entity(\
            self.__model.entity_types[entity_type_name])
        species.dummy = dummy
        entity.dummy = dummy
        return species

    def __add_dummies(self, reactants, products):
        '''
        Adds the dummy species to the reactants when new species
        appear and to the products when species disappear, and
        updates the list of temporay species.
        '''
        # Checks the number of entities of each entitiy types.
        entity_types_set = set()
        reactant_entity_map = {}
        for r in reactants:
            for e in r.entities.itervalues():
                if not e.entity_type in reactant_entity_map:
                    reactant_entity_map[e.entity_type] = []
                reactant_entity_map[e.entity_type].append(e)
                entity_types_set.add(e.entity_type)
        product_entity_map = {}
        for p in products:
            for e in p.entities.itervalues():
                if not e.entity_type in product_entity_map:
                    product_entity_map[e.entity_type] = []
                product_entity_map[e.entity_type].append(e)
                entity_types_set.add(e.entity_type)

        # Adds dummy species.
        for entity_type in entity_types_set:
            if not entity_type in reactant_entity_map:
                reactant_entity_map[entity_type] = {}
            r_entities = reactant_entity_map[entity_type]
            if not entity_type in product_entity_map:
                product_entity_map[entity_type] = {}
            p_entities = product_entity_map[entity_type]
            num_diff = len(p_entities) - len(r_entities)
            if num_diff > 0:
                # appearance of entities
                p_list = self.__reactants
            elif num_diff < 0:
                # disappearance of entities
                p_list = self.__products
            if num_diff != 0:
                sp = self.__create_temporary_species(entity_type.name, \
                    True)
                for i in range(abs(num_diff)):
                    cp = sp.copy()
                    p_list.append(cp)

        # Updates the temporary species list. 
        for r in self.__reactants:
            if r.dummy:
                en = r.entities.values()[0]
                sp = self.__create_temporary_species(\
                    en.entity_type.name, False)
                self.__temporary_species_list.append(sp)

    def __create_correspondence(self):
        '''
        Creates the correspondence list between entities 
        in reactant species and those in product species.
        '''
        entity_pairs = []
        for i, r in enumerate(self.__reactants):
            for re in r.entities.itervalues():
                found = False
                for j, p in enumerate(self.__products):
                    for pe in p.entities.itervalues():
                        if re.entity_type is pe.entity_type:
                            # The product entity must be more specific
                            # than the reactant entity 
                            # exception the case of dummy product
                            # entity for disappearance of species.
                            if not pe.dummy:
                                if not pe.is_more_specific(re):
                                    continue

                            # The product entity must be specific
                            # for the appearance of species.
                            if re.dummy:
                                if not pe.is_specific():
                                    continue

                            # Creates a pair and add to the list.
                            pair = ReactantProductEntityPair(i, re, j, pe)
                            entity_pairs.append(pair)
                            found = True

                if not found:
                    msg = ""
                    msg += 'This reaction rule is invalid: %s.' \
                        % self.str_simple()
                    raise Error(msg)

        correspondence_list = create_correspondence_list(\
            entity_pairs)
        self.__reactant_product_correspondences = correspondence_list

    @property
    def id(self):
        '''Returns the ID of this reaction rule.'''
        return self.__id

    @property
    def reactants(self):
        '''
        Returns the list of reactants. This list may containt dummy reactant 
        species that are generated automatically when new species appears in 
        the products.
        '''
        return self.__reactants

    @property
    def products(self):
        '''
        Returns the list of products. This list may containt dummy product 
        species that are generated automatically when species disappears from 
        the reactants.
        '''
        return self.__products

    @property
    def input_reactants(self):
        ''' Returns the list of input reactants.'''
        return self.__input_reactants

    @property
    def input_products(self):
        ''' Returns the list of input products.'''
        return self.__input_products

    @property
    def condition(self):
        '''Returns the condition.'''
        return self.__condition

    @property
    def model(self):
        '''Returns the model.'''
        return self.__model

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

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

    def __str_species(self, species_list):
        retval = ''
        for i, species in enumerate(species_list):
            if species.dummy:
                continue
            if i > 0:
                retval += ' + '
            retval += species.str_simple()
        return retval

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = ''
        retval += self.__str_species(self.__reactants)
#        retval += ' -> '
        retval += ' > '
        retval += self.__str_species(self.__products)
        if not self.__condition is None:
            retval += ' %s' % str(self.__condition)
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'ReactionRule('
        retval += 'id=%d, ' % self.__id
        retval += 'reactants=('
        for i, species in enumerate(self.__reactants):
            if i > 0:
                retval += ', '
            retval += str(species)
        retval += '), '
        retval += 'products=('
        for i, species in enumerate(self.__products):
            if i > 0:
                retval += ', '
            retval += str(species)
        retval += '), '
        retval += 'condition=%s ,' % self.__condition
        retval += '), '
        retval += 'attrs=%r' % self.__attrs
        retval += ')'
        return retval

    def __is_temporary_species(self, sp):
        '''
        Checks whether a given species is in the temporary species list.
        '''
        for t in self.__temporary_species_list:
            # To checks the equality, 'equals' method is used
            # because species are often copied and the equality
            # of the instances of species is not ensured.
            if sp.equals(t):
                return True
        return False

    def __cmp_species_list(self, sp_list_1, sp_list_2):
        list_1 = list(sp_list_1)
        list_1.sort(lambda x,y: x.id - y.id)
        list_2 = list(sp_list_2)
        list_2.sort(lambda x,y: x.id - y.id)
        for i in range(len(list_1)):
            if not list_1[i].equals(list_2[i]):
                return False
        return True

    def equals(self, rule, cmp_input=True):
        '''
        Returns whether the given reaction rule is equal to this object.

        rule: A reaction rule.
        '''
        if self == rule:
            return True

        if cmp_input:
            self_reactants = self.input_reactants
            self_products = self.input_products
            rule_reactants = rule.input_reactants
            rule_products = rule.input_products
        else:
            self_reactants = self.reactants
            self_products = self.products
            rule_reactants = rule.reactants
            rule_products = rule.products

        # Length of reactants and products.
        if len(self_reactants) != len(rule_reactants):
            return False
        if len(self_products) != len(rule_products):
            return False

        # Reactant and product species.
        if len(self_reactants) <= len(self_products):
            self_first = self_reactants
            rule_first = rule_reactants
            self_second = self_products
            rule_second = rule_products
        else:
            self_first = self_products
            rule_first = rule_products
            self_second = self_reactants
            rule_second = rule_reactants

        if not self.__cmp_species_list(self_first, rule_first):
            return False
        if not self.__cmp_species_list(self_second, rule_second):
            return False

        # Conditions.
        if self.condition != rule.condition:
            return False

        return True

    def __create_all_combinations(self, el_lists):
        arrays = []
        for i, el_list in enumerate(el_lists):
            if i == 0:
                # Adds first elements.
                for el in el_list:
                    arrays.append([el])
            else:
                arrays_new = []
                for array in arrays:
                    for el in el_list:
                        a = list(array)
                        a.append(el)
                        arrays_new.append(a)
                arrays = arrays_new
        return arrays

    def generate_reactions(self, reactant_species_list):
        '''
        Generates reactions from given species under this reaction rule.
        '''

        # Checks the input species.
#        for sp in reactant_species_list:
#            assert sp.check_concreteness()
#            assert sp in self.model.species.values()

        # Updates the reactant species list for dummy reactants 
        # that exist when new species appears in this reaction.
        for sp in self.__temporary_species_list:
            reactant_species_list.append(sp.copy())

        # Creates a list of lists for each reactant species.
        reactant_lists = []
        for pattern in self.__reactants:
            r_list = []
            for r in reactant_species_list:
                # Applies the reactant patterns to given species.
                if r.matches(pattern, True):
                    if pattern.dummy:
                        # If the pattern is a dummy species,
                        # selects only the equal reactant species.
                        if r.equals(pattern):
                            r_list.append(r.copy())
                            break
                    else:
                        r_list.append(r.copy())

            # If no species matches to the reactant pattern, 
            # returns an empty list.
            if len(r_list) == 0:
                return []

            reactant_lists.append(r_list)

        # Creates a list of lists of concrete reactants species 
        # for each reaction.
        reactant_arrays = self.__create_all_combinations(reactant_lists)

        # Creates the species of products.
        product_lists = []
        for reactant_list in reactant_arrays:
            p_lists = self.__create_products(reactant_list)
            product_lists.append(p_lists)

        # Creates a list of reactions.
        reactions = []
        for i, reactants in enumerate(reactant_arrays):
            p_lists = product_lists[i]

            # Remove duplicated combination of the products.
            p_lists_new = []
            for j, products in enumerate(p_lists):
                if j == 0:
                    p_lists_new.append(products)
                else:
                    exists = False
                    for sp_list in p_lists_new:
                        if self.__is_equal_species_list(sp_list, products):
                            exists = True
                            break
                    if not exists:
                        p_lists_new.append(products)

            for products in p_lists_new:
                # If the number of generated product species is 
                # different from that of the reaction rule, 
                # skips this products.
                if len(products) != len(self.input_products):
                    continue

                # Checks whether the products are different from 
                # the reactants.
                if len(products) == len(reactants):
                    r_list = list(reactants)
                    p_list = list(products)
                    for i, r in enumerate(reactants):
                        for j, p in enumerate(products):
                            if r.equals(p):
                                if r in r_list:
                                    r_list.remove(r)
                                if p in p_list:
                                    p_list.remove(p)
                    if not len(r_list) and not len(p_list):
                        # If the length is different, skip this reaction.
                        continue

                # Removes temporay reactant speciess used for 
                # appearance of species.
                reactants_temp = list(reactants)
                for r in reactants_temp:
                    if self.__is_temporary_species(r):
                        reactants.remove(r)

                # Regiesters concrete species.
                products_new = []
                for p in products:
                    p_new = self.__model.register_species(p)
                    products_new.append(p_new)

                reactants_new = []
                for r in reactants:
                    r_found = None
                    for sp in self.__model.species.itervalues():
                        if sp.equals(r):
                            r_found = sp
                            break
                    assert r_found is not None
                    reactants_new.append(r_found)

                # Registers a concrete reaction.
                reaction = self.__model.add_concrete_reaction(\
                    self, reactants_new, products_new)
                if reaction is None:
                    continue
                reactions.append(reaction)

        return reactions

    def __is_equal_species_list(self, list_1, list_2):
        if len(list_1) != len(list_2):
            return False
        '''
        sp_list = list(list_2)
        for sp_1 in list_1:
            for sp_2 in list_2:
                if sp_2.equals(sp_1):
                    if sp_2 in sp_list:
                        sp_list.remove(sp_2)
                    break
        if len(sp_list):
            return False
        '''
        for i, sp_1 in enumerate(list_1):
            sp_2 = list_2[i]
            if not sp_2.equals(sp_1):
                return False
        return True

    def __create_products(self, reactant_species_list):
        '''
        Creates a list of the lists of product species from given \
        reactant species.
        '''
        # Creates correspondence lists between reactant and species.
        reactant_species_correspondence_lists = []
        for i, reactant in enumerate(self.reactants):
            # Gets the information of matched patterns.
            sp = reactant_species_list[i]
            info = sp.pattern_matching_info[reactant.id]
            reactant_species_correspondence_lists.append(\
                list(info.correspondences))

        reactant_species_correspondence_lists = \
            self.__create_all_combinations(\
                reactant_species_correspondence_lists)

        # Recreate the correspondece between all reactants and species.
        rs_correspondence_list = []
        for i, rsc_list in enumerate(\
            reactant_species_correspondence_lists):
            rs_correspondence = Correspondence()
            for j, rsc in enumerate(rsc_list):
                for pair in rsc.pairs:
                    pair_new = ReactantSpeciesEntityPair(\
                        j, pair.pattern_entity, pair.matched_entity)
                    rs_correspondence.add_pair(pair_new)
            rs_correspondence_list.append(rs_correspondence)

        created_species_lists = []
        for reactant_species_correspondence in rs_correspondence_list:
            species_lists = self.__apply_reaction_rule(
                reactant_species_list, reactant_species_correspondence)
            for species_list in species_lists:
                created_species_lists.append(species_list)

        return created_species_lists

    def __apply_reaction_rule(self, reactant_species_list, \
        reactant_species_correspondence):
        '''
        Applies this reaction rule to given reactant species 
        with given reactant-species correspondence.
        '''
        # Loops for all correspondence between reactant-species. 
        created_species_lists = []
        for reactant_product_correspondence in \
            self.__reactant_product_correspondences:
            created_species_list = self.__apply_reaction_rule_sub(\
                reactant_species_list, \
                reactant_product_correspondence, \
                reactant_species_correspondence)
            merged_species_lists = self.__merge_species(\
                created_species_list, \
                reactant_species_list)
            for merged_species_list in merged_species_lists:
                created_species_lists.append(merged_species_list)
        return created_species_lists

    def __apply_reaction_rule_sub(self, reactant_species_list, \
            reactant_product_correspondence, \
            reactant_species_correspondence):
        '''
        Applies this reaction rule to given reactant species 
        with given correspondence between reactant-products 
        and reactant-species.
        '''
        # Creates the copies of concrete reactant species.
        reactant_cp_list = []
        for r in reactant_species_list:
            sp_copy = r.copy()
            reactant_cp_list.append(sp_copy)

        # The list of sets of concrete species that is related to
        # each product pattern.
        related_species_sets = []
        for i in range(len(self.__products)):
            related_species_sets.append(set())

        # The list of pairs of components in a concrete species
        # connected with a link.
        linked_component_map = {}

        # Loop for correspondence pairs.
        for rp_pair in reactant_product_correspondence.pairs:
            reactant_index = rp_pair.reactant_index
            reactant_entity = rp_pair.reactant_entity
            product_index = rp_pair.product_index

            if not product_index in linked_component_map:
                linked_component_map[product_index] = {}

            # Concrete reactant species.
            sp_copy = reactant_cp_list[reactant_index]

            # Finds the pair of reactant species.
            rs_pair = None
            for rsp in reactant_species_correspondence.pairs:
                if rsp.reactant_index == reactant_index \
                and rsp.reactant_entity == reactant_entity:
                    rs_pair = rsp
                    break

            # Loop for the correspondence between all reactants 
            # and concrete species.
            self.__apply_reaction_rule_to_entity(rp_pair, rs_pair, \
                sp_copy, linked_component_map, related_species_sets)

        created_species_set = set()
        for s in related_species_sets:
            for sp in s:
                created_species_set.add(sp)
        created_species_list_new = list(created_species_set)

        return created_species_list_new

    def __apply_reaction_rule_to_entity(self, rp_pair, rs_pair, \
        sp_copy, linked_component_map, related_species_sets):

        product_entity = rp_pair.product_entity
        product_index = rp_pair.product_index

        sp_entity_id = rs_pair.species_entity.id
        sp_entity = sp_copy.entities[sp_entity_id]

        # -- For the disappearance of entities. --
        # If the product entity is an entity in a dummy species, 
        # remove the entity in a concrete species.
        # Sets the dummy flag of the entity to true.
        if product_entity.species.dummy:
            sp_entity.dummy = True
            related_species_sets[product_index].add(sp_copy)
            return

        # Loop for the components.
        for (comp_id, comp) in sp_entity.components.iteritems():
            product_component = product_entity.components[comp_id]

            # Edits the binding between the components. 
            product_binding_state = product_component.binding_state

            if product_binding_state == BINDING_SPECIFIED:
                # Replaces bindings if it exists or adds a new 
                # binding if it does not exist.
                self.__delete_binding(comp)
                self.__add_binding(sp_entity, product_component, \
                    linked_component_map, rp_pair, \
                    related_species_sets)
            elif product_binding_state == BINDING_NONE:
                # Deletes the binding if it exists.
                self.__delete_binding(comp)
                related_species_sets[product_index].add(sp_copy)
            else:
                # Only changes the states.
                related_species_sets[product_index].add(sp_copy)

            # Sets the binding state of the components.
            if product_binding_state != BINDING_UNSPECIFIED \
                and product_binding_state != BINDING_ANY:
                comp.binding_state = product_binding_state

            # Sets the states of the components.
            for (key, state) in product_component.states.iteritems():
                if state != STATE_UNSPECIFIED:
                    comp.states[key] = state

    def __delete_binding(self, comp):
        if not comp.binding is None:
            comp.binding.deleted = True

    def __add_binding(self, sp_entity, product_component, \
            linked_component_map, rp_pair, related_species_sets):
        comp_1 = sp_entity.components[product_component.id]
        lc_map = linked_component_map[rp_pair.product_index]
        binding = product_component.binding
        product_index = rp_pair.product_index
        if binding.id in lc_map:
            sp_1 = sp_entity.species
            comp_2 = lc_map[binding.id]
            sp_2 = comp_2.entity.species
            sp_1.add_binding(comp_1, comp_2, True)
            related_species_sets[product_index].add(sp_1)
            related_species_sets[product_index].add(sp_2)
            del lc_map[binding.id]
        else:
            lc_map[binding.id] = comp_1

    def __create_invalid_disappearance_errmsg(self, original_species_list, \
        merged_species_list):
        retval = ''
        retval += 'Some molecules disappear '
        retval += 'that are not specified explicitly.\n'
        retval += 'reaction rule: %s\n' % self.str_simple()
        retval += 'reactant species: ['
        for i, sp in enumerate(original_species_list):
            if i > 0:
                retval += ', '
            retval += sp.str_simple()
        retval += ']\n'
        retval += 'resultant products: ['
        for i, sp in enumerate(merged_species_list):
            if i > 0:
                retval += ', '
            retval += sp.str_simple()
        retval += ']'
        return retval

    def __merge_species(self, species_list, original_species_list):
        '''
        Merges given species and creates concrete species.
        '''
        # The list of merged species.
        merged_list = []

        # Sets the dummy flag of input species to False,
        # whidh are set to True for appeared species.
        for species in species_list:
            species.dummy = False

        # Removes deleted bindings.
        removed_binding_entity_set = set() 
        for species in species_list:
            bindings = species.bindings.copy()
            for b in bindings.itervalues():
                if b.deleted:
                    removed_binding_entity_set.add(b.entity_1)
                    removed_binding_entity_set.add(b.entity_2)
                    species.remove_binding(b)

        # Creates the list of entity sets.
        entity_set_list = []
        for i, species in enumerate(species_list):
            entity_set_list = species.get_entity_set_list(entity_set_list)

        # Loop for entities with deleted binding.
        for i, e in enumerate(removed_binding_entity_set):
            found = False
            for entity_set in entity_set_list:
                if e in entity_set:
                    found = True
                    break
            if not found:
                s = set()
                s.add(e)
                entity_set_list.append(s)

        # Completes the temporary bindings.
        for species in species_list:
            for b in species.bindings.itervalues():
                if b.temporary:
                    b.component_1.binding = b
                    b.component_2.binding = b
                    b.temporay = False

        # Merges the species.
        for entity_set in entity_set_list:

            # Gets all bindings.
            all_binding_set = set()
            for entity in entity_set:
                for b in entity.bindings:
                    all_binding_set.add(b)

            # Gets all entities.
            all_entities = []
            for entity in entity_set:
                all_entities.append(entity)

            # Creates a new species.
            sp = Species()
            sp.add_elements(all_entities, list(all_binding_set))

            # Adds to the list.
            merged_list.append(sp)

        # Checks dummy entities.
        # If all entities in a new species are dummy ones,
        # remove the species.
        # If a part of entities in a species are dummy ones,
        # this reaction rule cannot be adopted to the current
        # reactant species.
        merged_list_new = []
        for i, sp in enumerate(merged_list):
            d_set = set()
            for en in sp.entities.itervalues():
                d_set.add(en.dummy)
            if True in d_set and False in d_set:
                if self.model.disallow_implicit_disappearance:
                    msg = self.__create_invalid_disappearance_errmsg(\
                        original_species_list, merged_list)
                    raise Error(msg)
                else:
                    return []
            if False in d_set:
                merged_list_new.append(sp)

        # Checks the size of merged product species.
        # If the number of merged product species is larger than
        # the number of product patterns, some molecules may be disappeared.
        if len(merged_list_new) > len(self.__products):
            if self.model.disallow_implicit_disappearance:
                msg = self.__create_invalid_disappearance_errmsg(\
                    original_species_list, merged_list_new)
                raise Error(msg)
            else:
                return []

        # Checks the consistency.
        for sp in merged_list_new:
            if not sp.check_concreteness():
                msg = 'Created species is inconsistent: '
                msg += '%s' % sp.str_simple()
                raise Error(msg)

        # Sorts the merged species.
        product_list = []
        for i, p in enumerate(self.products):
            for sp in merged_list_new:
                if sp.matches(p):
                    product_list.append(sp)
                    merged_list_new.remove(sp)
                    break

        # To sort the merged species in order of product species, 
        # creates a list of lists for each product species.
        product_lists = []
        for product in self.products:
            p_list = []
            # Skips the dummy species.
            if product.dummy:
                continue
            for p in product_list:
                # Applies the product patterns to merged species.
                if p.matches(product):
                    p_list.append(p)
            product_lists.append(p_list)

        # Creates a list of lists of concrete product species 
        # for each reaction.
        product_arrays = self.__create_all_combinations(product_lists)
        product_arrays_new = []
        for p_array in product_arrays:
            # Removes combinations with duplicated instances of species.
            p_set = set(p_array)
            if len(p_set) == len(p_array):
                product_arrays_new.append(p_array)

        # When no products exist, adds an empty list.
        if not len(product_arrays_new):
            product_arrays_new.append([])

        return product_arrays_new


class Model(object):
    '''
    The rule-based model.
    '''

    def __init__(self, **attrs):
        '''
        Initializes this model.

        attrs: Map of attributes.
        '''
        self.__state_types = {}
        self.__entity_types = {}
        self.__species = {}
        self.__concrete_species = {}
        self.__reaction_rules = {}
        self.__reaction_results = {}
        self.__disallow_implicit_disappearance = True
        self.__serial_species = 0
        self.__serial_reaction_rules = 0
        self.__serial_reaction_results = 0
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def state_types(self):
        '''Returns the map of state types.'''
        return self.__state_types

    @property
    def entity_types(self):
        '''Returns the map of entity types.'''
        return self.__entity_types

    @property
    def species(self):
        '''Returns the map of all species.'''
        return self.__species

    @property
    def concrete_species(self):
        '''Returns the map of concrete species.'''
        return self.__concrete_species

    @property
    def reaction_rules(self):
        '''Returns the map of reaction rules.'''
        return self.__reaction_rules

    @property
    def reaction_results(self):
        '''Returns the map of reaction results.'''
        return self.__reaction_results

    @property
    def concrete_reactions(self):
        '''Returns the list of concrete reactions.'''
        reactions = []
        for result in self.reaction_results.itervalues():
            for reaction in result.reactions:
                reactions.append(reaction)
        reactions.sort(lambda x,y: x.id - y.id)
        return reactions

    def getdisallow_implicit_disappearance(self):
        '''
        Returns the flag whether to disallow implicit disappearance of 
        entities through the reaction.
        '''
        return self.__disallow_implicit_disappearance

    def setdisallow_implicit_disappearance(self, b):
        '''
        Sets the flag whether to disallow implicit disappearance of 
        entities through the reaction.

        b: The flag to set.
        '''
        self.__disallow_implicit_disappearance = b

    disallow_implicit_disappearance = property(\
        getdisallow_implicit_disappearance, \
        setdisallow_implicit_disappearance)

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

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

    def add_state_type(self, name, states, **attrs):
        '''
        Creates and registers a new state type.

        name: the name of state type
        states: array of the states
        attrs: Map of attributes.
        '''
        assert name not in self.__state_types
        state_type = StateType(name, list(states), **attrs)
        self.__state_types[name] = state_type
        return state_type

    def add_entity_type(self, name, **attrs):
        '''
        Creates and registers a new entity type.

        states: a map of internal states of a spacies
        attrs: Map of attributes.
        '''
        assert name not in self.__entity_types
        entity_type = EntityType(name, **attrs)
        self.__entity_types[name] = entity_type
        return entity_type

    def register_species(self, species):
        '''
        Registeres a given species.
        Returns the registered species object.
        If equivalent pattern species already exists, returns it.

        species: a species
        '''
        # Checks whether given species already exists.
        for sp in self.__species.itervalues():
            if species.equals(sp):
                return sp

        # Updates the concreteness flag.
        species.concrete = species.check_concreteness()

        self.__serial_species += 1
        cp = species.copy(self.__serial_species)
        self.__species[self.__serial_species] = cp
        if species.concrete:
            self.__concrete_species[self.__serial_species] = cp
        return cp

    def add_reaction_rule(self, reactants, products, condition=None, \
        **attrs):
        '''
        Creates and registers a new reaction rule.

        reactants: List of pattern species of reactants.
        products: List of pattern species of products.
        condition: The condition for this reaction rule.
        attrs: Map of attributes.
        '''

        # Gets the condition for this reaction rule.
        cond = None
        if not condition is None:
             if isinstance(condition, list):
                 cond = AndCondition(condition)
             else:
                 cond = condition

        # Creates an instance of a reaction rule.
        serial = self.__serial_reaction_rules + 1
        reaction_rule = ReactionRule(serial, self, list(reactants), \
            list(products), False, cond, **attrs)

        # Checks whether given reaction rule is already exists.
        for rule in self.__reaction_rules.itervalues():
            if rule.equals(reaction_rule):
                # If an equivalent reaction rule already exists, 
                # returns None.
                return None

        self.__serial_reaction_rules = serial
        self.__reaction_rules[serial] = reaction_rule
        return reaction_rule

    def add_concrete_reaction(self, rule, reactants, products):
        '''
        Creates and registers a new reaction with concrete reactant 
        and product species.
        '''
        # Checks the concreteness.
        for sp in reactants:
            assert sp.check_concreteness()
        for sp in products:
            assert sp.check_concreteness()

        # Creates a concrete reaction.
        serial = self.__serial_reaction_results + 1
        reaction = ReactionRule(serial, self, reactants, products, True)

        # Checks whether the reaction satisfies the condition.
        if not rule.condition is None:
            if not rule.condition.satisfies(reaction):
                return None

        # Checks whether given reaction rule is already exists.
        for ex_rule_id, ex_result in self.reaction_results.iteritems():
            for ex_reaction in ex_result.reactions:
                if ex_reaction.equals(reaction):
                    if rule.id == ex_rule_id:
                        return None
                    else:
                        msg = 'A concrete reaction \n'
                        msg += '  %s\n' % reaction.str_simple()
                        msg += 'is generated from multiple reaction rules:\n'
                        msg += '  %s\n' % rule.str_simple()
                        msg += 'and \n'
                        msg += '  %s.' % ex_result.reaction_rule.str_simple()
                        raise Error(msg)

        # Updates the attributes.
        self.__serial_reaction_results = serial
        if not rule.id in self.reaction_results:
            self.reaction_results[rule.id] = ReactionResult(rule)
        self.reaction_results[rule.id].add_reaction(reaction)

        return reaction

    def generate_reactions(self, species_list):
        '''
        Generates the reactions by applying all reaction rules to given species 
        and generated species.
        '''
        result_list = []
        rules = self.reaction_rules.copy()
        sp_list = list(species_list)
        for rule in rules.itervalues():
            reactions = rule.generate_reactions(sp_list)
            if len(reactions):
                result = ReactionResult(rule)
                for r in reactions:
                    result.add_reaction(r)
                result_list.append(result)
        return result_list

    def generate_reaction_network(self, species_list, max_iteration=1):
        '''
        Generates the reaction network by applying all reaction rules 
        to the species given and generated in iterations.

        species_list: The list of seed species.
        max_iteration: The maximum number of the iteration.
        '''

        assert max_iteration > 0

        # Reactions for each reaction ruls.
        reaction_list_map = {}
        for (rule_id, rule) in self.reaction_rules.iteritems():
            reaction_list_map[rule_id] = []

        # Initializes the list of species with given seed species.
        sp_list = list(species_list)

        # Loops until the list of species does not vary or up to the 
        # max iteration number.
        for i in range(max_iteration):

            # The counter for new species.
            new_species_cnt = 0

            # Finds the reaction rules and reactions.
            results = self.generate_reactions(sp_list)

            # Loops for the results.
            for result in results:
                rule = result.reaction_rule

                # Loops for the reactions.
                for reaction in result.reactions:
                    # Checks whether created reaction exists in the list 
                    # of reactions.
                    exists = False
                    reaction_list = reaction_list_map[rule.id]
                    for r in reaction_list:
                        if r.equals(reaction):
                            exists = True
                            break

                    # If the created reaction is a new one, add it 
                    # to the list of reactions.
                    if not exists:
                        reaction_list.append(reaction)

                    # Loops for the reactant species.
                    for p in reaction.products:
                        # Checks whether created species exists 
                        # in the list of species.
                        exists = False
                        for sp in sp_list:
                            if p.equals(sp):
                                exists = True
                                break
                        # If the created species is a new one, add it 
                        # to the species list.
                        if not exists:
                            sp_list.append(p)
                            new_species_cnt += 1

            # If new species are not generated, breaks the loop.
            if not new_species_cnt:
                break

        # Creates the returned value.
        result_list = []
        for (rule_id, reactions) in reaction_list_map.iteritems():
            rule = self.reaction_rules[rule_id]
            result = ReactionResult(rule)
            for r in reactions:
                result.add_reaction(r)
            result_list.append(result)
        return result_list


class ReactionResult(object):
    '''
    The result of reactions that has a reaction rule and concrete reactions 
    derived from the reaction rule.
    '''

    def __init__(self, rule):
        '''
        Initializes this result.

        rule: A reaction rule.
        '''
        self.__reaction_rule = rule
        self.__reactions = []

    @property
    def reaction_rule(self):
        '''Returns the reaction rule.'''
        return self.__reaction_rule

    @property
    def reactions(self):
        '''Returns the list of concrete reactions.'''
        return list(self.__reactions)

    def add_reaction(self, reaction):
        '''
        Adds a concrete reaction.

        reaction: A concrete reaction to add.
        '''
        self.__reactions.append(reaction)

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = ''
        retval += '[reaction rule=\'%s\', ' % self.reaction_rule.str_simple()
        retval += 'reactions=['
        for i, r in enumerate(self.reactions):
            if i > 0:
                retval += ', '
            retval += '%d: \'%s\'' % (r.id, r.str_simple())
        retval += ']]'
        return retval


class Condition(object):
    '''
    The base class of conditions.
    '''
    def satisfies(self, obj):
        '''
        Checks whether a given object satisfies this condition.

        obj: An object to check.
        '''
        raise Error('Not implemented.')


class AndCondition(Condition):
    '''A condition that has child conditions with AND condition.'''

    def __init__(self, conditions):
        '''
        Initializes this condition.

        conditions: List of conditions for child conditions.
        '''
        assert len(conditions)
        self.__conditions = list(conditions)

    def satisfies(self, obj):
        '''
        Checks and returns whether a given object satisfies all child 
        conditions.

        obj: An object to check.
        '''
        for cond in self.__conditions:
            if not cond.satisfies(obj):
                return False
        return True

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = ''
        for i, cond in enumerate(self.__conditions):
            if i > 0:
                retval += ' and '
            retval += '('
            retval += str(cond)
            retval += ')'
        return retval

    def __eq__(self, other):
        '''
        Returns whether this condition is equal to the given condition.

        other: A condition.
        '''
        if not isinstance(other, AndCondition):
            return False
        return self.__conditions == other.__conditions


class OrCondition(Condition):
    '''A condition that has child conditions with OR condition.'''

    def __init__(self, conditions):
        '''
        Initializes this condition.

        conditions: List of conditions for child conditions.
        '''
        assert len(conditions)
        self.__conditions = list(conditions)

    def satisfies(self, obj):
        '''
        Checks and returns whether a given object satisfies one of the child 
        conditions.

        obj: An object to check.
        '''
        for cond in self.__conditions:
            if cond.satisfies(obj):
                return True
        return False

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = ''
        for i, cond in enumerate(self.__conditions):
            if i > 0:
                retval += ' or '
            retval += '('
            retval += str(cond)
            retval += ')'
        return retval

    def __eq__(self, other):
        '''
        Returns whether this condition is equal to the given condition.

        other: A condition.
        '''
        if not isinstance(other, OrCondition):
            return False
        return self.__conditions == other.__conditions


class NotCondition(Condition):

    def __init__(self, condition):
        '''
        Initializes this condition.

        condition: A condition.
        '''
        self.__condition = condition

    @property
    def condition(self):
        '''Returns the condition.'''
        return self.__condition

    def satisfies(self, obj):
        '''
        Checks and returns whether a given object do not satisfy the child 
        condition.

        obj: An object to check.
        '''
        return not self.__condition.satisfies(obj)

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'not ('
        retval += str(self.__condition)
        retval += ')'
        return retval

    def __eq__(self, other):
        '''
        Returns whether this condition is equal to the given condition.

        other: A condition.
        '''
        if not isinstance(other, NotCondition):
            return False
        return self.__condition == other.__condition


class IncludingEntityCondition(Condition):
    '''
    The condition whether the reaction rule contains an entity of given type.
    '''

    def __init__(self, side, index, entity_type):
        '''
        Initializes this object.

        side: Specification of reactant or product. 
              (Constant of REACTANTS or PRODUCTS.)
        index: The index of reactant or product that starts from 1.
        entity_type: The entity type.
        '''
        assert side == REACTANTS or side == PRODUCTS
        assert index > 0
        self.__side = side
        self.__entity_type = entity_type

        # The index that starts from 0 is set to the attribute.
        self.__index = index - 1

    @property
    def side(self):
        '''Returns the specification of reactants or products.'''
        return self.__side

    @property
    def index(self):
        '''Returns the index of reactant or products that starts from 0.'''
        return self.__index

    @property
    def entity_type(self):
        '''Returns the entity type.'''
        return self.__entity_type

    def __get_species_list(self, rule):
        sp_list = None
        if self.side == REACTANTS:
            sp_list = rule.input_reactants
        else:
            sp_list = rule.input_products
        return sp_list

    def satisfies(self, rule):
        '''
        Checks whether a given reaction rule satisfies this condition.

        rule: the reaction rule to check
        '''

        # Gets the list of reactants or products.
        sp_list = self.__get_species_list(rule)
        assert self.index < len(sp_list)

        # Gets the species.
        sp = sp_list[self.index]

        # Searches the existence of an entity of given type.
        ret = False
        for en in sp.entities.itervalues():
#            if en.entity_type == self.entity_type:
            if en.entity_type.name == self.entity_type.name:
                ret = True
                break
        return ret

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = ''
        retval += 'include_'
        if self.side == REACTANTS:
            retval += 'reactants'
        else:
            retval += 'products'
        retval += '('
        retval += str(self.index + 1)
        retval += ','
        retval += self.entity_type.name
        retval += ')'
        return retval

    def __eq__(self, other):
        '''
        Returns whether this condition is equal to the given condition.

        other: A condition.
        '''
        if self.side != other.side:
            return False
        if self.index != other.index:
            return False
        if self.entity_type != other.entity_type:
            return False
        return True


class Error(Exception):
    '''The error.'''

    def __init__(self, value):
        '''
        Initializes this error object.

        value: A value set to this error.
        '''
        self.__value = value

    def __str__(self):
        '''Returns the string representation of this object.'''
        return str(self.__value)


