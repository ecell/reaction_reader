- setup
  >>> from model.general_func import *
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
  >>> from model.Pair import PatternMatchingEntityPair
  >>> from model.Correspondence import Correspondence

  >>> p_state = StateType('phosphorylation', ['U', 'P'])
  >>> entity_type_a = EntityType('A')
  >>> comp_r_a = entity_type_a.add_component('r', {'p': p_state})
  >>> comp_d_a = entity_type_a.add_component('d')
  >>> entity_type_b = EntityType('B')
  >>> comp_r_b = entity_type_b.add_component('r', {'p': p_state})
  >>> comp_d_b = entity_type_b.add_component('d')
  >>> entity_type_c = EntityType('C')
  >>> comp_r_c = entity_type_c.add_component('r', {'p': p_state})
  >>> comp_d_c = entity_type_c.add_component('d')
  >>> entity_type_d = EntityType('D')
  >>> comp_r_d = entity_type_d.add_component('r', {'p': p_state})
  >>> comp_d_d = entity_type_d.add_component('d')
  >>> parser = Parser()
  >>> parser.add_entity_type(entity_type_a)
  >>> parser.add_entity_type(entity_type_b)
  >>> parser.add_entity_type(entity_type_c)
  >>> parser.add_entity_type(entity_type_d)

- create_correspondence_list
  >>> sp_text = 'A().A()'
  >>> sp_1 = parser.parse_species(sp_text)
  >>> entities_1 = sp_1.entities
  >>> sp_text = 'A().A().A()'
  >>> sp_2 = parser.parse_species(sp_text)
  >>> entities_2 = sp_2.entities
  >>> pairs = []
  >>> p = PatternMatchingEntityPair(entities_1[1], entities_2[2])
  >>> pairs.append(p)
  >>> p = PatternMatchingEntityPair(entities_1[1], entities_2[3])
  >>> pairs.append(p)
  >>> p = PatternMatchingEntityPair(entities_1[2], entities_2[1])
  >>> pairs.append(p)
  >>> p = PatternMatchingEntityPair(entities_1[2], entities_2[2])
  >>> pairs.append(p)
  >>> c_list = create_correspondence_list(pairs)
  >>> c_1 = Correspondence()
  >>> c_1.add_pair(PatternMatchingEntityPair(entities_1[1], entities_2[2]))
  >>> c_1.add_pair(PatternMatchingEntityPair(entities_1[2], entities_2[1]))
  >>> c_2 = Correspondence()
  >>> c_2.add_pair(PatternMatchingEntityPair(entities_1[1], entities_2[3]))
  >>> c_2.add_pair(PatternMatchingEntityPair(entities_1[2], entities_2[1]))
  >>> c_3 = Correspondence()
  >>> c_3.add_pair(PatternMatchingEntityPair(entities_1[1], entities_2[3]))
  >>> c_3.add_pair(PatternMatchingEntityPair(entities_1[2], entities_2[2]))
  >>> len(c_list)
  3
  >>> c_1 in c_list
  True
  >>> c_2 in c_list
  True
  >>> c_3 in c_list
  True
