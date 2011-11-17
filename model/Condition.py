from Model import *

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


