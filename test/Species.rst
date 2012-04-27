- setup
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> from model.PatternMatchingInfo import PatternMatchingInfo
  >>> from model.Pair import Pair
  >>> from model.Binding import Binding
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
  >>> from model.general_func import *

  >>> p_state = StateType('phosphorylation', ['U', 'P'])
  >>> a_state = StateType('acetylation', ['U', 'A'])
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

  >>> entity_types = [entity_type_a, entity_type_b, entity_type_c, entity_type_d]

- init
  >>> sp = Species()
  >>> sp = Species(10)
  >>> sp = Species(1, key_1='value_1', key_2='value_2')
  >>> sp['key_1'], sp['key_2']
  ('value_1', 'value_2')

- id
  >>> sp = Species()
  >>> sp.id
  0
  >>> sp = Species(10)
  >>> sp.id
  10

- getdummy, setdummy
  >>> sp = Species()
  >>> sp.dummy
  False
  >>> sp.dummy = True
  >>> sp.dummy
  True

- getconcrete, setconcrete
  >>> sp = Species()
  >>> sp.concrete
  False
  >>> sp.concrete = True
  >>> sp.concrete
  True

- item, attributes
  >>> sp = Species()
  >>> sp['key'] = 'value'
  >>> sp['key']
  'value'
  >>> sp['key_2'] = 'value_2'
  >>> sp['key_3'] = 'value_3'
  >>> sp.attributes == {'key':'value', 'key_2':'value_2', 'key_3':'value_3'}
  True

- entities
  >>> sp = Species()
  >>> sp.entities
  {}

- add_entity
  >>> sp = Species()
  >>> en_a = sp.add_entity(entity_types[0])
  >>> en_b = sp.add_entity(entity_types[1])
  >>> sp.entities == {1:en_a, 2:en_b}
  True

- bindings
  >>> sp = Species()
  >>> sp.bindings
  {}

- add_bindings
  >>> sp = Species()
  >>> en_a = sp.add_entity(entity_types[0])
  >>> c_a_1 = en_a.components[1]
  >>> c_a_2 = en_a.components[2]
  >>> en_b = sp.add_entity(entity_types[1])
  >>> c_b_1 = en_b.components[1]
  >>> c_b_2 = en_b.components[2]
  >>> b_1 = sp.add_binding(c_a_2, c_b_1)
  >>> sp.bindings == {1: b_1}
  True
  >>> b_2 = sp.add_binding(c_b_2, c_a_1)
  >>> sp.bindings == {1: b_1, 2: b_2}
  True

- remove_binding
  >>> sp_2 = Species()
  >>> sp_2.remove_binding(b_1)
  Traceback (most recent call last):
  AssertionError
  >>> sp.remove_binding(b_2)
  >>> sp.bindings == {1: b_1}
  True
  >>> sp.remove_binding(b_1)
  >>> sp.bindings == {}
  True

- add_elements
  >>> entity_list = []
  >>> binding_list = []
  >>> sp = Species()
  >>> en = sp.add_entity(entity_types[0])
  >>> entity_list.append(en)
  >>> sp = Species()
  >>> en_a = sp.add_entity(entity_types[0])
  >>> entity_list.append(en_a)
  >>> en_b = sp.add_entity(entity_types[1])
  >>> entity_list.append(en_b)
  >>> c_a_1 = en_a.components[1]
  >>> c_a_2 = en_a.components[2]
  >>> c_b_1 = en_b.components[1]
  >>> c_b_2 = en_b.components[2]
  >>> b = sp.add_binding(c_a_2, c_b_1)
  >>> binding_list.append(b)
  >>> sp = Species()
  >>> sp.add_elements(entity_list, binding_list)
  >>> sp.entities == {1: en, 2: en_a, 3: en_b}
  True
  >>> sp.bindings == {1: b}
  True

- str_simple, str
  >>> sp = Species()
  >>> sp.str_simple()
  ''
  >>> en_a = sp.add_entity(entity_types[0])
  >>> c_a_1 = en_a.components[1]
  >>> c_a_2 = en_a.components[2]
  >>> en_b = sp.add_entity(entity_types[1])
  >>> c_b_1 = en_b.components[1]
  >>> c_b_2 = en_b.components[2]
  >>> b_1 = sp.add_binding(c_a_2, c_b_1)
  >>> b_2 = sp.add_binding(c_b_2, c_a_1)
  >>> c_a_1.set_state('p', 'U')
  >>> c_a_1.set_state('p', 'P')
  >>> c_a_1.binding_state = BINDING_SPECIFIED
  >>> c_a_2.binding_state = BINDING_SPECIFIED
  >>> c_b_1.binding_state = BINDING_SPECIFIED
  >>> c_b_2.binding_state = BINDING_SPECIFIED
  >>> en = sp.add_entity(entity_types[0])
  >>> sp.str_simple()
  'A(r(P)[2],d[1]).B(r(?)[1],d[2]).A(r(?)[?],d[?])'
