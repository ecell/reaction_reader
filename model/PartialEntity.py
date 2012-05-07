class PartialEntity(object):
    def __init__(self, key, sp):
        self.__key = key

        if type(sp) == RuleEntitySet:
            self.__sp = sp
        elif type(sp) == RuleEntity:
            self.__sp = RuleEntitySet(sp)
        else:
            raise TypeError

    @property
    def key(self):
        return self.__key
        
    @property
    def sp(self):
        return self.__sp
        
    def __call__(self, *args, **kwargs):
        entity = RuleEntity(self.key)

        for i in args:
            entity.join(RuleEntityComponent(i))
        for k, v in kwargs:
            entity.join(RuleEntityComponent(k, state = v))

        self.sp.join(entity)

        return self.sp

    def str_simple(self):
        return self.__str__()

    def __str__(self):
        return self.key + self.sp

