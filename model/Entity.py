from EntityComponent import *


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


