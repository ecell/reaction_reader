----------
Condition  
----------

- setup
  >>> from model.Condition import *

- satisfies
  >>> Condition().satisfies(1)
  Traceback (most recent call last):
  Error: Not implemented.

-------------
AndCondition
-------------

- setup
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
  >>> from model.general_func import *
  >>> from model.Model import Model

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

- init
  >>> AndCondition([])
  Traceback (most recent call last):
  AssertionError
  >>> cond1 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> cond2 = IncludingEntityCondition(PRODUCTS, 1, entity_type_b)
  >>> cond = AndCondition([cond1])

- satisfies
  >>> m = Model()
  >>> sp_1 = m.register_species(p.parse_species('A(r~U)'))
  >>> sp_2 = m.register_species(p.parse_species('B(r~U)'))
  >>> sp_3 = m.register_species(p.parse_species('A(r~U!1).B(r~U!1)'))
  >>> cond = AndCondition([cond1, cond2])
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> cond.satisfies(rule)
  True
  >>> m = Model()
  >>> cond1 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> cond2 = IncludingEntityCondition(PRODUCTS, 1, entity_type_c)
  >>> c_1 = AndCondition([cond1, cond2])
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> c_1.satisfies(rule)
  False

- eq
  >>> c_2 = AndCondition([cond1, cond2])
  >>> c_1 == c_2
  True
  >>> cond != c_2
  True
  >>> c_3 = AndCondition([cond1, cond2])
  >>> c_1 != c_3
  True

- str
  >>> str(cond)
  '(include_reactants(1,A)) and (include_products(1,B))'

-------------
OrCondition
-------------

- setup
  >>> m = Model()

- init
  >>> OrCondition([])
  Traceback (most recent call last):
  AssertionError
  >>> cond1 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> cond2 = IncludingEntityCondition(PRODUCTS, 1, entity_type_c)
  >>> cond = OrCondition([cond1])

- satisfies
  >>> sp_1 = m.register_species(p.parse_species('A(r~U)'))
  >>> sp_2 = m.register_species(p.parse_species('B(r~U)'))
  >>> sp_3 = m.register_species(p.parse_species('A(r~U!1).B(r~U!1)'))
  >>> cond = OrCondition([cond1, cond2])
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> cond.satisfies(rule)
  True
  >>> m = Model()
  >>> cond1 = IncludingEntityCondition(REACTANTS, 1, entity_type_c)
  >>> cond2 = IncludingEntityCondition(PRODUCTS, 1, entity_type_d)
  >>> c_1 = OrCondition([cond1, cond2])
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> c_1.satisfies(rule)
  False

- eq
  >>> c_2 = OrCondition([cond1, cond2])
  >>> c_1 == c_2
  True
  >>> cond != c_2
  True
  >>> c_3 = AndCondition([cond1, cond2])
  >>> c_1 != c_3
  True

- str
  >>> str(cond)
  '(include_reactants(1,A)) or (include_products(1,C))'

-------------
NotCondition
-------------

- init
  >>> cond = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> o = NotCondition([cond])

- safisfies
  >>> m = Model()
  >>> sp_1 = m.register_species(p.parse_species('A(r~U)'))
  >>> sp_2 = m.register_species(p.parse_species('B(r~U)'))
  >>> sp_3 = m.register_species(p.parse_species('A(r~U!1).B(r~U!1)'))
  >>> cond_1 = IncludingEntityCondition(REACTANTS, 1, entity_type_c)
  >>> cond = NotCondition(cond_1)
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> cond.satisfies(rule)
  True

- str
  >>> str(cond)
  'not (include_reactants(1,C))'

- eq
  >>> m2 = Model()
  >>> cond_1 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> c_1 = NotCondition(cond_1)
  >>> rule = m2.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> c_1.satisfies(rule)
  False
  >>> cond_2 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> c_2 = NotCondition(cond_2)
  >>> c_1 == c_2
  True
  >>> cond_3 = IncludingEntityCondition(PRODUCTS, 1, entity_type_a)
  >>> c_3 = NotCondition(cond_3)
  >>> c_1 != c_3
  True
  >>> cond_4 = IncludingEntityCondition(PRODUCTS, 1, entity_type_a)
  >>> c_4 = cond_4
  >>> c_1 != c_4
  True

-------------------------
IncludingEntityCondition
-------------------------

- setup

- init
  >>> IncludingEntityCondition(0, 1, entity_type_a)
  Traceback (most recent call last):
  AssertionError
  >>> IncludingEntityCondition(REACTANTS, 0, entity_type_a)
  Traceback (most recent call last):
  AssertionError

- side
  >>> o = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> o.side == REACTANTS
  True

- index
  >>> index = 3
  >>> o2 = IncludingEntityCondition(REACTANTS, index, entity_type_a)
  >>> o2.index == index - 1
  True

- entity_type
  >>> o.entity_type == entity_type_a
  True

- eq
  >>> o != IncludingEntityCondition(PRODUCTS, 1, entity_type_a)
  True
  >>> o != IncludingEntityCondition(REACTANTS, 2, entity_type_a)
  True
  >>> o != IncludingEntityCondition(REACTANTS, 1, entity_type_b)
  True

- satisfies
  >>> rule_text = 'A(r~U,d) + B(r~U,d) -> A(r~U,d!1).B(r~U,d!1)'
  >>> rule = p.parse_reaction(rule_text, m)
  >>> o3 = IncludingEntityCondition(REACTANTS, 3, entity_type_a)
  >>> o3.satisfies(rule)
  Traceback (most recent call last):
  AssertionError
  >>> o3 = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> o3.satisfies(rule)
  True
  >>> o3 = IncludingEntityCondition(REACTANTS, 2, entity_type_a)
  >>> o3.satisfies(rule)
  False
  >>> o3 = IncludingEntityCondition(PRODUCTS, 1, entity_type_a)
  >>> o3.satisfies(rule)
  True

- str
  >>> str(o3)
  'include_products(1,A)'
