- setUp
  >>> from model.ReactionResult import ReactionResult
  >>> from model.StateType import StateType
  >>> from model.EntityType import EntityType
  >>> from model.parser import Parser
  >>> from model.general_func import *
  >>> from model.Model import Model
  >>> from model.ReactionRule import ReactionRule

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


- init, reaction_rule
  >>> m = Model()
  >>> sp_1 = m.register_species(parser.parse_species('A(r~U)'))
  >>> sp_2 = m.register_species(parser.parse_species('B(r~U)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~U!1).B(r~U!1)'))
  >>> rule = ReactionRule(1, m, [sp_1, sp_2], [sp_3], False)
  >>> result = ReactionResult(rule)
  >>> result.reaction_rule == rule
  True

- reactions
  >>> m = Model()
  >>> sp_1 = m.register_species(parser.parse_species('A(r~?)'))
  >>> sp_2 = m.register_species(parser.parse_species('B(r~?)'))
  >>> sp_3 = m.register_species(parser.parse_species('A(r~?!1).B(r~?!1)'))
  >>> rule = ReactionRule(1, m, [sp_1, sp_2], [sp_3], False)
  >>> sp_4 = m.register_species(parser.parse_species('A(r~U,d)'))
  >>> sp_5 = m.register_species(parser.parse_species('B(r~U,d)'))
  >>> sp_6 = m.register_species(parser.parse_species('A(r~U!1,d).B(r~U!1,d)'))
  >>> reaction_1 = ReactionRule(2, m, [sp_4, sp_5], [sp_6], True)
  >>> sp_7 = m.register_species(parser.parse_species('A(r~P,d)'))
  >>> sp_8 = m.register_species(parser.parse_species('B(r~P,d)'))
  >>> sp_9 = m.register_species(parser.parse_species('A(r~P!1,d).B(r~P!1,d)'))
  >>> reaction_2 = ReactionRule(3, m, [sp_7, sp_8], [sp_9], True)
  >>> result = ReactionResult(rule)
  >>> result.reactions == []
  True
  >>> result.add_reaction(reaction_1)
  >>> result.add_reaction(reaction_2)
  >>> result.reactions == [reaction_1, reaction_2]
  True

- str
  >>> str(result)
  "[reaction rule='A(r(?),d[?]) + B(r(?),d[?]) > A(r(?)[1],d[?]).B(r(?)[1],d[?])', reactions=[2: 'A(r(U),d) + B(r(U),d) > A(r(U)[1],d).B(r(U)[1],d)', 3: 'A(r(P),d) + B(r(P),d) > A(r(P)[1],d).B(r(P)[1],d)']]"
