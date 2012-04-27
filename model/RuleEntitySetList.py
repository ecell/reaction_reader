from Error import Error

class RuleEntitySetList(object):
    '''The list of RuleEntitySets(aka Species.)'''

    def __init__(self, **attrs):
        '''
        Initializes the list.

        model: The model.
        attrs: Map of attributes.
        '''
        self.__species = []
        self.__serial_species = 0
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def species(self):
        '''Returns the list of species.'''
        return self.__species

    @property
    def serial_species(self):
        '''Returns the number of species.'''
        return self.__serial_species

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

    def join(self, sp):
        '''
        Adds species to set.

        species: Species.
        '''
        self.__species.append(sp)
        self.__serial_species += 1

        return

    def __gt__(self, rhs):
        '''
        Creates a new reaction rule, registers it to model, and returns it.

        rhs: RuleEntitySetList that represents products.
        '''

        if type(rhs) != RuleEntitySetList:
            raise Error('Incomplete reaction rule.')

        # reaction_rule = self.__model.add_reaction_rule(self.species, 
        #                                                rhs.species)
        reaction_rule = None

        return reaction_rule

    def str_simple(self):
        ''''''
        return [i.str_simple() for i in self.__species]
