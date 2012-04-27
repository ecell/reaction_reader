- setup
  >>> from model.Model import Model
  >>> from model.parser import Parser
  >>> from model.Binding import Binding
  >>> from model.Condition import Condition
  >>> from model.Component import Component
  >>> from model.Correspondence import Correspondence
  >>> from model.Entity import Entity
  >>> from model.EntityComponent import EntityComponent
  >>> from model.EntityType import EntityType
  >>> from model.Pair import Pair
  >>> from model.ReactionRule import ReactionRule
  >>> from model.ReactionResult import ReactionResult
  >>> from model.StateType import StateType
  >>> from model.general_func import *
  >>> from model.Condition import IncludingEntityCondition, AndCondition

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

- init
  >>> m = Model()
  >>> m = Model(key_1='value_1', key_2='value_2')
  >>> m['key_1'], m['key_2']
  ('value_1', 'value_2')

- getdisallow_implicit_disappearance, setdisallow_implicit_disappearance
  >>> m = Model()
  >>> m.disallow_implicit_disappearance
  True
  >>> m.disallow_implicit_disappearance = False
  >>> m.disallow_implicit_disappearance
  False

- item
  >>> m = Model()
  >>> m['key'] = 'value'
  >>> m['key']
  'value'
  >>> m['aaa'] == None
  True

- attributes
  >>> m = Model()
  >>> m['key_1'] = 'value_1'
  >>> m['key_2'] = 'value_2'
  >>> m['key_3'] = 'value_3'
  >>> m.attributes == {'key_1':'value_1','key_2':'value_2','key_3':'value_3'}
  True

- add_state_types
  >>> m = Model()
  >>> p_state = m.add_state_type('phosphorylation', ['U', 'P'])
  >>> p_state.name, p_state.states
  ('phosphorylation', ['U', 'P'])

- state_types
  >>> m = Model()
  >>> m.state_types
  {}
  >>> m = Model()
  >>> p_state = m.add_state_type('phosphorylation', ['U', 'P'])
  >>> a_state = m.add_state_type('acetylation', ['U', 'A'])
  >>> state_types = m.state_types
  >>> len(state_types)
  2
  >>> state_types['phosphorylation'] == p_state
  True
  >>> state_types['acetylation'] == a_state
  True

- add_entity_type
  >>> m = Model()
  >>> entity_type = m.add_entity_type('A')
  >>> entity_type.name
  'A'
  >>> m.add_entity_type('A')
  Traceback (most recent call last):
  AssertionError

- entity_types
  >>> m = Model()
  >>> m.entity_types
  {}
  >>> ent_type_a = m.add_entity_type('A')
  >>> ent_type_b = m.add_entity_type('B')
  >>> entity_types = m.entity_types
  >>> len(entity_types)
  2
  >>> entity_types['A'] == ent_type_a
  True
  >>> entity_types['B'] == ent_type_b
  True

- register_species
  >>> m = Model()
  >>> sp = parser.parse_species('A(r~U!1,d).B(r~U!1,d).A(r~P,d)')
  >>> reg_sp = m.register_species(sp)
  >>> reg_sp.concrete
  False
  >>> sp = parser.parse_species('A(r~U!1,d).B(r~U!1,d!2).A(r~P,d!2)')
  >>> reg_sp = m.register_species(sp)
  >>> reg_sp.concrete
  True
  >>> m = Model()
  >>> sp = parser.parse_species('A(r~U,d)')
  >>> o = m.register_species(sp)
  >>> sp = parser.parse_species('A(r~P,d)')
  >>> sp_old = m.register_species(sp)
  >>> sp = parser.parse_species('A(r~P!1,d).B(r~U!1,d)')
  >>> o = m.register_species(sp)
  >>> sp = parser.parse_species('A(r~P,d)')
  >>> reg_sp = sp_old = m.register_species(sp)
  >>> reg_sp == sp_old
  True

- species
  >>> m = Model()
  >>> m.species
  {}
  >>> sp_1 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_2 = m.register_species(parser.parse_species('A(r~P,d)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~P!1,d).B(r~U!1,d)'))
  >>> m.species == {1: sp_1, 2: sp_2, 3: sp_3}
  True

- concrete_species
  >>> m = Model()
  >>> m.concrete_species
  {}
  >>> sp_1 = m.register_species(parser.parse_species('A(r~?,d)'))
  >>> sp_2 = m.register_species(parser.parse_species('A(r~P,d).B(r~U,d)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> m.concrete_species == {3: sp_3}
  True
  
- add_reaction_rule
  >>> m = Model()
  >>> sp_1 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_2 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> rule.reactants == [sp_1, sp_2]
  True
  >>> rule.products == [sp_3]
  True
  >>> cond = IncludingEntityCondition(REACTANTS, 1, entity_type_a)
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3], cond)
  >>> rule.condition == cond
  True
  >>> cond_2 = IncludingEntityCondition(REACTANTS, 2, entity_type_b)
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3], [cond, cond_2])
  >>> rule.condition == AndCondition([cond, cond_2])
  True
  >>> m = Model()
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3], key_1='value_1')
  >>> rule['key_1']
  'value_1'

