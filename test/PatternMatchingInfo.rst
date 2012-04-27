- setup
  >>> from model.PatternMatchingInfo import PatternMatchingInfo
  >>> from model.Correspondence import Correspondence
  >>> from model.EntityType import EntityType
  >>> from model.Species import Species
  >>> entity_type_a = EntityType('A')
  >>> entity_type_b = EntityType('B')
  >>> sp_1 = Species()
  >>> o = sp_1.add_entity(entity_type_a)
  >>> o = sp_1.add_entity(entity_type_b)
  >>> sp_2 = Species()
  >>> o = sp_2.add_entity(entity_type_a)
  >>> o = sp_2.add_entity(entity_type_b)

- init
  >>> info = PatternMatchingInfo(sp_1, sp_2)

- species
  >>> info.species == sp_1
  True

- pattern
  >>> info.pattern == sp_2
  True

- correspondences
  >>> info.correspondences
  []

- str
  >>> str(info)
  "PatternMatchingInfo(Pattern='A().B()', Species='A().B()', )"

- add_correspondence
  >>> c_1 = Correspondence()
  >>> info.add_correspondence(c_1)
  >>> c_2 = Correspondence()
  >>> info.add_correspondence(c_2)
  >>> info.correspondences == [c_1, c_2]
  True

- str
  >>> str(info)
  "PatternMatchingInfo(Pattern='A().B()', Species='A().B()', Correspondence(), Correspondence())"
