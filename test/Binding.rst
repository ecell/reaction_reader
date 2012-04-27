- setup
  >>> from model.Binding import Binding
  >>> from model.Species import Species
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
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
  >>> species = Species()
  >>> entity_a = species.add_entity(entity_type_a)
  >>> entity_b = species.add_entity(entity_type_b)
  >>> entity_c = species.add_entity(entity_type_c)
  >>> entity_d = species.add_entity(entity_type_d)
  >>> comp_r_a = entity_a.components[1]
  >>> comp_d_a = entity_a.components[2]
  >>> comp_r_b = entity_b.components[1]
  >>> comp_d_b = entity_b.components[2]

- init
  >>> b = Binding(1, species, comp_r_a, comp_r_b, False)
  >>> b = Binding(1, species, comp_r_a, comp_r_b, False, key_1='value_1', 
  ... key_2='value_2', key_3='value_3')
  >>> b['key_1']
  'value_1'
  >>> b['key_2']
  'value_2'
  >>> b['key_3']
  'value_3'

- getid, setid
  >>> b.id
  1
  >>> b.id = 2
  >>> b.id
  2

- species
  >>> b.species == species
  True

- component
  >>> b.component_1 == comp_r_a
  True
  >>> b.component_2 == comp_r_b
  True

- entity
  >>> b.entity_1 == entity_a
  True
  >>> b.entity_2 == entity_b
  True

- temporary
  >>> b = Binding(1, species, comp_r_a, comp_r_b, True)
  >>> b.temporary
  True
  >>> b.temporary = False
  >>> b.temporary
  False

- deleted
  >>> b.deleted
  False
  >>> b.deleted = True
  >>> b.deleted
  True

- item
  >>> b['key'] = 'value'
  >>> b['key']
  'value'
  >>> b['aaa'] == None
  True

- attributes
  >>> b['key_2'] = 'value_2'
  >>> b['key_3'] = 'value_3'
  >>> b.attributes == {'key':'value', 'key_2':'value_2', 'key_3':'value_3'}
  True
    
- find_component
  >>> b.find_component(entity_a) == comp_r_a
  True
  >>> b.find_component(entity_b) == comp_r_b
  True
  >>> sp = Species()
  >>> en = sp.add_entity(entity_type_a)
  >>> b.find_component(en) == None
  True

- find_counterpart_entity
  >>> b = Binding(1, species, comp_r_a, comp_r_b, True)
  >>> b.find_counterpart_entity(entity_a) == entity_b
  True
  >>> b.find_counterpart_entity(entity_b) == entity_a
  True
  >>> b.find_counterpart_entity(en) == None
  True

- matches
  >>> sp = Species()
  >>> entity_a_1 = sp.add_entity(entity_type_a)
  >>> entity_a_2 = sp.add_entity(entity_type_a)
  >>> comp_a_1 = entity_a_1.components[1]
  >>> comp_a_2 = entity_a_2.components[1]
  >>> b_1 = Binding(1, sp, comp_a_1, comp_a_2, False)
  >>> sp = Species()
  >>> entity_b_1 = sp.add_entity(entity_type_b)
  >>> entity_b_2 = sp.add_entity(entity_type_b)
  >>> comp_b_1 = entity_b_1.components[1]
  >>> comp_b_2 = entity_b_2.components[1]
  >>> b_2 = Binding(1, sp, comp_b_1, comp_b_2, False)
  >>> b_1.matches(b_2)
  False
  >>> entity_b_1 = sp.add_entity(entity_type_a)
  >>> entity_b_2 = sp.add_entity(entity_type_a)
  >>> comp_b_1 = entity_b_1.components[1]
  >>> comp_b_2 = entity_b_2.components[1]
  >>> b_2 = Binding(1, sp, comp_b_1, comp_b_2, False)
  >>> b_1.matches(b_2)
  True

- str
  >>> sp = Species()
  >>> entity_1 = sp.add_entity(entity_type_a)
  >>> entity_2 = sp.add_entity(entity_type_b)
  >>> comp_1 = entity_1.components[1]
  >>> comp_2 = entity_2.components[2]
  >>> b = Binding(1, sp, comp_1, comp_2, False)
  >>> str(b)
  "Binding(id='1', temporary=False, deleted=False, A(1).r-B(2).d)"
