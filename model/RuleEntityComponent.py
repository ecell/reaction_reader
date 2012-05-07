class RuleEntityComponent(object):
    def __init__(self, key, bind = None, state = None, label = None, **attrs):
        self.__key = key
        self.__bind = bind
        self.__sate = state
        self.__label = label
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

    @property
    def key(self):
        return self.__key

    @property
    def bind(self):
        return self.__bind

    @property
    def state(self):
        return self.__state

    @property
    def label(self):
        return self.__label

    def __setitem__(self, k, v):
        self.__attrs[k] = v

    def __getitem(self, k):
        return self.__attrs.get(k, None)

    @property
    def attributes(self):
        return self.__attrs

    def __str__(sef):
        return self.key
