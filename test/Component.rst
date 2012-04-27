- setup
  >>> from model.StateType import StateType
  >>> from model.Component import Component
  >>> p_state = StateType('phosphorylation', ['U', 'P'])
  >>> a_state = StateType('acetylation', ['U', 'A'])
  >>> states = {'p': p_state, 'a': a_state}

- init
  >>> o = Component(1, 'name')
  >>> o2 = Component(1, 'name', states)
  >>> o2.state_types == states
  True

  >>> o3 = Component(1, 'name', key_1 = 'value_1', key_2 = 'value_2',
  ... key_3 = 'value_3')
  >>> o3['key_1'], o3['key_2'], o3['key_3']
  ('value_1', 'value_2', 'value_3')

  >>> o4 = Component(1, 'name', states, key_1 = 'value_1', key_2 = 'value_2',
  ... key_3 = 'value_3')
  >>> o4.state_types == states
  True

  >>> o4['key_1'], o4['key_2'],  o4['key_3']
  ('value_1', 'value_2', 'value_3')

- id, name, state_types
  >>> o.id, o.name, o.state_types
  (1, 'name', {})

- item
  >>> o['key'] = 'value'
  >>> o['key']
  'value'
  >>> o['aaa'] == None
  True

- attributes
  >>> o4.attributes == {'key_1': 'value_1', 'key_2': 'value_2',
  ... 'key_3': 'value_3'}
  True

- str
  >>> str(o2)
  "Component(id=1, name='name', state_types={'a': ['U', 'A'], 'p': ['U', 'P']}, attrs={})"

