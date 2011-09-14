import model
import sys

class Parser(object):

    def __init__(self):
        self.__entity_types = {}

    def add_entity_type(self, entity_type):
        self.__entity_types[entity_type.name] = entity_type

    def parse_species(self, sp_text):
        split_list = sp_text.split('.')
        if not len(split_list):
            return None
        split_list_new = []
        for str in split_list:
            split_list_new.append(str.strip())
        entity_name_list = []
        entity_content_list = []
        for str in split_list_new:
            if not str.endswith(')'):
                return None
            end_index = len(str) - 1
            start_index = str.find('(')
            if start_index == -1:
                return None
            if start_index == 0:
                return None
            entity_name = str[0:start_index]
            if start_index == end_index - 1:
                entity_content = ''
            else:
                entity_content = str[start_index + 1:end_index]
            entity_name_list.append(entity_name.strip())
            entity_content_list.append(entity_content.strip())

        sp = model.Species()
        binding_components = {}
        for i, name in enumerate(entity_name_list):

            # Creates an entity.
            if not name in self.__entity_types:
                return None
            entity_type = self.__entity_types[name]
            en = sp.add_entity(entity_type)

            # Gets text string for components.
            content_text = entity_content_list[i]
            comma_index_set = set()
            for j in range(len(content_text)):
                if content_text[j] == ',':
                    comma_index_set.add(j)
            inside_bracket = False
            for j in range(len(content_text)):
                if content_text[j] == '[':
                    inside_bracket = True
                if content_text[j] == ']':
                    inside_bracket = False
                    continue
                if inside_bracket:
                    if content_text[j] == ',':
                        comma_index_set.remove(j)
            comma_index_list = list(comma_index_set)
            comma_index_list.sort()

            split_list = []
            start_index = 0
            for comma_index in comma_index_list:
                split_list.append(content_text[start_index:comma_index])
                start_index = comma_index + 1
            split_list.append(content_text[start_index:len(content_text)])

            split_list_new = []
            for c_str in split_list:
                split_list_new.append(c_str.strip())

            for c_str in split_list_new:
                if not len(c_str):
                    continue

                # Binding.
                binding_id = None
                comp_str_list = c_str.split('!')
                if len(comp_str_list) == 1:
                    binding_state = model.BINDING_NONE
                elif len(comp_str_list) == 2:
                    binding_value = comp_str_list[1].strip()
                    if binding_value.isdigit():
                        binding_state = model.BINDING_SPECIFIED
                        binding_id = int(binding_value)
                    else:
                        if binding_value == model.BINDING_UNSPECIFIED_STRING:
                            binding_state = model.BINDING_UNSPECIFIED
                        elif binding_value == model.BINDING_ANY_STRING:
                            binding_state = model.BINDING_ANY
                        else:
                            return None
                else:
                    return None

                # A text string for the name and states of a component.
                comp_name_and_states = comp_str_list[0].strip()

                # Name and states.
                comp_str_list = comp_name_and_states.split('~')
                if len(comp_str_list) == 1:
                    comp_states_list = []
                elif len(comp_str_list) == 2:
                    comp_states_str = comp_str_list[1].strip()
                    sb = comp_states_str.startswith('[')
                    eb = comp_states_str.endswith(']')
                    if sb and eb:
                        comp_states_str = comp_states_str[\
                            1:len(comp_states_str) - 1]
                    elif not sb and not eb:
                        pass
                    else:
                        return None
                    comp_states_list = comp_states_str.split(',')
                else:
                    return None

                # A text string for the name of a component.
                comp_name = comp_str_list[0].strip()

                # Finds the components.
                components = en.find_components(comp_name)
                if not len(components):
                    return None
                if len(components) != 1:
                    raise Exception('Unsupported')
                en_comp = components[0]

                # Sets the states.
                for comp_state in comp_states_list:
                    str_list = comp_state.split(':')
                    if len(str_list) == 1:
                        state_value = str_list[0]
                        states = en_comp.states
                        if len(states) != 1:
                            return None
                        state_name = states.keys()[0]
                    elif len(str_list) == 2:
                        state_name = str_list[0]
                        if not state_name in en_comp.state_types:
                            return None
                        state_value = str_list[1]
                    else:
                        return None
                    en_comp.set_state(state_name, state_value)

                # Sets the binding state.
                en_comp.binding_state = binding_state

                # Sets binding component to the map.
                if binding_id != None:
                    if not binding_id in binding_components:
                        binding_components[binding_id] = []
                    binding_components[binding_id].append(en_comp)

        # Sets the bindings.
        for comps in binding_components.itervalues():
            if len(comps) != 2:
                return None
            sp.add_binding(comps[0], comps[1])

        return sp


    def parse_species_array(self, sp_str_list, model=None):
        sp_list = []
        for sp_str in sp_str_list:
            sp = self.parse_species(sp_str)
            print "# *** sp_str_list in parser.parer_species_array ***"
            print '# ', str(sp_str_list)
            print "# *** sp  in parser.parer_species_array ***"
            print '# ', str(sp).partition("@")[0].replace('\n','')
            print "# *** end of parser.parer_species_array ***"
            if sp is None:
                print sp_str
            if model != None:
                sp = model.register_species(sp)
            sp_list.append(sp)
        return sp_list

    def __split_species_array_string(self, sp_array_str):
        plus_index_set = set()
        for i in range(len(sp_array_str)):
            if sp_array_str[i] == '+':
                plus_index_set.add(i)
        inside_bracket = False
        for i in range(len(sp_array_str)):
            if sp_array_str[i] == '(':
                inside_bracket = True
                continue
            elif sp_array_str[i] == ')':
                inside_bracket = False
                continue
            elif sp_array_str[i] == '+':
                if inside_bracket:
                    plus_index_set.remove(i)
        plus_index_list = list(plus_index_set)
        plus_index_list.sort()
        split_str_list = []
        start_index = 0
        for index in plus_index_list:
            split_str_list.append(sp_array_str[start_index:index])
            start_index = index + 1
            if start_index >= len(sp_array_str):
                return None
        split_str_list.append(sp_array_str[start_index:len(sp_array_str)])
        return split_str_list

    def parse_reaction(self, rule_text, m, id=0, concrete=False, \
            condition=None, register=False, **attrs):
        rp_str_list = rule_text.split('->')
        if len(rp_str_list) != 2:
            return None
        reactants_str = rp_str_list[0]
        if reactants_str.isspace() or len(reactants_str) == 0:
            reactants = []
        else:
            reactants_str_list = self.__split_species_array_string(\
                reactants_str)
            reactants = self.parse_species_array(reactants_str_list, m)
        products_str = rp_str_list[1]
        if products_str.isspace() or len(products_str) == 0:
            products = []
        else:
            products_str_list = self.__split_species_array_string(\
                products_str)
            products = self.parse_species_array(products_str_list, m)
        if register:
            rule = m.add_reaction_rule(reactants, products, condition, **attrs)
        else:
            rule = model.ReactionRule(id, m, reactants, products, concrete, \
                condition, **attrs)
        return rule


