=====
Pair
=====

- setup
  >>> from model.Pair import Pair

- has_equal_first_element
  >>> Pair().has_equal_first_element(Pair())
  Traceback (most recent call last):
  Error: Not implemented.

- has_equal_second_element
  >>> Pair().has_equal_second_element(Pair())
  Traceback (most recent call last):
  Error: Not implemented.


==========================
PatternMatchingEntityPair
==========================

- setup
  >>> from model.Pair import PatternMatchingEntityPair
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> entity_type_a = EntityType('A')
  >>> entity_type_b = EntityType('B')
  >>> entity_type_c = EntityType('C')
  >>> species = Species()
  >>> entity_1 = Entity(1, entity_type_a, species)
  >>> entity_2 = Entity(2, entity_type_b, species)
  >>> entity_3 = Entity(3, entity_type_c, species)

- init
  >>> o = PatternMatchingEntityPair(entity_1, entity_2)

- pattern_entity
  >>> o.pattern_entity == entity_1
  True

- matched_entity
  >>> o.matched_entity == entity_2
  True

- has_equal_first_element, has_equal_second_element
  >>> o2 = PatternMatchingEntityPair(entity_1, entity_2)
  >>> o.has_equal_first_element(o2), o.has_equal_second_element(o2)
  (True, True)
  >>> o3 = PatternMatchingEntityPair(entity_2, entity_1)
  >>> o.has_equal_first_element(o3), o.has_equal_second_element(o3)
  (False, False)

- cmp
  >>> species = Species()
  >>> ent1 = Entity(1, entity_type_a, species)
  >>> ent2 = Entity(2, entity_type_a, species)
  >>> ent3 = Entity(1, entity_type_b, species)
  >>> pair_1 = PatternMatchingEntityPair(ent1, ent3)
  >>> pair_2 = PatternMatchingEntityPair(ent2, ent3)
  >>> pair_1 < pair_2
  True
  >>> pair_1 != pair_2
  True
  >>> pair_3 = PatternMatchingEntityPair(ent3, ent1)
  >>> pair_4 = PatternMatchingEntityPair(ent3, ent2)
  >>> pair_3 < pair_4
  True
  >>> pair_3 != pair_4
  True
  >>> pair_5 = PatternMatchingEntityPair(ent3, ent2)
  >>> pair_4 < pair_5
  False
  >>> pair_4 == pair_5
  True
  >>> pair_4 > pair_5
  False

- str
  >>> str(o)
  'A(1)-B(2)'


==========================
ReactantProductEntityPair
==========================

- setup
  >>> from model.Pair import ReactantProductEntityPair
  >>> from model.Entity import Entity
  >>> from model.Species import Species
  >>> from model.Pair import PatternMatchingEntityPair
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> entity_type_a = EntityType('A')
  >>> entity_type_b = EntityType('B')
  >>> entity_type_c = EntityType('C')
  >>> species = Species()
  >>> entity_1 = Entity(1, entity_type_a, species)
  >>> entity_2 = Entity(2, entity_type_b, species)
  >>> entity_3 = Entity(3, entity_type_c, species)

- init
  >>> o = ReactantProductEntityPair(0, entity_1, 1, entity_2)

- reactant_entity, product_entity
  >>> o.reactant_entity == entity_1
  True
  >>> o.product_entity == entity_2
  True

- reactant_index, product_index
  >>> pair_1 = ReactantProductEntityPair(2, entity_1, 1, entity_2)
  >>> pair_1.reactant_index, pair_1.product_index
  (2, 1)

- has_equal_first_element, has_equal_second_element
  >>> pair_1 = ReactantProductEntityPair(2, entity_1, 1, entity_2)
  >>> pair_2 = ReactantProductEntityPair(2, entity_1, 1, entity_2)
  >>> pair_3 = ReactantProductEntityPair(2, entity_3, 1, entity_2)
  >>> pair_4 = ReactantProductEntityPair(3, entity_1, 1, entity_2)
  >>> pair_5 = ReactantProductEntityPair(3, entity_1, 1, entity_3)
  >>> pair_6 = ReactantProductEntityPair(2, entity_1, 3, entity_2)
  >>> pair_1.has_equal_first_element(pair_2)
  True
  >>> pair_1.has_equal_first_element(pair_3)
  False
  >>> pair_1.has_equal_first_element(pair_4)
  False
  >>> pair_1.has_equal_second_element(pair_2)
  True
  >>> pair_1.has_equal_second_element(pair_5)
  False
  >>> pair_1.has_equal_second_element(pair_6)
  False

- cmp
  >>> pair_1 < pair_4, pair_1 != pair_4
  (True, True)
  >>> pair_1 < pair_3, pair_1 != pair_3
  (True, True)
  >>> pair_1 < pair_6, pair_1 != pair_6
  (True, True)
  >>> pair_1 < pair_5, pair_1 != pair_5
  (True, True)
  >>> pair_1 == pair_2
  True

- str
  >>> str(pair_1)
  'A(2,1)-B(1,2)'


==========================
ReactantSpeciesEntityPair
==========================

- setup
  >>> from model.Pair import ReactantSpeciesEntityPair
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> entity_type_a = EntityType('A')
  >>> entity_type_b = EntityType('B')
  >>> entity_type_c = EntityType('C')
  >>> species = Species()
  >>> entity_1 = Entity(1, entity_type_a, species)
  >>> entity_2 = Entity(2, entity_type_b, species)
  >>> entity_3 = Entity(3, entity_type_c, species)

- init
  >>> o = ReactantSpeciesEntityPair(0, entity_1, entity_2)
  >>> o2 = ReactantSpeciesEntityPair(1, entity_1, entity_2)
  >>> o3 = ReactantSpeciesEntityPair(1, entity_1, entity_2)
  >>> o4 = ReactantSpeciesEntityPair(1, entity_3, entity_2)
  >>> o5 = ReactantSpeciesEntityPair(1, entity_1, entity_3)
  >>> o6 = ReactantSpeciesEntityPair(0, entity_3, entity_2)

- index
  >>> o2.reactant_index
  1

- reactant_entity, species_entity
  >>> (o2.reactant_entity, o2.species_entity) == (entity_1, entity_2)
  True

- has_equal_first_element, has_equal_second_element
  >>> o2.has_equal_first_element(o3), o2.has_equal_second_element(o3)
  (True, True)
  >>> o2.has_equal_first_element(o)
  False
  >>> o2.has_equal_first_element(o4)
  False
  >>> o2.has_equal_second_element(o5)
  False

- cmp
  >>> o < o2
  True
  >>> o != o2
  True
  >>> o2 > o
  True
  >>> o < o6
  True
  >>> o != o6
  True
  >>> o6 > o
  True
  >>> o2 == o3
  True

- str
  >>> str(o)
  'A(0,1)-B(2)'
