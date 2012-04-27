from Error import Error

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


