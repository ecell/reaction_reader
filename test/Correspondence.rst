- setup
  >>> from model.Correspondence import Correspondence
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> from model.Entity import Entity
  >>> from model.Pair import PatternMatchingEntityPair

  >>> entity_type_a = EntityType('A')
  >>> entity_type_b = EntityType('B')
  >>> species = Species()
  >>> entity_1 = Entity(1, entity_type_a, species)
  >>> entity_2 = Entity(2, entity_type_b, species)
  >>> species = Species()
  >>> entity_3 = Entity(1, entity_type_a, species)
  >>> entity_4 = Entity(2, entity_type_b, species)

- init
  >>> o = Correspondence()
  >>> o.pairs
  []

- pairs
  >>> pair_1 = PatternMatchingEntityPair(entity_1, entity_2)
  >>> pair_2 = PatternMatchingEntityPair(entity_3, entity_4)
  >>> pair_3 = PatternMatchingEntityPair(entity_1, entity_4)
  >>> o.add_pair(pair_1)
  >>> o.add_pair(pair_2)
  >>> o.add_pair(pair_3)
  >>> o.pairs == [pair_1, pair_2, pair_3]
  True

- add_pair
  >>> o2 = Correspondence()
  >>> o2.add_pair(pair_1)
  >>> o2.add_pair(pair_2)
  >>> o3 = Correspondence()
  >>> o3.add_pair(pair_1)
  >>> o3.add_pair(pair_2)
  >>> o2 == o3
  True

- eq
  >>> pair_4 = PatternMatchingEntityPair(entity_2, entity_3)
  >>> o4 = Correspondence()
  >>> o4.add_pair(pair_1)
  >>> o4.add_pair(pair_4)
  >>> o2 != o4
  True

- copy
  >>> o5 = o2.copy()
  >>> o2.pairs == o5.pairs
  True

- str
  >>> str(o2)
  'Correspondence(A(1)-B(2), A(1)-B(2))'
