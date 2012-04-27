- setup
  >>> from model.Entity import Entity
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
  >>> from model.Species import Species
  >>> from model.Binding import Binding
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
  >>> p = Parser()
  >>> p.add_entity_type(entity_type_a)
  >>> p.add_entity_type(entity_type_b)
  >>> p.add_entity_type(entity_type_c)
  >>> p.add_entity_type(entity_type_d)
  >>> species = Species()
  >>> entity_a = species.add_entity(entity_type_a)
  >>> entity_b = species.add_entity(entity_type_b)

- init
  >>> en = Entity(1, entity_type_a, species)
  >>> en = Entity(1, entity_type_a, species, key_1='value_1', key_2='value_2')
  >>> en['key_1']
  'value_1'
  >>> en['key_2']
  'value_2'

- getid, setid
  >>> en.id
  1
  >>> en.id = 5
  >>> en.id
  5

- entity_type
  >>> en.entity_type == entity_type_a
  True

- species
  >>> en.species == species
  True

- components
  >>> en.components[1].name
  'r'
  >>> en.components[2].name
  'd'

  - name
  >>> en.name == entity_type_a.name
  True

- getdummy, setdummy
  >>> en.dummy
  False
  >>> en.dummy = True
  >>> en.dummy
  True

- bindings
  >>> en.bindings
  []
  >>> en_a = Entity(1, entity_type_a, species)
  >>> en_b = Entity(2, entity_type_b, species)
  >>> comp_a_1 = en_a.components[1]
  >>> comp_a_2 = en_a.components[2]
  >>> comp_b_1 = en_b.components[1]
  >>> comp_b_2 = en_b.components[2]
  >>> b_1 = Binding(1, species, comp_a_1, comp_b_1, False)
  >>> comp_a_1.binding = b_1
  >>> comp_b_1.binding = b_1
  >>> b_2 = Binding(2, species, comp_a_2, comp_b_2, False)
  >>> comp_a_2.binding = b_2
  >>> comp_b_2.binding = b_2
  >>> b_1 in en_a.bindings
  True
  >>> b_2 in en_a.bindings
  True

- item
  >>> en['key'] = 'value'
  >>> en['key']
  'value'
  >>> en['aaa'] == None
  True

- attributes
  >>> en = Entity(1, entity_type_a, species)
  >>> en['key_1'] = 'value_1'
  >>> en['key_2'] = 'value_2'
  >>> en['key_3'] = 'value_3'
  >>> en.attributes == {'key_1':'value_1','key_2':'value_2','key_3':'value_3'}
  True

- is_specific
  >>> en = Entity(1, entity_type_a, species)
  >>> comp_1 = en.components[1]
  >>> comp_2 = en.components[2]
  >>> comp_1.set_state('p', 'U')
  >>> comp_1.binding_state = BINDING_UNSPECIFIED
  >>> comp_2.binding_satte = BINDING_NONE
  >>> en.is_specific()
  False
  >>> comp_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_1.binding_state = BINDING_NONE
  >>> comp_2.binding_state = BINDING_NONE
  >>> en.is_specific()
  False
  >>> comp_1.set_state('p', 'U')
  >>> comp_1.binding_state = BINDING_NONE
  >>> comp_2.binding_state = BINDING_NONE
  >>> en.is_specific()
  True

- is_more_specific
  >>> en_a = Entity(1, entity_type_a, species)
  >>> en_b = Entity(2, entity_type_b, species)
  >>> comp_a_1 = en_a.components[1]
  >>> comp_a_2 = en_a.components[2]
  >>> comp_b_1 = en_b.components[1]
  >>> comp_b_2 = en_b.components[2]
  >>> comp_a_1.set_state('p', 'U')
  >>> comp_a_1.binding_state = BINDING_NONE
  >>> comp_a_2.binding_state = BINDING_NONE
  >>> comp_b_1.set_state('p', 'U')
  >>> comp_b_1.binding_state = BINDING_NONE
  >>> comp_b_2.binding_state = BINDING_NONE
  >>> en_a.is_more_specific(en_b)
  Traceback (most recent call last):
  AssertionError
  >>> en_a = Entity(1, entity_type_a, species)
  >>> en_b = Entity(1, entity_type_a, species)
  >>> comp_a_1 = en_a.components[1]
  >>> comp_a_2 = en_a.components[2]
  >>> comp_b_1 = en_b.components[1]
  >>> comp_b_2 = en_b.components[2]
  >>> comp_a_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_a_1.binding_state = BINDING_NONE
  >>> comp_a_2.binding_state = BINDING_NONE
  >>> comp_b_1.set_state('p', 'U')
  >>> comp_b_1.binding_state = BINDING_NONE
  >>> comp_b_2.binding_state = BINDING_NONE
  >>> en_a.is_more_specific(en_b)
  False
  >>> comp_a_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_a_1.binding_state = BINDING_NONE
  >>> comp_a_2.binding_state = BINDING_ANY
  >>> comp_b_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_b_1.binding_state = BINDING_NONE
  >>> comp_b_2.binding_state = BINDING_ANY
  >>> en_a.is_more_specific(en_b)
  True

- matches
  >>> en_a = Entity(1, entity_type_a, species)
  >>> en_b = Entity(1, entity_type_b, species)
  >>> comp_a_1 = en_a.components[1]
  >>> comp_a_2 = en_a.components[2]
  >>> comp_b_1 = en_b.components[1]
  >>> comp_b_2 = en_b.components[2]
  >>> comp_a_1.set_state('p', 'U')
  >>> comp_a_1.binding_state = BINDING_NONE
  >>> comp_a_2.binding_state = BINDING_NONE
  >>> comp_b_1.set_state('p', 'U')
  >>> comp_b_1.binding_state = BINDING_NONE
  >>> comp_b_2.binding_state = BINDING_NONE
  >>> en_a.matches(en_b)
  False
  >>> en_c = Entity(1, entity_type_a, species)
  >>> comp_c_1 = en_c.components[1]
  >>> comp_c_2 = en_c.components[2]
  >>> comp_c_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_c_1.binding_state = BINDING_NONE
  >>> comp_c_2.binding_state = BINDING_ANY
  >>> en_a.matches(en_c)
  False
  >>> en_d = Entity(1, entity_type_a, species)
  >>> comp_d_1 = en_d.components[1]
  >>> comp_d_2 = en_d.components[2]
  >>> comp_d_1.set_state('p', 'U')
  >>> comp_d_1.binding_state = BINDING_NONE
  >>> comp_d_2.binding_state = BINDING_SPECIFIED
  >>> comp_d_2.binding = Binding(1, species, comp_d_2, None, False)
  >>> en_d.matches(en_c)
  True
  
- str_simple
  >>> en = Entity(1, entity_type_a, species)
  >>> comp_1 = en.components[1]
  >>> comp_2 = en.components[2]
  >>> comp_1.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> comp_1.binding_state = BINDING_SPECIFIED
  >>> comp_2.binding_state = BINDING_ANY
  >>> en.str_simple()
  'A(r(?)[],d[+])'

  - str
  >>> str(en)
  "Entity(id=1, entity_type='A', components={EntityComponent(id=1, name='r', states={'p': '?'}, binding_state='specified'), EntityComponent(id=2, name='d', binding_state='exists')}, dummy=False, attrs={})"

