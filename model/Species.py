from Entity import *
from PatternMatchingInfo import *
from Pair import *
from Binding import *

class Species(object):
    '''The species.'''

    def __init__(self, id=0, **attrs):
        '''
        Initializes the species.

        id: The ID of this species. Value of zero is set by default.
        attrs: Map of attributes.
        '''
        self.__id = id
        self.__entities = {}
        self.__bindings = {}
        self.__dummy = False
        self.__concrete = False
        self.__serial_entity = 0
        self.__serial_binding = 0
        self.__attrs = {}
        for (k, v) in attrs.iteritems():
            self.__attrs[k] = v

        # List of information of the patterns that match to this species.
        self.__pattern_matching_info = {}

        # List of patterns that do not match to this species.
        self.__unmatched_patterns = []


    @property
    def id(self):
        '''Returns the ID.'''
        return self.__id

    @property
    def entities(self):
        '''Returns the list of entities in this species.'''
        return self.__entities

    @property
    def bindings(self):
        '''Returns the list of bindings in this species.'''
        return self.__bindings

    def getdummy(self):
        '''Returns the dummy flag.'''
        return self.__dummy

    def setdummy(self, b):
        '''
        Sets the dummy flag.

        b: The dummy flag to set.
        '''
        self.__dummy = b

    dummy = property(getdummy, setdummy)

    def getconcrete(self):
        '''Returns the concreteness flag.'''
        return self.__concrete

    def setconcrete(self, b):
        '''
        Sets the concrete flag.

        b: The concrete flag to set.
        '''
        self.__concrete = b

    concrete = property(getconcrete, setconcrete)

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

    @property
    def attributes(self):
        '''Returns the list of attributes.'''
        return self.__attrs

    @property
    def pattern_matching_info(self):
        '''Returns the information of pattern matching.'''
        return self.__pattern_matching_info

#    def add_entity(self, entity_type):
    def add_entity(self, entity_type, **attrs):
        '''
        Add entities of this molecular species.

        entity_type: The type of species for the new entity.
        '''
        self.__serial_entity += 1
