from unittest import TestCase, main
import model
import parser

class ModelTest(TestCase):

    def setUp(self):
        m = model.Model()

        p_state = m.add_state_type(
            'phosphorylation', ['U', 'P'])
        a_state = m.add_state_type(
            'acetylation', ['U', 'A'])

        entity_type_L = m.add_entity_type('L')
        comp_r_L = entity_type_L.add_component('r')

        entity_type_R = m.add_entity_type('R')
        comp_l_R = entity_type_R.add_component('l')
        comp_d_R = entity_type_R.add_component('d')
        comp_Y_R = entity_type_R.add_component('Y', {'p': p_state})

        entity_type_A = m.add_entity_type('A')
        comp_SH2_A = entity_type_A.add_component('SH2')
        comp_Y_A = entity_type_A.add_component('Y', {'p': p_state})

        p = parser.Parser()
        p.add_entity_type(entity_type_L)
        p.add_entity_type(entity_type_R)
        p.add_entity_type(entity_type_A)

        self.entity_type_L = entity_type_L
        self.entity_type_R = entity_type_R
        self.entity_type_A = entity_type_A
        self.parser = p
        self.m = m

    def __check_reactions(self, reactions, reaction_text_list):
        if len(reactions) != len(reaction_text_list):
            print len(reactions), '!=', len(reaction_text_list)
            return False
        answer_reactions = []
        for reaction_text in reaction_text_list:
            reaction = self.parser.parse_reaction(reaction_text, self.m)
            answer_reactions.append(reaction)
        for r in reactions:
            found = False
            tmp = list(answer_reactions)
            for a in tmp:
                if r.equals(a):
                    answer_reactions.remove(a)
                    found = True
                    break
            if not found:
                print 'Not Found:', r.str_simple()
                return False
        if len(answer_reactions):
            print 'Reactions exist.'
            return False
        return True

    def test_init_1(self):
        sp_text = 'R(l,d,Y~U)'
        sp_r = self.parser.parse_species(sp_text)
        sp_text = 'R(l,d,Y~P)'
        sp_p = self.parser.parse_species(sp_text)
        self.m.register_species(sp_p)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            [sp_r], [sp_p], False)

    def test_init_2(self):
        sp_text = 'R(l,d,Y~U)'
        sp_r = self.parser.parse_species(sp_text)
        sp_text = 'R(l,d,Y~P)'
        sp_p = self.parser.parse_species(sp_text)
        self.m.register_species(sp_r)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            [sp_r], [sp_p], False)

    def test_init_3(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~?)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, True)

    def test_init_4(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~?)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, True)

    def test_init_5(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp = r_list[1]
        en = sp.entities[1]
        en.components[3].binding_state = model.BINDING_NONE
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, True)

    def test_init_6(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp = r_list[1]
        en = sp.entities[1]
        en.components[3].binding_state = model.BINDING_NONE
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_7(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp = r_list[1]
        en = sp.entities[1]
        en.components[3].binding_state = model.BINDING_NONE
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, True)

    def test_init_8(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp = r_list[1]
        en = sp.entities[1]
        en.components[3].binding_state = model.BINDING_NONE
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_9(self):
        sp_str_list = ['R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['R(l,d,Y~?!?)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_10(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        model.ReactionRule(1, self.m, r_list, p_list, False)

    def test_init_11(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        model.ReactionRule(1, self.m, r_list, p_list, False)

    def test_init_12(self):
        sp_str_list = ['L(r)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        model.ReactionRule(1, self.m, r_list, p_list, False)

    def test_init_13(self):
        sp_str_list = ['L(r!1).R(l!1)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L()', 'R()']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_14(self):
        sp_str_list = ['L(r)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)', 'R(l)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_15(self):
        sp_str_list = ['R(l,d,Y~?)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['R(l,d,Y~?!1).A(SH2!1,Y~?)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, model.ReactionRule, 1, self.m, \
            r_list, p_list, False)

    def test_init_16(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False, \
            key_1='value_1', key_2='value_2')
        self.assertEqual(rule['key_1'], 'value_1')
        self.assertEqual(rule['key_2'], 'value_2')

    def test_id(self):
        rule_id = 10
        rule = model.ReactionRule(rule_id, self.m, [], [], False)
        self.assertEqual(rule.id, rule_id)

    def test_input_reactants_1(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.input_reactants, r_list)

    def test_input_reactants_2(self):
        sp_str_list = ['L(r)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.input_reactants, r_list)

    def test_input_products_1(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.input_products, p_list)

    def test_input_products_2(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.input_products, p_list)

    def test_reactants_1(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.reactants, r_list)

    def test_reactants_2(self):
        sp_str_list = ['L(r)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(len(rule.reactants), len(r_list) + 1)

    def test_products_1(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(rule.products, p_list)

    def test_products_2(self):
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule = model.ReactionRule(1, self.m, r_list, p_list, False)
        self.assertEqual(len(rule.products), len(p_list) + 1)

    def test_model(self):
        rule = model.ReactionRule(1, self.m, [], [], False)
        self.assertEqual(rule.model, self.m)

    def test_condition_1(self):
        rule = model.ReactionRule(1, self.m, [], [], False)
        self.assertEqual(rule.condition, None)

    def test_condition_2(self):
        condition = model.IncludingEntityCondition(model.REACTANTS, \
            1, self.entity_type_A)
        rule = model.ReactionRule(1, self.m, [], [], False, condition)
        self.assertEqual(rule.condition, condition)

    def test_item(self):
        rule = model.ReactionRule(1, self.m, [], [], False)
        rule['key'] = 'value'
        self.assertEqual(rule['key'], 'value')
        self.assertEqual(rule['aaa'], None)

    def test_attributes(self):
        rule = model.ReactionRule(1, self.m, [], [], False)
        rule['key_1'] = 'value_1'
        rule['key_2'] = 'value_2'
        rule['key_3'] = 'value_3'
        self.assertEqual(rule.attributes, \
            {'key_1': 'value_1', 'key_2': 'value_2', 'key_3': 'value_3'})

    def test_str_simple(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        self.assertEqual(rule.str_simple(), \
            'L(r) + R(l,d!?,Y~?!?) -> L(r!1).R(l!1,d!?,Y~?!?)')

    def test_str(self):
        rule_text = 'L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        str(rule)

    def test_equals_1(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule_1 = self.parser.parse_reaction(rule_text, self.m, 1)
        rule_2 = rule_1
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_equals_2(self):
        rule_text = 'L(r) + R(l) -> L(r!1).R(l!1)'
        rule_1 = self.parser.parse_reaction(rule_text, self.m, 1)
        rule_text = 'L(r) + R(l,Y~U) + A(SH2) -> L(r!1).R(l!1,Y~U!2).A(SH2!2)'
        rule_2 = self.parser.parse_reaction(rule_text, self.m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_3(self):
        rule_text = 'L(r!1).R(l!1) -> L(r) + R(l)'
        rule_1 = self.parser.parse_reaction(rule_text, self.m, 1)
        rule_text = 'L(r!1).R(l!1,Y~U!2).A(SH2!2) -> L(r) + R(l,Y~U) + A(SH2)'
        rule_2 = self.parser.parse_reaction(rule_text, self.m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_4(self):
        rule_text = 'L(r!1).R(l!1,Y~U) -> L(r) + R(l,Y~U)'
        rule_1 = self.parser.parse_reaction(rule_text, self.m, 1)
        rule_text = 'L(r!1).R(l!1,Y~P) -> L(r) + R(l,Y~U)'
        rule_2 = self.parser.parse_reaction(rule_text, self.m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_5(self):
        rule_text = 'L(r) + R(l,Y~U) -> L(r!1).R(l!1,Y~U)'
        rule_1 = self.parser.parse_reaction(rule_text, self.m, 1)
        rule_text = 'L(r) + R(l,Y~U) -> L(r!1).R(l!1,Y~P)'
        rule_2 = self.parser.parse_reaction(rule_text, self.m, 2)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_6(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_L)
        rule_1 = model.ReactionRule(1, self.m, r_list, p_list, False, c)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_R)
        rule_2 = model.ReactionRule(2, self.m, r_list, p_list, False, c)
        self.assertFalse(rule_1.equals(rule_2, True))

    def test_equals_7(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule_1 = model.ReactionRule(1, self.m, r_list, p_list, False)
        rule_2 = model.ReactionRule(2, self.m, r_list, p_list, False)
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_equals_8(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        rule_1 = model.ReactionRule(1, self.m, r_list, p_list, False)
        rule_2 = model.ReactionRule(2, self.m, r_list, p_list, False)
        self.assertTrue(rule_1.equals(rule_2, False))

    def test_equals_9(self):
        sp_str_list = ['L(r)', 'R(l)']
        r_list = self.parser.parse_species_array(sp_str_list, self.m)
        sp_str_list = ['L(r!1).R(l!1)']
        p_list = self.parser.parse_species_array(sp_str_list, self.m)
        c = model.IncludingEntityCondition(\
            model.REACTANTS, 1, self.entity_type_L)
        rule_1 = model.ReactionRule(1, self.m, r_list, p_list, False, c)
        rule_2 = model.ReactionRule(2, self.m, r_list, p_list, False, c)
        self.assertTrue(rule_1.equals(rule_2, True))

    def test_generate_reactions_1(self):
        rule_text = ' -> '
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_2(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = []
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_3(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_4(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d,Y~U)', 'R(l,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~P) -> R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_5(self):
        rule_text = 'R(l,d,Y~?!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = [\
            'R(l,d,Y~U!1).A(SH2!1,Y~U)', \
            'R(l,d,Y~U!1).A(SH2!1,Y~P)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~U)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'R(l,d,Y~U!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)', \
            'R(l,d,Y~P!1).A(SH2!1,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_6(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) -> L(r!1).R(l!1,d,Y~?!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)', \
            'L(r) + R(l,d,Y~P) -> L(r!1).R(l!1,d,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_7(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?!?) -> L(r) + R(l,d,Y~P!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)', 'L(r!1).R(l!1,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r!1).R(l!1,d,Y~U) -> L(r) + R(l,d,Y~P)', \
            'L(r!1).R(l!1,d,Y~P) -> L(r) + R(l,d,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_8(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) -> L(r!1).R(l!1,d,Y~?!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_9(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?!?) -> L(r) + R(l,d,Y~?!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~P) -> L(r) + R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_10(self):
        rule_text = 'R(l,d!+,Y~U!?) -> R(l,d!+,Y~P!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U)',\
            'R(l,d!1,Y~U).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> R(l,d!1,Y~U).R(l,d!1,Y~P!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_11(self):
        rule_text = 'L(r) + R(l,d!1,Y~P!?).R(l,d!1,Y~U!?) -> L(r!1).R(l!1,d,Y~P!?) + R(l,d,Y~U!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~P) + R(l,d,Y~U!1).A(SH2!1,Y~U)', \
            'L(r) + R(l,d!1,Y~P).R(l,d!1,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U) + R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_12(self):
        rule_text = 'R(Y~U!?) -> R(Y~P!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d!1,Y~U).R(l,d!1,Y~U) -> R(l,d!1,Y~P).R(l,d!1,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_13(self):
        rule_text = 'R(l,d,Y~U) -> '
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U) -> ']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_14(self):
        rule_text = 'L(r) + R(l,d,Y~?!?) + A() -> L(r)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) + A(SH2,Y~U) -> L(r)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_15(self):
        rule_text = 'R(l,d,Y~?!1).A(SH2!1,Y~?) -> '
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U!1).A(SH2!1,Y~U) -> ']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_16(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> L(r)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> L(r)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_17(self):
        rule_text = 'R(Y~?!1).A(SH2!1) -> R(Y~?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U) -> L(r!1).R(l!1,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_18(self):
        rule_text = 'L(r!1).R(l!1,Y~?!2).A(SH2!2) -> A(SH2)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U) -> A(SH2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_19(self):
        rule_text = 'L(r!1).R(l!1,Y~?!2).A(SH2!2) -> L(r) + A(SH2)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3) -> L(r) + A(SH2,Y~U!1).A(SH2,Y~P!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_20(self):
        ori = self.m.disallow_implicit_disappearance
        self.m.disallow_implicit_disappearance = False
        rule_text = 'R(Y~?!1).A(SH2!1) -> A(SH2)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)
        self.m.disallow_implicit_disappearance = ori

    def test_generate_reactions_21(self):
        ori = self.m.disallow_implicit_disappearance
        self.m.disallow_implicit_disappearance = True
        rule_text = 'R(Y~?!1).A(SH2!1) -> A(SH2)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, rule.generate_reactions, sp_list)
        self.m.disallow_implicit_disappearance = False
        self.m.disallow_implicit_disappearance = ori

    def test_generate_reactions_22(self):
        rule_text = ' -> R(l,d,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = []
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [' -> R(l,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_23(self):
        rule_text = 'L(r) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_24(self):
        rule_text = 'L(r) -> L(r) + R(l,d,Y~U!1).A(SH2!1,Y~P)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) -> L(r) + R(l,d,Y~U!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_25(self):
        rule_text = 'R(l,d,Y~?) -> R(l,d,Y~?!1).A(SH2!1,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['R(l,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['R(l,d,Y~U) -> R(l,d,Y~U!1).A(SH2!1,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_26(self):
        rule_text = 'A(SH2,Y~?) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['A(SH2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_27(self):
        rule_text = 'L(r) + A(SH2,Y~?) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'A(SH2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_28(self):
        rule_text = 'L(r!?) + R(l,d,Y~?) -> A(SH2,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> A(SH2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_29(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> R(l,d,Y~P!1).A(SH2!1,Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> R(l,d,Y~P!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_30(self):
        rule_text = 'L(r!1).R(l!1,d,Y~?) -> R(l,d,Y~P!1).A(SH2!1,Y~U) + R(l,d,Y~P!1).A(SH2!1,Y~P)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~U) -> R(l,d,Y~P!1).A(SH2!1,Y~U) + R(l,d,Y~P!1).A(SH2!1,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_31(self):
        ori = self.m.disallow_implicit_disappearance
        self.m.disallow_implicit_disappearance = False
        rule_text = 'L() + R() -> L(r!1).R(l!1)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U)', 'R(l,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)
        self.m.disallow_implicit_disappearance = ori

    def test_generate_reactions_32(self):
        ori = self.m.disallow_implicit_disappearance
        self.m.disallow_implicit_disappearance = True
        rule_text = 'L() + R() -> L(r!1).R(l!1)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P!2).A(SH2!2,Y~U)', 'R(l,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(model.Error, rule.generate_reactions, sp_list)
        self.m.disallow_implicit_disappearance = ori

    def test_generate_reactions_33(self):
        rule_text = 'R().R() -> R() + R()'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d!3,Y~P).L(r!2).R(l!2,d!3,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        self.assertEqual(len(reactions), 0)

    def test_generate_reactions_34(self):
        rule_text = 'R(d) + R(d) -> R(d!1).R(d!1)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~P)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r!1).R(l!1,d,Y~P) + L(r!1).R(l!1,d,Y~P) -> L(r!1).R(l!1,d!3,Y~P).L(r!2).R(l!2,d!3,Y~P)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_35(self):
        rule_text = 'A(SH2).A(Y~U) -> A(SH2!1).A(Y~U!1)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U) -> A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_36(self):
        rule_text = 'A(SH2!1).A(Y~U!1) -> A(SH2).A(Y~U)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['A(SH2!3,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U!3) -> A(SH2,Y~U!1).A(SH2!1,Y~U!2).A(SH2!2,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_37(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_38(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_i = model.IncludingEntityCondition(model.REACTANTS, 2, \
            self.entity_type_A)
        c = model.NotCondition(c_i)
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U) -> L(r!1).R(l!1,d,Y~U)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_39(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.PRODUCTS, 1, \
            self.entity_type_A)
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = ['L(r) + R(l,d,Y~U!1).A(SH2!1,Y~U) -> A(SH2!2,Y~U).R(l!1,d,Y~U!2).L(r!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_40(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c_i = model.IncludingEntityCondition(model.PRODUCTS, 1, \
            self.entity_type_A)
        c = model.NotCondition(c_i)
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
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
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
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
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
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
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = []
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_44(self):
        rule_text = 'L(r) + R(l,Y~?!?) -> L(r!1).R(l!1,Y~?!?)'
        c = model.IncludingEntityCondition(model.PRODUCTS, 3, \
            self.entity_type_A)
        rule = self.parser.parse_reaction(rule_text, self.m, condition=c)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'R(l,d,Y~U!1).A(SH2!1,Y~U)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        self.assertRaises(AssertionError, rule.generate_reactions, sp_list)

    def test_generate_reactions_45(self):
        rule_text = 'L(r) + R(l,d!?,Y~?) + A(SH2,Y~?!?) -> L(r!1).R(l!1,d!?,Y~?!2).A(SH2!2,Y~?!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r)', 'R(l,d,Y~U)', 'A(SH2,Y~U)', \
            'A(SH2,Y~P!1).A(SH2,Y~U!1)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r) + R(l,d,Y~U) + A(SH2,Y~U) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U)', \
            'L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U!3).A(SH2,Y~P!3)', \
            'L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1) -> L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))

    def test_generate_reactions_46(self):
        rule_text = 'L(r!1).R(l!1,d!?,Y~?!2).A(SH2!2,Y~?!?) -> L(r) + R(l,d!?,Y~?) + A(SH2,Y~?!?)'
        rule = self.parser.parse_reaction(rule_text, self.m)
        sp_str_list = ['L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3)']
        sp_list = self.parser.parse_species_array(sp_str_list, self.m)
        reactions = rule.generate_reactions(sp_list)
        reaction_text_list = [\
            'L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~P!3).A(SH2,Y~U!3) -> L(r) + R(l,d,Y~U) + A(SH2,Y~P!1).A(SH2,Y~U!1)']
        self.assertTrue(self.__check_reactions(reactions, reaction_text_list))


if __name__ == '__main__':
    main()

