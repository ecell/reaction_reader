from __future__ import with_statement
import sys
#import model

global_list = []

tmp_dict = {}
tmp_list = []

end_flag = 0
popped_index = None

class AnyCallable(object):
    def __init__(self, key, outer=None):
        global global_list
        global tmp_dict
        global tmp_list
        global end_flag
        global popped_index

        if end_flag == 1:
            global_list.append(tmp_dict)
            tmp_dict = {}
            tmp_list = []
            end_flag = 0
            popped_index = None

            print global_list

        tmp_list.append({"name": key})

        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

    def __call__(self, *arg, **kwarg):
        global tmp_dict
        global tmp_list
        global end_flag
        global popped_index

        end_flag = 1
        print "end:" + self._key

        tmp_list.reverse()
        for i, a_dict in enumerate(tmp_list):
            if a_dict["name"] == self._key:
                parent = tmp_list.pop(i)

                if tmp_dict.has_key("children"):
                    children = tmp_list[popped_index:i]
                    del tmp_list[popped_index:i]
                    tmp_list.reverse()
                    children.append(tmp_dict)
                    tmp_dict = {"name": parent["name"], "children": children}
                else:
                    tmp_list.reverse()
                    parent["children"] = tmp_list
                    tmp_dict           = parent

                popped_index = i

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
