class Binding(object):
    """The binding between two components.

    
    """
    def __init__(self, id, species, component_1, component_2, specified, temporary, \
        **attrs):
        '''
        Initializes the binding.

        id: ID of this biding.
        species: The graph that this binding belongs to.
        component_1: The first component.
        component_2: The second component.
        specified: The specified flag.
        temporary: The temporary flag.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__species = species
        self.__component_1 = component_1
        self.__component_2 = component_2
        self.__specified = specified
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

    def getspecified(self):
        '''Returns the specified flag.'''
        return self.__specified

    def setspecified(self, b):
        '''
        Sets the specified flag.

        b: The temporary flag to set.
        '''
        self.__specified = b

    specified = property(getspecified, setspecified)

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
        retval += 'specified=%s, ' % self.__specified
        retval += 'temporary=%s, ' % self.__temporary
        retval += 'deleted=%s, ' % self.__deleted
        retval += '%s(%d).%s' % (self.entity_1.name, self.entity_1.id, \
            self.component_1.name)
        retval += '-'
        retval += '%s(%d).%s' % (self.entity_2.name, self.entity_2.id, \
            self.component_2.name)
        retval += ')'
        return retval


