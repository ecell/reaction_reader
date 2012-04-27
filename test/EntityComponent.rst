setup
  >>> from model.EntityComponent import EntityComponent
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> from model.Binding import Binding
  >>> from model.general_func import *
  >>> p_state = StateType('phosphorylation', ['U', 'P'])
  >>> a_state = StateType('phosphorylation', ['U', 'A'])
  >>> entity_type_a = EntityType('A')
  >>> comp_a = entity_type_a.add_component('r', {'p': p_state})
  >>> entity_type_b = EntityType('B')
  >>> comp_b = entity_type_b.add_component('r', {'p': p_state, 'a': a_state})
  >>> species = Species()
  >>> entity = Entity(1, entity_type_a, species)
  >>> species = Species()
  >>> entity_2 = Entity(1, entity_type_b, species)
  >>> species = Species()
  >>> entity_3 = Entity(1, entity_type_a, species)
  >>> species = Species()
  >>> entity_4 = Entity(1, entity_type_b, species)
  >>> component = comp_a
  >>> component_2 = comp_b
  >>> component_3 = comp_a
  >>> component_4 = comp_b

- init
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp = EntityComponent(component,entity,key_1='value_1',key_2='value_2')
  >>> en_comp['key_1']
  'value_1'
  >>> en_comp['key_2']
  'value_2'

- component
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.component == component
  True

- id
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.id == component.id
  True

- name
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.name == component.name
  True

- state_types
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.state_types == component.state_types
  True

- entity
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.entity == entity
  True

- set_state
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('a', 'U')
  Traceback (most recent call last):
  AssertionError
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'Q')
  Traceback (most recent call last):
  AssertionError
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.states == {'p': 1}
  True
  >>> en_comp = EntityComponent(component_2, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.set_state('a', 'A')
  >>> en_comp.states == {'p': 0, 'a': 1}
  True

- states
  >>> 
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.states == {'p': STATE_UNSPECIFIED}
  True
  >>> en_comp = EntityComponent(component_2, entity)
  >>> en_comp.states == {'p': STATE_UNSPECIFIED, 'a': STATE_UNSPECIFIED}
  True

- getbinding_state
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.binding_state == BINDING_UNSPECIFIED
  True

- setbinding_state
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp.binding_state == BINDING_NONE
  True

- getbinding
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.binding == None
  True

- setbinding
  >>> en_comp = EntityComponent(component, entity)
  >>> b = Binding(1, None, en_comp, None, True)
  >>> en_comp.binding = b
  >>> en_comp.binding == b
  True

- item
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp['key'] = 'value'
  >>> en_comp['key'] == 'value'
  True
  >>> en_comp['aaa'] == None
  True

- attributes
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp['key_1'] = 'value_1'
  >>> en_comp['key_2'] = 'value_2'
  >>> en_comp['key_3'] = 'value_3'
  >>> en_comp.attributes == {'key_1':'value_1','key_2':'value_2','key_3':'value_3'}
  True

- str
  >>> en_comp = EntityComponent(component, entity)
  >>> str(en_comp)
  "EntityComponent(id=1, name='r', states={'p': '?'}, binding_state='unspecified')"

- str_simple
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.binding_state = BINDING_SPECIFIED
  >>> b = Binding(2, None, en_comp, None, True)
  >>> en_comp.binding = b
  >>> en_comp.str_simple()
  'r(P)[2]'

- is_specific
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_UNSPECIFIED
  >>> en_comp.is_specific()
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_ANY
  >>> en_comp.is_specific()
  False
  >>> en_comp = EntityComponent(component_2, entity_2)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.set_state('a', 'A')
  >>> en_comp.binding_state = BINDING_UNSPECIFIED
  >>> en_comp.is_specific()
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp.is_specific()
  False
  >>> en_comp = EntityComponent(component_2, entity_2)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.set_state('a', STATE_UNSPECIFIED_STRING)
  >>> en_comp.binding_state = BINDING_UNSPECIFIED
  >>> en_comp.is_specific()
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp.is_specific()
  True
  >>> en_comp = EntityComponent(component_2, entity_2)
  >>> en_comp.set_state('p', 'P')
  >>> en_comp.set_state('a', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp.is_specific()
  True

- is_more_specific
  >>> entity_type = EntityType('A')
  >>> comp = entity_type.add_component('d')
  >>> species = Species()
  >>> entity = Entity(1, entity_type, species)
  >>> en_comp_other = EntityComponent(comp, entity)
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.is_more_specific(en_comp_other)
  Traceback (most recent call last):
  AssertionError
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_UNSPECIFIED
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_state = BINDING_NONE
  >>> en_comp.is_more_specific(en_comp_other)
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_state = BINDING_UNSPECIFIED
  >>> en_comp.is_more_specific(en_comp_other)
  True

- matches
  >>> entity_type = EntityType('A')
  >>> comp = entity_type.add_component('d')
  >>> species = Species()
  >>> entity = Entity(1, entity_type, species)
  >>> en_comp_other = EntityComponent(comp, entity)
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.matches(en_comp_other)
  Traceback (most recent call last):
  AssertionError
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'P')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> en_comp.matches(en_comp_other)
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'P')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> en_comp.matches(en_comp_other)
  False
  >>> en_comp = EntityComponent(component_2, entity_2)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.set_state('a', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_4, entity_4)
  >>> en_comp_other.set_state('p', 'P')
  >>> en_comp_other.set_state('a', 'U')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> en_comp.matches(en_comp_other)
  False
  >>> en_comp = EntityComponent(component_2, entity_2)
  >>> en_comp.set_state('p', STATE_UNSPECIFIED_STRING)
  >>> en_comp.set_state('a', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_4, entity_4)
  >>> en_comp_other.set_state('p', 'P')
  >>> en_comp_other.set_state('a', 'U')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> en_comp.matches(en_comp_other)
  False
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> en_comp.matches(en_comp_other)
  True
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_SPECIFIED
  >>> b = Binding(1, None, en_comp, None, False)
  >>> en_comp.binding = b
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_stte = BINDING_NONE
  >>> b = Binding(1, None, en_comp_other, None, False)
  >>> en_comp.binding = b
  >>> en_comp.matches(en_comp_other)
  True
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_NONE
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_stte = BINDING_UNSPECIFIED
  >>> en_comp.matches(en_comp_other)
  True
  >>> en_comp = EntityComponent(component, entity)
  >>> en_comp.set_state('p', 'U')
  >>> en_comp.binding_state = BINDING_SPECIFIED
  >>> b = Binding(1, None, en_comp, None, False)
  >>> en_comp.binding = b
  >>> en_comp_other = EntityComponent(component_3, entity_3)
  >>> en_comp_other.set_state('p', 'U')
  >>> en_comp_other.binding_stte = BINDING_UNSPECIFIED
  >>> en_comp.matches(en_comp_other)
  True
