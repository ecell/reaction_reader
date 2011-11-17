from generac_func import *
from Pair import *
from Error import *
from Species import *

class ReactionRule(object):
    '''
    The reaction rule both for pattern species and for concrete species.
    '''

    def __init__(self, id, model, reactants, products, concrete, \
        condition=None, **attrs):
        '''
        Initializes this reaction rule.

        id: The ID of this reaction rule.
        model: The model.
        reactants: List of reactant species.
        products: List of product species.
        concrete: The concreteness of this reaction rule.
        condition: The condition for this reaction rule.
        attrs: Map of attributes.
        '''

#        print '# *** reactants ***'
#        for i in reactants:
#            print '# ', str(i).partition("@")[0].replace('\n','')
#            print '# '
#
#        print '# *** products ***'
#        for i in products:
#            print '# ', str(i).partition("@")[0].replace('\n','')
#            print '# '

        self.__id = id
        self.__model = model
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

        # Checks whether given species are registered to the model.
        for sp in reactants:
            assert sp in self.model.species.values()
        for sp in products:
            assert sp in self.model.species.values()

        if concrete:
            # Checks the concreteness of species.
            for sp in reactants:
                assert sp.check_concreteness()
            for sp in products:
                assert sp.check_concreteness()
        else:
            # Checks the consistency of species.
            for sp in reactants:
                assert sp.is_consistent()
            for sp in products:
                assert sp.is_consistent()

        # Reactants and products.
        # Attributes with prefix 'input' means that they holds 
        # bare input values.
        # Attributes without the prefix is modified in the case 
        # that species appears or disappear in a reaction: 
        # dummy species are add to reactants and products for the
        # case of appearance and disappearance, respectively.
        self.__reactants = list(reactants)
        self.__products = list(products)
        self.__input_reactants = list(reactants)
        self.__input_products = list(products)

        # List of temporarily created concrete species.
        # They are used when new species appears in this reaction.
        self.__temporary_species_list = []

        # List of correspondences between reactants and products.
        self.__reactant_product_correspondences = []

        if concrete:
            self.__condition = None
        else:
            # Sets the given condition to the attribute.
            self.__condition = condition

            # Adds the dummy species to the reactants.
            self.__add_dummies(reactants, products)

            # Creates the correspondence list.
            self.__create_correspondence()

    def __create_temporary_species(\
        self, entity_type_name, dummy):
        '''
        Creates a temporary species which are used when species 
        appear or disappear.
        '''
        species = Species()
        entity = species.add_entity(\
            self.__model.entity_types[entity_type_name])
        species.dummy = dummy
        entity.dummy = dummy
        return species

    def __add_dummies(self, reactants, products):
        '''
        Adds the dummy species to the reactants when new species
        appear and to the products when species disappear, and
        updates the list of temporay species.
        '''
        # Checks the number of entities of each entitiy types.
        entity_types_set = set()
        reactant_entity_map = {}
        for r in reactants:
            for e in r.entities.itervalues():
                if not e.entity_type in reactant_entity_map:
                    reactant_entity_map[e.entity_type] = []
                reactant_entity_map[e.entity_type].append(e)
                entity_types_set.add(e.entity_type)
        product_entity_map = {}
        for p in products:
            for e in p.entities.itervalues():
                if not e.entity_type in product_entity_map:
                    product_entity_map[e.entity_type] = []
                product_entity_map[e.entity_type].append(e)
                entity_types_set.add(e.entity_type)

        # Adds dummy species.
        for entity_type in entity_types_set:
            if not entity_type in reactant_entity_map:
                reactant_entity_map[entity_type] = {}
            r_entities = reactant_entity_map[entity_type]
            if not entity_type in product_entity_map:
                product_entity_map[entity_type] = {}
            p_entities = product_entity_map[entity_type]
            num_diff = len(p_entities) - len(r_entities)
            if num_diff > 0:
                # appearance of entities
                p_list = self.__reactants
            elif num_diff < 0:
                # disappearance of entities
                p_list = self.__products
            if num_diff != 0:
                sp = self.__create_temporary_species(entity_type.name, \
                    True)
                for i in range(abs(num_diff)):
                    cp = sp.copy()
                    p_list.append(cp)

        # Updates the temporary species list. 
        for r in self.__reactants:
            if r.dummy:
                en = r.entities.values()[0]
                sp = self.__create_temporary_species(\
                    en.entity_type.name, False)
                self.__temporary_species_list.append(sp)

    def __create_correspondence(self):
        '''
        Creates the correspondence list between entities 
        in reactant species and those in product species.
        '''
        entity_pairs = []
        for i, r in enumerate(self.__reactants):
            for re in r.entities.itervalues():
                found = False
                for j, p in enumerate(self.__products):
                    for pe in p.entities.itervalues():
                        if re.entity_type is pe.entity_type:
                            # The product entity must be more specific
                            # than the reactant entity 
                            # exception the case of dummy product
                            # entity for disappearance of species.
                            if not pe.dummy:
                                if not pe.is_more_specific(re):
                                    continue

                            # The product entity must be specific
                            # for the appearance of species.
                            if re.dummy:
                                if not pe.is_specific():
                                    continue

                            # Creates a pair and add to the list.
                            pair = ReactantProductEntityPair(i, re, j, pe)
                            entity_pairs.append(pair)
                            found = True

                if not found:
                    msg = ""
                    msg += 'This reaction rule is invalid: %s.' \
                        % self.str_simple()
                    raise Error(msg)

        correspondence_list = create_correspondence_list(\
            entity_pairs)
        self.__reactant_product_correspondences = correspondence_list

    @property
    def id(self):
        '''Returns the ID of this reaction rule.'''
        return self.__id

    @property
    def reactants(self):
        '''
        Returns the list of reactants. This list may containt dummy reactant 
        species that are generated automatically when new species appears in 
        the products.
        '''
        return self.__reactants

    @property
    def products(self):
        '''
        Returns the list of products. This list may containt dummy product 
        species that are generated automatically when species disappears from 
        the reactants.
        '''
        return self.__products

    @property
    def input_reactants(self):
        ''' Returns the list of input reactants.'''
        return self.__input_reactants

    @property
    def input_products(self):
        ''' Returns the list of input products.'''
        return self.__input_products

    @property
    def condition(self):
        '''Returns the condition.'''
        return self.__condition

    @property
    def model(self):
        '''Returns the model.'''
        return self.__model

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

    def __setitem__(self, k, v):
        '''
        Sets the attributes.

        k: The key.
        v: The value.
        '''
        self.__attrs[k] = v

    def __getitem__(self, k):
        '''
        Returns the value of the attribute of given key.
        If given key is not found, returns None.

        k: The key.
        '''
        return self.__attrs.get(k, None)

    def __str_species(self, species_list):
        retval = ''
        for i, species in enumerate(species_list):
            if species.dummy:
                continue
            if i > 0:
                retval += ' + '
            retval += species.str_simple()
        return retval

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = ''
        retval += self.__str_species(self.__reactants)
