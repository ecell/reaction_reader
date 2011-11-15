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


