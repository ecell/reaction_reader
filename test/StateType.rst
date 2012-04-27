- setup
  >>> from model.StateType import StateType

- init
  >>> x = StateType('name', [])
  Traceback (most recent call last):
  AssertionError
  >>> x2 = StateType('name', ['U', 'P', 'P'])
  Traceback (most recent call last):
  AssertionError
  >>> o = StateType('name', ['U', 'P', 'A'])
  >>> o2 = StateType('name', ['U', 'P', 'A'], key_1 = 'value_1', 
  ... key_2 = 'value_2', key_3 = 'value_3')
  >>> o2['key_1'], o2['key_2'], o2['key_3']
  ('value_1', 'value_2', 'value_3')

- name, states
  >>> o2.name, o2.states
  ('name', ['U', 'P', 'A'])

- state_index
  >>> o2.state_index('Q')
  Traceback (most recent call last):
  AssertionError
  >>> o2.state_index('U'), o2.state_index('P'), o2.state_index('A')
  (0, 1, 2)

- item
  >>> o2['key'] = 'value'
  >>> o2['key']
  'value'
  >>> o2['aaa'] == None
  True

- attributes
  >>> o3 = StateType('name', ['U', 'P', 'A'])
  >>> o3['key_1'] = 'value_1'
  >>> o3['key_2'] = 'value_2'
  >>> o3['key_3'] = 'value_3'
  >>> o3.attributes == {'key_1':'value_1','key_2':'value_2','key_3': 'value_3'}
  True

- str
  >>> str(StateType('name', ['U', 'P', 'A']))
  "['U', 'P', 'A']"
