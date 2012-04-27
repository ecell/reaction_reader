- setup

  >>> from model.EntityType import EntityType
  >>> from model.Component import Component
  >>> from model.StateType import StateType
  >>> p_state = StateType('phosphorylation', ['U', 'P'])
  >>> a_state = StateType('acetylation', ['U', 'A'])
  >>> states = {'p': p_state, 'a': a_state}

- init
  >>> o = EntityType('name')
  >>> o2 = EntityType('name', key_1='value_1', key_2='value_2', key_3='value_3')
  >>> o2['key_1'], o2['key_2'], o2['key_3']
  ('value_1', 'value_2', 'value_3')

- name
  >>> o.name
  'name'

- components
  >>> o3 = EntityType('A')
  >>> o3.components
  {}

- add_components
  >>> comp = o3.add_component('d')
  >>> comp in o3.components.values()
  True
  >>> comp2 = o3.add_component('Y', states)
  >>> comp2 in o3.components.values()
  True

- find_components
  >>> o3.find_components('d') == [comp]
  True
  >>> o3.find_components('x')
  []

- item
  >>> o3['key'] = 'value'
  >>> o3['key']
  'value'
  >>> o3['aaa'] == None
  True

- attributes
  >>> o3['key_2'] = 'value_2'
  >>> o3['key_3'] = 'value_3'
  >>> o3.attributes == {'key': 'value', 'key_2': 'value_2', 'key_3': 'value_3'}
  True

- str
  >>> str(o)
  "EntityType(name='name', components={}, attrs={})"
