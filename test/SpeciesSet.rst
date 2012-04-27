- setup
  >>> from model.SpeciesSet import SpeciesSet
  >>> from model.Model import Model
  >>> from model.parser import Parser
  >>> from model.general_func import *

  >>> m = Model()
  >>> entity_type_L = m.add_entity_type('L')
  >>> comp_r_L = entity_type_L.add_component('r')
  >>> entity_type_R = m.add_entity_type('R')
  >>> comp_l_R = entity_type_R.add_component('l')
  >>> entity_type_A = m.add_entity_type('A')
  >>> comp_a_A = entity_type_A.add_component('a')

  >>> p = Parser()
  >>> p.add_entity_type(entity_type_L)
  >>> p.add_entity_type(entity_type_R)
  >>> p.add_entity_type(entity_type_A)

  >>> sp_text = 'L(r)'
  >>> s_l = p.parse_species(sp_text)
  >>> sp_text = 'R(l)'
  >>> s_r = p.parse_species(sp_text)
  >>> sp_text = 'A(a)'
  >>> s_a = p.parse_species(sp_text)

- init
  >>> o = SpeciesSet(m)
  >>> type(o)
  <class 'model.SpeciesSet.SpeciesSet'>

- species, serial_species
  >>> o = SpeciesSet(m)
  >>> o.species
  []
  >>> o.serial_species
  0

- add_species
  >>> o = SpeciesSet(m)
  >>> o.add_species(s_l)
  >>> o.species[0].equals(s_l)
  True
  >>> o.serial_species
  1

  >>> m.species

- __gt__1
  >>> o = SpeciesSet(m)
  >>> o.add_species(s_l)
  >>> rule = o > s_r
  Traceback (most recent call last):
  Error: Incomplete reaction rule.

- __gt__2
  >>> o1 = SpeciesSet(m)
  >>> o1.add_species(s_l)
  >>> o1.add_species(s_r)
  >>> o2 = SpeciesSet(m)
  >>> o2.add_species(s_a)

  >>> rule = o1 > o2
  >>> type(rule)
  <class 'model.ReactionRule.ReactionRule'>
  >>> rule.str_simple()
  'L(r) + R(l) > A(a)'
  >>> rule == m.reaction_rules[1]
  True

- str_simple()
  >>> o = SpeciesSet(m)
  >>> o.add_species(s_l)
  >>> o.add_species(s_r)
  >>> o.str_simple()
  ['L(r)', 'R(l)']