#        entity = Entity(self.__serial_entity, entity_type, self)
        entity = Entity(self.__serial_entity, entity_type, self, **attrs)
        self.__entities[self.__serial_entity] = entity
        return entity

    def add_binding(self, component_1, component_2, temporary=False):
        '''
        Adds a binding between two components.

        component_1: The first component for new binding.
        component_2: The second component for new binding.
        temporay: The temporary flag for new binding.
        '''
        self.__serial_binding += 1
        b_id = self.__serial_binding

        # creates a binding object
        b = Binding(b_id, self, component_1, component_2, temporary)
        self.__bindings[b_id] = b

        # Sets the binding to entities if it is not temporary one.
        if not temporary:
            component_1.binding = b
            component_2.binding = b

        return b

    def remove_binding(self, binding):
        '''
        Removes the binding from this species.

        binding: A binding to be removed.
        '''
        assert binding in self.__bindings.values()
        b = self.__bindings[binding.id]
        b.component_1.binding = None
        b.component_2.binding = None
        del self.__bindings[binding.id]

    def add_elements(self, entity_list, binding_list):
        '''
        Adds entities and bindings.

        entity_list: List of entities added to this species.
        binding_list: List of bindings added to this species.
        '''
        for e in entity_list:
            self.__serial_entity += 1
            e.id = self.__serial_entity
            self.__entities[e.id] = e
        for b in binding_list:
            self.__serial_binding += 1
            b.id = self.__serial_binding
            self.__bindings[b.id] = b

    def str_simple(self):
        '''
        Returns the string representation of the simple version of this 
        object.
        '''
        retval = ''
        for i, entity in enumerate(self.__entities.itervalues()):
            retval += entity.str_simple()
            if i < len(self.__entities) - 1:
                retval += '.'
        return retval

    def __str__(self):
        '''Returns the string representation of this object.'''
        retval = 'Species('
        retval += 'id=%d, ' % self.__id
        retval += 'dummy=%s, ' % self.dummy
        retval += 'concrete=%s, ' % self.concrete
        retval += 'attrs=%s, ' % self.__attrs
        retval += '\n'
        retval += 'entities={'
        for i, (en_id, entity) in enumerate(self.entities.iteritems()):
            if i > 0:
                retval += ', '
            retval += '\n'
            retval += '%d: \'%s\'' % (en_id, entity)
        retval += '\n'
        retval += '}, '
        retval += '\n'
        retval += 'bindings={'
        for i, (b_id, binding) in enumerate(self.bindings.iteritems()):
            if i > 0:
                retval += ', '
            retval += '\n'
            retval += '%d: \'%s\'' % (b_id, binding)
        retval += '\n'
        retval += '}'
        retval += ')'
        return retval

    def matches(self, pattern, use_cache=False):
        '''
        Returns whether this species matches the given pattern species.

        pattern: A pattern species.
        use_cache: A flag whether to use the cache.
        '''
        if use_cache:
            # Checks whether the given pattern is contained
            # in the matched list or unmatched list.
            for p in self.__unmatched_patterns:
                if p is pattern:
                    return False
            for info in self.pattern_matching_info.itervalues():
                if info.pattern is pattern:
                    return True
        info = PatternMatchingInfo(self, pattern)
        matched = self.__matches_sub(pattern, info, use_cache)
        if use_cache:
            if matched:
                self.__pattern_matching_info[pattern.id] = info
            else:
                self.__unmatched_patterns.append(pattern)

        return matched

    def __matches_sub(self, pattern, info, use_cache):

        # Compares the number of entities between this species
        # and given pattern.
        if len(self.__entities) < len(pattern.__entities):
            return False

        # Checks the internal states and binding states.
        entity_pairs = []
        matched_entities = {}
        for (p_id, p_entity) in pattern.entities.iteritems():
            matched_entities[p_id] = []
            for (s_id, s_entity) in self.entities.iteritems():
                if s_entity.matches(p_entity):
                    pair = PatternMatchingEntityPair(p_entity, s_entity)
                    entity_pairs.append(pair)
                    matched_entities[p_id].append(s_id)

        # If no matched entities exist for any entitiy
        # of the pattern, returns False.
        for entities in matched_entities.itervalues():
            if not len(entities):
                return False

        # Gets the list of entity correspondence between a reactant pattern 
        # and a species.
        correspondence_list = create_correspondence_list(entity_pairs)

        # Checks the binding for each correspondence.
        valid_correspondence_list = []
        correspondence_found = False
        for i, c in enumerate(correspondence_list):

            # Loop for all entity pairs of correspondence.
            valid_correspondence = True
            for j, pair in enumerate(c.pairs):
                p_en = pair.pattern_entity
                m_en = pair.matched_entity

                # Checks the equality of bindings.
                for p_b in  p_en.bindings:
                    p_c_en = p_b.find_counterpart_entity(p_en)

                    binding_found = False
                    for m_b in m_en.bindings:
                        # Skips unmatched binding.
                        if not m_b.matches(p_b):
                            continue

                        # Skips the binding with different components.
                        m_c_en = m_b.find_counterpart_entity(m_en)
                        p_comp = p_b.find_component(p_en).component
                        m_comp = m_b.find_component(m_en).component
                        if p_comp != m_comp:
                            continue
                        p_c_comp = p_b.find_component(p_c_en).component
                        m_c_comp = m_b.find_component(m_c_en).component
                        if p_c_comp != m_c_comp:
                            continue

                        # Counterpart entity must be contained 
                        # in the pair.
                        pair_found = False
                        for p in c.pairs:
                            if p == pair:
                                continue
                            if p.pattern_entity == p_c_en \
                            and p.matched_entity == m_c_en:
                                pair_found = True
                                break

                        if pair_found:
                            binding_found = True
                            break

                    # If matched binding is not found, returns False.
                    if not binding_found:
                        valid_correspondence = False
                        break

                if not valid_correspondence:
                    break

            if valid_correspondence:
                correspondence_found = True
                valid_correspondence_list.append(c)

            # If not caching the pattern matching information, 
            # returns true when one correspondence is found.
            if not use_cache and correspondence_found:
                return True

        # If no correspondence is found.
        if not correspondence_found:
            return False

        if use_cache:
            for c in valid_correspondence_list:
                info.add_correspondence(c)

        return True

    def equals(self, sp):
        '''
        Returns whether this species is equals to the given species.

        sp: A species to compare.
        '''
        if self == sp:
            return True
        if len(self.entities) != len(sp.entities):
            return False
        if len(self.bindings) != len(sp.bindings):
            return False
        if not self.matches(sp):
            return False
        if not sp.matches(self):
            return False

        # for labeled/unlabeled species
        for i, v in enumerate(self.entities):
            for j, w in enumerate(self.entities[v].components):
                a = self.entities[v].components[w]
                try:  # for labeled/unlabeld species
                    b = sp.entities[v].components[w]
                    if hasattr(a, "label") != hasattr(b, "label"):
                        return False
                    elif a.label != b.label:
                        return False
                except:  # for normal species
                    pass


        return True

    def copy(self, id=0):
        '''
        Creates the copy of this species.

        id: The ID of copied species.
        '''
        s = Species(id)
        s.__attrs = self.__attrs.copy()
        s.__dummy = self.__dummy
        s.__concrete = self.__concrete
        for entity in self.entities.itervalues():
            e = s.add_entity(entity.entity_type)
            for (comp_id, comp) in entity.components.iteritems():
                c = e.components[comp_id]
                for (name, state) in comp.states.iteritems():
                    c.states[name] = comp.states[name]
                c.binding_state = comp.binding_state
                try: #
                    c.label = comp.label
                except:
                    pass


            e.dummy = entity.dummy
        for binding in self.bindings.itervalues():
            e_1 = s.entities[binding.entity_1.id]
            e_2 = s.entities[binding.entity_2.id]
            c_1 = e_1.components[binding.component_1.id]
            c_2 = e_2.components[binding.component_2.id]
            s.add_binding(c_1, c_2)
        for (pattern_id, info) in self.pattern_matching_info.iteritems():
            cp_info = PatternMatchingInfo(s, info.pattern)
            for c in info.correspondences:
                cp_info.add_correspondence(c.copy())
            s.__pattern_matching_info[pattern_id] = cp_info
        s.__unmathced_patterns = list(self.__unmatched_patterns)
        return s

    def is_specific(self):
        '''
        Checks and returns whether this species has specific properties.
        '''
        for en in self.entities.itervalues():
            if not en.is_specific():
                return False
        return True

    def is_consistent(self):
        '''
        Checks and returns whether there is no inconsistency in this species.
        '''
        # Checks the consistency between the binding state of each component 
        # and the bindings in the attribute.
        for en in self.entities.itervalues():
            for comp in en.components.itervalues():
                if comp.binding_state == BINDING_NONE:
                    if not comp.binding is None:
                        return False
                if comp.binding_state == BINDING_SPECIFIED:
                    if comp.binding is None:
                        return False

        # Checks the bindings.
        for b in self.bindings.itervalues():
            # Checks the binding state of the components of each binding.
            if b.component_1.binding_state == BINDING_NONE:
                return False
            if b.component_2.binding_state == BINDING_NONE:
                return False

            # Checks whether both components of each binding exists in the
            # list of entities of this species.
            found_1 = False
            found_2 = False
            for en in self.entities.itervalues():
                if not found_1:
                    if b.component_1 in en.components.itervalues():
                        found_1 = True
                if not found_2:
                    if b.component_2 in en.components.itervalues():
                        found_2 = True
                if found_1 and found_2:
                    break
            if not found_1 or not found_2:
                return False

        return True

    def check_concreteness(self):
        '''
        Checks and returns whether this species is appropriate as a 
        concrete species.
        '''
        # Checks whether all states are unambiguous.
        if not self.is_specific():
            return False

        # Checks the consistency.
        if not self.is_consistent():
            return False

        # Checks whether all entities in this species are connected with 
        # the bindings or this species is composed of only one entity.
        entity_set_list = self.get_entity_set_list()
        if len(entity_set_list) > 1:
            return False

        return True

    def get_entity_set_list(self, init_list=[]):
        '''
        Returns a list of the sets of entities that constitute this species.

        init_list: The initial list of the sets of entities.
        '''
        entity_set_list = []

        # Copies the input list of entity sets.
        for s in init_list:
            entity_set_list.append(s.copy())

        for b in self.bindings.itervalues():
            e_1 = b.entity_1
            e_2 = b.entity_2
            if not len(entity_set_list):
                # Creates the first element.
                s = set()
                s.add(e_1)
                s.add(e_2)
                entity_set_list.append(s)
            else:
                set_1 = None
                for s in entity_set_list:
                    if e_1 in s:
                        set_1 = s
                        break
                set_2 = None
                for s in entity_set_list:
                    if e_2 in s:
                        set_2 = s
                        break
                if not set_1 is None:
                    if not set_2 is None:
                        s = set()
                        for e in set_1:
                            s.add(e)
                        for e in set_2:
                            s.add(e)
                        entity_set_list.remove(set_1)
                        if set_1 != set_2:
                            entity_set_list.remove(set_2)
                        entity_set_list.append(s)
                    else:
                        set_1.add(e_2)
                else:
                    if not set_2 is None:
                        set_2.add(e_1)
                    else:
                        s = set()
                        s.add(e_1)
                        s.add(e_2)
                        entity_set_list.append(s)

        # Loop for entities that have no bindings.
        isolated_entity_list = []
        for e in self.entities.itervalues():
            if len(e.bindings):
                continue
            found = False
            for entity_set in entity_set_list:
                if e in entity_set:
                    found = True
                    break
            if not found:
                isolated_entity_list.append(e)
        for e in isolated_entity_list:
            s = set()
            s.add(e)
            entity_set_list.append(s)

        return entity_set_list

    def has_label(self):
        '''
        Returns True if any Entitiy of this species have label.
        '''
        for Ent in self.entities.itervalues():
            for Com in Ent.components.itervalues():
                if hasattr(Com, "label"):
                    return True

        return False


