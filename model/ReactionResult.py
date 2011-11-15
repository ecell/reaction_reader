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