- add_concrete_reaction
  >>> m = Model()
  >>> sp_1 = m.register_species(parser.parse_species('A(r~?)'))
  >>> sp_2 = m.register_species(parser.parse_species('B(r~?)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~?!1).B(r~?!1)'))
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> sp_4 = m.register_species(parser.parse_species('A(r~?,d)'))
  >>> sp_5 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_6 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> m.add_concrete_reaction(rule, [sp_4, sp_5], [sp_6])
  Traceback (most recent call last):
  AssertionError
  >>> sp_4 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_5 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_6 = m.register_species(parser.parse_species('A(r~U,d).B(r~U,d)'))
  >>> m.add_concrete_reaction(rule, [sp_4, sp_5], [sp_6])
  Traceback (most recent call last):
  AssertionError
  >>> sp_4 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_5 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_6 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> reaction = m.add_concrete_reaction(rule, [sp_4, sp_5], [sp_6])

- reaction_results, concrete_reactions
  >>> m = Model()
  >>> m.reaction_results
  {}
  >>> m.concrete_reactions
  []
  >>> sp_1 = m.register_species(parser.parse_species('A(r~?)'))
  >>> sp_2 = m.register_species(parser.parse_species('B(r~?)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~?!1).B(r~?!1)'))
  >>> rule = m.add_reaction_rule([sp_1, sp_2], [sp_3])
  >>> sp_4 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_5 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_6 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> reaction = m.add_concrete_reaction(rule, [sp_4, sp_5], [sp_6])
  >>> results = m.reaction_results
  >>> len(results)
  1
  >>> result = results[1]
  >>> result.reaction_rule == rule
  True
  >>> result.reactions == [reaction]
  True
  >>> m.concrete_reactions == [reaction]
  True

- generate_reactions
  >>> m = Model()
  >>> rule_text = 'A(d) + B(d) -> A(d!1).B(d!1)'
  >>> rule_1 = parser.parse_reaction(rule_text, m, register=True)
  >>> rule_text = 'A(d!1).B(d!1) -> A(d) + B(d)'
  >>> rule_2 = parser.parse_reaction(rule_text, m, register=True)
  >>> sp_str_list = ['A(r~U,d)', 'C(r~U,d)']
  >>> sp_list = parser.parse_species_array(sp_str_list, m)
  >>> results = m.generate_reactions(sp_list)
  >>> results
  []
  >>> sp_str_list = ['A(r~U,d)', 'C(r~U,d)', 'B(r~U,d)']
  >>> sp_list = parser.parse_species_array(sp_str_list, m)
  >>> results = m.generate_reactions(sp_list)
  >>> len(results)
  1
  >>> r = results[0]
  >>> rule_text = 'A(r~U,d) + B(r~U,d) -> A(r~U,d!1).B(r~U,d!1)'
  >>> reaction = parser.parse_reaction(rule_text, m)
  >>> len(r.reactions)
  1
  >>> r.reactions[0].equals(reaction)
  True

- generate_reaction_network
  >>> m = Model()
  >>> rule_text = 'A(d) + B(d) -> A(d!1).B(d!1)'
  >>> rule_1 = parser.parse_reaction(rule_text, m, register=True)
  >>> rule_text = 'A(d!1).B(d!1) -> A(d) + B(d)'
  >>> rule_2 = parser.parse_reaction(rule_text, m, register=True)
  >>> sp_str_list = ['A(r~U,d)', 'B(r~U,d)', 'C(r~U,d)']
  >>> sp_list = parser.parse_species_array(sp_str_list, m)
  >>> m.generate_reaction_network(sp_list, 0)
  Traceback (most recent call last):
  AssertionError
  >>> results = m.generate_reaction_network(sp_list, 10)
  >>> len(results)
  2
  >>> r_1 = results[0]
  >>> rule_text = 'A(r~U,d) + B(r~U,d) -> A(r~U,d!1).B(r~U,d!1)'
  >>> reaction = parser.parse_reaction(rule_text, m)
  >>> len(r_1.reactions)
  1
  >>> r_1.reactions[0].equals(reaction)
  True
  >>> r_2 = results[1]
  >>> rule_text = 'A(r~U,d!1).B(r~U,d!1) -> A(r~U,d) + B(r~U,d)'
  >>> reaction = parser.parse_reaction(rule_text, m)
  >>> len(r_2.reactions)
  1
  >>> r_2.reactions[0].equals(reaction)
  True
