from Component import *

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


