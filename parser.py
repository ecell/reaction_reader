import sys
#import model

global_dict = {}

tmp_dict = {}
tmp_list = []

class AnyCallable(object):
    def __init__(self, key, outer=None):
        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)
        tmp_list.append(key)

    def __call__(self, *arg, **kwarg):
        global tmp_list
        #global tmp_dict
        print tmp_list
        print "end:" + self._key
        tmp_list.remove(self._key)
        #tmp_dict[self._key] = tmp_list.pop(tmp_list.index(self._key) + 1)
        print tmp_list
        global_dict[self._key] = tmp_list
        print global_dict
        tmp_list = []
        return self

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, key):
        try:
            return super(AnyCallable, self).__getattr__(key)
        except:
            return AnyCallable(key, self)

    def __getitem__(self, key):
        print "parameter: " + str(key)
        return self

    def __gt__(self, rhs):
        print "gt"

    def __lt__(self, rhs):
        print "lt"

    def __ne__(self, rhs):
        print "neq"

    def __add__(self,rhs):
        return self

class MyDict(dict):
    def __init__(self):
        super(MyDict, self).__init__()

    def __setitem__(self, key, val):
        super(MyDict, self).__setitem__(key, val)

    def __getitem__(self, key):
        retval = self.get(key)
        if retval is None:
            retval = AnyCallable(key)
        return retval

class ReactionRules(object):
    def __enter__(self):
        pass

    def __exit__(self, *arg):
        pass

class MoleculeTypes(object):
    def __enter__(self):
        pass

    def __exit__(self, *arg):
        pass

globals = MyDict()
globals['reaction_rules'] = ReactionRules()
globals['molecule_types'] = MoleculeTypes()

exec file(sys.argv[1]) in globals