#        retval += ' -> '
        retval += ' > '
        retval += self.__str_species(self.__products)
        if not self.__condition is None:
            retval += ' %s' % str(self.__condition)
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'ReactionRule('
        retval += 'id=%d, ' % self.__id
        retval += 'reactants=('
        for i, species in enumerate(self.__reactants):
            if i > 0:
                retval += ', '
            retval += str(species)
        retval += '), '
        retval += 'products=('
        for i, species in enumerate(self.__products):
            if i > 0:
                retval += ', '
            retval += str(species)
        retval += '), '
        retval += 'condition=%s ,' % self.__condition
        retval += '), '
        retval += 'attrs=%r' % self.__attrs
        retval += ')'
        return retval

    def __is_temporary_species(self, sp):
        '''
        Checks whether a given species is in the temporary species list.
        '''
        for t in self.__temporary_species_list:
            # To checks the equality, 'equals' method is used
            # because species are often copied and the equality
            # of the instances of species is not ensured.
            if sp.equals(t):
                return True
        return False

    def __cmp_species_list(self, sp_list_1, sp_list_2):
        list_1 = list(sp_list_1)
        list_1.sort(lambda x,y: x.id - y.id)
        list_2 = list(sp_list_2)
        list_2.sort(lambda x,y: x.id - y.id)
        for i in range(len(list_1)):
            if not list_1[i].equals(list_2[i]):
                return False
        return True

    def equals(self, rule, cmp_input=True):
        '''
        Returns whether the given reaction rule is equal to this object.

        rule: A reaction rule.
        '''
        if self == rule:
            return True

        if cmp_input:
            self_reactants = self.input_reactants
            self_products = self.input_products
            rule_reactants = rule.input_reactants
            rule_products = rule.input_products
        else:
            self_reactants = self.reactants
            self_products = self.products
            rule_reactants = rule.reactants
            rule_products = rule.products

        # Length of reactants and products.
        if len(self_reactants) != len(rule_reactants):
            return False
        if len(self_products) != len(rule_products):
            return False

        # Reactant and product species.
        if len(self_reactants) <= len(self_products):
            self_first = self_reactants
            rule_first = rule_reactants
            self_second = self_products
            rule_second = rule_products
        else:
            self_first = self_products
            rule_first = rule_products
            self_second = self_reactants
            rule_second = rule_reactants

        if not self.__cmp_species_list(self_first, rule_first):
            return False
        if not self.__cmp_species_list(self_second, rule_second):
            return False

        # Conditions.
        if self.condition != rule.condition:
            return False

        return True

    def __create_all_combinations(self, el_lists):

        arrays = []
        for i, el_list in enumerate(el_lists):
            if i == 0:
                # Adds first elements.
                for el in el_list:
                    arrays.append([el])
            else:
                arrays_new = []
                for array in arrays:
                    for el in el_list:
                        a = list(array)
                        a.append(el)
                        arrays_new.append(a)
                arrays = arrays_new

        return arrays

    def generate_reactions(self, reactant_species_list):
        '''
        Returns own reaction rule as the result of reaction generation.
        '''
        
        reactants_new = []
        for sp in self.__reactants:
            if not sp.dummy:
                reactants_new.append(sp)
        self.__reactants = reactants_new

        products_new = []
        for sp in self.__products:
            if not sp.dummy:
                products_new.append(sp)
        self.__products = products_new

        reactions = []

        reaction = self.__model.add_concrete_reaction(\
            self, self.__reactants, self.__products)
        reactions.append(reaction)


        return reactions


    def generate_reactions_orig(self, reactant_species_list):
        '''
        Generates reactions from given species under this reaction rule.
        '''

        # Checks the input species.
