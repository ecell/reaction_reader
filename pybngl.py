from __future__ import with_statement
import sys
from model import Model
from parser import Parser
from model import Species
from model import BINDING_SPECIFIED
from model import BINDING_NONE
from model import BINDING_ANY
from model import BINDING_UNSPECIFIED

m      = Model()
parser = Parser()

global_list = []
tmp_list    = []

class AnyCallable(object):
    def __init__(self, key, outer=None):
        global tmp_list

        tmp_list.append({"name": key})

        print "start: " + key
        super(AnyCallable, self).__setattr__('_key', key)
        super(AnyCallable, self).__setattr__('_outer', outer)

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

        if "children" in tmp_list[-1]:
            tmp_list[-1]["children"].append({"type": "bracket", "value": str(key)})
        else:
            tmp_list[-1]["children"] = [{"type": "bracket", "value": str(key)}]

        return self

    def operator(self, rhs):
        global global_list
        global tmp_list
        tmp_dict = {}
        print rhs

        tmp_dict["type"]     = rhs
        tmp_dict["children"] = tmp_list
        global_list.append(tmp_dict)

        tmp_list = []

    def __gt__(self, rhs):
        self.operator("gt")

    def __lt__(self, rhs):
        print "lt"

    def __ne__(self, rhs):
        self.operator("neq")

    def __add__(self,rhs):
        global tmp_list

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
        mole_state_list  = [] # string. check for state_type registration.
        mole_state_dict  = {} # tuple.   key:State_type
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
                parser.add_entity_type(tmpmole)

#        print '*** tmp_list / MoleculeTypes.__exit__ ***'
#        print tmp_list
        tmp_list = []

globals = MyDict()
globals['reaction_rules'] = ReactionRules()
globals['molecule_types'] = MoleculeTypes()

exec file(sys.argv[1]) in globals

def read_entity(sp, m, p, entity, binding_components):

    if 'type' in entity:
#        print 'function'
        return

    entity_name = entity['name']
#    print '*** entity_name***', entity_name
    entity_type = p._Parser__entity_types[entity_name]
    en = sp.add_entity(entity_type)

#    print '*** sp ***'
#    print sp

    for i in filter(lambda x: 'name' in x, entity['children']):
        comp_name = i['name']
#        print 'compname: ', comp_name
        components = en.find_components(comp_name)
        try:
            en_comp = components[0]
            en_comp.binding_state = BINDING_NONE
#            print '*** components ***\n', en_comp

#            for j in filter(lambda x: 'children' in x, i['children']):
##            for j in filter(lambda x: 'children' in x, i):
#                print '***j***', j
#                print '\n*** children of comp ***', j

            if 'children' in i:
                for j in i['children']:

                    if 'name' in j:  # states input
                        k = en_comp.states.keys()[0]
                        v = j['name']
                        en_comp.set_state(k, v)

                    if 'type' in j:  # binding input
                        binding_type = j['value']
                        if binding_type == '+':
                            en_comp.binding_state = BINDING_ANY
                        elif binding_type == '?':
                            en_comp.binding_state = BINDING_UNSPECIFIED
                        elif binding_type.isdigit():
                            en_comp.binding_state = BINDING_SPECIFIED
                            binding_id = int(binding_type)
                            if not binding_id in binding_components:
                                binding_components[binding_id] = []
                            binding_components[binding_id].append(en_comp)

        except IndexError:
#            print 'components not found (', comp_name, ')'
            quit()
        except KeyError:
            pass


def read_species(m, p, species):

    sp = Species()

    bind_comp = {}

    if species['name'] == '.':  #   A.B
        for entity in species['children']:
#            print '***ent***', entity
            read_entity(sp, m, p, entity, bind_comp)
        for comps in bind_comp.itervalues():
            if len(comps) != 2:
                pass
            else:
                sp.add_binding(comps[0], comps[1])
    else:                       #   A
        read_entity(sp, m, p, species, bind_comp)

    return sp


def read_patterns(m, p, species):

    s_list = []
    
    if 'type' in species and species['type'] == 'add':
        for entity in species['children']:
            sp = read_species(m, p, entity)
            sp = m.register_species(sp)
            s_list.append(sp)

    else:
        sp = read_species(m, p, species)
        sp = m.register_species(sp)
        s_list.append(sp)


    return s_list


#print '**global_list***'
#print global_list[1]


id = 10

print '\n*** reactants ***'
reactants = read_patterns(m, parser, global_list[id]['children'][0])
for i in reactants:
    print i

print '\n*** products ***'
products = read_patterns(m, parser, global_list[id]['children'][1])
for i in products:
    print i

rule = m.add_reaction_rule(reactants, products)
print m.reaction_rules.items()
#print m.reaction_rules[1]


#    egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) + Sos(dom) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]).Sos(dom[2]) [michaelis_menten]

N_A = 6.0221367e+23
sp_str_list = ['Sos(dom)']
seed_species = parser.parse_species_array(sp_str_list, m)
seed_values = [10000. * N_A]

