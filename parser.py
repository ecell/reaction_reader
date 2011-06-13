from __future__ import with_statement
import sys
#import model

global_dict = {}

tmp_dict = {}
tmp_list = []

class AnyCallable(object):
    def __init__(self, key, outer=None):
        global tmp_list

        tmp_list.append({"name": key})

        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)
        print tmp_list

    def __call__(self, *arg, **kwarg):
        global tmp_list
        print "end:" + self._key

        tmp_list.reverse()

        for i, a_dict in enumerate(tmp_list):
            if a_dict["name"] == self._key:
                tmp_list.reverse()
                latest_end_index = len(tmp_list) - i - 1
                parent   = tmp_list.pop(latest_end_index)
                children = tmp_list[latest_end_index:]
                del tmp_list[latest_end_index:]
                tmp_list.append({"name": parent["name"], "children": children})
                print tmp_list
                continue

        return self

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, key):
        try:
            return super(AnyCallable, self).__getattr__(key)
        except:
            return AnyCallable(key, self)

    def __getitem__(self, key):
        global tmp_list
        print "parameter: " + str(key)
        print tmp_list[-1]
        tmp_list[-1]["children"] = [{"type": "bracket", "value": str(key)}]
        return self

    def __gt__(self, rhs):
        print "gt"

    def __lt__(self, rhs):
        print "lt"

    def __ne__(self, rhs):
        global global_dict
        global_dict["type"]     = "neq"
        global_dict["children"] = tmp_list
        print "neq"

    def __add__(self,rhs):
        global tmp_dict
        tmp_dict["type"] = "add"
        tmp_dict["children"] = tmp_list
        print tmp_dict
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

print global_dict
