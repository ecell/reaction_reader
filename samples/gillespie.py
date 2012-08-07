with molecule_types:
    X(x)
    Y(y)

with molecule_inits:
    X(x)    [.1]
    Y(y)    [.1]

with reaction_rules:
    X(x) == Y(y) | (.5, .2)
#2X() == Z() | (.4, .2)
#X() + Y() == Z() | ()
