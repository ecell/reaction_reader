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

