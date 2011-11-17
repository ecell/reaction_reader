'''

'''

from func import *

with molecule_types:
    Q(t, l, f)
    S(m, l)
    M(m, l)
    R(m, l)

with molecule_inits:
    Q(t, l, f) [10000]
    S(m, l) [10000]
    M(m, l) [10000]
    R(m, l) [10000]

with reaction_rules:
    Q(t) + S(m, l) <_> Q(t[1]).S(m[1], l) | MassAction2(.3, .1)
    Q(t) + M(m, l) <_> Q(t[1]).M(m[1], l) | MassAction2(.3, .1)
    Q(t) + R(m, l) <_> Q(t[1]).R(m[1], l) | MassAction2(.3, .1)