#        for sp in reactant_species_list:
#            assert sp.check_concreteness()
#            assert sp in self.model.species.values()

        # Updates the reactant species list for dummy reactants 
        # that exist when new species appears in this reaction.
        for sp in self.__temporary_species_list:
            reactant_species_list.append(sp.copy())

        # Creates a list of lists for each reactant species.
        reactant_lists = []
        for pattern in self.__reactants:
            r_list = []
            for r in reactant_species_list:
                # Applies the reactant patterns to given species.
                if r.matches(pattern, True):
                    if pattern.dummy:
                        # If the pattern is a dummy species,
                        # selects only the equal reactant species.
                        if r.equals(pattern):
                            r_list.append(r.copy())
                            break
                    else:
                        r_list.append(r.copy())

            # If no species matches to the reactant pattern, 
            # returns an empty list.
            if len(r_list) == 0:
                return []

            reactant_lists.append(r_list)

	#import pdb; pdb.set_trace()

        # Creates a list of lists of concrete reactants species 
        # for each reaction.
        reactant_arrays = self.__create_all_combinations(reactant_lists)

	#import pdb; pdb.set_trace()

        # Creates the species of products.
        product_lists = []
        for reactant_list in reactant_arrays:
            p_lists = self.__create_products(reactant_list)
            product_lists.append(p_lists)

        # Creates a list of reactions.
        reactions = []
        for i, reactants in enumerate(reactant_arrays):
            p_lists = product_lists[i]

            # Remove duplicated combination of the products.
            p_lists_new = []
            for j, products in enumerate(p_lists):
                if j == 0:
                    p_lists_new.append(products)
                else:
                    exists = False
                    for sp_list in p_lists_new:
                        if self.__is_equal_species_list(sp_list, products):
                            exists = True
                            break
                    if not exists:
                        p_lists_new.append(products)

            for products in p_lists_new:
                # If the number of generated product species is 
                # different from that of the reaction rule, 
                # skips this products.
                if len(products) != len(self.input_products):
                    continue

                # Checks whether the products are different from 
                # the reactants.
                if len(products) == len(reactants):
                    r_list = list(reactants)
                    p_list = list(products)
                    for i, r in enumerate(reactants):
                        for j, p in enumerate(products):
                            if r.equals(p):
                                if r in r_list:
                                    r_list.remove(r)
                                if p in p_list:
                                    p_list.remove(p)
                    if not len(r_list) and not len(p_list):
                        # If the length is different, skip this reaction.
                        continue

                # Removes temporay reactant speciess used for 
                # appearance of species.
                reactants_temp = list(reactants)
                for r in reactants_temp:
                    if self.__is_temporary_species(r):
                        reactants.remove(r)

                # Regiesters concrete species.
                products_new = []
                for p in products:
                    p_new = self.__model.register_species(p)
                    products_new.append(p_new)

                reactants_new = []
                for r in reactants:
                    r_found = None
                    for sp in self.__model.species.itervalues():
                        if sp.equals(r):
                            r_found = sp
                            break
                    assert r_found is not None
                    reactants_new.append(r_found)

                # Registers a concrete reaction.
                reaction = self.__model.add_concrete_reaction(\
                    self, reactants_new, products_new)
                if reaction is None:
                    continue
                reactions.append(reaction)

        for i in reactions:
            print type(i)

	import pdb; pdb.set_trace()

        return reactions

    def __is_equal_species_list(self, list_1, list_2):
        if len(list_1) != len(list_2):
            return False
        '''
        sp_list = list(list_2)
        for sp_1 in list_1:
            for sp_2 in list_2:
                if sp_2.equals(sp_1):
                    if sp_2 in sp_list:
                        sp_list.remove(sp_2)
                    break
        if len(sp_list):
            return False
        '''
        for i, sp_1 in enumerate(list_1):
            sp_2 = list_2[i]
            if not sp_2.equals(sp_1):
                return False
        return True

    def __create_products(self, reactant_species_list):
        '''
        Creates a list of the lists of product species from given \
        reactant species.
        '''
        # Creates correspondence lists between reactant and species.
        reactant_species_correspondence_lists = []
        for i, reactant in enumerate(self.reactants):
            # Gets the information of matched patterns.
            sp = reactant_species_list[i]
            info = sp.pattern_matching_info[reactant.id]
            reactant_species_correspondence_lists.append(\
                list(info.correspondences))

	#import pdb; pdb.set_trace()
	
        reactant_species_correspondence_lists = \
            self.__create_all_combinations(\
                reactant_species_correspondence_lists)

	#import pdb; pdb.set_trace()

        # Recreate the correspondece between all reactants and species.
        rs_correspondence_list = []
        for i, rsc_list in enumerate(\
            reactant_species_correspondence_lists):
            rs_correspondence = Correspondence()
            for j, rsc in enumerate(rsc_list):
                for pair in rsc.pairs:
                    pair_new = ReactantSpeciesEntityPair(\
                        j, pair.pattern_entity, pair.matched_entity)
                    rs_correspondence.add_pair(pair_new)
            rs_correspondence_list.append(rs_correspondence)

        created_species_lists = []
        for reactant_species_correspondence in rs_correspondence_list:
            species_lists = self.__apply_reaction_rule(
                reactant_species_list, reactant_species_correspondence)
            for species_list in species_lists:
                created_species_lists.append(species_list)

        return created_species_lists

    def __apply_reaction_rule(self, reactant_species_list, \
        reactant_species_correspondence):
        '''
        Applies this reaction rule to given reactant species 
        with given reactant-species correspondence.
        '''
        # Loops for all correspondence between reactant-species. 
        created_species_lists = []
        for reactant_product_correspondence in \
            self.__reactant_product_correspondences:
            created_species_list = self.__apply_reaction_rule_sub(\
                reactant_species_list, \
                reactant_product_correspondence, \
                reactant_species_correspondence)
            merged_species_lists = self.__merge_species(\
                created_species_list, \
                reactant_species_list)
            for merged_species_list in merged_species_lists:
                created_species_lists.append(merged_species_list)
        return created_species_lists

    def __apply_reaction_rule_sub(self, reactant_species_list, \
            reactant_product_correspondence, \
            reactant_species_correspondence):
        '''
        Applies this reaction rule to given reactant species 
        with given correspondence between reactant-products 
        and reactant-species.
        '''
        # Creates the copies of concrete reactant species.
        reactant_cp_list = []
        for r in reactant_species_list:
            sp_copy = r.copy()
            reactant_cp_list.append(sp_copy)

        # The list of sets of concrete species that is related to
        # each product pattern.
        related_species_sets = []
        for i in range(len(self.__products)):
            related_species_sets.append(set())

        # The list of pairs of components in a concrete species
        # connected with a link.
        linked_component_map = {}

        # Loop for correspondence pairs.
        for rp_pair in reactant_product_correspondence.pairs:
            reactant_index = rp_pair.reactant_index
            reactant_entity = rp_pair.reactant_entity
            product_index = rp_pair.product_index

            if not product_index in linked_component_map:
                linked_component_map[product_index] = {}

            # Concrete reactant species.
            sp_copy = reactant_cp_list[reactant_index]

            # Finds the pair of reactant species.
            rs_pair = None
            for rsp in reactant_species_correspondence.pairs:
                if rsp.reactant_index == reactant_index \
                and rsp.reactant_entity == reactant_entity:
                    rs_pair = rsp
                    break

            # Loop for the correspondence between all reactants 
            # and concrete species.
            self.__apply_reaction_rule_to_entity(rp_pair, rs_pair, \
                sp_copy, linked_component_map, related_species_sets)

        created_species_set = set()
        for s in related_species_sets:
            for sp in s:
                created_species_set.add(sp)
        created_species_list_new = list(created_species_set)

        return created_species_list_new

    def __apply_reaction_rule_to_entity(self, rp_pair, rs_pair, \
        sp_copy, linked_component_map, related_species_sets):

        product_entity = rp_pair.product_entity
        product_index = rp_pair.product_index

        sp_entity_id = rs_pair.species_entity.id
        sp_entity = sp_copy.entities[sp_entity_id]

        # -- For the disappearance of entities. --
        # If the product entity is an entity in a dummy species, 
        # remove the entity in a concrete species.
        # Sets the dummy flag of the entity to true.
        if product_entity.species.dummy:
            sp_entity.dummy = True
            related_species_sets[product_index].add(sp_copy)
            return

        # Loop for the components.
        for (comp_id, comp) in sp_entity.components.iteritems():
            product_component = product_entity.components[comp_id]

            # Edits the binding between the components. 
            product_binding_state = product_component.binding_state

            if product_binding_state == BINDING_SPECIFIED:
                # Replaces bindings if it exists or adds a new 
                # binding if it does not exist.
                self.__delete_binding(comp)
                self.__add_binding(sp_entity, product_component, \
                    linked_component_map, rp_pair, \
                    related_species_sets)
            elif product_binding_state == BINDING_NONE:
                # Deletes the binding if it exists.
                self.__delete_binding(comp)
                related_species_sets[product_index].add(sp_copy)
            else:
                # Only changes the states.
                related_species_sets[product_index].add(sp_copy)

            # Sets the binding state of the components.
            if product_binding_state != BINDING_UNSPECIFIED \
                and product_binding_state != BINDING_ANY:
                comp.binding_state = product_binding_state

            # Sets the states of the components.
            for (key, state) in product_component.states.iteritems():
                if state != STATE_UNSPECIFIED:
                    comp.states[key] = state

    def __delete_binding(self, comp):
        if not comp.binding is None:
            comp.binding.deleted = True

    def __add_binding(self, sp_entity, product_component, \
            linked_component_map, rp_pair, related_species_sets):
        comp_1 = sp_entity.components[product_component.id]
        lc_map = linked_component_map[rp_pair.product_index]
        binding = product_component.binding
        product_index = rp_pair.product_index
        if binding.id in lc_map:
            sp_1 = sp_entity.species
            comp_2 = lc_map[binding.id]
            sp_2 = comp_2.entity.species
            sp_1.add_binding(comp_1, comp_2, True)
            related_species_sets[product_index].add(sp_1)
            related_species_sets[product_index].add(sp_2)
            del lc_map[binding.id]
        else:
            lc_map[binding.id] = comp_1

    def __create_invalid_disappearance_errmsg(self, original_species_list, \
        merged_species_list):
        retval = ''
        retval += 'Some molecules disappear '
        retval += 'that are not specified explicitly.\n'
        retval += 'reaction rule: %s\n' % self.str_simple()
        retval += 'reactant species: ['
        for i, sp in enumerate(original_species_list):
            if i > 0:
                retval += ', '
            retval += sp.str_simple()
        retval += ']\n'
        retval += 'resultant products: ['
        for i, sp in enumerate(merged_species_list):
            if i > 0:
                retval += ', '
            retval += sp.str_simple()
        retval += ']'
        return retval

    def __merge_species(self, species_list, original_species_list):
        '''
        Merges given species and creates concrete species.
        '''
        # The list of merged species.
        merged_list = []

        # Sets the dummy flag of input species to False,
        # whidh are set to True for appeared species.
        for species in species_list:
            species.dummy = False

        # Removes deleted bindings.
        removed_binding_entity_set = set() 
        for species in species_list:
            bindings = species.bindings.copy()
            for b in bindings.itervalues():
                if b.deleted:
                    removed_binding_entity_set.add(b.entity_1)
                    removed_binding_entity_set.add(b.entity_2)
                    species.remove_binding(b)

        # Creates the list of entity sets.
        entity_set_list = []
        for i, species in enumerate(species_list):
            entity_set_list = species.get_entity_set_list(entity_set_list)

        # Loop for entities with deleted binding.
        for i, e in enumerate(removed_binding_entity_set):
            found = False
            for entity_set in entity_set_list:
                if e in entity_set:
                    found = True
                    break
            if not found:
                s = set()
                s.add(e)
                entity_set_list.append(s)

        # Completes the temporary bindings.
        for species in species_list:
            for b in species.bindings.itervalues():
                if b.temporary:
                    b.component_1.binding = b
                    b.component_2.binding = b
                    b.temporay = False

        # Merges the species.
        for entity_set in entity_set_list:

            # Gets all bindings.
            all_binding_set = set()
            for entity in entity_set:
                for b in entity.bindings:
                    all_binding_set.add(b)

            # Gets all entities.
            all_entities = []
            for entity in entity_set:
                all_entities.append(entity)

            # Creates a new species.
            sp = Species()
            sp.add_elements(all_entities, list(all_binding_set))

            # Adds to the list.
            merged_list.append(sp)

        # Checks dummy entities.
        # If all entities in a new species are dummy ones,
        # remove the species.
        # If a part of entities in a species are dummy ones,
        # this reaction rule cannot be adopted to the current
        # reactant species.
        merged_list_new = []
        for i, sp in enumerate(merged_list):
            d_set = set()
            for en in sp.entities.itervalues():
                d_set.add(en.dummy)
            if True in d_set and False in d_set:
                if self.model.disallow_implicit_disappearance:
                    msg = self.__create_invalid_disappearance_errmsg(\
                        original_species_list, merged_list)
                    raise Error(msg)
                else:
                    return []
            if False in d_set:
                merged_list_new.append(sp)

        # Checks the size of merged product species.
        # If the number of merged product species is larger than
        # the number of product patterns, some molecules may be disappeared.
        if len(merged_list_new) > len(self.__products):
            if self.model.disallow_implicit_disappearance:
                msg = self.__create_invalid_disappearance_errmsg(\
                    original_species_list, merged_list_new)
                raise Error(msg)
            else:
                return []

        # Checks the consistency.
        for sp in merged_list_new:
            if not sp.check_concreteness():
                msg = 'Created species is inconsistent: '
                msg += '%s' % sp.str_simple()
                raise Error(msg)

        # Sorts the merged species.
        product_list = []
        for i, p in enumerate(self.products):
            for sp in merged_list_new:
                if sp.matches(p):
                    product_list.append(sp)
                    merged_list_new.remove(sp)
                    break

        # To sort the merged species in order of product species, 
        # creates a list of lists for each product species.
        product_lists = []
        for product in self.products:
            p_list = []
            # Skips the dummy species.
            if product.dummy:
                continue
            for p in product_list:
                # Applies the product patterns to merged species.
                if p.matches(product):
                    p_list.append(p)
            product_lists.append(p_list)

        # Creates a list of lists of concrete product species 
        # for each reaction.
        product_arrays = self.__create_all_combinations(product_lists)
        product_arrays_new = []
        for p_array in product_arrays:
            # Removes combinations with duplicated instances of species.
            p_set = set(p_array)
            if len(p_set) == len(p_array):
                product_arrays_new.append(p_array)

        # When no products exist, adds an empty list.
        if not len(product_arrays_new):
            product_arrays_new.append([])

        return product_arrays_new


