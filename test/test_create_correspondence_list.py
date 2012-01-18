from unittest import TestCase, main
import model
import parser

class ModelTest(TestCase):
    def setUp(self):
        p_state = model.StateType(
            'phosphorylation', ['U', 'P'])
        a_state = model.StateType(
            'acetylation', ['U', 'A'])

        entity_type_a = model.EntityType('A')
        comp_r_a = entity_type_a.add_component('r', {'p': p_state})
        comp_d_a = entity_type_a.add_component('d')

        entity_type_b = model.EntityType('B')
        comp_r_b = entity_type_b.add_component('r', {'p': p_state})
        comp_d_b = entity_type_b.add_component('d')

        entity_type_c = model.EntityType('C')
        comp_r_c = entity_type_c.add_component('r', {'p': p_state})
        comp_d_c = entity_type_c.add_component('d')

        entity_type_d = model.EntityType('D')
        comp_r_d = entity_type_d.add_component('r', {'p': p_state})
        comp_d_d = entity_type_d.add_component('d')

        p = parser.Parser()
        p.add_entity_type(entity_type_a)
        p.add_entity_type(entity_type_b)
        p.add_entity_type(entity_type_c)
        p.add_entity_type(entity_type_d)
        self.parser = p


    def test_create_correspondence_list(self):
        sp_text = 'A().A()'
        sp_1 = self.parser.parse_species(sp_text)
        entities_1 = sp_1.entities
        sp_text = 'A().A().A()'
        sp_2 = self.parser.parse_species(sp_text)
        entities_2 = sp_2.entities
        pairs = []
        p = model.PatternMatchingEntityPair(entities_1[1], entities_2[2])
        pairs.append(p)
        p = model.PatternMatchingEntityPair(entities_1[1], entities_2[3])
        pairs.append(p)
        p = model.PatternMatchingEntityPair(entities_1[2], entities_2[1])
        pairs.append(p)
        p = model.PatternMatchingEntityPair(entities_1[2], entities_2[2])
        pairs.append(p)
        c_list = model.create_correspondence_list(pairs)
        c_1 = model.Correspondence()
        c_1.add_pair(model.PatternMatchingEntityPair(\
            entities_1[1], entities_2[2]))
        c_1.add_pair(model.PatternMatchingEntityPair(\
            entities_1[2], entities_2[1]))
        c_2 = model.Correspondence()
        c_2.add_pair(model.PatternMatchingEntityPair(\
            entities_1[1], entities_2[3]))
        c_2.add_pair(model.PatternMatchingEntityPair(\
            entities_1[2], entities_2[1]))
        c_3 = model.Correspondence()
        c_3.add_pair(model.PatternMatchingEntityPair(\
            entities_1[1], entities_2[3]))
        c_3.add_pair(model.PatternMatchingEntityPair(\
            entities_1[2], entities_2[2]))

        import pdb; pdb.set_trace()

        self.assertEqual(len(c_list), 3)
        self.assertTrue(c_1 in c_list)
        self.assertTrue(c_2 in c_list)
        self.assertTrue(c_3 in c_list)


if __name__ == '__main__':
    main()

