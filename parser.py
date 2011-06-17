from __future__ import with_statement
#from operator import itemgetter
import sys
from model import Model
#from parser import Parser
#from model import Species

m = Model()
#parser = Parser()

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
        #print tmp_list

    def __call__(self, *arg, **kwarg):
        global tmp_list
        print "end:" + self._key

        matched_indices = []

        for i, a_dict in enumerate(tmp_list):
            if a_dict.get("name") == self._key:
                matched_indices.append(i)

        parent   = tmp_list.pop(matched_indices[-1])
        children = tmp_list[matched_indices[-1]:]
        del tmp_list[matched_indices[-1]:]
        tmp_list.append({"name": parent["name"], "children": children})
        #print tmp_list

        if 'name' in tmp_list[len(tmp_list)-2]:
            if tmp_list[len(tmp_list)-2]['name'] is '.':
                if 'name' in tmp_list[len(tmp_list)-3] and tmp_list[len(tmp_list)-3]['name'] is '.':
                    tmp_list[len(tmp_list)-3]['children'].append(tmp_list.pop(len(tmp_list)-1))
                    tmp_list.pop(len(tmp_list)-1)
                elif len(tmp_list)-2 <> 0:
                    dot_list = []
                    dot_list.append(tmp_list.pop(len(tmp_list)-1))
                    dot_list.append(tmp_list.pop(len(tmp_list)-2))
                    tmp_list[len(tmp_list)-1]['children'] = dot_list

        return self

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, key):
        try:
            return super(AnyCallable, self).__getattr__(key)
        except:
            global tmp_list
            tmp_list.append({"name": "."})
            return AnyCallable(key, self)

    def __getitem__(self, key):
        global tmp_list
        print "parameter: " + str(key)
        #print tmp_list[-1]
        if "children" in tmp_list[-1]:
            tmp_list[-1]["children"].append({"type": "bracket", "value": str(key)})
        else:
            tmp_list[-1]["children"] = [{"type": "bracket", "value": str(key)}]
#        tmp_list[-1]["children"] = [{"type": "bracket", "value": str(key)}]
        #print tmp_list
        return self

    def __gt__(self, rhs):
        print "gt"

    def __lt__(self, rhs):
        print "lt"

    def __ne__(self, rhs):
        global global_dict
        global tmp_list

        bind_indices = []

#        for i, a_dict in enumerate(tmp_list):
#            if a_dict.get("type") == "add":
#                # write me!!
#                pass
#            if a_dict.get("name") == ".":
#                bind_indices.append(i)

        #print bind_indices
        #getter = itemgetter(bind_indices)

#        complex_list = tmp_list[min(bind_indices) - 1:max(bind_indices) + 2]
#        complex_dict = {"type": "dot", "children": complex_list}
#        #print complex_list
#        tmp_list[min(bind_indices) - 1] = complex_dict
#        del tmp_list[min(bind_indices) : max(bind_indices) + 2]
        #print tmp_list

        global_dict["type"]     = "neq"
        global_dict["children"] = tmp_list
        print "neq"

        print "*** global_dict in ne ***"
        print global_dict

        tmp_list = []

    def __add__(self,rhs):
        global tmp_list
        global tmp_dict
#        tmp_dict["type"]     = "add"
#        tmp_dict["children"] = tmp_list
#        tmp_list = [tmp_dict]
#        return self

        if tmp_list[len(tmp_list)-2].has_key('type'):
            tmp_list[len(tmp_list)-2]['children'].append(tmp_list.pop(len(tmp_list)-1))
        else:
            add_dict = {}
            add_list = []
            add_dict["type"] = "add"
            add_list.append(tmp_list.pop(len(tmp_list)-1))
            add_list.append(tmp_list.pop(len(tmp_list)-1))

            add_dict["children"] = add_list

            tmp_list.append(add_dict)

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
        global tmp_list
        mole_entity_list = [] # string. check for double registration such as A and A.B.
        mole_state_list = []  # string. check for state_type registration.
        mole_state_dict = {}  # tuple.   key:State_type
        for i in tmp_list:

            if i['name'] not in mole_entity_list and i['name'] != '.':
                tmpmole = m.add_entity_type(i['name'])
                mole_entity_list.append(i['name'])

                for j in i['children']:
                    if j.has_key('children'):
                        if j['children'][0]['name'] not in mole_state_list:
                            new_state = j['children'][0]['name']
                            new_state_P = 'p' + new_state
                            p_state = m.add_state_type('state_'+new_state, [new_state, new_state_P])
                            mole_state_dict[new_state] = p_state
                            mole_state_list.append(new_state)
                        tmpmole.add_component(j['name'], {new_state: mole_state_dict[new_state]})
                    else:
                        tmpmole.add_component(j['name'])

        print '*** tmp_list / MoleculeTypes.__exit__ ***'
        print tmp_list
        tmp_list = []
#            parser.add_entity_type(tmpmole)

globals = MyDict()
globals['reaction_rules'] = ReactionRules()
globals['molecule_types'] = MoleculeTypes()

exec file(sys.argv[1]) in globals

#print global_dict

#for i in m.state_types:
#    print i, m.state_types[i]

#for i in m.entity_types.items():
#    print i[1]
