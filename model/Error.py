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


