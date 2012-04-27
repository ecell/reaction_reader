- Setup
  >>> from model.Model import Model
  >>> from model.parser import Parser
  >>> from model.ReactionRule import ReactionRule
  >>> from model.general_func import *
  >>> from model.Condition import IncludingEntityCondition

  >>> m = Model()

  >>> p_state = m.add_state_type('phosphorylation', ['U', 'P'])
  >>> a_state = m.add_state_type('acetylation', ['U', 'A'])

  >>> entity_type_L = m.add_entity_type('L')
  >>> comp_r_L = entity_type_L.add_component('r')

  >>> entity_type_R = m.add_entity_type('R')
  >>> comp_l_R = entity_type_R.add_component('l')
  >>> comp_d_R = entity_type_R.add_component('d')
  >>> comp_Y_R = entity_type_R.add_component('Y', {'p': p_state})

  >>> entity_type_A = m.add_entity_type('A')
  >>> comp_SH2_A = entity_type_A.add_component('SH2')
  >>> comp_Y_A = entity_type_A.add_component('Y', {'p': p_state})

  >>> p = Parser()
  >>> p.add_entity_type(entity_type_L)
  >>> p.add_entity_type(entity_type_R)
  >>> p.add_entity_type(entity_type_A)

- init_1
  >>> sp_text = 'R(l,d,Y~U)'
  >>> sp_r = p.parse_species(sp_text)
  >>> sp_text = 'R(l,d,Y~P)'
  >>> sp_p = p.parse_species(sp_text)
  >>> o = m.register_species(sp_p)
  >>> r = ReactionRule(1, m, [sp_r], [sp_p], False)

- init_2
  >>> sp_text = 'R(l,d,Y~U)'
  >>> sp_r = p.parse_species(sp_text)
  >>> sp_text = 'R(l,d,Y~P)'
  >>> sp_p = p.parse_species(sp_text)
  >>> o = m.register_species(sp_r)
  >>> r = ReactionRule(1, m, [sp_r], [sp_p], False)

- init_3
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~?)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, True)
  Traceback (most recent call last):
  AssertionError

- init_4  
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~?)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, True)
  Traceback (most recent call last):
  AssertionError

- init_5
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp = r_list[1]
  >>> en = sp.entities[1]
  >>> en.components[3].binding_state = BINDING_NONE
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, True)
  Traceback (most recent call last):
  AssertionError

- init_6
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp = r_list[1]
  >>> en = sp.entities[1]
  >>> en.components[3].binding_state = BINDING_NONE
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, False)
  Traceback (most recent call last):
  AssertionError

- init_7
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp = r_list[1]
  >>> en = sp.entities[1]
  >>> en.components[3].binding_state = BINDING_NONE
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, True)
  Traceback (most recent call last):
  AssertionError

- init_8
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp = r_list[1]
  >>> en = sp.entities[1]
  >>> en.components[3].binding_state = BINDING_NONE
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> ReactionRule(1, m, r_list, p_list, False)
  Traceback (most recent call last):
  AssertionError

    def test_init_9(self):
        sp_str_list = ['R(l,d,Y~U)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['R(l,d,Y~?!?)']
        p_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, model.ReactionRule, 1, m, \
            r_list, p_list, False)

    def test_init_10(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = p.parse_species_array(sp_str_list, m)
        model.ReactionRule(1, m, r_list, p_list, False)

    def test_init_11(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r)']
        p_list = p.parse_species_array(sp_str_list, m)
        model.ReactionRule(1, m, r_list, p_list, False)

    def test_init_12(self):
        sp_str_list = ['L(r)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        p_list = p.parse_species_array(sp_str_list, m)
        model.ReactionRule(1, m, r_list, p_list, False)

    def test_init_13(self):
        sp_str_list = ['L(r!1).R(l!1)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L()', 'R()']
        p_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, model.ReactionRule, 1, m, \
            r_list, p_list, False)

    def test_init_14(self):
        sp_str_list = ['L(r)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r)', 'R(l)']
        p_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, model.ReactionRule, 1, m, \
            r_list, p_list, False)

    def test_init_15(self):
        sp_str_list = ['R(l,d,Y~?)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['R(l,d,Y~?!1).A(SH2!1,Y~?)']
        p_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, model.ReactionRule, 1, m, \
            r_list, p_list, False)

    def test_init_16(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = p.parse_species_array(sp_str_list, m)
        rule = model.ReactionRule(1, m, r_list, p_list, False, \
            key_1='value_1', key_2='value_2')
        self.assertEqual(rule['key_1'], 'value_1')
        self.assertEqual(rule['key_2'], 'value_2')

- id
  >>> rule_id = 10
  >>> rule = ReactionRule(rule_id, m, [], [], False)
  >>> rule.id == rule_id
  True

- input_reactants_1
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.input_reactants == r_list
  True

- test_input_reactants_2(self):
  >>> sp_str_list = ['L(r)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.input_reactants == r_list
  True

- test_input_products_1(self):
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.input_products == p_list
  True

- test_input_products_2(self):
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.input_products == p_list
  True

- test_reactants_1(self):
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.reactants == r_list
  True

- test_reactants_2(self):
  >>> sp_str_list = ['L(r)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> len(rule.reactants) == len(r_list) + 1
  True

- test_products_1(self):
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> rule.products == p_list
  True

- test_products_2(self):
  >>> sp_str_list = ['L(r)', 'R(l,d,Y~U)']
  >>> r_list = p.parse_species_array(sp_str_list, m)
  >>> sp_str_list = ['L(r)']
  >>> p_list = p.parse_species_array(sp_str_list, m)
  >>> rule = ReactionRule(1, m, r_list, p_list, False)
  >>> len(rule.products) == len(p_list) + 1
  True

- test_model(self):
  >>> rule = ReactionRule(1, m, [], [], False)
  >>> rule.model == m
  True

- test_condition_1(self):
  >>> rule = ReactionRule(1, m, [], [], False)
  >>> rule.condition == None
  True

- test_condition_2(self):
  >>> condition = IncludingEntityCondition(REACTANTS, 1, entity_type_A)
  >>> rule = ReactionRule(1, m, [], [], False, condition)
  >>> rule.condition == condition
  True

- test_item(self):
  >>> rule = ReactionRule(1, m, [], [], False)
  >>> rule['key'] = 'value'
  >>> rule['key'] == 'value'
  True
  >>> rule['aaa'] == None
  True

    def test_attributes(self):
        rule = ReactionRule(1, m, [], [], False)
        rule['key_1'] = 'value_1'
        rule['key_2'] = 'value_2'
        rule['key_3'] = 'value_3'
        self.assertEqual(rule.attributes, \
            {'key_1': 'value_1', 'key_2': 'value_2', 'key_3': 'value_3'})

    def test_str_simple(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule = p.parse_reaction(rule_text, m)
        self.assertEqual(rule.str_simple(), \
            'L(r) + R(l,d!?,Y~?!?) -> L(r!1).R(l!1,d!?,Y~?!?)')

    def test_str(self):
        rule_text = 'L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        str(rule)

    def test_equals_1(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule_1 = p.parse_reaction(rule_text, m, 1)
        rule_2 = rule_1
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_equals_2(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule_1 = p.parse_reaction(rule_text, m, 1)
        rule_text = 'L(r) + R(l,Y~U) + A(SH2) -> L(r!1).R(l!1,Y~U!2).A(SH2!2)'
        rule_2 = p.parse_reaction(rule_text, m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_3(self):
        rule_text = 'L(r!1).R(l!1) -> L(r) + R(l)'
        rule_1 = p.parse_reaction(rule_text, m, 1)
        rule_text = 'L(r!1).R(l!1,Y~U!2).A(SH2!2) -> L(r) + R(l,Y~U) + A(SH2)'
        rule_2 = p.parse_reaction(rule_text, m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_4(self):
        rule_text = 'L(r!1).R(l!1,Y~U) -> L(r) + R(l,Y~U)'
        rule_1 = p.parse_reaction(rule_text, m, 1)
        rule_text = 'L(r!1).R(l!1,Y~P) -> L(r) + R(l,Y~U)'
        rule_2 = p.parse_reaction(rule_text, m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_5(self):
        rule_text = 'L(r) + R(l,Y~U) -> L(r!1).R(l!1,Y~U)'
        rule_1 = p.parse_reaction(rule_text, m, 1)
        rule_text = 'L(r) + R(l,Y~U) -> L(r!1).R(l!1,Y~P)'
        rule_2 = p.parse_reaction(rule_text, m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_6(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = p.parse_species_array(sp_str_list, m)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_L)
        rule_1 = ReactionRule(1, m, r_list, p_list, False, c)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_R)
        rule_2 = ReactionRule(2, m, r_list, p_list, False, c)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_7(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = p.parse_species_array(sp_str_list, m)
        rule_1 = ReactionRule(1, m, r_list, p_list, False)
        rule_2 = ReactionRule(2, m, r_list, p_list, False)
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_equals_8(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r)']
        p_list = p.parse_species_array(sp_str_list, m)
        rule_1 = ReactionRule(1, m, r_list, p_list, False)
        rule_2 = ReactionRule(2, m, r_list, p_list, False)
        self.assertTrue(rule_1.equals(rule_2, False))

    def test_equals_9(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = p.parse_species_array(sp_str_list, m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = p.parse_species_array(sp_str_list, m)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_L)
        rule_1 = ReactionRule(1, m, r_list, p_list, False, c)
        rule_2 = ReactionRule(2, m, r_list, p_list, False, c)
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_generate_reactions_1(self):
        rule_text = ' -> '
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_2(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = []
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_3(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_4(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d,Y~U)', 'R(l,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~P) -> R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_5(self):
        rule_text = 'R(l,d,Y~?!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = [\
            'R(l,d,Y~U!1).A(SH2!1,Y~U)', \
            'R(l,d,Y~U!1).A(SH2!1,Y~P)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~U)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'R(l,d,Y~U!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_6(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) -> L(r!1).R(l!1,d,Y~?!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)', \
            'L(r) + R(l,d,Y~P) -> L(r!1).R(l!1,d,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_7(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?!?) -> L(r) + R(l,d,Y~P!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)', 'L(r!1).R(l!1,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r!1).R(l!1,d,Y~U) -> L(r) + R(l,d,Y~P)', \
            'L(r!1).R(l!1,d,Y~P) -> L(r) + R(l,d,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_8(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) -> L(r!1).R(l!1,d,Y~?!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_9(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?!?) -> L(r) + R(l,d,Y~?!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~P) -> L(r) + R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_10(self):
        rule_text = 'R(l,d!+,Y~U!?) -> R(l,d!+,Y~P!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U)',\
            'R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> R(l,d!1,Y~U).R(l,d!1,Y~P!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_11(self):
        rule_text = 'L(r) + R(l,d!1,Y~P!?).R(l,d!1,Y~U!?) -> L(r!1).R(l!1,d,Y~P!?) + R(l,d,Y~U!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~P) + R(l,d,Y~U!1).A(SH2!1,Y~U)', \
            'L(r) + R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U) + R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_12(self):
        rule_text = 'R(Y~U!?) -> R(Y~P!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U) -> R(l,d!1,Y~P).R(l,d!1,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_13(self):
        rule_text = 'R(l,d,Y~U) -> '
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U) -> ']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_14(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) + A() -> L(r)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) + A(SH2,Y~U) -> L(r)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_15(self):
        rule_text = 'R(l,d,Y~?!1).A(SH2!1,Y~?) -> '
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U) -> ']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_16(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> L(r)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> L(r)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_17(self):
        rule_text = 'R(Y~?!1).A(SH2!1) -> R(Y~?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_18(self):
        rule_text = 'L(r!1).R(l!1,Y~?!2).A(SH2!2) -> A(SH2)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U) -> A(SH2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_19(self):
        rule_text = 'L(r!1).R(l!1,Y~?!2).A(SH2!2) -> L(r) + A(SH2)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3) -> L(r) + A(SH2,Y~U!1).A(SH2,Y~P!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_20(self):
        ori = m.disallow_implicit_disappearance
        m.disallow_implicit_disappearance = False
        rule_text = 'R(Y~?!1).A(SH2!1) -> A(SH2)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)
        m.disallow_implicit_disappearance = ori

    def test_generate_reactions_21(self):
        ori = m.disallow_implicit_disappearance
        m.disallow_implicit_disappearance = True
        rule_text = 'R(Y~?!1).A(SH2!1) -> A(SH2)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, rule.generate_reactions, sp_list)
        m.disallow_implicit_disappearance = False
        m.disallow_implicit_disappearance = ori

    def test_generate_reactions_22(self):
        rule_text = ' -> R(l,d,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = []
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [' -> R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_23(self):
        rule_text = 'L(r) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_24(self):
        rule_text = 'L(r) -> L(r) + R(l,d,Y~U!1).A(SH2!1,Y~P)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) -> L(r) + R(l,d,Y~U!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_25(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~?!1).A(SH2!1,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U) -> R(l,d,Y~U!1).A(SH2!1,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_26(self):
        rule_text = 'A(SH2,Y~?) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['A(SH2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_27(self):
        rule_text = 'L(r) + A(SH2,Y~?) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'A(SH2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_28(self):
        rule_text = 'L(r!?) + R(l,d,Y~?) -> A(SH2,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> A(SH2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_29(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> R(l,d,Y~P!1).A(SH2!1,Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> R(l,d,Y~P!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_30(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> R(l,d,Y~P!1).A(SH2!1,Y~U) + R(l,d,Y~P!1).A(SH2!1,Y~P)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~U) + R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_31(self):
        ori = m.disallow_implicit_disappearance
        m.disallow_implicit_disappearance = False
        rule_text = 'L() + R() -> L(r!1).R(l!1)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U)', 'R(l,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)
        m.disallow_implicit_disappearance = ori

    def test_generate_reactions_32(self):
        ori = m.disallow_implicit_disappearance
        m.disallow_implicit_disappearance = True
        rule_text = 'L() + R() -> L(r!1).R(l!1)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U)', 'R(l,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(model.Error, rule.generate_reactions, sp_list)
        m.disallow_implicit_disappearance = ori

    def test_generate_reactions_33(self):
        rule_text = 'R().R() -> R() + R()'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d!3,Y~P).L(r!2).R(l!2,d!3,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_34(self):
        rule_text = 'R(d) + R(d) -> R(d!1).R(d!1)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~P) + L(r!1).R(l!1,d,Y~P) -> L(r!1).R(l!1,d!3,Y~P).L(r!2).R(l!2,d!3,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_35(self):
        rule_text = 'A(SH2).A(Y~U) -> A(SH2!1).A(Y~U!1)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U) -> A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_36(self):
        rule_text = 'A(SH2!1).A(Y~U!1) -> A(SH2).A(Y~U)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3) -> A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_37(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_38(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_i = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c = model.NotCondition(c_i)
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_39(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.PRODUCTS, 1, \
            self.entity_type_A)
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_40(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_i = model.IncludingEntityCondition(model.PRODUCTS, 1, \
            self.entity_type_A)
        c = model.NotCondition(c_i)
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_41(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_1 = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c_2 = model.IncludingEntityCondition(model.REACTANTS, 1, \
            self.entity_type_L)
        c = model.AndCondition([c_1, c_2])
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_42(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_1 = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c_2 = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c_2 = model.NotCondition(c_2)
        c = model.OrCondition([c_1, c_2])
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)', \
            'L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_43(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_1 = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c_2 = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c_2 = model.NotCondition(c_2)
        c = model.AndCondition([c_1, c_2])
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = []
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_44(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.PRODUCTS, 3, \
            self.entity_type_A)
        rule = p.parse_reaction(rule_text, m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = p.parse_species_array(sp_str_list, m)
        self.assertRaises(AssertionError, rule.generate_reactions, sp_list)

    def test_generate_reactions_45(self):
        rule_text = 'L(r) + R(l,d!?,Y~?) + A(SH2,Y~?!?) -> L(r!1).R(l!1,d!?,Y~?!2).A(SH2!2,Y~?!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)', \
            'A(SH2,Y~P!1).A(SH2,Y~U!1)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r) + R(l,d,Y~U) + A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)', \
            'L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3)', \
            'L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_46(self):
        rule_text = 'L(r!1).R(l!1,d!?,Y~?!2).A(SH2!2,Y~?!?) -> L(r) + R(l,d!?,Y~?) + A(SH2,Y~?!?)'
        rule = p.parse_reaction(rule_text, m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3)']
        sp_list = p.parse_species_array(sp_str_list, m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))


if __name__ == '__main__':
    main()




